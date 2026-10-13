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
