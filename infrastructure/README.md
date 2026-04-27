# Infrastructure Setup Guide

Step-by-step technical setup for connecting the data and execution infrastructure that makes Crucible's agents operational on live data rather than described data.

## Recommended Setup Order

Complete these in sequence. Each step is a prerequisite for the next.

```
1. environment-setup.md      — Python environment, packages, credentials
2. brokers/ibkr-setup-guide.md  — IBKR Pro account and API access
3. data/fred-setup-guide.md     — FRED macro data pipeline
4. data/norgate-setup-guide.md  — Norgate futures data pipeline
5. data/kalshi-setup-guide.md   — Kalshi prediction market feed
6. data/data-pipeline-guide.md  — Unified daily pipeline wiring all sources
7. deployment/docker-compose-guide.md — Containerized pipeline (optional but recommended)
```

---

## AUM-Tier Infrastructure Recommendations

| AUM | Broker | Market Data | Admin | Notes |
|-----|--------|-------------|-------|-------|
| **$0–1M** | IBKR Pro (individual or LLC) | FRED (free) + Norgate Futures Standard + Kalshi free tier | Self-administered | All free or low-cost. Sufficient for full Crucible agent stack. IBKR minimum commission model works at this scale. Norgate ~$270/yr covers all futures. |
| **$1–10M** | IBKR Pro (fund structure / Advisor) | FRED + Norgate Futures Professional + Kalshi | Third-party fund admin engagement + auditor RFP | Engage a fund administrator (NAV calculation, investor statements). Begin auditor relationship — required for most LP mandates above $1M. Kalshi volume limits may require upgrade. |
| **$10M+** | Prime broker upgrade (Goldman, Citi, Marex, Wedbush) | Bloomberg Terminal ($25K/yr) or Refinitiv Eikon + Norgate + Kalshi Pro | Dedicated fund admin + Big-4 affiliated auditor | Bloomberg eliminates data fragmentation; single API covers rates, FX, futures, news. Prime broker provides portfolio financing, securities lending, institutional clearing. Dedicated server (bare metal or EC2 c5.xlarge) for pipeline reliability. |

### Notes on IBKR for Funds

IBKR supports multiple account structures relevant to emerging managers:

- **Individual LLC**: Works for solo GPs trading a single strategy. Simple but offers no investor segregation.
- **Investment Advisor (RIA)**: Use if managing outside capital. IBKR Advisor account lets you manage multiple client accounts under one login with allocation rules.
- **Hedge Fund Account**: For pooled vehicles with formal fund structure (LP/LLC). Requires fund documents, auditor, and in most cases a qualified custodian arrangement.

---

## Guide Index

| File | What It Covers |
|------|----------------|
| [environment-setup.md](deployment/environment-setup.md) | Python 3.11 environment, all packages, .env template, credential verification |
| [ibkr-setup-guide.md](brokers/ibkr-setup-guide.md) | IBKR account setup, TWS/Gateway, ib_insync API, paper trading, common errors |
| [fred-setup-guide.md](data/fred-setup-guide.md) | FRED API key, 20 core macro series, pandas pull, daily context update |
| [norgate-setup-guide.md](data/norgate-setup-guide.md) | Norgate subscription, NDU, norgatedata package, 24 core futures, roll conventions |
| [kalshi-setup-guide.md](data/kalshi-setup-guide.md) | Kalshi API, Python client, 15 market categories, regime weight conversion |
| [data-pipeline-guide.md](data/data-pipeline-guide.md) | scripts/update-context.py, cron job, macOS launchd, Linux crontab |
| [docker-compose-guide.md](deployment/docker-compose-guide.md) | Containerized pipeline, docker-compose.yml, log checking, credential management |

---

## What the Pipeline Produces

After a successful daily pipeline run, three context files are fresh:

```
context/macro-state.md     — FRED series + Norgate futures summary
context/portfolio-state.md — Live positions pulled from IBKR
context/kalshi-state.md    — Current Kalshi market probabilities
```

These files are read by Crucible agents at invocation time. The agents in `/run-pipeline` are only as good as the data in these files. Stale context = stale analysis.
