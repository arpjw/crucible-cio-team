# Crucible CIO Team — Codespace Quickstart

Your Codespace has automatically installed all Python dependencies, Claude Code, and initialized the SQLite database. Follow these steps to get operational.

---

## Step 1 — Configure Environment Variables

Copy the environment template and add your API keys:

```bash
cp .env.template .env
```

Open `.env` and fill in:

```
ANTHROPIC_API_KEY=sk-ant-...      # Required — get from console.anthropic.com
FRED_API_KEY=...                   # Required — get from fred.stlouisfed.org/docs/api/api_key.html
IB_HOST=127.0.0.1                  # Optional — only if connecting to Interactive Brokers
IB_PORT=7497
IB_CLIENT_ID=1
```

---

## Step 2 — Verify FRED Connection

Confirm your FRED API key is working:

```bash
python scripts/verify-fred.py
```

Expected output: `FRED connection OK — [indicator name] retrieved successfully.`

If you see an error, double-check your `FRED_API_KEY` in `.env`.

---

## Step 3 — Open Claude Code

```bash
claude
```

Claude Code will open in the integrated terminal. All 40+ slash commands are immediately available.

---

## Step 4 — Configure Your Fund

Run the interactive onboarding wizard. This populates `context/fund-mandate.md`, `context/portfolio-state.md`, and `context/risk-limits.md` — required inputs for every agent.

```
/setup
```

The wizard conducts a five-stage interview: Fund Identity, Strategy, Risk Parameters, Operations, and Regulatory. Takes about ten minutes. **Nothing works correctly until this is complete.**

---

## Step 5 — Run Your First Pipeline

Once setup is complete, submit your first paper trade through the full agent stack:

```
/run-pipeline Long 2% NAV ES futures, trend signal fires on 20-day breakout
```

The pipeline will run all 11 agents in sequence, apply the context bus, and produce a unified Pipeline Report with a final actionable instruction.

---

## Available Commands (once setup is complete)

| Command | What it does |
|---------|-------------|
| `/run-pipeline [decision]` | Full pipeline — primary entry point for all trade decisions |
| `/stress-test` | Run portfolio through 5 historical crisis scenarios |
| `/calibration-report` | Monthly agent accuracy and calibration metrics |
| `/export-audit` | Compile 30-day audit document for LP review |
| `/crucible [trade]` | Five-agent panel review (compliance, risk, macro, signal, systems) |
| `/postmortem [trade] \| [outcome] \| [date]` | Feed losing trade back through agents to find what was missed |
| `/regime-classifier` | Current market regime state machine |
| `/drawdown-monitor` | Portfolio drawdown circuit breaker status |

See `CLAUDE.md` for the full command reference.
