"""Guardião (gestor único) — spec, auditoria, quitação de débitos e ciclo RALF."""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.domain import Status  # noqa: E402
from pipeline.guardian import GESTOR, RALF, SPEC_FILE, Guardian  # noqa: E402


@pytest.fixture()
def g(tmp_path):
    shutil.copytree(ROOT / ".session", tmp_path / ".session")
    for nome in (".igc-profile.yml", ".igc-registry.yml", SPEC_FILE):
        shutil.copy(ROOT / nome, tmp_path / nome)
    shutil.copytree(ROOT / ".ci", tmp_path / ".ci", ignore=shutil.ignore_patterns("*.sqlite3"))
    return Guardian(tmp_path)


def test_spec_real_e_valida_e_define_gestor_unico():
    spec, errs = Guardian(ROOT).spec()
    assert errs == [], errs
    assert spec["gestor"]["unico"] == GESTOR
    assert tuple(spec["ralf"]["fases"]) == RALF
    assert len(spec["aceite"]) >= 8 and spec["doD"]


def test_audit_mede_1_linhagem_0_paralelas_e_gates(g):
    env = g.audit()
    assert env.status in (int(Status.SUCCESS), int(Status.PENDING))
    m = env.metrics
    assert m["linhagens_ativas"] == 1 and m["sessoes_paralelas"] == []
    assert m["gates"]["site"] == 2 and "site" in m["gates_vermelhos"]
    assert len(m["debitos_abertos"]) >= 10 and m["gestor"] == GESTOR


def test_audit_detecta_sessao_paralela_e_gera_conflito(g):
    g.registry.write_entry("sessao-paralela", branch="sessao/9/outra",
                           checkpoint_ref="a" * 40, ativa=True, gestor="outro-agente")
    env = g.audit()
    assert env.status == int(Status.ERROR_CONTENT)
    assert "sessao-paralela" in env.metrics["sessoes_paralelas"]
    unico = g.assert_single_manager()
    assert unico.status == int(Status.ERROR_CONTENT) and "paralela" in unico.message
    assert any(e["evento"] == "CONFLICT" for e in g.mem.wal_entries())      # G4


def test_gestor_unico_e_declarado_no_registry(g):
    env = g.assert_single_manager()
    assert env.status == int(Status.SUCCESS)
    slug = env.metrics["slug"]
    assert g.registry.entry(slug)["gestor"] == GESTOR
    assert any(e["evento"] == "GESTOR" for e in g.mem.wal_entries())


def test_settle_quita_com_evidencia_e_recusa_sem_evidencia(g):
    abertos = g.debts_open()
    alvo = abertos[0]
    ruim = g.settle(alvo, "curto")
    assert ruim.status == int(Status.ERROR_CONTENT) and alvo in g.debts_open()
    ok = g.settle(alvo, "LICENSE MIT + NOTICE.md criados e versionados")
    assert ok.status == int(Status.SUCCESS)
    assert alvo not in g.debts_open() and len(ok.metrics["restantes"]) == len(abertos) - 1
    assert "RESOLVIDO" in g.mem.debt_file.read_text(encoding="utf-8")
    assert any(e["evento"] == "SETTLE" for e in g.mem.wal_entries())
    assert g.settle("D999", "débito inexistente não pode ser quitado").status == 1


def test_proxima_acao_prioriza_gate_vermelho_depois_debito_depois_release(g):
    prox = g.next_action()
    assert prox["classe"] == "FIX" and prox["alvo"] == "gate site"
    st = json.loads((g.root / ".ci/pipeline-state.json").read_text(encoding="utf-8"))
    for e in st["envelopes"]:
        e["status"] = 0
    (g.root / ".ci/pipeline-state.json").write_text(json.dumps(st), encoding="utf-8")
    assert g.next_action()["classe"] == "DEBT"          # débitos bloqueantes da spec
    spec = yaml.safe_load((g.root / SPEC_FILE).read_text(encoding="utf-8"))
    spec["debitos_bloqueantes"] = []
    (g.root / SPEC_FILE).write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")
    fim = g.next_action()
    assert fim["classe"] == "CONTINUE" and fim["spec_gate"] == "release"


def test_ralf_executa_as_4_fases_e_avanca_checkpoint(g):
    antes = len(g.mem.wal_entries())
    env = g.ralf(run_id="run-1")
    fases = env.metrics["fases"]
    assert list(fases) >= list(RALF) and env.metrics["gestor"] == GESTOR
    assert fases["AGIR"]["alvo"] == "gate site" and fases["FECHAR"]["classe"] == "FIX"
    assert fases["LOGGAR"]["checkpoint"] and len(g.mem.wal_entries()) > antes
    assert env.checkpoint_ref and env.status == int(Status.PENDING)   # continuidade ≠ falha
    dup = g.ralf(run_id="run-1")                                       # E4/G2
    assert dup.metrics["fases"]["FECHAR"]["idempotente"] is True


def test_D14_fechamento_mede_a_verificacao(g):
    prof = yaml.safe_load((g.root / ".igc-profile.yml").read_text(encoding="utf-8"))
    prof["verificacao"]["comando"] = "true"
    (g.root / ".igc-profile.yml").write_text(yaml.safe_dump(prof, allow_unicode=True), encoding="utf-8")
    assert g.mem.measure_verification() is True
    prof["verificacao"]["comando"] = "false"
    (g.root / ".igc-profile.yml").write_text(yaml.safe_dump(prof, allow_unicode=True), encoding="utf-8")
    assert g.mem.measure_verification() is False
    g.mem.contract_emit(EventClass_fix := __import__("pipeline.igc", fromlist=["EventClass"]).EventClass.CONTINUE, "ref")
    g.mem.write_checkpoint(sha="a" * 40, state="GATE")
    gate = g.mem.closing_gate(territorio_pruned=True, modo="continuidade")
    assert gate.metrics["checks"]["verificacao_verde"] is False     # medido, não declarado


def test_cli_do_guardiao_devolve_envelope_json(g):
    proc = subprocess.run([sys.executable, "-m", "pipeline.guardian", "--root", str(g.root),
                           "--audit"], capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert {"id", "status", "message", "checkpoint_ref"} <= set(env)
    assert env["metrics"]["gestor"] == GESTOR


def test_workflow_guardian_existe_com_cron_c1_c2_e_timeout():
    wf = ROOT / ".github/workflows/guardian.yml"
    texto = wf.read_text(encoding="utf-8")
    dados = yaml.safe_load(texto)
    on = dados.get("on") or dados.get(True)
    assert on["schedule"][0]["cron"] and "workflow_dispatch" in on
    assert on["push"]["paths"] and ".session" not in " ".join(on["push"]["paths"])   # C2
    assert "Checkpoint IGC" in texto and "[igc-checkpoint]" in texto                 # C1
    assert dados["jobs"]["guardian"]["timeout-minutes"] <= 30
    assert dados["permissions"]["contents"] == "write"


# ------------------------------------------- /ralf por issue + mediador de merge
class GhFake:
    """gh injetável: testes hermeticos, sem rede (o contrato exige medição, não sorte)."""

    def __init__(self, issues=None, prs=None, rc=0):
        self.calls, self.issues, self.prs, self.rc = [], issues or [], prs or [], rc

    def __call__(self, args):
        self.calls.append(list(args))

        class R:
            returncode, stdout, stderr = self.rc, "", ""
        r = R()
        if args[:2] == ["issue", "list"]:
            r.stdout = json.dumps(self.issues)
        elif args[:2] == ["pr", "list"]:
            r.stdout = json.dumps(self.prs)
        elif args[:2] == ["issue", "create"]:
            r.stdout = "https://github.com/x/y/issues/99"
        elif args[:2] == ["pr", "merge"]:
            r.stdout = "https://github.com/x/y/pull/2/merges"
        return r

    def chamou(self, *prefixo):
        return [c for c in self.calls if c[:len(prefixo)] == list(prefixo)]


def verde_todos(g):
    st = json.loads((g.root / ".ci/pipeline-state.json").read_text(encoding="utf-8"))
    for e in st["envelopes"]:
        e["status"] = 0
    (g.root / ".ci/pipeline-state.json").write_text(json.dumps(st), encoding="utf-8")
    spec = yaml.safe_load((g.root / SPEC_FILE).read_text(encoding="utf-8"))
    spec["debitos_bloqueantes"] = []
    (g.root / SPEC_FILE).write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")


def test_ralf_por_issue_comenta_a_unica_instrucao(g):
    gh = GhFake(issues=[{"number": 7, "title": "t", "url": "u"}])
    env = g.issue_cycle(runner=gh, run_id="r1")
    assert gh.chamou("issue", "comment", "7") and not gh.chamou("issue", "create")
    assert env.metrics["issue"]["number"] == 7 and env.metrics["consolidadas"] == []
    assert env.metrics["fases"][:4] == list(RALF)


def test_ralf_por_issue_consolida_multiplas_e_preserva_a_menor(g):
    gh = GhFake(issues=[{"number": 8, "title": "b", "url": "u"}, {"number": 3, "title": "a", "url": "u"}])
    env = g.issue_cycle(runner=gh)
    assert env.metrics["issue"]["number"] == 3 and env.metrics["consolidadas"] == [8]
    assert gh.chamou("issue", "close", "8") and not gh.chamou("issue", "close", "3")
    assert any(e["evento"] == "ISSUE-CONSOLID" for e in g.mem.wal_entries())


def test_ralf_por_issue_cria_quando_nao_existe_instrucao(g):
    gh = GhFake(issues=[])
    env = g.issue_cycle(runner=gh)
    criadas = gh.chamou("issue", "create")
    assert criadas and "gate site" in " ".join(criadas[0])
    assert any(e["evento"] == "ISSUE-CREATE" for e in g.mem.wal_entries())
    assert env.status == int(Status.PENDING)


def test_ralf_por_issue_fecha_a_issue_quando_o_gate_fica_verde(g):
    verde_todos(g)
    gh = GhFake(issues=[{"number": 5, "title": "t", "url": "u"}])
    env = g.issue_cycle(runner=gh)
    assert gh.chamou("issue", "close", "5") and env.metrics["fechada"] is True
    assert any(e["evento"] == "EMIT" for e in g.mem.wal_entries())      # E5 contraído


def test_mediador_recusa_merge_com_gates_vermelhos(g):
    gh = GhFake(prs=[{"number": 2, "headRefName": "arena/x", "mergeable": "MERGEABLE"}])
    env = g.merge_mediator(runner=gh, pr=2, nota=10.0)
    assert env.status == int(Status.PENDING)
    assert "gates_verdes" in env.metrics["bloqueios"]
    assert not gh.chamou("pr", "merge")                                 # nunca mergir no escuro
    assert any(e["evento"] == "MEDIATOR" for e in g.mem.wal_entries())


def test_mediador_autoriza_em_dry_run_com_dod_verde(g):
    verde_todos(g)
    gh = GhFake(prs=[{"number": 2, "headRefName": "arena/x", "mergeable": "MERGEABLE"}])
    env = g.merge_mediator(runner=gh, pr=2, nota=10.0)
    assert env.status == int(Status.SUCCESS) and env.metrics["executado"] is False
    assert not gh.chamou("pr", "merge") and env.metrics["dod"]["release_zero"] is True


def test_mediador_executa_e_contrai_o_merge_quando_autorizado(g):
    verde_todos(g)
    gh = GhFake(prs=[{"number": 2, "headRefName": "arena/x", "mergeable": "MERGEABLE"}])
    env = g.merge_mediator(runner=gh, pr=2, nota=9.8, dry_run=False)
    assert env.status == int(Status.SUCCESS) and env.metrics["executado"] is True
    assert gh.chamou("pr", "merge", "2", "--merge")
    assert any(e["evento"] == "EMIT" and "merge" in e["resultado"] for e in g.mem.wal_entries())


def test_mediador_recusa_sem_nota_minima_mesmo_com_gates_verdes(g):
    verde_todos(g)
    gh = GhFake(prs=[{"number": 2, "headRefName": "arena/x", "mergeable": "MERGEABLE"}])
    env = g.merge_mediator(runner=gh, pr=2, nota=8.0)
    assert env.status == int(Status.PENDING)
    assert any(b.startswith("nota_minima") for b in env.metrics["bloqueios"])


def test_D24_rebase_vem_antes_da_memoria_e_sem_X_theirs():
    for nome in ("gate-pipeline.yml", "validate.yml", "guardian.yml"):
        s = (ROOT / ".github/workflows" / nome).read_text(encoding="utf-8")
        bloco = s.split("Checkpoint IGC", 1)[1].split("- name:", 1)[0]   # só o step C1
        assert bloco.index("git pull --rebase") < bloco.index("ci_checkpoint.py"), nome
        assert "-X theirs" not in bloco, f"{nome}: -X theirs sobrescreve o CHECKPOINT (M4)"
        assert bloco.count("git push origin") >= 2, f"{nome}: push sem retry"
