# Crucible CIO Team

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/arpjw/crucible-cio-team)

**An adversarial decision framework for systematic fund managers. 45 AI agents that challenge every fund decision before you execute.**

Crucible is not an assistant — it is an adversary. Every agent is built to find the reason your trade, strategy, or deployment should not proceed. The framework spans six layers covering every function of an institutional fund: governance, execution, research, intelligence, operations, and specialized roles. It is connected to live market data, persists every decision to a local database, and self-improves through postmortem analysis.

---

## How It Works

**`/run-pipeline` is the primary entry point.** One command executes the full agent stack in the correct order, passes outputs between agents automatically via the context bus, and produces a unified Pipeline Report with a final actionable instruction.

```
/run-pipeline Long 2% NAV ES futures, trend signal fires on 20-day breakout
/run-pipeline Adding EM FX carry basket, 3% NAV, 6 positions equally weighted
/run-pipeline Roll front-month CL to M+1, current position 1.5% NAV long
```

### Context Bus
The context bus (`orchestrator/context-bus.md`) is the shared state between all agents. `regime-classifier` writes `REGIME_STATE` at Stage 1 — every downstream agent reads it. `portfolio-optimizer` writes target weights at Stage 5 — `rebalancer` and `order-router` consume them at Stage 6.

### Execution Graph
```
Stage 0  Bus init — loads portfolio-state.md + risk-limits.md + macro-state.md
Stage 1  regime-classifier → writes REGIME_STATE to bus
Stage 2  compliance (hard gate) → drawdown-monitor (hard gate)
Stage 3  risk-officer + macro-analyst + kalshi-reader  [parallel]
Stage 4  signal-researcher  [if signal-related submission]
Stage 5  portfolio-optimizer → writes target weights to bus
Stage 6  rebalancer + order-router  [parallel]
Stage 7  audit-logger  [final gate]
Stage 8  unified Pipeline Report → logged to db/crucible.db
```

### Halt Behavior
- **HARD HALT** — compliance `VIOLATION` or drawdown `HALT`: pipeline stops, no execution instructions issued
- **SOFT HALT** — any other block or warning: pipeline pauses, issue surfaced, override auto-logged

### Persistence
Every Pipeline Report is written to `db/crucible.db` (SQLite) on completion. `/postmortem` reads from it to identify what agents missed. `/calibration-report` tracks agent accuracy over time. `/export-audit` compiles 30-day history for LP and regulatory distribution.

### Live Data
`scripts/update-context.py` runs daily at 6:30am and writes real data to context files before each session:
- **FRED**: 20 core macro series → `context/macro-state.md` with auto-computed regime signal summary
- **IBKR**: live positions and account summary → `context/portfolio-state.md`
- **Kalshi**: prediction market probabilities → `context/kalshi-state.md`

---

## The Stack

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 5 — GOVERNANCE                                   │
│  risk-officer · signal-researcher · systems-architect   │
│  compliance-officer · macro-analyst                     │
│  /crucible · /run-pipeline                              │
├─────────────────────────────────────────────────────────┤
│  LAYER 4 — EXECUTION                                    │
│  order-router · slippage-monitor · position-reconciler  │
│  rebalancer · roll-manager                              │
├─────────────────────────────────────────────────────────┤
│  LAYER 3 — RESEARCH                                     │
│  signal-generator · backtest-designer · correlation-mapper│
│  capacity-estimator · decay-tracker · portfolio-optimizer│
├─────────────────────────────────────────────────────────┤
│  LAYER 2 — INTELLIGENCE                                 │
│  macro-scanner · regime-classifier · flow-analyst       │
│  sentiment-tracker · earnings-watcher · kalshi-reader   │
├─────────────────────────────────────────────────────────┤
│  LAYER 1 — OPERATIONS                                   │
│  drawdown-monitor · vendor-monitor · audit-logger       │
│  cash-manager · nav-calculator · lp-reporter · tax-tracker│
├─────────────────────────────────────────────────────────┤
│  LAYER 0 — HUMAN ROLES (core)                           │
│  quant-researcher · infrastructure-auditor · fund-accountant│
│  chief-risk-officer · investor-relations · general-counsel│
│  head-of-trading                                        │
├─────────────────────────────────────────────────────────┤
│  LAYER 0 — DEEP FUND FUNCTIONS                          │
│  alternative-data-analyst · derivatives-desk            │
│  securities-lending · factor-attribution                │
│  capital-allocator · counterparty-risk                  │
│  esg-analyst · business-development                     │
├─────────────────────────────────────────────────────────┤
│  ORCHESTRATION                                          │
│  Context bus · Execution graph · Halt protocol          │
├─────────────────────────────────────────────────────────┤
│  PERSISTENCE                                            │
│  SQLite db/ · pipeline_runs · nav_snapshots · agent_verdicts│
├─────────────────────────────────────────────────────────┤
│  LIVE DATA PIPELINE                                     │
│  FRED (20 series) · IBKR (positions) · Kalshi · Norgate │
└─────────────────────────────────────────────────────────┘
```

---

## The Agents (45 total)

### Layer 5 — Governance
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Risk Officer | `/risk` | Position sizing, VaR, drawdown, tail risk | HARD BLOCK / SOFT FLAG / CLEAR |
| Signal Researcher | `/signal` | Statistical validity, overfitting, look-ahead, regime decomposition | BLOCK / CONDITIONAL / CLEAR |
| Systems Architect | `/systems` | Execution infrastructure, data pipelines, deployment readiness | DEPLOY BLOCKER / PRE-DEPLOY REQUIRED / MONITOR |
| Compliance Officer | `/compliance` | Mandate, regulatory limits, LP alignment, audit trail | VIOLATION / WARNING / CLEAR |
| Macro Analyst | `/macro` | Regime, cross-asset consistency, thesis falsifiability, crowding | OPPOSED / CONDITIONAL / ALIGNED |

### Layer 4 — Execution
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Order Router | `/order-router` | Venue, timing, order type, slippage budget | ROUTE / OUTSIZED ORDER |
| Slippage Monitor | `/slippage-monitor` | Fill quality vs. model, broker attribution | ACCEPTABLE / ELEVATED / INVESTIGATE |
| Position Reconciler | `/position-reconciler` | Broker vs. OMS vs. signal three-way reconciliation | CLEAN / BREAKS DETECTED |
| Rebalancer | `/rebalancer` | Optimal rebalance trades, transaction cost vs. Sharpe benefit | REBALANCE / PARTIAL / UNECONOMIC |
| Roll Manager | `/roll-manager` | Futures expiry calendar, roll cost, timing | ROLL SCHEDULED / URGENT ROLL |

### Layer 3 — Research
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Signal Generator | `/signal-generator` | Alpha hypothesis generation from regime context | HYPOTHESIS — NOT VALIDATED |
| Backtest Designer | `/backtest-designer` | Rigorous backtest specification before code is written | BACKTEST SPEC |
| Correlation Mapper | `/correlation-mapper` | Factor exposure of new signals vs. existing portfolio | ADDITIVE / REDUNDANT |
| Capacity Estimator | `/capacity-estimator` | AUM ceiling before signal decay | CAPACITY CEILING / CAPACITY CONSTRAINED |
| Decay Tracker | `/decay-tracker` | Live Sharpe vs. backtest baseline, decay curve fitting | HEALTHY / DEGRADING / FAILED |
| Portfolio Optimizer | `/portfolio-optimizer` | Risk parity / mean-variance sizing, binding constraint | REBALANCE TRIGGER / URGENT |

### Layer 2 — Intelligence
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Macro Scanner | `/macro-scanner` | Daily FRED/Kalshi/news digest, regime shift detection | Daily brief |
| Regime Classifier | `/regime-classifier` | Four-dimension continuous regime state machine | REGIME_STATE {} block |
| Flow Analyst | `/flow-analyst` | COT positioning, crowding, squeeze scenarios | CROWDED / ELEVATED / NEUTRAL / CONTRARIAN |
| Sentiment Tracker | `/sentiment-tracker` | FinBERT news sentiment, price-sentiment divergence | NARRATIVE SHIFT / DISTRIBUTION / ACCUMULATION |
| Earnings Watcher | `/earnings-watcher` | Index constituent earnings risk, implied vs. historical move | HIGH / MODERATE / LOW |
| Kalshi Reader | `/kalshi-reader` | Prediction market signal extraction, consensus divergence | DIVERGENCE FLAG / signal strength ranking |

### Layer 1 — Operations
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Drawdown Monitor | `/drawdown-monitor` | Circuit breaker, velocity-based HALT override | MONITOR / WARN / SUSPEND / HALT |
| Vendor Monitor | `/vendor-monitor` | Data feed health, silent failure detection | HEALTHY / DEGRADED / STALE / FAILED |
| Audit Logger | `/audit-logger` | Pre-trade rationale completeness enforcer | COMPLETE / INCOMPLETE |
| Cash Manager | `/cash-manager` | Margin utilization, cash drag, runway | WARNING 70% / CRITICAL 90% |
| NAV Calculator | `/nav-calculator` | Daily NAV with price source verification | VERIFIED / UNVERIFIED |
| LP Reporter | `/lp-reporter` | Monthly/quarterly LP letter drafting | DRAFT — REVIEW REQUIRED |
| Tax Tracker | `/tax-tracker` | Wash sale, harvest opportunities, after-tax return | HARVEST NOW / WASH SALE RISK / CLEAN |

### Layer 0 — Human Roles (Core)
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Quant Researcher | `/quant-researcher` | Distributional assumptions, parameter stability, deflated Sharpe | VALIDATED / CONDITIONAL / INVALID |
| Infrastructure Auditor | `/infrastructure-auditor` | Race conditions, idempotency, dependency integrity | PRODUCTION READY / CONDITIONAL / NOT READY |
| Fund Accountant | `/fund-accountant` | P&L attribution, fee calculation, financial statements | AUDIT READY / REQUIRES REMEDIATION |
| Chief Risk Officer | `/chief-risk-officer` | Portfolio VaR, crisis stress tests, board risk report | RED / AMBER / GREEN |
| Investor Relations | `/investor-relations` | LP DDQ simulation, quarterly call prep, raise readiness | IR READY / CONDITIONAL / NOT READY |
| General Counsel | `/general-counsel` | Regulatory status, horizon scanning, trade legal risk | LEGAL CLEAR / REVIEW REQUIRED / LEGAL HOLD |
| Head of Trading | `/head-of-trading` | Broker scorecard, commission audit, prime broker fit | OPTIMIZED / REVIEW REQUIRED / RESTRUCTURE |

### Layer 0 — Deep Fund Functions
| Agent | Command | Function | Key Output |
|---|---|---|---|
| Alternative Data Analyst | `/alternative-data-analyst` | Data tier classification, half-life, legality, cost ROI | DIFFERENTIATED EDGE / COMMODITIZED / LEGAL REVIEW |
| Derivatives Desk | `/derivatives-desk` | Options overlay, hedge ratio, Greeks, expiration risk | HEDGE APPROVED / OVERPRICED / HARD BLOCK |
| Securities Lending | `/securities-lending` | Borrow cost, locate risk, recall, short squeeze scenario | SHORT APPROVED / UNECONOMIC / RECALL IMMINENT |
| Factor Attribution | `/factor-attribution` | Return decomposition, factor drift, replication test | ALPHA CONFIRMED / ALPHA ILLUSION / FACTOR DRIFT |
| Capital Allocator | `/capital-allocator` | Risk budget across strategies, pod P&L, capacity planning | OPTIMALLY ALLOCATED / MISALLOCATED / SHUTDOWN |
| Counterparty Risk | `/counterparty-risk` | Prime broker exposure, CVA, settlement, PB failure scenario | CLEAN / CONCENTRATION WARNING / HARD BLOCK |
| ESG Analyst | `/esg-analyst` | Exclusion screening, carbon footprint, LP ESG compatibility | ESG COMPLIANT / EXCLUSION BREACH / INCOMPATIBLE |
| Business Development | `/business-development` | LP pipeline, raise readiness, pitch audit, emerging programs | PIPELINE HEALTHY / RAISE READY / NOT READY |

---

## Key Commands

| Command | What It Does |
|---|---|
| `/setup` | Interactive fund onboarding wizard — populates all context files, generates legal and broker checklists |
| `/run-pipeline` | Full 8-stage orchestrated review — primary entry point for all decisions |
| `/crucible` | Five-agent governance panel — GO / CONDITIONAL GO / NO-GO verdict |
| `/stress-test` | Portfolio through GFC 2008, COVID 2020, 2022 Rate Shock, 1994, LTCM 1998 simultaneously |
| `/postmortem` | Feed losing trade outcomes back through agents — identifies misses, improves thresholds |
| `/calibration-report` | Agent accuracy over time — false positive/negative rates, health scores, recalibration recommendations |
| `/export-audit` | 30-day Pipeline Report history compiled for LP and regulatory distribution |
| `/debate` | Bull and bear case for a trade — forces steelmanning before commitment, no verdict |

---

## Top Workflows

### 1. Full Pre-Trade Gauntlet
Use `/run-pipeline` — the orchestrator runs the full stack in the correct order automatically.

### 2. Morning Briefing
```
/macro-scanner          # regime and macro digest
/regime-classifier      # updates REGIME_STATE for the session
/event-calendar         # upcoming risk events in the next 30 days
```

### 3. New Signal Onboarding
```
/alternative-data-analyst   # is the data differentiated?
/signal-generator           # hypothesis formation
/signal-researcher          # statistical validation
/backtest-designer          # rigorous backtest spec
/correlation-mapper         # factor exposure vs. existing portfolio
/capacity-estimator         # AUM ceiling
```

### 4. Drawdown Response Protocol
```
/drawdown-monitor           # current severity and velocity
/chief-risk-officer         # portfolio-wide risk assessment
/stress-test                # how bad can it get across crisis scenarios
/factor-attribution         # what factor exposure is driving the loss
/capital-allocator          # should risk budget be reallocated
```

### 5. Strategy Deployment Checklist
```
/quant-researcher           # model validity
/infrastructure-auditor     # code quality and deployment readiness
/run-pipeline               # full pre-deployment review
```

### 6. End of Month Close
```
/nav-calculator             # verified NAV
/fund-accountant            # P&L attribution and fee calculation
/tax-tracker                # harvest opportunities, wash sale check
/lp-reporter                # draft LP letter
/export-audit               # 30-day audit trail for records
/general-counsel            # any disclosure obligations this period
```

---

## Setup

**Option A — GitHub Codespace (recommended, no local install)**

Click the badge at the top of this page. A pre-configured environment opens in your browser with all dependencies installed. Then:

```bash
cp .env.template .env   # add your ANTHROPIC_API_KEY and FRED_API_KEY
claude                  # open Claude Code
/setup                  # configure your fund
```

**Option B — Local**

```bash
git clone https://github.com/arpjw/crucible-cio-team.git
cd crucible-cio-team
pip install -r requirements.txt
npm install -g @anthropic-ai/claude-code
cp .env.template .env   # add API keys
python db/init.py       # initialize SQLite database
python scripts/verify-fred.py  # confirm live data connection
claude
/setup
```

After `/setup`, read `PLAYBOOK.md` for the day-zero to day-100 operational guide.

---

## Verdict Logic

| Verdict | Condition |
|---|---|
| **NO-GO** | Any HARD BLOCK (Risk), VIOLATION (Compliance), DEPLOY BLOCKER (Systems), or EXCLUSION LIST BREACH (ESG) |
| **CONDITIONAL GO** | Any soft flags, warnings, or Macro OPPOSED without a hard block |
| **GO** | All agents clear — includes mandatory post-execution monitoring |

---

## What's Included

```
crucible-cio-team/
├── agents/              (45 agent persona files)
├── .claude/commands/    (53 slash commands)
├── orchestrator/        (pipeline.md, context-bus.md, halt-protocol.md)
├── db/                  (init.py, query.py, README.md — SQLite persistence)
├── scripts/             (update-context.py, sync-ibkr.py, verify-fred.py, verify-ibkr.py)
├── context/             (fund-mandate.md, risk-limits.md, portfolio-state.md, macro-state.md)
├── legal/               (Delaware LLC checklist, NFA guide, Series 65 plan, templates, DDQ)
├── fundraising/         (pitch deck outline, LP letter templates, targeting guide)
├── infrastructure/      (IBKR, FRED, Norgate, Kalshi setup guides, Docker, environment)
├── strategies/          (TSMOM, Carry, Macro Discretionary starter packs)
├── tests/               (manual testing guide and scenarios)
├── .devcontainer/       (Codespace config and Dockerfile)
├── AGENTS.md            (complete agent registry)
├── PLAYBOOK.md          (day-zero to running fund operational guide)
├── CONTRIBUTING.md      (contribution guide and quality bar)
└── CLAUDE.md            (Claude Code entry point)
```

---

## Contributing

Crucible is open for contributions. The highest-value additions are agents for strategies not yet covered: options, crypto, equity long/short, fixed income credit, family office structure.

See `CONTRIBUTING.md` for the quality bar, issue templates, and PR checklist. Open an Agent Proposal issue before building — the proposal template requires named formulas and escalation thresholds before any code is written.

GitHub Discussions is enabled for ideas, Q&A, and Show and Tell.

---

## License

MIT. Use it, fork it, adapt it to your fund.

---

*Built with Claude Code. The most important question before any trade is not "why should I do this" — it is "what would make this wrong."*
