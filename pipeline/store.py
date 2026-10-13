"""Backend de persistência (SQLite) do pipeline gate-driven — padrão Repository."""
from __future__ import annotations

import dataclasses
import datetime as _dt
import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

from .domain import Addendum, Envelope, NextIssue, Status, utcnow

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id            TEXT PRIMARY KEY,
    started_at    TEXT NOT NULL,
    finished_at   TEXT,
    status        INTEGER,
    direction     TEXT,
    trigger       TEXT,
    next_issue    TEXT,
    summary       TEXT
);
CREATE TABLE IF NOT EXISTS envelopes (
    id          TEXT PRIMARY KEY,
    run_id      TEXT NOT NULL REFERENCES runs(id),
    gate        TEXT NOT NULL,
    action      TEXT NOT NULL,
    status      INTEGER NOT NULL,
    message     TEXT NOT NULL,
    direction   TEXT NOT NULL,
    payload     TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS addenda (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    envelope_id  TEXT NOT NULL REFERENCES envelopes(id),
    kind         TEXT NOT NULL,
    path         TEXT NOT NULL,
    name         TEXT,
    note         TEXT
);
CREATE TABLE IF NOT EXISTS issues (
    key         TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    gate        TEXT NOT NULL,
    direction   TEXT NOT NULL,
    reason      TEXT,
    body        TEXT,
    number      INTEGER,
    url         TEXT,
    state       TEXT NOT NULL DEFAULT 'proposed',
    created_at  TEXT NOT NULL,
    closed_at   TEXT
);
CREATE INDEX IF NOT EXISTS idx_env_gate ON envelopes(gate, created_at);
CREATE INDEX IF NOT EXISTS idx_issue_state ON issues(state, gate);
"""


@dataclasses.dataclass(slots=True)
class IssueRecord:
    key: str
    title: str
    gate: str
    direction: str
    reason: str
    body: str
    number: int | None = None
    url: str | None = None
    state: str = "proposed"
    created_at: str = ""
    closed_at: str | None = None


class PipelineStore:
    """Repositório SQLite: runs, envelopes, addenda e issues (estado de continuidade)."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    # ---------------- runs ---------------- #
    def start_run(self, run_id: str, trigger: str) -> str:
        self.conn.execute(
            "INSERT OR REPLACE INTO runs (id, started_at, trigger) VALUES (?, ?, ?)",
            (run_id, utcnow(), trigger),
        )
        self.conn.commit()
        return run_id

    def finish_run(self, run_id: str, status: int, direction: str, next_issue: str | None,
                   summary: str) -> None:
        self.conn.execute(
            "UPDATE runs SET finished_at=?, status=?, direction=?, next_issue=?, summary=? WHERE id=?",
            (utcnow(), status, direction, next_issue, summary, run_id),
        )
        self.conn.commit()

    # ---------------- envelopes ---------------- #
    def record(self, run_id: str, env: Envelope) -> Envelope:
        self.conn.execute(
            "INSERT OR REPLACE INTO envelopes (id, run_id, gate, action, status, message,"
            " direction, payload, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (env.id, run_id, env.gate, env.action, env.status, env.message,
             env.direction, json.dumps(env.to_dict(), ensure_ascii=False), utcnow()),
        )
        for a in env.addenda:
            self.conn.execute(
                "INSERT INTO addenda (envelope_id, kind, path, name, note) VALUES (?,?,?,?,?)",
                (env.id, a.kind, a.path, a.name, a.note),
            )
        self.conn.commit()
        return env

    def last_envelope(self, gate: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT payload FROM envelopes WHERE gate=? ORDER BY created_at DESC, rowid DESC LIMIT 1",
            (gate,),
        ).fetchone()
        return json.loads(row["payload"]) if row else None

    def history(self, limit: int = 50) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT payload FROM envelopes ORDER BY rowid DESC LIMIT ?", (limit,)
        ).fetchall()
        return [json.loads(r["payload"]) for r in rows]

    # ---------------- issues ---------------- #
    def save_issue(self, rec: IssueRecord) -> IssueRecord:
        self.conn.execute(
            "INSERT INTO issues (key, title, gate, direction, reason, body, number, url,"
            " state, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)"
            " ON CONFLICT(key) DO UPDATE SET title=excluded.title, body=excluded.body,"
            " reason=excluded.reason, direction=excluded.direction,"
            " number=COALESCE(excluded.number, issues.number),"
            " url=COALESCE(excluded.url, issues.url), state=excluded.state",
            (rec.key, rec.title, rec.gate, rec.direction, rec.reason, rec.body,
             rec.number, rec.url, rec.state, rec.created_at or utcnow()),
        )
        self.conn.commit()
        return rec

    def issue(self, key: str) -> IssueRecord | None:
        row = self.conn.execute("SELECT * FROM issues WHERE key=?", (key,)).fetchone()
        return IssueRecord(**dict(row)) if row else None

    def open_issues(self, gate: str | None = None) -> list[IssueRecord]:
        q = "SELECT * FROM issues WHERE state IN ('proposed','open')"
        args: tuple[Any, ...] = ()
        if gate:
            q += " AND gate=?"
            args = (gate,)
        return [IssueRecord(**dict(r)) for r in self.conn.execute(q + " ORDER BY created_at", args)]

    def close_issue(self, key: str) -> None:
        self.conn.execute("UPDATE issues SET state='closed', closed_at=? WHERE key=?",
                          (utcnow(), key))
        self.conn.commit()

    # ---------------- estado agregado ---------------- #
    def state(self) -> dict[str, Any]:
        runs = self.conn.execute(
            "SELECT COUNT(*) AS n, MAX(started_at) AS last FROM runs").fetchone()
        envs = self.conn.execute(
            "SELECT status, COUNT(*) AS n FROM envelopes GROUP BY status").fetchall()
        issues = self.conn.execute(
            "SELECT state, COUNT(*) AS n FROM issues GROUP BY state").fetchall()
        return {
            "runs": runs["n"],
            "last_run": runs["last"],
            "envelopes_by_status": {Status(int(r["status"])).name.lower(): r["n"] for r in envs},
            "issues_by_state": {r["state"]: r["n"] for r in issues},
        }

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "PipelineStore":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
