#!/usr/bin/env python3
"""
Crucible query helpers — read and write pipeline runs, NAV snapshots, and agent verdicts.
All functions open and close their own connection; safe to call from any context.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "crucible.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Writes ────────────────────────────────────────────────────────────────────

def log_pipeline_run(
    submission: str,
    verdicts_dict: dict[str, str],
    final_verdict: str,
    override_log: str | None = None,
    full_report: str | None = None,
) -> int:
    """
    Write a completed pipeline run to pipeline_runs.
    verdicts_dict keys: compliance, risk, macro, signal, systems
    Returns the new row id.
    """
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO pipeline_runs
                (timestamp, submission, submission_type,
                 compliance_verdict, risk_verdict, macro_verdict,
                 signal_verdict, systems_verdict,
                 final_verdict, override_log, pipeline_report)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _now(),
                submission,
                verdicts_dict.get("submission_type"),
                verdicts_dict.get("compliance"),
                verdicts_dict.get("risk"),
                verdicts_dict.get("macro"),
                verdicts_dict.get("signal"),
                verdicts_dict.get("systems"),
                final_verdict,
                override_log,
                full_report,
            ),
        )
        return cur.lastrowid


def log_nav_snapshot(
    date: str,
    nav: float | None,
    positions_hash: str | None,
    gross_lev: float | None,
    net_lev: float | None,
    margin_util: float | None,
) -> int:
    """Write a daily NAV snapshot. Returns the new row id."""
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO nav_snapshots
                (date, nav_usd, positions_hash,
                 gross_leverage, net_leverage, margin_utilization)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date, nav, positions_hash, gross_lev, net_lev, margin_util),
        )
        return cur.lastrowid


def log_agent_verdict(
    pipeline_run_id: int,
    agent_name: str,
    verdict: str,
    inputs: Any = None,
    outputs: Any = None,
    flags: Any = None,
) -> int:
    """
    Write an individual agent verdict linked to a pipeline run.
    inputs/outputs/flags are serialized to JSON if they are not already strings.
    Returns the new row id.
    """
    def _ser(v: Any) -> str | None:
        if v is None:
            return None
        return v if isinstance(v, str) else json.dumps(v)

    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO agent_verdicts
                (pipeline_run_id, agent_name, verdict,
                 inputs, outputs, flags, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pipeline_run_id,
                agent_name,
                verdict,
                _ser(inputs),
                _ser(outputs),
                _ser(flags),
                _now(),
            ),
        )
        return cur.lastrowid


def update_outcome(
    pipeline_run_id: int,
    actual_outcome: str,
    miss_type: str | None = None,
) -> None:
    """
    Record the actual outcome of a pipeline run (used by /postmortem).
    Updates all agent_verdicts rows for the given run.
    """
    with _connect() as conn:
        conn.execute(
            """
            UPDATE agent_verdicts
            SET actual_outcome = ?, miss_type = ?
            WHERE pipeline_run_id = ?
            """,
            (actual_outcome, miss_type, pipeline_run_id),
        )


# ── Reads ─────────────────────────────────────────────────────────────────────

def get_recent_runs(n: int = 30) -> list[dict]:
    """Return the last N pipeline runs as a list of dicts, newest first."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM pipeline_runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (n,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_verdict_distribution(days: int = 30) -> dict[str, int]:
    """
    Return counts of GO / CONDITIONAL GO / NO-GO final verdicts
    over the last N days.
    """
    since = datetime.now(timezone.utc).strftime(f"%Y-%m-%d")
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT final_verdict, COUNT(*) AS cnt
            FROM pipeline_runs
            WHERE date(timestamp) >= date('now', ? || ' days')
            GROUP BY final_verdict
            """,
            (f"-{days}",),
        ).fetchall()
    return {r["final_verdict"]: r["cnt"] for r in rows}


def get_agent_flag_frequency(days: int = 30) -> dict[str, int]:
    """
    Return how often each agent fired a flag (any non-null flags column)
    over the last N days, sorted descending by frequency.
    """
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT agent_name, COUNT(*) AS cnt
            FROM agent_verdicts
            WHERE flags IS NOT NULL
              AND date(timestamp) >= date('now', ? || ' days')
            GROUP BY agent_name
            ORDER BY cnt DESC
            """,
            (f"-{days}",),
        ).fetchall()
    return {r["agent_name"]: r["cnt"] for r in rows}
