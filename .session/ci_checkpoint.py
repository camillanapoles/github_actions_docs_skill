#!/usr/bin/env python3
"""IGC v2.1 — Artigo 8 (C1): step final obrigatório de todo pipeline de gate.

Grava a entrada do run no WAL, recalcula o hash do WAL -> CHECKPOINT e atualiza o
registry (D2) no MESMO commit. Falha aqui = falha do job (C3). Em linhagem sem
.session/ faz o bootstrap do protocolo naquele run (C4).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from pipeline.domain import Status  # noqa: E402
from pipeline.igc import EventClass, Registry, SessionMemoryV21  # noqa: E402

STATE_FILE = ROOT / ".ci" / "pipeline-state.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="checkpoint IGC do CI (C1)")
    ap.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "local"))
    ap.add_argument("--gate", default=os.environ.get("GATE", "pipeline"))
    ap.add_argument("--classe", default="")
    ap.add_argument("--causa", default="")
    ap.add_argument("--acao", default="")
    ap.add_argument("--resultado", default="")
    ap.add_argument("--sha", default="")
    ap.add_argument("--state", default="")
    ap.add_argument("--slug", default="github-actions-docs-skill")
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args()

    root = pathlib.Path(a.root)
    mem = SessionMemoryV21(root)
    status_ci, gates_ok, gates_total = 1, 0, 0
    if STATE_FILE.exists() and root == ROOT:
        try:
            st = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            status_ci = int(st.get("status", 1))
            envelopes = st.get("envelopes") or st.get("gates") or []
            gates_total = len(envelopes)
            gates_ok = sum(1 for e in envelopes if int(e.get("status", 1)) in (0, 4))
        except Exception as exc:  # noqa: BLE001
            print(f"aviso: pipeline-state.json ilegível ({exc})", file=sys.stderr)

    if not (mem.dir / "WAL.md").exists():                     # C4
        mem.wal_append("BOOT", EventClass.IMPLEMENT,
                       "pipeline em linhagem sem .session/ (C4)",
                       f"bootstrap do protocolo no run {a.run_id}", "memória criada")

    classe = EventClass(a.classe) if a.classe else (
        EventClass.CONTINUE if status_ci == 0 else EventClass.FIX)
    sha = a.sha or mem.git_head() or "0" * 40
    resultado = a.resultado or (
        f"status {status_ci} · {gates_ok}/{gates_total or 7} gates aprovados")
    wal = mem.wal_append(f"CI run {a.run_id} ({a.gate})", classe,
                         a.causa or f"execução do gate '{a.gate}' no CI",
                         a.acao or "pipeline gate-driven + testes determinísticos",
                         resultado, sha[:12])
    estado = a.state or (mem.state().value if mem.state() else ("GATE" if status_ci == 0 else "EXEC"))
    cp = mem.write_checkpoint(sha=sha, state=estado)
    Registry(root).write_entry(
        a.slug, branch=os.environ.get("GITHUB_REF_NAME", "-"), checkpoint_ref=sha,
        ativa=True, estado_fsm=estado, modo="continuidade",
        ultima_verificacao=resultado, profile=".igc-profile.yml", memoria=".session/")

    envelope = {"id": cp.id, "status": cp.status, "status_label": Status(cp.status).name.lower(),
                "message": cp.message, "checkpoint_ref": sha, "wal_hash": mem.wal_hash(),
                "wal_entries": wal.metrics.get("entries"), "state": estado,
                "classe": classe.value, "registry": a.slug, "tag": "[igc-checkpoint]",
                "addenda": [{"kind": "checkpoint", "path": ".session/CHECKPOINT"},
                            {"kind": "log", "path": ".session/WAL.md"},
                            {"kind": "config", "path": ".igc-registry.yml"}]}
    print(json.dumps(envelope, ensure_ascii=False, indent=2))
    out = root / ".ci" / "igc-checkpoint.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if cp.status == 0 else 1                        # C3


if __name__ == "__main__":
    raise SystemExit(main())
