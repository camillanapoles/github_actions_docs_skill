"""Testes do pipeline gate-driven: contrato do envelope, store SQLite, blueprint,
fábrica de issues e roteamento do orquestrador. Rodar: python3 -m pytest tests/ -q
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline import blueprint  # noqa: E402
from pipeline.domain import Addendum, Envelope, Status  # noqa: E402
from pipeline.engine import Action, Context, IssueFactory, Orchestrator, SkillAction  # noqa: E402
from pipeline.store import PipelineStore  # noqa: E402

CONTRACT_KEYS = {"id", "blueprint", "gate", "action", "status", "status_label", "message",
                 "direction", "addenda", "next_issue", "metrics", "started_at",
                 "finished_at", "duration_s"}


# --------------------------------------------------------------------------- #
# contrato do envelope JSON
# --------------------------------------------------------------------------- #

def test_envelope_tem_contrato_completo():
    env = Envelope.of("tests", "pytest", Status.SUCCESS, "9 passed",
                      addenda=[Addendum("report", "knowledge/validation.md", note="relatório")],
                      metrics={"passed": 9})
    d = json.loads(env.to_json())
    assert CONTRACT_KEYS <= set(d), set(d) ^ CONTRACT_KEYS
    assert d["status"] == 0 and d["status_label"] == "success" and d["direction"] == "continue"
    assert d["addenda"][0] == {"kind": "report", "path": "knowledge/validation.md",
                               "note": "relatório"}
    assert d["next_issue"] is None and d["metrics"] == {"passed": 9}
    assert d["id"].startswith("tests:")


@pytest.mark.parametrize("status,direction,label", [
    (Status.SUCCESS, "continue", "success"),
    (Status.ERROR_CONTENT, "fix", "error_content"),
    (Status.ERROR_INFRA, "retry", "error_infra"),
    (Status.PENDING, "continue", "pending"),
    (Status.SKIPPED, "continue", "skipped"),
])
def test_codigos_de_status_e_direcao(status, direction, label):
    d = Envelope.of("g", "a", status, "m").to_dict()
    assert d["status"] == int(status) and d["direction"] == direction and d["status_label"] == label


# --------------------------------------------------------------------------- #
# store (SQLite)
# --------------------------------------------------------------------------- #

def test_store_persiste_envelopes_e_issues(tmp_path):
    with PipelineStore(tmp_path / "p.sqlite3") as store:
        store.start_run("run-1", "test")
        env = Envelope.of("tests", "pytest", Status.SUCCESS, "ok",
                          addenda=[Addendum("log", ".ci/x.log")])
        store.record("run-1", env)
        last = store.last_envelope("tests")
        assert last and last["status"] == 0 and last["message"] == "ok"

        from pipeline.store import IssueRecord
        store.save_issue(IssueRecord(key="k1", title="[gate:tests] t", gate="tests",
                                     direction="fix", reason="r", body="b"))
        assert len(store.open_issues()) == 1
        store.close_issue("k1")
        assert store.open_issues() == []
        store.finish_run("run-1", 0, "continue", None, "1/1 gates aprovados")
        state = store.state()
        assert state["runs"] == 1 and state["envelopes_by_status"]["success"] == 1


# --------------------------------------------------------------------------- #
# blueprint BPMN
# --------------------------------------------------------------------------- #

def test_blueprint_ordem_e_transicoes():
    seq = blueprint.ordered()
    assert [g.id for g in seq] == ["tests", "capture", "conformity", "site", "skill",
                                   "ci-issues", "release"]
    assert [g.order for g in seq] == sorted(g.order for g in seq)
    assert blueprint.after("tests").id == "capture"
    assert blueprint.after("release") is None
    bpmn = blueprint.as_bpmn_dict()
    release = next(n for n in bpmn["nodes"] if n["id"] == "release")
    assert release["type"] == "gateway" and release["out"]["success"] == "END"
    tests = next(n for n in bpmn["nodes"] if n["id"] == "tests")
    assert tests["out"]["failure"] == "issue:tests" and tests["acceptance"]


# --------------------------------------------------------------------------- #
# fábrica de issues
# --------------------------------------------------------------------------- #

def _env(gate: str, status: Status, msg: str = "m") -> Envelope:
    return Envelope.of(gate, "a", status, msg)


def test_factory_roteia_para_o_gate_reprovado(tmp_path):
    with PipelineStore(tmp_path / "p.sqlite3") as store:
        envs = [_env("tests", Status.SUCCESS), _env("capture", Status.ERROR_CONTENT, "3 falhas"),
                _env("conformity", Status.SUCCESS)]
        nxt = IssueFactory(store).build(envs)
        assert nxt.gate == "capture" and nxt.direction == "fix"
        assert nxt.key.startswith("capture:fix:")
        assert any("scripts/extract.py" in i or "executar" in i for i in nxt.instructions)
        body = store.issue(nxt.key).body
        assert "[gate:capture]" in body and "Critérios de aceite" in body
        assert "próximo gate indexado" in body and "'conformity'" in body


def test_factory_e_deterministica_e_idempotente(tmp_path):
    with PipelineStore(tmp_path / "p.sqlite3") as store:
        envs = [_env("tests", Status.SUCCESS), _env("capture", Status.SUCCESS),
                _env("conformity", Status.SUCCESS), _env("site", Status.SUCCESS),
                _env("skill", Status.PENDING, "skill incompleta"),
                _env("ci-issues", Status.SKIPPED), _env("release", Status.PENDING)]
        f = IssueFactory(store)
        a, b = f.build(envs), f.build(envs)
        assert a.key == b.key and a.gate == "skill"
        assert len(store.open_issues()) == 1          # não duplica issue


def test_factory_sem_bloqueio_aponta_conclusao(tmp_path):
    with PipelineStore(tmp_path / "p.sqlite3") as store:
        envs = [_env(g, Status.SUCCESS) for g in ("tests", "capture", "conformity", "site", "skill")]
        nxt = IssueFactory(store).build(envs)
        assert nxt.gate == "skill" and nxt.direction == "continue"
        assert "concluíd" in nxt.title.lower() or "done" in nxt.key


# --------------------------------------------------------------------------- #
# actions reais (rápidas e determinísticas)
# --------------------------------------------------------------------------- #

def test_skill_action_mede_o_que_falta(tmp_path):
    ctx = Context(root=ROOT, run_id="run-t", online=False)
    env = SkillAction(blueprint.BY_ID["skill"]).execute(ctx)
    assert env.status in (Status.PENDING, Status.SUCCESS)
    m = env.metrics
    assert m["promised"]["references"] == 14 and m["promised"]["scripts"] == 4
    assert {"lint_workflows.sh", "new_workflow.py", "validate_skill.py",
            "install_tools.sh"} <= set(m["missing"]["scripts"])
    assert m["promised"]["templates"] >= 20, m["promised"]
    assert {"workflows/ci-node.yml", "workflows/gitops-argocd-sync.yml"} <= set(m["missing"]["templates"])
    assert set(m["missing"]) == {"references", "templates", "scripts"}
    assert m["delivered"]["references"] == len(list((ROOT / "skills/github-actions/references").glob("*.md")))


def test_ci_issues_action_offline_e_ignorado():
    ctx = Context(root=ROOT, run_id="run-t", online=False)
    env = blueprint.BY_ID["ci-issues"]
    from pipeline.engine import CiIssuesAction
    out = CiIssuesAction(env).execute(ctx)
    assert out.status == Status.SKIPPED and out.metrics["mode"] == "offline"


# --------------------------------------------------------------------------- #
# orquestrador
# --------------------------------------------------------------------------- #

class _FakeAction(Action):
    """Action configurável para testar o roteamento sem executar comandos."""

    statuses: dict[str, Status] = {}

    def run(self, ctx, started):  # noqa: D102
        st = self.statuses.get(self.spec.id, Status.SUCCESS)
        return self.envelope(st, f"{self.spec.id}: {st.name.lower()}", started=started,
                             metrics={"gate": self.spec.id})


def _orchestrate(tmp_path, statuses: dict[str, Status]) -> dict:
    _FakeAction.statuses = statuses
    original = dict(Orchestrator.ACTIONS)
    Orchestrator.ACTIONS = {k: _FakeAction for k in original}
    try:
        ctx = Context(root=ROOT, run_id="run-o", trigger="test")
        ctx.ci.mkdir(parents=True, exist_ok=True)
        with PipelineStore(tmp_path / "p.sqlite3") as store:
            return Orchestrator(store, ctx).run()
    finally:
        Orchestrator.ACTIONS = original


def test_orquestrador_aprovado_vai_para_proxima_indexada(tmp_path):
    state = _orchestrate(tmp_path, {})
    assert state["status"] == 0 and state["direction"] == "continue"
    assert state["message"].startswith("7/7")
    assert state["next_issue"]["gate"] == "release"
    assert (ROOT / ".ci" / "pipeline-state.json").exists()


def test_orquestrador_reprovado_devolve_erro_e_continuidade(tmp_path):
    state = _orchestrate(tmp_path, {"conformity": Status.ERROR_CONTENT,
                                    "site": Status.ERROR_CONTENT})
    assert state["status"] == 1 and state["direction"] == "fix"
    assert state["next_issue"]["gate"] == "conformity"      # primeiro gate reprovado
    assert any(e["gate"] == "release" and e["status"] != 0 for e in state["envelopes"])
    nxt = pathlib.Path(ROOT / ".ci" / "next-issue.md")
    assert nxt.exists() and "[gate:conformity]" in nxt.read_text(encoding="utf-8")


def test_orquestrador_erro_de_infra_vira_retry(tmp_path):
    state = _orchestrate(tmp_path, {"site": Status.ERROR_INFRA})
    assert state["status"] == 2 and state["direction"] == "retry"
    assert state["next_issue"]["gate"] == "site"


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
