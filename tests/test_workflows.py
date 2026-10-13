"""Testes que garantem o fluxo operacional dos workflows (sucesso por teste).

Cobrem o que só aparecia em execução no CI:
  * YAML de todos os workflows parseia e casa com o JSON Schema oficial;
  * todo bloco `run:` bash tem sintaxe válida (`bash -n`) — expressões `${{ }}`
    são neutralizadas antes da checagem;
  * regressões reais já ocorridas: `bash -e {0}` (default do Actions) abortando o
    passo no primeiro 403/422, envelope jq sem `end`, `$REPO` colado no programa jq;
  * o gate final existe e reprova quando o status do pipeline != 0 (é gate de verdade);
  * a factory de continuidade é acionada em qualquer resultado (`if: always()`).

Rodar: python3 -m pytest tests/test_workflows.py -q
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
SCHEMA_DIR = ROOT / ".ci" / "schema"


def _load(wf: pathlib.Path) -> dict:
    return yaml.safe_load(wf.read_text(encoding="utf-8"))


def _steps(doc: dict):
    for job_id, job in (doc.get("jobs") or {}).items():
        for st in job.get("steps") or []:
            yield job_id, st


# --------------------------------------------------------------------------- #
# estrutura e schema
# --------------------------------------------------------------------------- #

def test_todos_os_workflows_parseiam():
    assert WORKFLOWS, "nenhum workflow encontrado"
    for wf in WORKFLOWS:
        doc = _load(wf)
        assert doc.get("jobs"), f"{wf.name} sem jobs"
        assert doc.get("permissions") is not None, f"{wf.name} sem permissions explícito"
        assert True in (k for k in doc if str(k).lower() in ("on", "true")), f"{wf.name} sem gatilho"


def test_workflows_contra_json_schema_oficial():
    pytest.importorskip("jsonschema")
    import jsonschema

    schema = json.loads((SCHEMA_DIR / "github-workflow.json").read_text(encoding="utf-8"))
    for wf in WORKFLOWS:
        jsonschema.validate(_load(wf), schema)


def test_jobs_tem_timeout_e_nome():
    for wf in WORKFLOWS:
        for job_id, job in _load(wf)["jobs"].items():
            assert job.get("runs-on"), f"{wf.name}:{job_id} sem runs-on"
            assert job.get("timeout-minutes"), f"{wf.name}:{job_id} sem timeout-minutes"


# --------------------------------------------------------------------------- #
# sintaxe shell de cada bloco run:
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("wf", WORKFLOWS, ids=lambda p: p.name)
def test_blocos_run_bash_tem_sintaxe_valida(wf):
    doc = _load(wf)
    for job_id, st in _steps(doc):
        run = st.get("run")
        if not run:
            continue
        shell = st.get("shell", "bash")
        if not str(shell).startswith(("bash", "sh")):
            continue
        code = re.sub(r"\$\{\{[^}]*\}\}", "x", run)
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as fh:
            fh.write(code)
            path = fh.name
        proc = subprocess.run(["bash", "-n", path], capture_output=True, text=True)
        assert proc.returncode == 0, (
            f"{wf.name} :: {job_id} :: {st.get('name')}\n{proc.stderr}"
        )


# --------------------------------------------------------------------------- #
# regressões reais (já ocorreram em produção)
# --------------------------------------------------------------------------- #

def test_admin_bootstrap_nao_aborta_no_primeiro_erro_de_api():
    """O default do Actions é `bash -e {0}`: sem `set +e` o primeiro 403/422 matava o passo."""
    wf = ROOT / ".github" / "workflows" / "admin-bootstrap.yml"
    doc = _load(wf)
    step = next(st for _j, st in _steps(doc) if "Avalia capacidade" in str(st.get("name")))
    run = step["run"]
    assert "set +e" in run, "falta `set +e` (o passo abortaria no primeiro erro de API)"
    assert "rc=$?" in run, "falta capturar o código de retorno da API"
    assert "admin-bootstrap.log" in run, "falta registrar o diagnóstico em .ci/*.log"


def test_admin_bootstrap_envelope_jq_e_valido():
    """Regressão: `if` sem `end` e `$REPO` colado no programa jq → envelope nunca escrito."""
    text = (ROOT / ".github" / "workflows" / "admin-bootstrap.yml").read_text(encoding="utf-8")
    prog = text[text.index("'{id:$id") + 1:]
    prog = prog[: prog.index("finished_at:$ts}") + len("finished_at:$ts}")]
    assert "end)" in prog, "if do jq sem `end`"
    assert "$REPO" not in prog, "variável de shell colada dentro do programa jq"
    assert "--arg repo" in text, "repo deve entrar como --arg do jq"
    if subprocess.run(["command", "-v", "jq"], shell=True, capture_output=True).returncode == 0:
        with tempfile.NamedTemporaryFile("w", suffix=".jq", delete=False) as fh:
            fh.write(prog)
            jqfile = fh.name
        proc = subprocess.run(
            ["jq", "-n", "--arg", "id", "t", "--arg", "repo", "o/r", "--arg", "gate", "governance",
             "--arg", "action", "a", "--argjson", "status", "3", "--arg", "direction", "continue",
             "--arg", "message", "m", "--arg", "addenda", '{"kind":"log","path":"p"}',
             "--arg", "ts", "2026-01-01T00:00:00Z", "-f", jqfile],
            capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        env = json.loads(proc.stdout)
        assert env["status"] == 3 and env["direction"] == "continue"
        assert env["next_issue"]["instructions"], "envelope sem instruções de continuidade"


def test_diagnostico_e_commitado_de_volta():
    """Logs do Actions são inacessíveis do sandbox → o workflow precisa commitar .ci/."""
    for name in ("admin-bootstrap.yml", "extract-docs.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        assert "git push" in text and ".ci" in text, f"{name} não devolve o diagnóstico via commit"


# --------------------------------------------------------------------------- #
# o gate é gate: reprova e garante continuidade
# --------------------------------------------------------------------------- #

def test_gate_pipeline_reprova_quando_status_diferente_de_zero():
    doc = _load(ROOT / ".github" / "workflows" / "gate-pipeline.yml")
    steps = list(_steps(doc))
    final = [st for _j, st in steps if "Gate final" in str(st.get("name"))]
    assert final, "gate-pipeline sem passo final de decisão"
    run = final[0]["run"]
    assert "exit 1" in run and 'STATUS' in run
    assert final[0].get("if") == "always()", "a decisão precisa rodar mesmo com passo anterior em erro"


def test_gate_pipeline_garante_proxima_issue_em_qualquer_resultado():
    doc = _load(ROOT / ".github" / "workflows" / "gate-pipeline.yml")
    names = {st.get("name"): st for _j, st in _steps(doc)}
    issue_step = next(st for n, st in names.items() if "próxima issue" in str(n))
    assert issue_step.get("if") == "always()", "continuidade só é garantida com if: always()"
    assert "gh issue create" in issue_step["run"] and "gh issue comment" in issue_step["run"]
    assert "pipeline:next" in issue_step["run"], "falta o rótulo de indexação da próxima issue"
    assert names[[n for n in names if "Executa os gates" in str(n)][0]].get("continue-on-error") is True, \
        "a execução dos gates não pode abortar antes de publicar a continuidade"


def test_admin_bootstrap_dispara_sem_precisar_de_dispatch():
    """workflow_dispatch só registra workflow presente no branch default."""
    doc = _load(ROOT / ".github" / "workflows" / "admin-bootstrap.yml")
    triggers = doc.get("on") or doc.get(True)
    push = triggers.get("push") if isinstance(triggers, dict) else None
    assert push and "arena/**" in push["branches"], \
        "sem push em arena/** o bootstrap não roda antes do merge em main"


def test_run_blocks_nao_interpolam_contexto_inputs():
    """`inputs` só existe em workflow_dispatch/workflow_call; em push/issues/schedule
    o actionlint reprova. O valor deve chegar por `env:` como github.event.inputs.*"""
    for wf in WORKFLOWS:
        for job_id, st in _steps(_load(wf)):
            run = st.get("run") or ""
            assert "${{ inputs." not in run, (
                f"{wf.name}::{job_id}::{st.get('name')} interpola inputs.* em run: "
                "(use env: com github.event.inputs.*)")
