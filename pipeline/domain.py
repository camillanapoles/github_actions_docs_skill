"""Domínio do pipeline gate-driven (BPMN-like) — entidades e contrato do envelope JSON.

Toda action do pipeline devolve um :class:`Envelope` serializável em JSON com:
``id``, ``gate``, ``action``, ``status`` (0=sucesso, 1=erro de conteúdo, 2=erro de
infra, 3=pendência/continuidade, 4=ignorado), ``message``, ``addenda`` (anexos:
paths/nomes gerados), ``next_issue`` (mesma issue se reprovou; próxima indexada se
aprovou), ``direction`` (fix|retry|continue|debt) e ``metrics``.
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import enum
import json
import uuid
from typing import Any, Iterable, Sequence


class Status(enum.IntEnum):
    """Códigos de status exigidos pelo contrato (extensível)."""

    SUCCESS = 0          # gate aprovado, testes determinísticos verdes
    ERROR_CONTENT = 1    # erro tipo 1: conteúdo/qualidade/conformidade → direção `fix`
    ERROR_INFRA = 2      # erro tipo 2: ambiente/rede/ferramenta ausente → direção `retry`
    PENDING = 3          # entrega incompleta (escopo pendente) → direção `continue`
    SKIPPED = 4          # gate não aplicável neste contexto → direção `continue`


DIRECTION: dict[Status, str] = {
    Status.SUCCESS: "continue",
    Status.ERROR_CONTENT: "fix",
    Status.ERROR_INFRA: "retry",
    Status.PENDING: "continue",
    Status.SKIPPED: "continue",
}


def utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


@dataclasses.dataclass(slots=True)
class Addendum:
    """Anexo produzido por uma action (relatório, log, artefato, site)."""

    kind: str                      # report | json | log | artifact | site | issue
    path: str                      # caminho no repositório (ou URL)
    name: str | None = None        # nome do arquivo, se diferente
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out = {"kind": self.kind, "path": self.path}
        if self.name:
            out["name"] = self.name
        if self.note:
            out["note"] = self.note
        return out


@dataclasses.dataclass(slots=True)
class NextIssue:
    """Ponteiro de continuidade: qual issue vem a seguir e por quê."""

    key: str                       # chave determinística (gate:direction:hash do estado)
    title: str
    gate: str
    direction: str
    reason: str
    number: int | None = None      # número no GitHub, quando criada
    url: str | None = None
    instructions: Sequence[str] = dataclasses.field(default_factory=list)
    acceptance: Sequence[str] = dataclasses.field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out = {
            "key": self.key,
            "title": self.title,
            "gate": self.gate,
            "direction": self.direction,
            "reason": self.reason,
            "instructions": list(self.instructions),
            "acceptance": list(self.acceptance),
        }
        if self.number is not None:
            out["number"] = self.number
        if self.url:
            out["url"] = self.url
        return out


@dataclasses.dataclass(slots=True)
class Envelope:
    """Objeto JSON obrigatório de retorno de TODA action."""

    id: str
    gate: str
    action: str
    status: int
    message: str
    direction: str
    addenda: list[Addendum] = dataclasses.field(default_factory=list)
    next_issue: NextIssue | None = None
    metrics: dict[str, Any] = dataclasses.field(default_factory=dict)
    started_at: str = ""
    finished_at: str = ""
    duration_s: float = 0.0
    blueprint: str = "gate-driven-bpmn/1"
    checkpoint_ref: str = ""   # IGC v2.1 E3: mínimo status+message+checkpoint_ref

    @classmethod
    def of(cls, gate: str, action: str, status: Status | int, message: str,
           *, addenda: Iterable[Addendum] = (), metrics: dict[str, Any] | None = None,
           started_at: str | None = None, checkpoint_ref: str = "") -> "Envelope":
        st = Status(int(status))
        return cls(
            id=f"{gate}:{uuid.uuid4().hex[:10]}",
            gate=gate,
            action=action,
            status=int(st),
            message=message,
            direction=DIRECTION[st],
            addenda=list(addenda),
            metrics=metrics or {},
            checkpoint_ref=checkpoint_ref,
            started_at=started_at or utcnow(),
            finished_at=utcnow(),
        )

    def close(self, started: float) -> "Envelope":
        import time

        self.finished_at = utcnow()
        self.duration_s = round(max(0.0, time.monotonic() - started), 3)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "blueprint": self.blueprint,
            "checkpoint_ref": self.checkpoint_ref,   # E3
            "gate": self.gate,
            "action": self.action,
            "status": self.status,
            "status_label": Status(self.status).name.lower(),
            "message": self.message,
            "direction": self.direction,
            "addenda": [a.to_dict() for a in self.addenda],
            "next_issue": self.next_issue.to_dict() if self.next_issue else None,
            "metrics": self.metrics,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_s": self.duration_s,
        }

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


@dataclasses.dataclass(frozen=True, slots=True)
class GateSpec:
    """Nó do blueprint BPMN: task + gateway de saída determinísticos."""

    id: str
    name: str
    order: int
    action: str                    # comando/função executada (auditável)
    kind: str = "task"             # task | gateway
    required: bool = True
    produces: tuple[str, ...] = ()  # addenda esperados (paths)
    acceptance: tuple[str, ...] = ()  # critérios de aceite da issue gerada
    next_on_success: str | None = None
    next_on_failure: str | None = None   # None → repete o mesmo gate (fix)
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
