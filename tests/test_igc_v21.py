"""IGC v2.1 — testes das garantias do Artigo 9 (T1-T8) + Art. 10/11/12, C1-C4, M6/M7."""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.domain import Status  # noqa: E402
from pipeline.igc import (EventClass, Registry, SessionMemoryV21, State,  # noqa: E402
                          profile_errors, probe_capabilities)


@pytest.fixture()
def mem(tmp_path):
    shutil.copytree(ROOT / ".session", tmp_path / ".session")
    for nome in (".igc-profile.yml", ".igc-registry.yml"):
        shutil.copy(ROOT / nome, tmp_path / nome)
    return SessionMemoryV21(tmp_path)


def git(*args, cwd="."):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


@pytest.fixture()
def repo_sintetico(tmp_path):
    """Repo git mínimo e autossuficiente (base SHA-pinada, W1')."""
    r = tmp_path / "repo"
    r.mkdir()
    git("init", "-q", "-b", "main", cwd=r)
    git("config", "user.email", "t@t", cwd=r)
    git("config", "user.name", "t", cwd=r)
    (r / "a.txt").write_text("base\n", encoding="utf-8")
    git("add", "-A", cwd=r)
    git("commit", "-qm", "base", cwd=r)
    return r


# --------------------------------------------------------------- T1 (E4/G2)
def test_T1_idempotencia_recusa_duplicata(mem):
    um = mem.emit(EventClass.FIX, "push do reparo", event_id="run-42", verified=True, sha="abc1234567")
    assert um.status == int(Status.SUCCESS) and um.checkpoint_ref == "abc1234567"
    dois = mem.emit(EventClass.FIX, "push do reparo", event_id="run-42", verified=True, sha="abc1234567")
    assert dois.status == int(Status.PENDING) and "já consta no WAL" in dois.message
    chave = "run-42@abc1234567"
    ocorrencias = [e for e in mem.wal_entries() if chave in f"{e.get('evento','')}|{e.get('resultado','')}"]
    assert len(ocorrencias) == 1, "WAL não pode duplicar a mesma chave (G2)"


def test_E3_envelope_minimo_status_message_checkpoint_ref(mem):
    env = mem.emit(EventClass.IMPLEMENT, "nova feature", event_id="e3", verified=True, sha="deadbeefcafe")
    d = env.to_dict()
    assert {"status", "message", "checkpoint_ref"} <= set(d) and d["checkpoint_ref"] == "deadbeefcafe"
    schema = json.loads((ROOT / ".ci/schema/envelope.schema.json").read_text(encoding="utf-8"))
    assert set(schema["required"]) == {"id", "status", "message", "checkpoint_ref"}
    assert "HANDOFF" in schema["properties"]["classe"]["enum"]          # A4


def test_A4_handoff_e_classe_de_emissao(mem):
    env = mem.emit(EventClass.HANDOFF, "bundle de transferência", event_id="h1",
                   verified=True, sha="feedface1234")
    assert env.status == int(Status.SUCCESS) and env.metrics["class"] == "HANDOFF"


# --------------------------------------------------------------- T2 (G4)
def test_T2_conflito_explicito_e_merge_silencioso_reprovado(mem):
    ok = mem.register_conflict("sessao/1/docs", "sessao/2/docs", "knowledge/pt/index.md")
    assert ok.status == int(Status.SUCCESS)
    assert any(e["evento"] == "CONFLICT" for e in mem.wal_entries())
    ruim = mem.register_conflict("sessao/1/docs", "sessao/2/docs", "knowledge/pt/index.md",
                                 merge_silencioso=True)
    assert ruim.status == int(Status.ERROR_CONTENT) and "reprovado" in ruim.message


# --------------------------------------------------------------- T3 (G5/W6)
def test_T3_varredura_de_orfaos_gera_debt_e_preserva_ativa(tmp_path):
    reg = Registry(tmp_path)
    reg.write_entry("orfã", branch="sessao/9/velha", checkpoint_ref="",
                    atualizado_em="2026-01-01")
    reg.write_entry("viva", branch="sessao/10/nova", checkpoint_ref="a" * 40,
                    atualizado_em="2026-10-13")
    orfaos = reg.sweep_orphans(hoje=dt.date(2026, 10, 13), days=30)
    assert orfaos == ["orfã"] and reg.entry("viva")["ativa"] is True


# --------------------------------------------------------------- T4 (D1-D3)
def test_T4_registry_roundtrip_e_adulteracao(mem, tmp_path):
    reg = mem.registry
    reg.write_entry("linhagem-x", branch="arena/x", checkpoint_ref="b" * 40, estado_fsm="EXEC")
    frio = SessionMemoryV21(tmp_path)
    frio.write_checkpoint(sha="b" * 40, state="EXEC")   # alinhado antes de descobrir
    env = frio.discover("linhagem-x")
    assert env.status == int(Status.SUCCESS) and env.metrics["branch"] == "arena/x"
    reg.write_entry("linhagem-x", branch="arena/x", checkpoint_ref="c" * 40)
    frio.write_checkpoint(sha="b" * 40, state="EXEC")
    div = frio.discover("linhagem-x")
    assert div.status == int(Status.ERROR_CONTENT) and div.metrics["divergencia"] is True
    assert "divergentes" in frio.debt_file.read_text(encoding="utf-8")     # D3 → DEBT


def test_R7_sem_registry_e_sem_memoria_e_boot_legitimo(tmp_path):
    env = SessionMemoryV21(tmp_path).discover()
    assert env.status == int(Status.SUCCESS) and env.metrics["boot"] is True
    assert any(e["evento"] == "BOOT" for e in SessionMemoryV21(tmp_path).wal_entries())


# --------------------------------------------------------------- T5 (C1-C4)
def test_T5_pipelines_contem_step_de_checkpoint_igc():
    for wf in ("gate-pipeline.yml", "validate.yml"):
        texto = (ROOT / ".github/workflows" / wf).read_text(encoding="utf-8")
        assert "Checkpoint IGC" in texto, f"{wf} sem step C1"
        assert "ci_checkpoint.py" in texto and "[igc-checkpoint]" in texto
    gp = (ROOT / ".github/workflows/gate-pipeline.yml").read_text(encoding="utf-8")
    assert 'paths-ignore' in gp and '".session/**"' in gp                 # C2
    assert "contents: write" in gp                                        # commit do bot


def test_T5_checkpoint_do_ci_avanca_wal_e_registry(mem, tmp_path):
    proc = subprocess.run(
        [sys.executable, str(ROOT / ".session/ci_checkpoint.py"), "--root", str(tmp_path),
         "--run-id", "999", "--gate", "tests", "--sha", "d" * 40, "--state", "GATE"],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert env["checkpoint_ref"] == "d" * 40 and env["tag"] == "[igc-checkpoint]"
    assert env["status"] == 0 and env["wal_hash"]
    assert json.loads((tmp_path / ".ci/igc-checkpoint.json").read_text(encoding="utf-8")) == env
    assert Registry(tmp_path).entry(env["registry"])["checkpoint_ref"] == "d" * 40    # D2
    assert any(e["evento"].startswith("CI run 999") for e in mem.wal_entries())


def test_C4_pipeline_em_linhagem_sem_memoria_faz_bootstrap(tmp_path):
    (tmp_path / ".igc-profile.yml").write_text("igc_profile: '1'\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(ROOT / ".session/ci_checkpoint.py"),
                           "--root", str(tmp_path), "--run-id", "1", "--sha", "e" * 40],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    wal = (tmp_path / ".session/WAL.md").read_text(encoding="utf-8")
    assert "BOOT" in wal and "C4" in wal


# --------------------------------------------------------------- T6 (Art.10)
def test_T6_boot_bloqueado_sem_profile(tmp_path):
    shutil.copytree(ROOT / ".session", tmp_path / ".session")
    m = SessionMemoryV21(tmp_path)
    env = m.bootstrap_v21()
    assert env.status == int(Status.ERROR_INFRA) and "Art. 10" in env.message
    assert ".igc-profile.yml ausente" in m.debt_file.read_text(encoding="utf-8")


def test_T6_profile_invalidado_vai_a_debt_e_recon(tmp_path):
    shutil.copytree(ROOT / ".session", tmp_path / ".session")
    (tmp_path / ".igc-profile.yml").write_text(
        "igc_profile: '1'\nlinhagem: {}\nevents: {}\n", encoding="utf-8")
    m = SessionMemoryV21(tmp_path)
    env = m.bootstrap_v21()
    assert env.status == int(Status.ERROR_CONTENT) and "profile inválido" in env.message
    assert "chave obrigatória ausente" in env.message
    assert any(e["evento"] == "PROFILE" for e in m.wal_entries())


def test_profile_real_e_valido_e_profile_errors_detecta_violacoes():
    prof, errs = SessionMemoryV21(ROOT).profile()
    assert errs == [], f"profile real inválido: {errs}"
    assert profile_errors({"envelope": {"minimo": ["status"]}})      # viola E3
    assert profile_errors({"runtime": {"requer": ["magia"]}})        # capability inexistente


# --------------------------------------------------------------- T7 (Art.11)
def test_T7_capabilities_ausentes_ativam_fallbacks_e_fsm_funciona(mem):
    caps = {"fs_write": True, "vcs": False, "exec": False, "append_wal": True}
    antes = [e for e in mem.wal_entries() if e["evento"] == "CAPABILITY"]
    env = mem.bootstrap_v21(caps=caps)
    assert env.status == int(Status.SUCCESS)
    assert sorted(env.metrics["faltando"]) == ["exec", "vcs"]
    entradas = [e for e in mem.wal_entries() if e["evento"] == "CAPABILITY"][len(antes):]
    assert len(entradas) == 2 and "fallback" in (entradas[0].get("acao") or entradas[0].get("ação", "")).lower()
    assert mem.transition(State.VERIFY, event="EXEC->VERIFY", classe=EventClass.FIX,
                          cause="x", action="y", result="z").status == int(Status.SUCCESS)
    assert mem.wal_append("WAL universal", EventClass.CONTINUE, "a", "b", "c").status == 0


def test_T7_boot_recusado_sem_fallback_para_capability_minima(mem):
    env = mem.bootstrap_v21(caps={"fs_write": False, "vcs": True, "exec": True,
                                  "append_wal": True})
    assert env.status == int(Status.ERROR_INFRA) and "recusado" in env.message
    assert "sem fallback" in mem.debt_file.read_text(encoding="utf-8")      # CP2/G6


def test_probe_de_capabilities_neste_runtime():
    caps = probe_capabilities(ROOT)
    assert caps == {"fs_write": True, "vcs": True, "exec": True, "append_wal": True}


# --------------------------------------------------------------- T8 (transporte)
def test_T8_roundtrip_bundle_offline(repo_sintetico, tmp_path):
    r, mem = repo_sintetico, None
    base = git("rev-parse", "main", cwd=r).stdout.strip()
    git("checkout", "-q", "-b", "sessao/1/linhagem", cwd=r)
    (r / "trabalho.md").write_text("estado acumulado (W7)\n", encoding="utf-8")
    git("add", "-A", cwd=r)
    git("commit", "-qm", "trabalho", cwd=r)
    tip = git("rev-parse", "HEAD", cwd=r).stdout.strip()
    m = SessionMemoryV21(r)
    bundle = tmp_path / "handoff.bundle"
    assert m.bundle_create(bundle, base=base, branch="sessao/1/linhagem").status == 0
    assert bundle.exists() and m.bundle_verify(bundle).status == int(Status.SUCCESS)
    frio = tmp_path / "frio"
    assert git("clone", "-q", "--no-local", str(r), str(frio)).returncode == 0
    git("checkout", "-q", base, cwd=frio)                       # clone limpo da base
    assert git("fetch", "-q", str(bundle), "sessao/1/linhagem", cwd=frio).returncode == 0
    git("checkout", "-q", "-B", "sessao/1/linhagem", "FETCH_HEAD", cwd=frio)
    assert git("rev-parse", "HEAD", cwd=frio).stdout.strip() == tip
    assert (frio / "trabalho.md").read_text(encoding="utf-8").startswith("estado acumulado")
    assert any(e["evento"] == "TRANSPORT" for e in m.wal_entries())


# ------------------------------------------------------------------- M7/W1'
def test_M7_base_limida_passa_e_anomalia_e_registrada(repo_sintetico, tmp_path):
    r = repo_sintetico
    base = git("rev-parse", "main", cwd=r).stdout.strip()
    m = SessionMemoryV21(r)
    assert m.base_sanity(base, "main").status == int(Status.SUCCESS)      # 0 divergências
    git("checkout", "-q", "-b", "anomalia", cwd=r)
    for i in range(250):                                                  # deleta em massa
        (r / f"f{i}.txt").write_text("x" * 100, encoding="utf-8")
    git("add", "-A", cwd=r)
    git("commit", "-qm", "250 arquivos", cwd=r)
    for i in range(250):
        (r / f"f{i}.txt").unlink()
    git("add", "-A", cwd=r)
    git("commit", "-qm", "revert massivo", cwd=r)
    env = m.base_sanity("anomalia~1", "anomalia")
    assert env.status == int(Status.ERROR_CONTENT) and env.metrics["anomalia"] is True
    assert any(e["evento"] == "M7-BASE" for e in m.wal_entries())


def test_W1_base_real_esta_sha_pinada_e_verificada():
    """A base desta linhagem é SHA (nunca ref solta) e passou por M7."""
    prof = SessionMemoryV21(ROOT).profile()[0]
    base = prof["linhagem"]["base_sha"]
    assert len(base) == 40 and "PASS" in prof["linhagem"]["m7_pre_base"]
    reg = Registry(ROOT).read()["linhagens"]["github-actions-docs-skill"]
    assert reg["base_sha"] == base and reg["ativa"] is True


# --------------------------------------------------------------------- M6
def test_M6_skips_justificados_e_skip_silencioso_e_falha(mem):
    ok, injust = mem.skips_justificados(["pandoc indisponível no ambiente"])
    assert ok and injust == []
    ok2, injust2 = mem.skips_justificados(["motivo obscuro qualquer"])
    assert not ok2 and injust2 == ["motivo obscuro qualquer"]


# ------------------------------------------------------- E5 + Art. 12 (fechamento)
def test_E5_contracao_causal_do_emit_resolve_debito(mem):
    sem = mem.contract_emit(EventClass.IMPLEMENT, "-")
    assert sem.status == int(Status.ERROR_CONTENT) and "contratação causal" in sem.message
    mem.add_debt("PR não aberto", "gate release vermelho", "produção bloqueada", "abrir PR")
    ok = mem.contract_emit(EventClass.IMPLEMENT, "https://github.com/x/pull/7", debt_id="D1")
    assert ok.status == int(Status.SUCCESS)
    assert any(e["evento"] == "EMIT" and "pull/7" in e["resultado"] for e in mem.wal_entries())
    assert "RESOLVIDO" in mem.debt_file.read_text(encoding="utf-8")


def test_art12_fechamento_verde_autoriza_close(mem):
    mem.contract_emit(EventClass.CONTINUE, "run 38462690420")
    mem.write_checkpoint(sha="f" * 40, state="GATE")
    env = mem.closing_gate(verificacao_verde=True, territorio_pruned=True,
                           modo="continuidade", skips=["pandoc indisponível"])
    assert env.status == int(Status.SUCCESS), env.metrics["pendencias"]
    assert env.metrics["nota"] == 10.0 and env.metrics["checks"]["emit_contratado_E5"]


def test_art12_nota_abaixo_de_9_5_nao_fecha_e_volta_a_exec(mem):
    mem.write_checkpoint(sha="f" * 40, state="GATE")
    env = mem.closing_gate(verificacao_verde=False, territorio_pruned=False,
                           modo="handoff", roundtrip_verde=False)
    assert env.status == int(Status.ERROR_CONTENT) and env.metrics["nota"] < 9.5
    assert "verificacao_verde" in env.metrics["pendencias"]
    assert mem.state() is State.EXEC                       # retorna a EXEC, nunca CLOSE


def test_M4_checkpoint_nao_fica_atrasado_apos_fechamento(mem):
    """Retificação: closing_gate/contract_emit acrescentam ao WAL ⇒ CHECKPOINT é refeito."""
    mem.write_checkpoint(sha="a" * 40, state="GATE")
    mem.contract_emit(EventClass.CONTINUE, "run 1")
    assert mem.read_checkpoint()["wal_sha256"] == mem.wal_hash()
    mem.closing_gate(verificacao_verde=True, territorio_pruned=True, modo="continuidade")
    assert mem.read_checkpoint()["wal_sha256"] == mem.wal_hash(), "M4: hash do WAL atrasado"
    assert mem.read_checkpoint()["sha"] == "a" * 40 and mem.read_checkpoint()["state"] == "GATE"
