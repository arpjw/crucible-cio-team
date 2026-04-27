# Crucible CIO Team

**Adversarial AI for systematic fund managers.**

Crucible is a 37-agent, 6-layer AI framework that challenges every fund decision before execution. It is not an assistant — it is an adversary. Five governance agents independently stress-test trades from compliance, risk, macro, signal, and systems perspectives, producing a binding panel verdict of GO, CONDITIONAL GO, or NO-GO. Ten operations agents run continuously to monitor drawdowns, data feeds, margin, NAV, and LP obligations. Four intelligence agents track regime state, positioning crowding, news sentiment, and earnings risk. Six research agents validate new signals from hypothesis through backtest spec, factor exposure, capacity, and decay. Five execution agents route orders, monitor slippage, reconcile positions, manage rolls, and generate rebalance trade lists. Every agent has explicit formulas, hard thresholds, and machine-readable output — not open-ended questions.

---

## How It Works

**`/run-pipeline` is the primary entry point for all trade, signal, rebalance, and roll decisions.** One command executes the full agent stack in the correct order, passes outputs between agents automatically via the context bus, and produces a unified Pipeline Report with the final actionable instruction.

```
/run-pipeline Long 2% NAV ES futures, trend signal fires on 20-day breakout
/run-pipeline Adding EM FX carry basket, 3% NAV, 6 positions equally weighted
/run-pipeline Roll front-month CL to M+1, current position 1.5% NAV long
```

### Context Bus

The context bus (`orchestrator/context-bus.md`) is the shared state between all agents in the pipeline. `regime-classifier` writes `REGIME_STATE` to the bus at Stage 1; every downstream agent reads it. `portfolio-optimizer` writes target weights at Stage 5; `rebalancer` and `order-router` consume them at Stage 6. Outputs flow automatically — no copy-paste between agents.

### Execution Graph

The pipeline runs in 8 stages with parallel execution at Stage 3:

```
Stage 0  Bus init — loads portfolio-state.md + risk-limits.md
Stage 1  regime-classifier → writes REGIME_STATE to bus
Stage 2  compliance (hard gate) → drawdown-monitor (hard gate)
Stage 3  risk-officer + macro-analyst + kalshi-reader  [parallel]
Stage 4  signal-researcher  [if signal-related submission]
Stage 5  portfolio-optimizer → writes target weights to bus
Stage 6  rebalancer + order-router  [parallel]
Stage 7  audit-logger  [final gate — execution withheld until COMPLETE]
Stage 8  unified Pipeline Report
```

### Halt Behavior

Halt behavior is enforced automatically — no manual stage skipping.

- **HARD HALT** — compliance `VIOLATION` or drawdown `HALT`: pipeline stops entirely, all pending stages cancelled, no execution instructions issued
- **SOFT HALT** — risk `BLOCKED`, signal `BLOCK`, rebalance `UNECONOMIC`, or audit `INCOMPLETE`: pipeline pauses, issue surfaced to PM, override auto-logged to audit record

---

## The Stack

```
  INPUT: trade idea · new signal · portfolio change · strategy deployment
  │
  │
  ▼
  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║  LAYER 2 · INTELLIGENCE            market context, read before Governance   ║
  ║                                                                              ║
  ║   /regime-classifier    /flow-analyst    /sentiment-tracker                 ║
  ║   /earnings-watcher                                                          ║
  ║                                                                              ║
  ║   regime-classifier produces REGIME_STATE block ──────────────────────────► ║
  ║   flow-analyst produces CROWDED/ELEVATED positioning data ─────────────────►║
  ║   sentiment-tracker produces NARRATIVE SHIFT flags ───────────────────────► ║
  ╚══════════════════════════════════════╤═══════════════════════════════════════╝
                                         │  regime state · crowd data
                                         │  sentiment · earnings risk
                                         ▼
  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║  LAYER 3 · RESEARCH               signal development & portfolio sizing     ║
  ║                                                                              ║
  ║   /signal-generator    /backtest-designer    /correlation-mapper            ║
  ║   /capacity-estimator  /decay-tracker        /portfolio-optimizer           ║
  ║                                                                              ║
  ║   signal-generator → backtest-designer → correlation-mapper → decay-tracker║
  ║   capacity-estimator enforces AUM ceiling ────────────────────────────────► ║
  ║   portfolio-optimizer produces target allocations ────────────────────────► ║
  ╚═════════════════════════════╤════════════════════════════╤═══════════════════╝
                                │  validated signals          │  target allocations
                                │  sizing constraints         │
                                ▼                             ▼
  ╔══════════════════════════════════════════════╗    ╔═══════════════════════════╗
  ║  LAYER 0 · GOVERNANCE   adversarial gate     ║    ║  LAYER 4 · EXECUTION      ║
  ║                                              ║    ║                           ║
  ║  Compliance → Risk → Macro → Signal → Systems║    ║  /rebalancer ◄────────────║
  ║                                              ║    ║  /order-router            ║
  ║  /compliance  /risk  /macro                  ║    ║  /position-reconciler     ║
  ║  /signal      /systems                       ║    ║  /slippage-monitor        ║
  ║                                              ║    ║  /roll-manager            ║
  ║  /crucible: full panel in sequence           ║    ║                           ║
  ║                                              ║    ║  portfolio-optimizer ──►  ║
  ║  Verdict:  GO | CONDITIONAL GO | NO-GO  ─────╫───►    rebalancer generates   ║
  ║                                              ║    ║    trade list             ║
  ╚══════════════════════════════════════════════╝    ╚═══════════════════════════╝

  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║  LAYER 1 · OPERATIONS          continuous, parallel to all layers           ║
  ║                                                                              ║
  ║   /drawdown-monitor   /vendor-monitor   /audit-logger   /cash-manager       ║
  ║   /nav-calculator     /lp-reporter      /tax-tracker    /macro-scanner       ║
  ║   /event-calendar     /kalshi-reader                                         ║
  ║                                                                              ║
  ║   drawdown-monitor feeds back to Risk Officer on velocity/depth              ║
  ║   audit-logger gates every trade before Execution layer can proceed          ║
  ║   macro-scanner + kalshi-reader feed regime context to Macro Analyst         ║
  ╚══════════════════════════════════════════════════════════════════════════════╝

  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║  LAYER 0 · HUMAN ROLES    institutional expertise, periodic fund audits     ║
  ║                                                                              ║
  ║   /quant-researcher      /infrastructure-auditor   /fund-accountant         ║
  ║   /chief-risk-officer    /investor-relations        /general-counsel         ║
  ║   /head-of-trading                                                           ║
  ║                                                                              ║
  ║   quant-researcher validates models that signal-researcher and risk rely on  ║
  ║   chief-risk-officer produces Board Risk Report from the full portfolio      ║
  ║   general-counsel monitors regulatory thresholds that compliance enforces    ║
  ╚══════════════════════════════════════════════════════════════════════════════╝
```

**Key cross-layer feeds:**
- `regime-classifier` (L2) → `macro-analyst` (L0): machine-readable `REGIME_STATE` block grounds the Macro Analyst's regime identification
- `flow-analyst` (L2) → `risk-officer` (L0): CROWDED positioning data informs squeeze risk in sizing assessment
- `portfolio-optimizer` (L3) → `rebalancer` (L4): target allocations are the direct input to the Rebalancer's trade list
- `signal-generator` (L3) → `signal-researcher` (L0): hypothesis spec is the input for the full signal governance review
- `audit-logger` (L1) → Execution gate: INCOMPLETE record suspends order routing

---

## The Agents

### Layer 0 — Human Roles

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Quant Researcher | `/quant-researcher` | Validates model mathematics via Jarque-Bera, rolling parameter stability, deflated Sharpe, and Ljung-Box residual tests | `MODEL VERDICT: INVALID \| CONDITIONAL \| VALIDATED` |
| Infrastructure Auditor | `/infrastructure-auditor` | Reviews race conditions, idempotency, dependency pinning, error handling, and engineering debt (0–100 score) | `INFRASTRUCTURE VERDICT: NOT READY \| CONDITIONAL \| PRODUCTION READY` |
| Fund Accountant | `/fund-accountant` | Reconciles P&L to NAV change (±0.01%), verifies fee calculations against LPA, checks expense allocation, and assesses audit readiness | `ACCOUNTING VERDICT: AUDIT FAILURE \| REQUIRES REMEDIATION \| AUDIT READY` |
| Chief Risk Officer | `/chief-risk-officer` | Computes portfolio VaR, runs five historical crisis stress tests, measures liquidation horizon vs. redemption notice, and produces board-ready RAG dashboard | `PORTFOLIO RISK STATUS: RED \| AMBER \| GREEN` |
| Investor Relations | `/investor-relations` | Simulates LP DDQ, prepares quarterly call with top-5 questions, assesses capital raise readiness, audits LP communications, and scores redemption risk | `IR VERDICT: NOT READY \| CONDITIONAL \| IR READY` |
| General Counsel | `/general-counsel` | Monitors regulatory exemption thresholds, scans pending rules, screens trades for sanctions/insider trading/manipulation risk, and reviews counterparty legal terms | `LEGAL VERDICT: LEGAL HOLD \| LEGAL REVIEW REQUIRED \| LEGAL CLEAR` |
| Head of Trading | `/head-of-trading` | Scores brokers on IS/fill rate/latency/commissions, audits commission drag, assesses prime broker fit, reviews execution strategy against the square-root model, and identifies market structure risks | `EXECUTION VERDICT: RESTRUCTURE NEEDED \| REVIEW REQUIRED \| EXECUTION OPTIMIZED` |

### Layer 0 — Governance

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Compliance Officer | `/compliance` | Checks trade permissibility against fund mandate, regulatory limits, LP alignment, and disclosure obligations | `COMPLIANCE VERDICT: VIOLATION \| WARNING \| CLEAR` |
| Risk Officer | `/risk` | Evaluates position sizing, VaR contribution, drawdown headroom, correlation clustering, and tail scenarios | `RISK VERDICT: BLOCKED \| FLAGGED \| APPROVED` |
| Macro Analyst | `/macro` | Challenges macro thesis coherence, regime identification, cross-asset consistency, and historical analog quality | `MACRO VERDICT: OPPOSED \| CONDITIONAL \| ALIGNED` |
| Signal Researcher | `/signal` | Stress-tests signal statistical validity, overfitting exposure, regime robustness, and live/backtest parity | `SIGNAL VERDICT: REJECTED \| FLAGGED \| VALIDATED` |
| Systems Architect | `/systems` | Audits execution infrastructure, data pipeline integrity, latency budget, and deployment readiness | `SYSTEMS VERDICT: BLOCKED \| CONDITIONAL \| CLEAR` |
| Full Panel | `/crucible` | Runs all five governance agents in sequence and synthesizes a binding panel verdict | `NO-GO \| CONDITIONAL GO \| GO` |

### Layer 1 — Operations

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Drawdown Monitor | `/drawdown-monitor` | Tracks drawdown velocity, depth, and correlation profile to trigger circuit breakers | `DRAWDOWN STATUS: MONITOR \| WARN \| SUSPEND \| HALT` |
| Vendor Monitor | `/vendor-monitor` | Monitors data feed health, staleness, and silent failure patterns across all market data sources | Feed status per instrument: `LIVE \| STALE \| FAILED \| SWITCHOVER` |
| Audit Logger | `/audit-logger` | Enforces five required pre-trade record elements and gates trades on completeness | `COMPLETE \| INCOMPLETE` |
| Cash Manager | `/cash-manager` | Tracks margin utilization, per-position headroom, cash drag, and margin call triggers | `MARGIN STATUS: OK \| WARNING \| CRITICAL` |
| NAV Calculator | `/nav-calculator` | Verifies daily NAV integrity against price sources, staleness, and corporate actions | `STAMP: VERIFIED \| VERIFIED WITH NOTES \| UNVERIFIED` |
| LP Reporter | `/lp-reporter` | Drafts the LP letter with return attribution, drawdown narrative, risk metrics, and disclosure scan | `DRAFT` stamp + disclosure checklist |
| Tax Tracker | `/tax-tracker` | Monitors tax lot holding periods, wash sale exposure, and harvest opportunities | `TAX STATUS` with lot-level harvest flags |
| Macro Scanner | `/macro-scanner` | Produces a daily four-dimension regime state digest with Kalshi overlay and portfolio implications | Regime state machine + `REGIME CHANGE DETECTED` flag |
| Event Calendar | `/event-calendar` | Builds a 30-day event risk calendar with ATR-based impact models and 5-day critical windows | `EVENT RISK — REVIEW POSITION \| EVENT RISK — MONITOR \| NO MATERIAL EVENT RISK` |
| Kalshi Reader | `/kalshi-reader` | Reads prediction market signals and flags consensus divergence ≥15pp | `HIGH SIGNAL \| NO SIGNAL`; `POLICY SHIFT SIGNAL` |

### Layer 2 — Intelligence

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Flow Analyst | `/flow-analyst` | Analyzes CFTC COT data for net positioning percentile, OI rate-of-change, and mechanical squeeze severity | `CROWDED \| ELEVATED \| NEUTRAL \| CONTRARIAN` per instrument |
| Sentiment Tracker | `/sentiment-tracker` | Scores news sentiment against a 30-day baseline and flags price-sentiment divergence | `NARRATIVE SHIFT \| STABLE \| DIVERGENCE` |
| Earnings Watcher | `/earnings-watcher` | Monitors corporate event risk using implied vs. historical move, vol premium, and beat/miss rates | `EARNINGS RISK HIGH \| MODERATE \| LOW` |
| Regime Classifier | `/regime-classifier` | Produces machine-readable four-dimension regime state and confidence score for downstream agents | `REGIME_STATE` block + `REGIME CLASSIFICATION` with confidence |

### Layer 3 — Research

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Signal Generator | `/signal-generator` | Proposes regime-consistent, non-redundant alpha hypotheses grounded in mechanism | `HYPOTHESIS — NOT VALIDATED` stamp |
| Backtest Designer | `/backtest-designer` | Runs a seven-check spec review: universe, regime coverage, cost model, timing, holdout, benchmark, power | `SPEC APPROVED \| SPEC REQUIRES REVISION` |
| Correlation Mapper | `/correlation-mapper` | Audits eight-factor loadings and pairwise correlations under normal and stress regimes | `APPROVED \| REDUNDANT \| CONCENTRATION WARNING` |
| Capacity Estimator | `/capacity-estimator` | Calculates AUM ceiling via the square-root impact model and flags when AUM approaches ceiling | `CAPACITY CONSTRAINED` when AUM is within 3× of ceiling |
| Decay Tracker | `/decay-tracker` | Compares rolling 3m/6m/12m live vs. backtest Sharpe and classifies signal decay curve shape | Health score 0–100 + `linear \| exponential \| episodic` |
| Portfolio Optimizer | `/portfolio-optimizer` | Computes target allocations via risk parity or mean-variance and identifies binding constraints | `ALLOCATION COMPLETE \| REBALANCE TRIGGER \| URGENT REBALANCE \| BINDING CONSTRAINT ACTIVE` |

### Layer 4 — Execution

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Order Router | `/order-router` | Selects venue and order type by instrument class, applies VWAP window, halts orders >10% ADV | `APPROVED \| OUTSIZED ORDER — HALT` |
| Slippage Monitor | `/slippage-monitor` | Benchmarks fills against arrival price and classifies broker performance by realized vs. modeled ratio | `ACCEPTABLE \| ELEVATED \| INVESTIGATE`; `FILL DEGRADATION` flag |
| Position Reconciler | `/position-reconciler` | Runs three-way reconciliation across broker, OMS, and signal register | `CLEAN \| BREAKS DETECTED`; `ORDER ROUTING GATE: CLEARED \| SUSPENDED` |
| Rebalancer | `/rebalancer` | Generates optimal trade list from Portfolio Optimizer targets, nets trades, sequences exits first | `REBALANCE APPROVED — FULL \| REBALANCE APPROVED — PARTIAL \| REBALANCE UNECONOMIC \| NO REBALANCE REQUIRED` |
| Roll Manager | `/roll-manager` | Maintains a 90-day futures expiry calendar and issues urgent roll alerts within 3 days of first notice | `URGENT ROLL \| ROLL NOW \| ROLL COST ELEVATED` |

---

## Top Workflows

### 1. The Full Pre-Trade Gauntlet

> **Use `/run-pipeline [trade description]`.** The pipeline runs the entire sequence below automatically in the correct order. Use individual commands only for targeted diagnostic analysis outside the pipeline.

*Run before entering any new position. Every step is a gate — if it blocks, stop.*

```
/regime-classifier
```
Establish current regime state. The Macro Analyst needs this before evaluating any thesis.

```
/flow-analyst [instrument]
```
Check positioning crowding. A CROWDED verdict means the stop is crowded too.

```
/event-calendar
```
Confirm no critical events within the 5-day window that should force position sizing down.

```
/correlation-mapper [proposed position + current portfolio]
```
Verify the new position doesn't replicate existing factor exposures. REDUNDANT blocks here.

```
/audit-logger [pre-trade record]
```
Gate on completeness before spending governance time. INCOMPLETE means fill in the gaps first.

```
/crucible [trade description]
```
Full five-agent panel review: Compliance → Risk → Macro → Signal → Systems. CONDITIONAL GO means conditions must be documented before order routing.

```
/order-router [order details]
```
Route the cleared order. OUTSIZED ORDER — HALT means the size needs to come down.

---

### 2. Morning Briefing

> **Use individual commands.** Morning briefing agents are monitoring and orientation tools, not a trade entry decision. `/run-pipeline` applies once a specific trade or position change is identified.

*Three-agent sequence to orient a PM at market open. Run before reviewing positions or making decisions.*

```
/macro-scanner
```
Daily four-dimension regime state digest. Read the REGIME CHANGE DETECTED flag first — if it fired overnight, everything else needs to be read in that context.

```
/event-calendar
```
Today's event risk. Any position flagged EVENT RISK — REVIEW POSITION requires an explicit sizing decision before the open.

```
/kalshi-reader
```
Prediction market consensus check. HIGH SIGNAL means the market's implied probability has diverged from the fund's macro view by ≥15pp — review positioning before the session.

---

### 3. New Signal Onboarding

> **Hybrid.** Use individual commands for research stages 1–5 (signal-generator through decay-tracker). Once the signal is validated and ready for governance review, use `/run-pipeline [signal description + backtest results]` for the final governance and execution gate.

*The research layer sequence to validate a new alpha idea before it touches capital. Do not skip steps.*

```
/signal-generator [concept]
```
Formalize the alpha hypothesis with mechanism, target regime, and expected behavior. Output is stamped HYPOTHESIS — NOT VALIDATED — that stamp does not clear until Step 6.

```
/backtest-designer [spec]
```
Run the seven-check spec review before backtesting begins. SPEC REQUIRES REVISION means stop here and fix the spec — do not run the backtest on a deficient spec.

```
/correlation-mapper [expected factor loadings]
```
Confirm the signal doesn't replicate an existing position's factor exposures. REDUNDANT at this stage means either differentiate the signal or replace the existing one.

```
/capacity-estimator [signal parameters + target AUM]
```
Verify the signal can support the target AUM at realistic ADV limits. CAPACITY CONSTRAINED now is better than discovering it after deployment.

```
/decay-tracker [signal history if available]
```
Classify the signal's decay profile and compute health score. Score < 50 or exponential decay pattern is a hard warning before governance review.

```
/signal [validated spec + backtest results]
```
Full governance review: statistical significance, overfitting exposure, regime robustness, live/backtest parity. VALIDATED clears the hypothesis stamp. REJECTED means the signal does not proceed.

---

### 4. Drawdown Response Protocol

> **Use individual commands.** Drawdown response is a diagnostic and assessment sequence. `/run-pipeline` applies when assessment is complete and you are ready to enter, reduce, or exit a specific position.

*The sequence to run when the fund is in drawdown. Sequence matters — assess before acting.*

```
/drawdown-monitor
```
Establish the escalation level first. HALT means no new positions, no exceptions. SUSPEND means reduce existing positions before anything else. Read velocity vs. depth — a fast shallow drawdown is a different problem than a slow deep one.

```
/cash-manager
```
Confirm margin headroom and runway before any position adjustments. A CRITICAL margin status means the order of operations for the unwind is constrained.

```
/flow-analyst [all portfolio positions]
```
Check whether the speculative crowd is building against the portfolio. CROWDED + MOMENTUM INFLOW is the worst case — the speculative exit will amplify the move.

```
/position-reconciler
```
Verify positions are exactly what the OMS says before making any changes under stress. BREAKS DETECTED during a drawdown means resolve the breaks before executing any trades.

```
/risk [current portfolio, updated context]
```
Reassess the full portfolio risk profile in the current drawdown context. The pre-trade risk parameters may have changed — update context files first.

---

### 5. Strategy Deployment Checklist

> **Hybrid.** Use individual commands for pre-deployment research and validation (backtest-designer through decay-tracker). Use `/run-pipeline [strategy + first trade description]` for the final governance and execution gate before the first trade goes live.

*The sequence before pushing a new strategy to live capital. This is the one-way door — every step is mandatory.*

```
/backtest-designer [final spec]
```
Confirm the spec passes all seven checks with an out-of-sample holdout period. If the backtest was run on a deficient spec, it cannot be used as evidence for deployment.

```
/decay-tracker [full signal history]
```
Verify health score ≥ 50 and no exponential decay pattern. Exponential decay means the signal is already dying — deploying it to live capital starts the clock.

```
/capacity-estimator [strategy parameters + live AUM]
```
Confirm the live AUM is within the capacity ceiling at the target ADV limit. CAPACITY CONSTRAINED before launch means reduce target allocation or recalibrate impact assumptions.

```
/signal [strategy + backtest results + live track record if any]
```
Full governance review of signal validity, overfitting exposure, and live deployment readiness. VALIDATED is required before Systems review.

```
/systems [infrastructure + deployment plan]
```
Execution infrastructure audit and deployment checklist. BLOCKED means do not deploy until the infrastructure issue is resolved.

```
/compliance [strategy description + mandate]
```
Regulatory and mandate clearance. A new strategy may require LP notification or regulatory filing that live deployment triggers — Compliance identifies these before the first trade.

```
/audit-logger [deployment record]
```
Gate on pre-trade record completeness for the first trade. The strategy is not deployed until the audit logger issues COMPLETE.

---

### 6. End of Month Close

> **Use individual commands.** Month-end close is an operational reporting sequence. `/run-pipeline` applies to any trade or position change decisions made during the close process, not to the reporting workflow itself.

*The ops sequence for LP reporting, NAV verification, and audit trail. Run in this order.*

```
/nav-calculator
```
Verify month-end NAV before any LP communication. UNVERIFIED means no LP reporting until the discrepancy is resolved. VERIFIED WITH NOTES requires disclosure in the LP letter.

```
/position-reconciler
```
Run three-way reconciliation at month-end. BREAKS DETECTED at month-end must be resolved and documented — these appear in the audit trail and may require LP disclosure.

```
/slippage-monitor
```
Monthly fill quality review. Any broker classified INVESTIGATE requires a formal performance review before the next month's order flow allocation is set.

```
/tax-tracker
```
Review tax lot status, wash sale exposure, and harvest windows. Positions approaching 12-month holding periods need explicit harvest-or-hold decisions before month-end.

```
/audit-logger [full trade log for the period]
```
Confirm the audit trail is COMPLETE for all positions opened and closed in the month. INCOMPLETE records from any trade must be resolved before LP reporting proceeds.

```
/lp-reporter
```
Draft the LP letter. The agent pulls period return, attribution, drawdown narrative, and risk metrics from context. DRAFT stamp plus disclosure checklist — review every checklist item before sending.

---

## Setup

**1. Clone**
```bash
git clone https://github.com/arpjw/crucible-cio-team.git
cd crucible-cio-team
```

**2. Install Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
```

**3. Open Claude Code and run `/setup`**
```bash
claude
```
```
/setup
```

`/setup` is a structured five-stage interview — Fund Identity, Strategy, Risk Parameters, Operations, and Regulatory. It takes about ten minutes and writes three things:

- **Context files** — `context/fund-mandate.md`, `context/risk-limits.md`, `context/portfolio-state.md` fully populated with your fund's actual parameters (no placeholders)
- **`SETUP_REPORT.md`** — one-page fund summary plus three appendices:
  - Appendix A: Legal formation checklist tailored to your jurisdiction (Delaware LLC / Cayman LP / other)
  - Appendix B: Broker and vendor setup checklist tailored to your selections (IBKR, Bloomberg, Norgate, FRED, Kalshi)
  - Appendix C: Day-by-day first-30-days outline

Run `/setup` again any time your fund parameters change.

**4. Run your first pipeline**
```
/run-pipeline Long EUR/USD via June futures, 2% NAV risk, thesis is ECB-Fed policy divergence widening through Q3
```

---

## Verdict Logic

| Verdict | Condition | Action |
|---|---|---|
| `NO-GO` | Any `BLOCKED` (Risk), `VIOLATION` (Compliance), or `BLOCKED` (Systems) | Do not proceed. Resolve the blocking issue before re-submitting. |
| `CONDITIONAL GO` | Any soft flags, warnings, or `OPPOSED` (Macro) without a hard block | Proceed only after documenting each condition and how it will be monitored. |
| `GO` | All five agents clear with no unresolved flags | Proceed. A clean panel review still generates mandatory post-execution monitoring items. |
| `HALT` | Drawdown Monitor | No new positions. Begin position reduction per the reduction protocol. |
| `SUSPEND` | Drawdown Monitor | No new positions. Reduce existing positions before next session. |
| `OUTSIZED ORDER — HALT` | Order Router | Order exceeds 10% ADV. Reduce size or split across sessions. |
| `BREAKS DETECTED` | Position Reconciler | Order routing gate suspended. Resolve all critical and material breaks before routing. |
| `UNVERIFIED` | NAV Calculator | Do not distribute or report NAV. Resolve price discrepancy first. |
| `REBALANCE UNECONOMIC` | Rebalancer | Execute partial rebalance to 85% of gap only. Full rebalance cost exceeds 50% of expected Sharpe benefit. |

---

## Structure

```
crucible-cio-team/
├── AGENTS.md                        # Complete agent registry — all 30 agents
├── CLAUDE.md                        # Project instructions
├── README.md                        # This file
│
├── orchestrator/                    # Orchestration layer
│   ├── pipeline.md                  # Execution graph: agent order, dependencies, bus contracts
│   ├── context-bus.md               # Shared context bus schema
│   └── halt-protocol.md             # Hard/soft halt definitions and override procedures
│
├── agents/                          # 37 agent persona definitions
│   │
│   │   — Layer 0: Human Roles —
│   ├── quant-researcher.md
│   ├── infrastructure-auditor.md
│   ├── fund-accountant.md
│   ├── chief-risk-officer.md
│   ├── investor-relations.md
│   ├── general-counsel.md
│   ├── head-of-trading.md
│   │
│   │   — Layer 0: Governance —
│   ├── compliance-officer.md
│   ├── risk-officer.md
│   ├── macro-analyst.md
│   ├── signal-researcher.md
│   ├── systems-architect.md
│   │
│   │   — Layer 1: Operations —
│   ├── drawdown-monitor.md
│   ├── vendor-monitor.md
│   ├── audit-logger.md
│   ├── cash-manager.md
│   ├── nav-calculator.md
│   ├── lp-reporter.md
│   ├── tax-tracker.md
│   ├── macro-scanner.md
│   ├── event-calendar.md
│   ├── kalshi-reader.md
│   │
│   │   — Layer 2: Intelligence —
│   ├── flow-analyst.md
│   ├── sentiment-tracker.md
│   ├── earnings-watcher.md
│   ├── regime-classifier.md
│   │
│   │   — Layer 3: Research —
│   ├── signal-generator.md
│   ├── backtest-designer.md
│   ├── correlation-mapper.md
│   ├── capacity-estimator.md
│   ├── decay-tracker.md
│   ├── portfolio-optimizer.md
│   │
│   │   — Layer 4: Execution —
│   ├── order-router.md
│   ├── slippage-monitor.md
│   ├── position-reconciler.md
│   ├── rebalancer.md
│   └── roll-manager.md
│
├── .claude/
│   └── commands/                    # 32 slash commands
│       ├── setup.md                 # First-time setup — interactive fund onboarding wizard
│       ├── run-pipeline.md          # Primary entry point — full pipeline orchestration
│       │
│       │   — Layer 0: Human Roles —
│       ├── quant-researcher.md
│       ├── infrastructure-auditor.md
│       ├── fund-accountant.md
│       ├── chief-risk-officer.md
│       ├── investor-relations.md
│       ├── general-counsel.md
│       ├── head-of-trading.md
│       │
│       ├── crucible.md              # Full panel meta-command (Layer 0)
│       ├── compliance.md
│       ├── risk.md
│       ├── macro.md
│       ├── signal.md
│       ├── systems.md
│       ├── drawdown-monitor.md
│       ├── vendor-monitor.md
│       ├── audit-logger.md
│       ├── cash-manager.md
│       ├── nav-calculator.md
│       ├── lp-reporter.md
│       ├── tax-tracker.md
│       ├── macro-scanner.md
│       ├── event-calendar.md
│       ├── kalshi-reader.md
│       ├── flow-analyst.md
│       ├── sentiment-tracker.md
│       ├── earnings-watcher.md
│       ├── regime-classifier.md
│       ├── signal-generator.md
│       ├── backtest-designer.md
│       ├── correlation-mapper.md
│       ├── capacity-estimator.md
│       ├── decay-tracker.md
│       ├── portfolio-optimizer.md
│       ├── order-router.md
│       ├── slippage-monitor.md
│       ├── position-reconciler.md
│       ├── rebalancer.md
│       └── roll-manager.md
│
└── context/                         # Fund parameters — populate before first use
    ├── fund-mandate.md              # Permitted instruments, geographies, strategies
    ├── risk-limits.md               # Leverage, VaR, drawdown, concentration limits
    └── portfolio-state.md           # Current NAV, positions, signals, risk clusters
```

---

## License

MIT. Use it, fork it, adapt it.

---

*The most important question before any trade is not "why should I do this" — it is "what would make this wrong." Crucible exists to answer that question before it costs you.*
