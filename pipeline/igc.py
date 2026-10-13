"""IGC v1.0 — memória de sessão versionada (WAL append-only, FSM, CHECKPOINT, DEBT).

Implementa o contrato de continuidade como objeto de domínio, devolvendo sempre o
mesmo envelope JSON do pipeline (status 0-4 + direction + next_issue).

Artigos cobertos: A1-A5, M1-M5, E1-E3, R1-R6, G1-G3.
"""
from __future__ import annotations

import enum
import hashlib
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

from .domain import Addendum, Envelope, Status, utcnow

SESSION_DIR = ".session"
WAL_HEADER = ("| timestamp | evento | classe | causa | ação | resultado | sha_commit |",
              "| --- | --- | --- | --- | --- | --- | --- |")


class EventClass(str, enum.Enum):
    """A4 — toda emissão é classificada."""

    FIX = "FIX"
    CONTINUE = "CONTINUE"
    IMPLEMENT = "IMPLEMENT"
    DEBT = "DEBT"


    HANDOFF = "HANDOFF"   # v2.1 (EV-3): transferência de sessão


class State(str, enum.Enum):
    """M2 — estados obrigatórios da FSM."""

    BOOT = "BOOT"
    RECON = "RECON"
    PLAN = "PLAN"
    EXEC = "EXEC"
    VERIFY = "VERIFY"
    GATE = "GATE"
    EMIT = "EMIT"
    CONTINUE = "CONTINUE"
    CLOSE = "CLOSE"


TRANSITIONS: dict[State, frozenset[State]] = {
    State.BOOT: frozenset({State.RECON, State.PLAN}),
    State.RECON: frozenset({State.PLAN, State.EXEC, State.BOOT}),
    State.PLAN: frozenset({State.EXEC, State.RECON}),
    State.EXEC: frozenset({State.VERIFY, State.RECON}),
    State.VERIFY: frozenset({State.GATE, State.EXEC}),
    State.GATE: frozenset({State.EMIT, State.EXEC}),      # E2: reprovado → loop de correção
    State.EMIT: frozenset({State.CONTINUE, State.CLOSE}),
    State.CONTINUE: frozenset({State.RECON, State.PLAN, State.EXEC, State.CLOSE}),
    State.CLOSE: frozenset(),
}


def classify(event: str, *, gate_red: bool = False, checkpoint_exists: bool = True,
             goal_open: bool = True, new_feature: bool = False, deferred: bool = False) -> EventClass:
    """E1 — classifica o evento observado na tabela do contrato."""
    if deferred:
        return EventClass.DEBT
    if gate_red or re.search(r"\b(failure|failed|bug|erro|red)\b", event, re.I):
        return EventClass.FIX
    if new_feature:
        return EventClass.IMPLEMENT
    if checkpoint_exists and goal_open:
        return EventClass.CONTINUE
    return EventClass.IMPLEMENT


class SessionMemory:
    """Repositório da memória de sessão (`.session/`) — nada vive no runner (A1)."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.dir = self.root / SESSION_DIR
        self.wal = self.dir / "WAL.md"
        self.state_file = self.dir / "STATE.yml"
        self.checkpoint_file = self.dir / "CHECKPOINT"
        self.debt_file = self.dir / "DEBT.md"
        self.intent_file = self.dir / "INTENT.md"
        self.context_file = self.dir / "CONTEXT.md"
        self.bootstrap_file = self.dir / "bootstrap.sh"

    # ------------------------------------------------------------------ WAL (M1)
    def wal_entries(self) -> list[dict[str, str]]:
        if not self.wal.exists():
            return []
        rows = []
        for line in self.wal.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| ") or line.startswith("| ---") or line.startswith("| timestamp"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 7:
                rows.append(dict(zip(
                    ("timestamp", "evento", "classe", "causa", "acao", "resultado", "sha"), cells)))
        return rows

    def wal_append(self, event: str, classe: EventClass | str, cause: str, action: str,
                   result: str, sha: str = "") -> Envelope:
        """Append-only: correção é entrada nova, nunca edição."""
        started = time.monotonic()
        self.dir.mkdir(parents=True, exist_ok=True)
        if not self.wal.exists():
            self.wal.write_text("# WAL — log append-only (M1)\n\n" + "\n".join(WAL_HEADER) + "\n",
                                encoding="utf-8")
        before = len(self.wal_entries())
        classe = EventClass(classe).value
        row = f"| {utcnow()} | {event} | {classe} | {cause} | {action} | {result} | {sha or '-'} |"
        with self.wal.open("a", encoding="utf-8") as fh:
            fh.write(row + "\n")
        env = Envelope.of("igc.wal", "SessionMemory.wal_append", Status.SUCCESS,
                          f"entrada {classe} gravada ({before} → {before + 1})",
                          addenda=[Addendum("log", f"{SESSION_DIR}/WAL.md")],
                          metrics={"entries": before + 1, "class": classe})
        return env.close(started)

    def wal_hash(self) -> str:
        return hashlib.sha256(self.wal.read_bytes()).hexdigest()[:16] if self.wal.exists() else ""

    # --------------------------------------------------------------- STATE (M2)
    def state(self) -> State | None:
        if not self.state_file.exists():
            return None
        m = re.search(r"^current_state:\s*(\w+)", self.state_file.read_text(encoding="utf-8"), re.M)
        return State(m.group(1)) if m else None

    def transition(self, to: State | str, *, event: str, classe: EventClass | str, cause: str,
                   action: str, result: str, sha: str = "") -> Envelope:
        """M2 — transição exige condição satisfeita + entrada no WAL + commit do estado."""
        started = time.monotonic()
        to = State(to)
        cur = self.state() or State.BOOT
        if to not in TRANSITIONS[cur]:
            self.wal_append(f"transição ilegal {cur.value}->{to.value}", classe, cause, action,
                            "rejeitada", sha)
            env = Envelope.of("igc.fsm", "SessionMemory.transition", Status.ERROR_CONTENT,
                              f"transição {cur.value} → {to.value} não permitida",
                              metrics={"from": cur.value, "to": to.value})
            return env.close(started)
        text = self.state_file.read_text(encoding="utf-8") if self.state_file.exists() else ""
        text = re.sub(r"^current_state:.*$", f"current_state: {to.value}", text, flags=re.M)
        text = re.sub(r"^previous_state:.*$", f"previous_state: {cur.value}", text, flags=re.M)
        self.state_file.write_text(text, encoding="utf-8")
        self.wal_append(f"{cur.value}->{to.value}", classe, cause, action, result, sha)
        env = Envelope.of("igc.fsm", "SessionMemory.transition", Status.SUCCESS,
                          f"FSM {cur.value} → {to.value}",
                          addenda=[Addendum("state", f"{SESSION_DIR}/STATE.yml"),
                                   Addendum("log", f"{SESSION_DIR}/WAL.md")],
                          metrics={"from": cur.value, "to": to.value})
        return env.close(started)

    # --------------------------------------------------------- CHECKPOINT (M4)
    def git_head(self) -> str:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root,
                              capture_output=True, text=True)
        return proc.stdout.strip() if proc.returncode == 0 else ""

    def write_checkpoint(self, sha: str | None = None, state: str = "EXEC") -> Envelope:
        started = time.monotonic()
        sha = sha or self.git_head()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file.write_text(
            f"sha={sha}\nwal_sha256={self.wal_hash()}\nstate={state}\nverified_at={utcnow()}\n",
            encoding="utf-8")
        env = Envelope.of("igc.checkpoint", "SessionMemory.write_checkpoint", Status.SUCCESS,
                          f"checkpoint {sha[:7]} + wal {self.wal_hash()}",
                          addenda=[Addendum("json", f"{SESSION_DIR}/CHECKPOINT")],
                          metrics={"sha": sha, "wal_sha256": self.wal_hash()})
        return env.close(started)

    def read_checkpoint(self) -> dict[str, str]:
        if not self.checkpoint_file.exists():
            return {}
        out = {}
        for line in self.checkpoint_file.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
        return out

    def verify(self) -> Envelope:
        """R2/M4 — `git fsck` + ancestralidade do SHA + integridade do WAL."""
        started = time.monotonic()
        cp = self.read_checkpoint()
        if not cp.get("sha"):
            return Envelope.of("igc.verify", "SessionMemory.verify", Status.ERROR_CONTENT,
                               "CHECKPOINT ausente → RECON obrigatório",
                               metrics={"recon_required": True}).close(started)
        fsck = subprocess.run(["git", "fsck", "--no-progress"], cwd=self.root,
                              capture_output=True, text=True)
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", cp["sha"], "HEAD"],
                             cwd=self.root, capture_output=True, text=True)
        wal_ok = cp.get("wal_sha256", "") == self.wal_hash()
        metrics = {"fsck_rc": fsck.returncode, "checkpoint_is_ancestor": anc.returncode == 0,
                   "wal_integro": wal_ok, "sha": cp["sha"]}
        if fsck.returncode != 0 or anc.returncode != 0 or not wal_ok:
            env = Envelope.of("igc.verify", "SessionMemory.verify", Status.ERROR_CONTENT,
                              "divergência detectada → estado RECON obrigatório antes de escrever",
                              metrics={**metrics, "recon_required": True},
                              addenda=[Addendum("json", f"{SESSION_DIR}/CHECKPOINT")])
            return env.close(started)
        return Envelope.of("igc.verify", "SessionMemory.verify", Status.SUCCESS,
                           f"integridade ok em {cp['sha'][:7]}", metrics=metrics).close(started)

    # ----------------------------------------------------------------- DEBT (M5)
    def add_debt(self, description: str, cause: str, impact: str, trigger: str,
                 debt_id: str = "") -> Envelope:
        started = time.monotonic()
        self.dir.mkdir(parents=True, exist_ok=True)
        if not self.debt_file.exists():
            self.debt_file.write_text(
                "# DEBT — débitos identificados e não executados (M5)\n\n"
                "| # | Descrição | Causa | Impacto | Gatilho de retomada |\n"
                "| --- | --- | --- | --- | --- |\n", encoding="utf-8")
        existing = self.debt_file.read_text(encoding="utf-8")
        existentes = len(re.findall(r"^\| D\d+", existing, re.M))
        debt_id = debt_id or f"D{existentes + 1}"
        with self.debt_file.open("a", encoding="utf-8") as fh:
            fh.write(f"| {debt_id} | {description} | {cause} | {impact} | {trigger} |\n")
        self.wal_append(f"débito {debt_id}", EventClass.DEBT, cause, description, "registrado")
        env = Envelope.of("igc.debt", "SessionMemory.add_debt", Status.PENDING,
                          f"débito {debt_id} registrado: {description[:120]}",
                          addenda=[Addendum("report", f"{SESSION_DIR}/DEBT.md")],
                          metrics={"debt_id": debt_id})
        return env.close(started)

    # --------------------------------------------------------------- EMIT (E2/E3)
    def emit_guard(self, classe: EventClass | str, target: str, *, verified: bool | None = None,
                   sha: str = "") -> Envelope:
        """E2 — gate antes de qualquer emissão; E3 — emissão mínima rotulada."""
        started = time.monotonic()
        classe = EventClass(classe)
        ver = self.verify() if verified is None else Envelope.of(
            "igc.verify", "external", Status.SUCCESS if verified else Status.ERROR_CONTENT,
            "verificação externa", metrics={"recon_required": not verified})
        head = sha or self.git_head()
        if ver.status != Status.SUCCESS:
            return Envelope.of("igc.emit", "SessionMemory.emit_guard", Status.ERROR_CONTENT,
                               f"emissão {classe.value} bloqueada: {ver.message}",
                               metrics={"target": target}).close(started)
        payload = {"class": classe.value, "target": target, "checkpoint": head,
                   "wal": f"{SESSION_DIR}/WAL.md#{len(self.wal_entries())}"}
        return Envelope.of("igc.emit", "SessionMemory.emit_guard", Status.SUCCESS,
                           f"emissão {classe.value} autorizada com checkpoint {head[:7]}",
                           addenda=[Addendum("json", f"{SESSION_DIR}/CHECKPOINT")],
                           metrics=payload).close(started)

    # ------------------------------------------------------------- RESUME (R1-R6)
    def resume(self) -> Envelope:
        """R1-R6 — sessão nova, zero contexto: reconstrói tudo lendo o repo."""
        started = time.monotonic()
        missing = [p.name for p in (self.wal, self.state_file, self.intent_file,
                                    self.context_file, self.debt_file, self.checkpoint_file)
                   if not p.exists()]
        if missing:
            return Envelope.of("igc.resume", "SessionMemory.resume", Status.ERROR_CONTENT,
                              f"memória incompleta: faltam {missing} → BOOT",
                              metrics={"missing": missing, "state": State.BOOT.value}).close(started)
        ver = self.verify()
        entries = self.wal_entries()
        cur = self.state() or State.BOOT
        recon = ver.status != Status.SUCCESS
        target = State.RECON if recon else (State.EXEC if cur in (State.EXEC, State.VERIFY) else cur)
        self.wal_append("RESUME", EventClass.CONTINUE,
                        f"retomada de linhagem (checkpoint {self.read_checkpoint().get('sha','')[:7]})",
                        "reconstrução a frio a partir de .session/",
                        f"estado {target.value}", self.git_head())
        env = Envelope.of(
            "igc.resume", "SessionMemory.resume",
            Status.SUCCESS if not recon else Status.PENDING,
            f"sessão retomada em {target.value} ({len(entries)} entradas de WAL)",
            addenda=[Addendum("log", f"{SESSION_DIR}/WAL.md"),
                     Addendum("state", f"{SESSION_DIR}/STATE.yml"),
                     Addendum("report", f"{SESSION_DIR}/DEBT.md")],
            metrics={"state": target.value, "wal_entries": len(entries),
                     "checkpoint": self.read_checkpoint(), "verify": ver.metrics,
                     "recon_required": recon})
        return env.close(started)

    # ------------------------------------------------------------------ BOOT (W2)
    def bootstrap(self) -> Envelope:
        """W2 — bootstrap verde é pré-condição para sair de BOOT."""
        started = time.monotonic()
        if not self.bootstrap_file.exists():
            return Envelope.of("igc.bootstrap", ".session/bootstrap.sh", Status.ERROR_INFRA,
                               "bootstrap.sh ausente").close(started)
        proc = subprocess.run(["bash", str(self.bootstrap_file)], cwd=self.root,
                              capture_output=True, text=True, timeout=1800)
        status = Status.SUCCESS if proc.returncode == 0 else Status.ERROR_INFRA
        return Envelope.of("igc.bootstrap", ".session/bootstrap.sh", status,
                           (proc.stdout or proc.stderr).strip().splitlines()[-1][:300] or "sem saída",
                           addenda=[Addendum("log", f"{SESSION_DIR}/bootstrap.sh")],
                           metrics={"rc": proc.returncode}).close(started)


# =============================================================================
# IGC v2.1 — Art. 7 (descoberta/registry) · 8 (WAL no CI) · 10 (profile) ·
# 11 (capabilities) · 12 (anti-padrões + gate de fechamento) · E3/E4/E5 ·
# G4/G5 · M6/M7 · T8 (transporte/HANDOFF). Tudo devolve o envelope padrão.
# =============================================================================
PROFILE_FILE = ".igc-profile.yml"
REGISTRY_FILE = ".igc-registry.yml"
IGC_TAG = "[igc-checkpoint]"
CAP_MINIMAS = ("fs_write", "vcs", "exec", "append_wal")
PROFILE_OBRIGATORIO = ("linhagem", "eventos", "bootstrap", "verificacao",
                       "integridade", "envelope", "ci", "runtime")


def _yaml(path: Path) -> tuple[dict, str]:
    try:
        import yaml
    except ImportError:                                   # pragma: no cover
        return {}, "pyyaml indisponível"
    if not path.exists():
        return {}, f"{path.name} ausente"
    try:
        return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}), ""
    except Exception as exc:                              # noqa: BLE001
        return {}, f"{path.name} inválido: {exc}"


def profile_errors(profile: dict) -> list[str]:
    """Art. 10: chaves mínimas + invariantes de conteúdo."""
    faltam = [k for k in PROFILE_OBRIGATORIO if k not in profile]
    errs = [f"chave obrigatória ausente: {k}" for k in faltam]
    if profile.get("igc_profile") not in ("1", 1, None) and not faltam:
        errs.append("igc_profile != '1'")
    env = profile.get("envelope", {}) or {}
    minimo = set(env.get("minimo") or [])
    if minimo and not {"status", "message", "checkpoint_ref"} <= minimo:
        errs.append("envelope.minimo viola E3 (status+message+checkpoint_ref)")
    rt = profile.get("runtime", {}) or {}
    for cap in rt.get("requer") or []:
        if cap not in CAP_MINIMAS:
            errs.append(f"capability desconhecida: {cap}")
    return errs


def probe_capabilities(root: Path) -> dict[str, bool]:
    """Art. 11: bootstrap TESTA capabilities antes de assumi-las."""
    root = Path(root)
    caps = {"append_wal": True}          # única garantia universal (WAL é texto puro)
    try:
        probe = root / ".igc-probe"
        probe.write_text("ok", encoding="utf-8")
        caps["fs_write"] = probe.read_text(encoding="utf-8") == "ok"
        probe.unlink()
    except OSError:
        caps["fs_write"] = False
    caps["vcs"] = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=root,
                                 capture_output=True).returncode == 0
    caps["exec"] = subprocess.run(["bash", "-c", "true"], cwd=root,
                                  capture_output=True).returncode == 0
    return caps


class Registry:
    """Art. 7 — descoberta de linhagens (D1/D2/D3) + G5 (órfãos remotos)."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.file = self.root / REGISTRY_FILE

    def read(self) -> dict:
        data, err = _yaml(self.file)
        return {"linhagens": (data.get("linhagens") or {}), "erro": err,
                "default_branch": data.get("default_branch", "main")}

    def entry(self, slug: str) -> dict:
        return self.read()["linhagens"].get(slug, {}) or {}

    def write_entry(self, slug: str, *, branch: str, checkpoint_ref: str, ativa: bool = True,
                    **extra) -> Envelope:
        """D2: registry atualizado no MESMO commit do CHECKPOINT."""
        started = time.monotonic()
        data, _ = _yaml(self.file)
        linh = dict(data.get("linhagens") or {})
        atual = dict(linh.get(slug) or {})
        atual.update({"branch": branch, "checkpoint_ref": checkpoint_ref, "ativa": ativa,
                      "atualizado_em": utcnow()[:10], **extra})
        linh[slug] = atual
        data.update({"igc_registry": "1", "linhagens": linh})
        import yaml
        self.file.write_text(
            "# IGC v2.1 — Artigo 7: registry de linhagens (D1/D2/D3)\n"
            + yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        return Envelope.of("igc.registry", "Registry.write_entry", Status.SUCCESS,
                           f"linhagem '{slug}' → {checkpoint_ref[:12]} (ativa={ativa})",
                           addenda=[Addendum("config", REGISTRY_FILE)],
                           metrics={"slug": slug, "checkpoint_ref": checkpoint_ref},
                           checkpoint_ref=checkpoint_ref).close(started)

    def divergence(self, slug: str, checkpoint_ref: str) -> bool:
        """D3: registry × CHECKPOINT divergentes ⇒ RECON + DEBT."""
        atual = (self.entry(slug).get("checkpoint_ref") or "").strip()
        return bool(atual) and not (atual.startswith(checkpoint_ref) or checkpoint_ref.startswith(atual))

    def sweep_orphans(self, *, hoje=None, days: int = 30) -> list[str]:
        """G5/W6: linhagem ativa >30d SEM checkpoint = órfã remota."""
        import datetime as _dt
        hoje = hoje or _dt.date.today()
        orfaos = []
        for slug, e in self.read()["linhagens"].items():
            ref = str(e.get("atualizado_em") or "")[:10]
            try:
                idade = (hoje - _dt.date.fromisoformat(ref)).days
            except ValueError:
                idade = days + 1
            if e.get("ativa", True) and idade > days and not e.get("checkpoint_ref"):
                orfaos.append(slug)
        return orfaos


class SessionMemoryV21(SessionMemory):
    """v2.1: profile, capabilities, idempotência, contração causal, fechamento."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root)
        self.repo = self.dir.parent
        self.registry = Registry(self.repo)

    # ------------------------------------------------------------ Art. 10/11
    def profile(self) -> tuple[dict, list[str]]:
        data, err = _yaml(self.repo / PROFILE_FILE)
        return data, ([err] if err else profile_errors(data))

    def bootstrap_v21(self, *, caps: dict[str, bool] | None = None,
                      executar: bool = False) -> Envelope:
        """T6/T7/G6: profile obrigatório; capability ausente ⇒ fallback ou BOOT recusado."""
        started = time.monotonic()
        prof, errs = self.profile()
        if not prof:
            self.add_debt(f"{PROFILE_FILE} ausente", "profile não declarado (Art. 10)",
                          "BOOT bloqueado; retomada sem mecanismo definido",
                          "criar .igc-profile.yml e reexecutar bootstrap")
            self.wal_append("PROFILE", EventClass.DEBT, errs[0] if errs else "ausente",
                            "registrar DEBT", "BOOT bloqueado (T6)")
            return Envelope.of("igc.boot", "bootstrap_v21", Status.ERROR_INFRA,
                               f"BOOT bloqueado: {errs[0] if errs else 'profile ausente'} "
                               "(Art. 10 obriga .igc-profile.yml)",
                               metrics={"erros": errs}).close(started)
        if errs:
            self.add_debt("profile inválido", "; ".join(errs), "RECON obrigatório",
                          "corrigir .igc-profile.yml")
            self.wal_append("PROFILE", EventClass.FIX, "; ".join(errs), "RECON", "profile a DEBT")
            return Envelope.of("igc.boot", "bootstrap_v21", Status.ERROR_CONTENT,
                               f"profile inválido: {'; '.join(errs)} → RECON + DEBT",
                               metrics={"erros": errs}).close(started)
        caps = probe_capabilities(self.repo) if caps is None else dict(caps)
        requer = tuple((prof.get("runtime") or {}).get("requer") or ("fs_write", "vcs", "exec"))
        fallbacks = (prof.get("runtime") or {}).get("fallbacks") or {}
        faltando = [c for c in requer if not caps.get(c, False)]
        sem_fb = [c for c in faltando if c not in fallbacks]
        if sem_fb:                                       # CP2 / G6
            self.add_debt(f"capability {','.join(sem_fb)} sem fallback", "runtime incapaz",
                          "execução parcial proibida", "declarar fallback ou trocar runtime")
            self.wal_append("CAPABILITY", EventClass.DEBT, f"{sem_fb} ausente e sem fallback",
                            "BOOT recusado", "DEBT registrado (CP2/G6)")
            return Envelope.of("igc.boot", "bootstrap_v21", Status.ERROR_INFRA,
                               f"BOOT recusado: {sem_fb} sem fallback declarado (G6/CP2) — "
                               "nunca execução parcial",
                               metrics={"caps": caps, "faltando": faltando}).close(started)
        for c in faltando:                               # CP1
            self.wal_append("CAPABILITY", EventClass.FIX, f"{c} ausente neste runtime",
                            f"fallback: {fallbacks[c]}", "ativado (CP1)")
        if executar:
            cmd = ((prof.get("bootstrap") or {}).get("comando") or "").strip()
            if cmd:
                rc = subprocess.run(["bash", "-c", cmd], cwd=self.repo).returncode
                if rc:
                    return Envelope.of("igc.boot", "bootstrap_v21", Status.ERROR_INFRA,
                                       f"bootstrap do profile falhou (exit {rc}); FSM não sai de BOOT (W2)",
                                       metrics={"caps": caps}).close(started)
        return Envelope.of("igc.boot", "bootstrap_v21", Status.SUCCESS,
                           f"BOOT verde: caps={sum(caps.values())}/{len(caps)}; "
                           f"fallbacks={[c for c in faltando] or 'nenhum'}",
                           metrics={"caps": caps, "faltando": faltando,
                                    "fallbacks_usados": [fallbacks.get(c, "") for c in faltando]},
                           checkpoint_ref=(self.read_checkpoint() or {}).get("sha", "")).close(started)

    # ------------------------------------------------------- Art. 7 (R1/R7/D3)
    def discover(self, slug: str = "") -> Envelope:
        """R1: registry → linhagem → .session/; R7: sem pista ⇒ BOOT legítimo."""
        started = time.monotonic()
        reg = self.registry.read()
        linh = reg["linhagens"]
        if not linh:
            if not self.dir.exists():
                self.wal_append("BOOT", EventClass.IMPLEMENT, "registry inexistente e sem .session/",
                                "BOOT legítimo (R7)", "não inventar linhagem")
                return Envelope.of("igc.discover", "discover", Status.SUCCESS,
                                   "nenhuma linhagem conhecida → BOOT legítimo (R7)",
                                   metrics={"linhagens": 0, "boot": True}).close(started)
            return Envelope.of("igc.discover", "discover", Status.PENDING,
                               "registry vazio, mas .session/ existe → reconstruir e publicar registry",
                               metrics={"linhagens": 0}).close(started)
        slug = slug or next(iter(linh))
        cp = self.read_checkpoint()
        div = self.registry.divergence(slug, cp.get("sha", ""))
        if div:
            self.add_debt(f"registry × CHECKPOINT divergentes ({slug})",
                          "emissão sem D2 ou checkpoint adulterado", "RECON obrigatório (D3)",
                          "realinhar registry e CHECKPOINT")
            self.wal_append("RECON", EventClass.FIX, f"divergência registry×checkpoint em {slug}",
                            "RECON + DEBT", "D3 aplicado")
        return Envelope.of("igc.discover", "discover", Status.SUCCESS if not div else Status.ERROR_CONTENT,
                           f"linhagem '{slug}' → {linh[slug].get('branch')} "
                           f"(checkpoint {linh[slug].get('checkpoint_ref', '-')[:12]})",
                           metrics={"slug": slug, "branch": linh[slug].get("branch"),
                                    "ativa": linh[slug].get("ativa"), "divergencia": div},
                           checkpoint_ref=cp.get("sha", "")).close(started)

    # ------------------------------------------------------------- E3/E4/E5
    def emit(self, classe: EventClass | str, target: str, *, event_id: str = "",
             verified: bool | None = None, sha: str = "") -> Envelope:
        """E4 (idempotência por chave) + E3 (rótulo+checkpoint+âncora WAL) + A4 (HANDOFF)."""
        started = time.monotonic()
        classe = EventClass(classe)
        cp_sha = sha or (self.read_checkpoint() or {}).get("sha", "") or self.git_head()
        key = f"{event_id}@{cp_sha[:12]}" if event_id else ""
        if key:
            vistos = [e for e in self.wal_entries()
                      if key in f"{e.get('evento','')}|{e.get('resultado','')}"]
            if vistos:                                   # E4 / G2
                return Envelope.of("igc.emit", "emit", Status.PENDING,
                                   f"emissão recusada: chave (event_id={event_id}, "
                                   f"checkpoint={cp_sha[:12]}) já consta no WAL → sem duplicata (E4/G2)",
                                   metrics={"key": key, "idempotente": True},
                                   checkpoint_ref=cp_sha).close(started)
        base = self.emit_guard(classe, target, verified=verified, sha=cp_sha)
        base.metrics.update({"event_id": event_id, "key": key, "class": classe.value})
        base.checkpoint_ref = cp_sha
        if base.status == int(Status.SUCCESS):
            self.wal_append(f"EMIT-PREP {key or classe.value}", classe,
                            f"emissão autorizada para {target}", "emit_guard (E2)",
                            f"chave={key or '-'}", cp_sha[:12])
        return base

    def contract_emit(self, classe: EventClass | str, ref: str, *, debt_id: str = "",
                      efeito_existe: bool = True) -> Envelope:
        """E5: contração causal do EMIT — efeito verificado + WAL + débito resolvido."""
        started = time.monotonic()
        classe = EventClass(classe)
        if not efeito_existe or not ref or ref == "-":
            self.wal_append("EMIT", classe, "efeito não confirmado", "contração falhou",
                            "emissão incompleta (E5)", "-")
            return Envelope.of("igc.emit", "contract_emit", Status.ERROR_CONTENT,
                               f"EMIT sem contratação causal: ref='{ref}' (E5) — lacuna de auditoria",
                               metrics={"ref": ref}).close(started)
        self.wal_append("EMIT", classe, "efeito contratado", f"verificar {ref}", f"ref={ref}", ref[:12])
        if debt_id:
            self.resolve_debt(debt_id, f"EMIT contratado: {ref}")
        return Envelope.of("igc.emit", "contract_emit", Status.SUCCESS,
                           f"EMIT {classe.value} contratado: {ref}",
                           metrics={"ref": ref, "debt_resolvido": debt_id or None},
                           checkpoint_ref=ref).close(started)

    def resolve_debt(self, debt_id: str, motivo: str) -> bool:
        """M5: débito resolvido por linha nova (nunca apagando histórico)."""
        if not self.debt_file.exists():
            return False
        txt = self.debt_file.read_text(encoding="utf-8")
        linhas = txt.splitlines()
        for i, ln in enumerate(linhas):
            if ln.startswith(f"| {debt_id} ") or ln.startswith(f"| {debt_id}|"):
                linhas.insert(i + 1, f"| {debt_id}-R | RESOLVIDO | {motivo} | "
                                     f"{utcnow()[:10]} | encerrado | {utcnow()[:19]} |")
                self.debt_file.write_text("\n".join(linhas) + "\n", encoding="utf-8")
                return True
        return False

    # ------------------------------------------------------------------- G4
    def register_conflict(self, linhagem_a: str, linhagem_b: str, artefato: str,
                          *, merge_silencioso: bool = False) -> Envelope:
        """G4: conflito visível, nunca silencioso; merge silencioso é reprovado."""
        started = time.monotonic()
        if merge_silencioso:
            self.wal_append("CONFLICT", EventClass.FIX,
                            f"{linhagem_a} × {linhagem_b} em {artefato}",
                            "merge silencioso detectado", "REPROVADO (G4)")
            return Envelope.of("igc.conflict", "register_conflict", Status.ERROR_CONTENT,
                               f"merge silencioso reprovado em {artefato} (G4) — conflito "
                               f"{linhagem_a} × {linhagem_b} exige entrada CONFLICT",
                               metrics={"artefato": artefato}).close(started)
        self.wal_append("CONFLICT", EventClass.DEBT,
                        f"{linhagem_a} × {linhagem_b} em {artefato}",
                        "conflito tornado explícito", "registrado (G4)")
        self.add_debt(f"conflito {linhagem_a} × {linhagem_b}", f"duas linhagens em {artefato}",
                      "risco de perda silenciosa", "resolver antes do merge")
        return Envelope.of("igc.conflict", "register_conflict", Status.SUCCESS,
                           f"conflito explícito registrado: {artefato} ({linhagem_a} × {linhagem_b})",
                           metrics={"artefato": artefato, "linhagens": [linhagem_a, linhagem_b]}).close(started)

    # ------------------------------------------------------------------- M7
    def base_sanity(self, base: str, upstream: str = "origin/main",
                    *, limiar_arquivos: int = 200, limiar_linhas: int = 5000) -> Envelope:
        """M7/W1': sanidade de base ANTES de criar linhagem (anti-padrão EV-1)."""
        started = time.monotonic()
        proc = subprocess.run(["git", "diff", "--stat", base, upstream], cwd=self.repo,
                              capture_output=True, text=True)
        tail = (proc.stdout.strip().splitlines() or [""])[-1]
        m = re.search(r"(\d+) files? changed(?:, (\d+) insertion)?", tail)
        files = int(m.group(1)) if m else 0
        ins = int(m.group(2)) if m and m.group(2) else 0
        d = re.search(r"(\d+) deletion", tail)
        dels = int(d.group(1)) if d else 0
        anomalia = proc.returncode != 0 or files > limiar_arquivos or dels > limiar_linhas
        if anomalia:
            causa = (f"anomalia de base: {files} arquivos/{dels} linhas removidas "
                     f"({base[:12]}..{upstream})")
            self.wal_append("M7-BASE", EventClass.FIX, causa, "base alternativa justificada",
                            "causa raiz registrada no WAL (EV-1)")
            return Envelope.of("igc.base", "base_sanity", Status.ERROR_CONTENT,
                               f"{causa} — linhagem NÃO pode usar essa base sem justificativa (M7/W1')",
                               metrics={"files": files, "insertions": ins, "deletions": dels,
                                        "anomalia": True}).close(started)
        self.wal_append("M7-BASE", EventClass.CONTINUE, f"base {base[:12]} vs {upstream}",
                        "diff amplo sem anomalia", f"PASS ({files} arquivos/{dels} deleções)")
        return Envelope.of("igc.base", "base_sanity", Status.SUCCESS,
                           f"sanidade de base PASS: {files} arquivos divergentes, {dels} deleções (M7)",
                           metrics={"files": files, "insertions": ins, "deletions": dels,
                                    "anomalia": False}).close(started)

    # ------------------------------------------------------- T8 (transporte)
    def bundle_create(self, dest: str | Path, *, base: str | None = None,
                      branch: str | None = None) -> Envelope:
        started = time.monotonic()
        dest = Path(dest)
        refspec = f"{base}..{branch}" if base and branch else (branch or "--all")
        args = ["git", "bundle", "create", str(dest)] + ([refspec] if isinstance(refspec, str) else refspec)
        if base and branch:
            args = ["git", "bundle", "create", str(dest), f"{base}..{branch}"]
        proc = subprocess.run(args, cwd=self.repo, capture_output=True, text=True)
        ok = proc.returncode == 0 and dest.exists()
        self.wal_append("TRANSPORT", EventClass.HANDOFF if ok else EventClass.FIX,
                        "handoff offline exigido (W7/T8)", f"git bundle create {dest.name}",
                        f"{'ok' if ok else 'falha'}: {dest.stat().st_size if dest.exists() else 0} B",
                        (branch or "")[:12])
        return Envelope.of("igc.transport", "bundle_create",
                           Status.SUCCESS if ok else Status.ERROR_INFRA,
                           f"bundle {'gerado' if ok else 'FALHOU'}: {dest} ({proc.stderr.strip()[:120]})",
                           addenda=[Addendum("bundle", str(dest))],
                           metrics={"bytes": dest.stat().st_size if dest.exists() else 0}).close(started)

    def bundle_verify(self, path: str | Path) -> Envelope:
        started = time.monotonic()
        proc = subprocess.run(["git", "bundle", "verify", str(path)], cwd=self.repo,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        return Envelope.of("igc.transport", "bundle_verify",
                           Status.SUCCESS if ok else Status.ERROR_INFRA,
                           "bundle verificado (T8)" if ok else f"bundle inválido: {proc.stderr.strip()[:160]}",
                           metrics={"ok": ok}).close(started)

    # ------------------------------------------------------------- M6 (skips)
    def skips_justificados(self, reasons: list[str]) -> tuple[bool, list[str]]:
        """M6: skip sem justificativa em INTENT.md/DEBT.md/profile = falha de VERIFY."""
        prof, _ = self.profile()
        texto = " ".join([
            " ".join((prof.get("verificacao") or {}).get("skips_justificados") or []),
            self.debt_file.read_text(encoding="utf-8") if self.debt_file.exists() else "",
            (self.dir / "INTENT.md").read_text(encoding="utf-8")
            if (self.dir / "INTENT.md").exists() else "",
        ]).lower()
        def justificado(r: str) -> bool:
            r = r.lower()
            if r in texto or r.split(":")[0].strip() in texto:
                return True
            tokens = [t for t in re.split(r"[\s/():.,;—-]+", r) if len(t) > 4]
            return bool(tokens) and all(t in texto for t in tokens)

        injust = [r for r in reasons if r and not justificado(r)]
        return (not injust), injust

    # ------------------------------------------------------- Art. 12 fechamento
    def _wal_append_only(self) -> bool:
        """Anti-padrão: edição de entrada do WAL em vez de entrada nova."""
        proc = subprocess.run(["git", "show", f"HEAD:{SESSION_DIR}/WAL.md"], cwd=self.repo,
                              capture_output=True, text=True)
        if proc.returncode != 0:
            return True                                  # primeira gravação
        atual = set(self.wal.read_text(encoding="utf-8").splitlines()) if self.wal.exists() else set()
        return all(ln in atual for ln in proc.stdout.splitlines() if ln.startswith("|"))

    def measure_verification(self) -> bool:
        """D14 quitado: verde é medido executando o comando de verificação do profile."""
        prof, _ = self.profile()
        cmd = ((prof.get("verificacao") or {}).get("comando") or "").strip()
        if not cmd:
            return False
        rc = subprocess.run(["bash", "-lc", cmd], cwd=self.repo, capture_output=True).returncode
        self.wal_append("VERIFY-MEDIDA", EventClass.CONTINUE,
                        "D14: fechamento não pode aceitar verde declarado", cmd, f"exit {rc}")
        return rc == 0

    def closing_gate(self, *, verificacao_verde: bool | None = None, roundtrip_verde: bool | None = None,
                     territorio_pruned: bool = True, modo: str = "continuidade",
                     skips: list[str] | None = None) -> Envelope:
        """Art. 12: auto-checagem antes de CLOSE. Nota < 9.5 ⇒ não fecha, volta a EXEC."""
        started = time.monotonic()
        cp = self.read_checkpoint()
        if verificacao_verde is None:                      # D14: medir, nunca aceitar declarado
            verificacao_verde = self.measure_verification()
        ok_skip, injust = self.skips_justificados(skips or [])
        contexto = (self.dir / "CONTEXT.md")
        checks = {
            "wal_append_only": self._wal_append_only(),
            "checkpoint_gravado": bool(cp) and cp.get("wal_sha256", "") == self.wal_hash(),
            "verificacao_verde": bool(verificacao_verde),
            "skips_justificados_M6": ok_skip,
            "emit_contratado_E5": any(e.get("evento") == "EMIT" and e.get("resultado", "-") not in ("-", "")
                                      for e in self.wal_entries()),
            "debitos_com_gatilho": self._debitos_ok(),
            "territorio_pruned": bool(territorio_pruned),
            "desvios_declarados": bool(contexto.exists() and "DEV-" in contexto.read_text(encoding="utf-8")),
            "roundtrip_verde_se_handoff": (roundtrip_verde is True) if modo == "handoff" else True,
        }
        nota = round(10.0 * sum(checks.values()) / len(checks), 2)
        pend = [k for k, v in checks.items() if not v]
        fecha = nota >= 9.5 and not pend
        self.wal_append("CLOSE-GATE", EventClass.CONTINUE if fecha else EventClass.FIX,
                        f"auto-checagem Art. 12 (nota {nota})",
                        "closing_gate", ("CLOSE autorizado" if fecha else f"volta a EXEC: {pend}"))
        if not fecha:
            self.transition(State.EXEC, event="CLOSE-GATE→EXEC", classe=EventClass.FIX,
                            cause=f"nota {nota} < 9.5", action="corrigir pendências",
                            result=str(pend))
        return Envelope.of("igc.close", "closing_gate",
                           Status.SUCCESS if fecha else Status.ERROR_CONTENT,
                           f"gate de fechamento: nota {nota}/10 — "
                           + ("CLOSE autorizado" if fecha else f"pendências {pend}; retorna a EXEC"),
                           metrics={"nota": nota, "checks": checks, "pendencias": pend,
                                    "skips_injustificados": injust},
                           checkpoint_ref=cp.get("sha", "")).close(started)

    def _debitos_ok(self) -> bool:
        if not self.debt_file.exists():
            return True
        linhas = [ln for ln in self.debt_file.read_text(encoding="utf-8").splitlines()
                  if ln.startswith("| D")]
        return all(len([c for c in ln.split("|")[1:-1] if c.strip()]) >= 4 for ln in linhas)
