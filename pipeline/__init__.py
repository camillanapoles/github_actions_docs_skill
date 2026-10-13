"""Pipeline gate-driven (BPMN-like) — backend OO + SQLite.

Toda action devolve um envelope JSON com ``id``, ``gate``, ``status``
(0=sucesso, 1=erro de conteúdo, 2=erro de infra, 3=pendência, 4=ignorado),
``message``, ``addenda`` (anexos/paths), ``next_issue`` (mesma se reprovou,
próxima indexada se aprovou) e ``direction`` (fix|retry|continue).
"""
from __future__ import annotations

from . import blueprint
from .domain import Addendum, Envelope, GateSpec, NextIssue, Status
from .engine import Action, Context, IssueFactory, Orchestrator, SkillAction
from .store import IssueRecord, PipelineStore

__all__ = [
    "Addendum", "Envelope", "GateSpec", "NextIssue", "Status",
    "Action", "Context", "IssueFactory", "Orchestrator", "SkillAction",
    "IssueRecord", "PipelineStore", "blueprint",
]
