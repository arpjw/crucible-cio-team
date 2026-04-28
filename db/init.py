#!/usr/bin/env python3
"""
Initialize the Crucible SQLite database.
Creates db/crucible.db with the three core tables if it doesn't exist.
Safe to run repeatedly — exits cleanly if the database is already initialized.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "crucible.db"

DDL = """
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp          TEXT NOT NULL,
    submission         TEXT NOT NULL,
    submission_type    TEXT,
    compliance_verdict TEXT,
    risk_verdict       TEXT,
    macro_verdict      TEXT,
    signal_verdict     TEXT,
    systems_verdict    TEXT,
    final_verdict      TEXT NOT NULL,
    override_log       TEXT,
    pipeline_report    TEXT,
    created_at         TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nav_snapshots (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    date               TEXT NOT NULL,
    nav_usd            REAL,
    positions_hash     TEXT,
    gross_leverage     REAL,
    net_leverage       REAL,
    margin_utilization REAL,
    created_at         TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_verdicts (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  INTEGER REFERENCES pipeline_runs(id),
    agent_name       TEXT NOT NULL,
    verdict          TEXT NOT NULL,
    inputs           TEXT,
    outputs          TEXT,
    flags            TEXT,
    timestamp        TEXT NOT NULL,
    actual_outcome   TEXT,
    miss_type        TEXT,
    created_at       TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db() -> bool:
    """Create the database and tables. Returns True if newly created, False if already existed."""
    already_existed = DB_PATH.exists()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(DDL)
        conn.commit()
    return not already_existed


def main() -> None:
    created = init_db()
    if created:
        print(f"[crucible-db] Database initialized: {DB_PATH}")
        print("[crucible-db] Tables created: pipeline_runs, nav_snapshots, agent_verdicts")
    else:
        print(f"[crucible-db] Database already exists: {DB_PATH} — no changes made")


if __name__ == "__main__":
    main()
