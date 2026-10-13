"""Testes do contrato IGC v1.0 — memória de sessão, FSM, checkpoint e emissão.

Garantem por teste os artigos: A3/A4 (emissão rotulada e commitada), M1 (WAL
append-only), M2 (transições), M4 (integridade do checkpoint), M5 (débito),
E1 (classificação), E2/E3 (gate antes de emitir), R1-R6 (retomada a frio).
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.domain import Status  # noqa: E402
from pipeline.igc import EventClass, SessionMemory, State, TRANSITIONS, classify  # noqa: E402

SESSION = ROOT / ".session"


@pytest.fixture()
def mem(tmp_path):
    """Cópia isolada da memória real (testes mutam a cópia, nunca o repo)."""
    shutil.copytree(SESSION, tmp_path / ".session")
    return SessionMemory(tmp_path)


# --------------------------------------------------------------------- E1
@pytest.mark.parametrize("kwargs,esperado", [
    ({"gate_red": True}, EventClass.FIX),
    ({"deferred": True}, EventClass.DEBT),
    ({"new_feature": True}, EventClass.IMPLEMENT),
    ({"checkpoint_exists": True, "goal_open": True}, EventClass.CONTINUE),
    ({"checkpoint_exists": False, "goal_open": False}, EventClass.IMPLEMENT),
])
def test_classificacao_de_eventos(kwargs, esperado):
    assert classify("evento observado", **kwargs) is esperado


def test_classificacao_por_texto_de_ci():
    assert classify("check suite failure em mkdocs build") is EventClass.FIX
    assert classify("issue closed: [gate:capture]") is EventClass.CONTINUE


# --------------------------------------------------------------------- M2
def test_transicoes_obrigatorias_existem():
    assert set(TRANSITIONS) == set(State)
    assert State.EXEC in TRANSITIONS[State.GATE]      # E2: reprovado → correção
    assert State.CLOSE not in TRANSITIONS[State.GATE]  # nunca emissão parcial
    assert TRANSITIONS[State.CLOSE] == frozenset()


def test_transicao_legal_atualiza_state_e_wal(mem):
    antes = len(mem.wal_entries())
    env = mem.transition(State.VERIFY, event="EXEC->VERIFY", classe=EventClass.FIX,
                         cause="reparo aplicado", action="pytest", result="verde")
    assert env.status == Status.SUCCESS
    assert mem.state() is State.VERIFY
    assert len(mem.wal_entries()) == antes + 1


def test_transicao_ilegal_e_rejeitada_e_registrada(mem):
    antes = len(mem.wal_entries())
    env = mem.transition(State.CLOSE, event="EXEC->CLOSE", classe=EventClass.FIX,
                         cause="tentativa inválida", action="-", result="-")
    assert env.status == Status.ERROR_CONTENT and env.direction == "fix"
    assert mem.state() is State.EXEC                     # estado preservado
    assert len(mem.wal_entries()) == antes + 1           # rejeição também vai ao WAL
    assert "ilegal" in mem.wal_entries()[-1]["evento"]


# --------------------------------------------------------------------- M1
def test_wal_e_append_only_e_parsavel(mem):
    n = len(mem.wal_entries())
    mem.wal_append("evento A", EventClass.IMPLEMENT, "causa", "ação", "resultado", "abc1234")
    mem.wal_append("evento B", EventClass.DEBT, "causa", "ação", "resultado")
    entries = mem.wal_entries()
    assert len(entries) == n + 2
    assert entries[-2]["classe"] == "IMPLEMENT" and entries[-1]["classe"] == "DEBT"
    assert all(len(e) == 7 for e in entries)             # 7 colunas do contrato
    assert entries[:n] == mem.wal_entries()[:n]          # nada foi reescrito


# --------------------------------------------------------------------- M4
def test_checkpoint_roundtrip_e_integridade_do_wal(mem):
    env = mem.write_checkpoint(sha="0" * 40, state="EXEC")
    assert env.status == Status.SUCCESS
    cp = mem.read_checkpoint()
    assert cp["sha"] == "0" * 40 and cp["wal_sha256"] == mem.wal_hash()
    mem.wal_append("adulteração", EventClass.FIX, "x", "y", "z")   # muda o WAL
    ver = mem.verify()
    assert ver.status == Status.ERROR_CONTENT
    assert ver.metrics["recon_required"] is True and ver.metrics["wal_integro"] is False


def test_checkpoint_real_do_repo_esta_integro():
    """Leitura pura: o CHECKPOINT commitado casa com HEAD e com o WAL real."""
    mem = SessionMemory(ROOT)
    cp = mem.read_checkpoint()
    assert cp and cp["wal_sha256"] == mem.wal_hash()
    head = mem.git_head()
    assert cp["sha"] == head or subprocess.run(
        ["git", "merge-base", "--is-ancestor", cp["sha"], "HEAD"], cwd=ROOT).returncode == 0


# --------------------------------------------------------------------- M5
def test_debito_e_cidadao_de_primeira_classe(mem):
    antes = len(mem.wal_entries())
    env = mem.add_debt("âncoras restantes", "align parcial", "gate site vermelho",
                       "fechar gate site")
    assert env.status == Status.PENDING
    assert env.metrics["debt_id"].startswith("D")
    text = mem.debt_file.read_text(encoding="utf-8")
    assert "âncoras restantes" in text
    assert len(mem.wal_entries()) == antes + 1
    assert mem.wal_entries()[-1]["classe"] == "DEBT"


# ----------------------------------------------------------------- E2 / E3
def test_emit_guard_bloqueia_sem_integridade(mem):
    mem.write_checkpoint(sha="0" * 40)
    mem.wal_append("quebra de integridade", EventClass.FIX, "x", "y", "z")
    env = mem.emit_guard(EventClass.FIX, "push do reparo")
    assert env.status == Status.ERROR_CONTENT and "bloqueada" in env.message


def test_emit_guard_autoriza_com_checkpoint_e_ancora_do_wal(mem):
    env = mem.emit_guard(EventClass.IMPLEMENT, "push", verified=True, sha="abc1234def")
    assert env.status == Status.SUCCESS
    assert env.metrics["class"] == "IMPLEMENT"
    assert env.metrics["checkpoint"] == "abc1234def"
    assert env.metrics["wal"].startswith(".session/WAL.md#")   # E3: cadeia auditável


# ------------------------------------------------------------- R1-R6 / A5
def test_resume_a_frio_reconstrui_estado(mem):
    env = mem.resume()
    assert env.status in (Status.SUCCESS, Status.PENDING)
    assert env.metrics["wal_entries"] > 10
    assert env.metrics["state"] in {s.value for s in State}
    assert mem.wal_entries()[-1]["evento"] == "RESUME"        # R6


def test_resume_sem_memoria_exige_boot(tmp_path):
    env = SessionMemory(tmp_path).resume()
    assert env.status == Status.ERROR_CONTENT
    assert set(env.metrics["missing"]) >= {"WAL.md", "STATE.yml", "CHECKPOINT"}


# ------------------------------------------------------------------- W2
def test_bootstrap_existe_e_tem_sintaxe_valida():
    sh = SESSION / "bootstrap.sh"
    assert sh.exists() and sh.stat().st_mode & 0o111, "bootstrap.sh ausente ou não executável"
    assert subprocess.run(["bash", "-n", str(sh)], capture_output=True).returncode == 0


def test_objetos_de_memoria_obrigatorios_estao_versionados():
    for name in ("WAL.md", "STATE.yml", "INTENT.md", "CONTEXT.md", "DEBT.md",
                 "CHECKPOINT", "bootstrap.sh"):
        assert (SESSION / name).exists(), f".session/{name} ausente (Artigo 2)"
    wal = (SESSION / "WAL.md").read_text(encoding="utf-8")
    assert wal.count("| FIX |") + wal.count("| IMPLEMENT |") + wal.count("| DEBT |") \
        + wal.count("| CONTINUE |") + wal.count("| RESUME |") >= 20
