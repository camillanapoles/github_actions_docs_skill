"""CLI do pipeline gate-driven (BPMN-like) com backend SQLite.

Uso:
    python3 -m pipeline.cli run                      # todos os gates, estado em .ci/
    python3 -m pipeline.cli run --gate tests --gate skill
    python3 -m pipeline.cli run --online             # consulta gh (runs/issues) no CI
    python3 -m pipeline.cli blueprint                # imprime o fluxo BPMN em JSON
    python3 -m pipeline.cli state                    # estado acumulado no SQLite

Todo gate devolve um envelope JSON (id, gate, status, message, addenda, next_issue,
direction). Exit code: 0 = todos aprovados; 1 = gate reprovado (continuidade publicada).
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

from . import blueprint
from .domain import Envelope, Status
from .engine import Context, Orchestrator
from .store import PipelineStore

ROOT = Path(__file__).resolve().parents[1]


def _cmd_run(args: argparse.Namespace) -> int:
    db = Path(args.db) if args.db else ROOT / ".ci" / "pipeline.sqlite3"
    ctx = Context(root=ROOT, run_id=args.run_id or f"run-{uuid.uuid4().hex[:8]}",
                  langs=tuple(x.strip() for x in args.langs.split(",") if x.strip()),
                  online=args.online, trigger=args.trigger)
    with PipelineStore(db) as store:
        state = Orchestrator(store, ctx).run(only=tuple(args.gate) if args.gate else None)

    if args.envelopes:
        for env in state["envelopes"]:
            print(json.dumps(env, ensure_ascii=False))
    else:
        print(json.dumps(state, ensure_ascii=False, indent=2))

    if not args.no_exit_code:
        return 0 if state["status"] == Status.SUCCESS else 1
    return 0


def _cmd_blueprint(_args: argparse.Namespace) -> int:
    print(json.dumps(blueprint.as_bpmn_dict(), ensure_ascii=False, indent=2))
    return 0


def _cmd_state(args: argparse.Namespace) -> int:
    db = Path(args.db) if args.db else ROOT / ".ci" / "pipeline.sqlite3"
    with PipelineStore(db) as store:
        payload = {"state": store.state(),
                   "history": store.history(limit=args.limit),
                   "open_issues": [json.loads(json.dumps(i.__dict__, default=str))
                                   for i in store.open_issues()]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pipeline", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command")

    run = sub.add_parser("run", help="executa os gates do blueprint")
    run.add_argument("--gate", action="append", default=[], help="gate específico (repetível)")
    run.add_argument("--db", default="", help="caminho do SQLite (default .ci/pipeline.sqlite3)")
    run.add_argument("--langs", default="pt,en")
    run.add_argument("--online", action="store_true", help="consulta gh (runs/issues)")
    run.add_argument("--trigger", default="manual")
    run.add_argument("--run-id", default="")
    run.add_argument("--envelopes", action="store_true", help="imprime 1 envelope JSON por linha (NDJSON)")
    run.add_argument("--no-exit-code", action="store_true", help="não reprova o processo em gate vermelho")
    run.set_defaults(func=_cmd_run)

    bp = sub.add_parser("blueprint", help="imprime o fluxo BPMN (nós e transições)")
    bp.set_defaults(func=_cmd_blueprint)

    st = sub.add_parser("state", help="estado acumulado (runs, envelopes, issues)")
    st.add_argument("--db", default="")
    st.add_argument("--limit", type=int, default=20)
    st.set_defaults(func=_cmd_state)

    args = ap.parse_args(argv)
    if not getattr(args, "command", None):
        ap.print_help()
        return 2
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
