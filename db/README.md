# Crucible Database

SQLite persistence layer for the Crucible CIO Team framework. Stores every pipeline run, daily NAV snapshot, and per-agent verdict for trend analysis, calibration, and postmortem review.

## Location

`db/crucible.db` — created automatically on first run of `db/init.py` or `scripts/update-context.py`. Never committed (listed in `.gitignore`).

## Schema

### `pipeline_runs`

One row per `/run-pipeline` execution.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment run ID |
| `timestamp` | TEXT | ISO-8601 UTC timestamp when the run completed |
| `submission` | TEXT | The full submission text passed to `/run-pipeline` |
| `submission_type` | TEXT | SIGNAL / REBALANCE / ROLL / OPERATIONAL |
| `compliance_verdict` | TEXT | CLEAR / WARNING / VIOLATION |
| `risk_verdict` | TEXT | APPROVED / FLAGGED / BLOCKED |
| `macro_verdict` | TEXT | SUPPORTS / NEUTRAL / CONTRADICTS |
| `signal_verdict` | TEXT | PASS / FLAG / BLOCK / NOT_EVALUATED |
| `systems_verdict` | TEXT | Systems Architect verdict if invoked |
| `final_verdict` | TEXT | PROCEED / WITHHELD / HARD HALT |
| `override_log` | TEXT | JSON blob of any soft-halt overrides with PM rationale |
| `pipeline_report` | TEXT | Full text of the Stage 8 Pipeline Report |
| `created_at` | TEXT | SQLite default timestamp |

### `nav_snapshots`

One row per verified NAV stamp from `/nav-calculator`.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `date` | TEXT | NAV date (YYYY-MM-DD) |
| `nav_usd` | REAL | Total fund NAV in USD |
| `positions_hash` | TEXT | MD5/SHA of portfolio-state.md at stamp time (for drift detection) |
| `gross_leverage` | REAL | Gross leverage as a decimal (e.g. 1.25 = 125%) |
| `net_leverage` | REAL | Net leverage as a decimal |
| `margin_utilization` | REAL | Margin used / margin available, 0–1 |
| `created_at` | TEXT | SQLite default timestamp |

### `agent_verdicts`

One row per agent invocation within a pipeline run.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `pipeline_run_id` | INTEGER FK | References `pipeline_runs.id` |
| `agent_name` | TEXT | e.g. `compliance-officer`, `risk-officer` |
| `verdict` | TEXT | Agent-specific verdict string |
| `inputs` | TEXT | JSON blob of inputs passed to the agent |
| `outputs` | TEXT | JSON blob of agent outputs written to the context bus |
| `flags` | TEXT | JSON array of flags raised (null if none) |
| `timestamp` | TEXT | ISO-8601 UTC |
| `actual_outcome` | TEXT | Filled by `/postmortem` — what actually happened |
| `miss_type` | TEXT | Filled by `/postmortem` — FALSE_POSITIVE / FALSE_NEGATIVE / CORRECT |
| `created_at` | TEXT | SQLite default timestamp |

## Manual Queries

Open the database with:

```bash
sqlite3 db/crucible.db
```

Useful queries:

```sql
-- Last 10 pipeline runs
SELECT id, timestamp, submission_type, final_verdict
FROM pipeline_runs ORDER BY id DESC LIMIT 10;

-- Verdict breakdown over last 30 days
SELECT final_verdict, COUNT(*) AS cnt
FROM pipeline_runs
WHERE date(timestamp) >= date('now', '-30 days')
GROUP BY final_verdict;

-- Which agents flag most often
SELECT agent_name, COUNT(*) AS flags
FROM agent_verdicts
WHERE flags IS NOT NULL
  AND date(timestamp) >= date('now', '-30 days')
GROUP BY agent_name ORDER BY flags DESC;

-- NAV trend
SELECT date, nav_usd, gross_leverage, net_leverage
FROM nav_snapshots ORDER BY date DESC LIMIT 30;

-- Full report for a specific run
SELECT pipeline_report FROM pipeline_runs WHERE id = 42;

-- Postmortem: runs where the agent was wrong
SELECT pr.id, pr.submission, av.agent_name, av.verdict, av.actual_outcome, av.miss_type
FROM agent_verdicts av
JOIN pipeline_runs pr ON pr.id = av.pipeline_run_id
WHERE av.miss_type IN ('FALSE_POSITIVE', 'FALSE_NEGATIVE');
```

## Backup

The database file is a single portable file. Back it up by copying it:

```bash
cp db/crucible.db db/crucible-$(date +%Y%m%d).db.bak
```

For automated backups, add a cron job that copies `crucible.db` to a cloud bucket after each pipeline run. The database is append-mostly and never exceeds a few hundred MB for years of daily use.

## Python API

All reads and writes go through `db/query.py`. Import directly:

```python
from db.query import log_pipeline_run, get_recent_runs, get_verdict_distribution
```

Initialize the database before first use:

```bash
python db/init.py
```

This is called automatically by `scripts/update-context.py` on every run.
