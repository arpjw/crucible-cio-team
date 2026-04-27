# Crucible CIO Team — Agent Registry

30 agents across 5 layers. Each entry: invocation command, one-sentence function, and the exact verdict or stamp the agent produces.

---

## Layer 0 — Governance

Pre-trade decision review. Five independent adversarial agents plus one full-panel meta-command. Run before any trade, strategy deployment, or portfolio change.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Compliance Officer | `/compliance` | Checks trade permissibility against fund mandate, regulatory limits, LP alignment, and disclosure obligations. | `COMPLIANCE VERDICT: VIOLATION \| WARNING \| CLEAR` |
| Risk Officer | `/risk` | Evaluates position sizing, VaR contribution, drawdown headroom, correlation clustering, and tail scenarios. | `RISK VERDICT: BLOCKED \| FLAGGED \| APPROVED` |
| Macro Analyst | `/macro` | Challenges macro thesis coherence, regime identification, cross-asset consistency, and historical analog quality. | `MACRO VERDICT: OPPOSED \| CONDITIONAL \| ALIGNED` |
| Signal Researcher | `/signal` | Stress-tests signal statistical validity, overfitting exposure, regime robustness, and live/backtest parity. | `SIGNAL VERDICT: REJECTED \| FLAGGED \| VALIDATED` |
| Systems Architect | `/systems` | Audits execution infrastructure, data pipeline integrity, latency budget, and deployment readiness. | `SYSTEMS VERDICT: BLOCKED \| CONDITIONAL \| CLEAR` |
| **Full Panel** | `/crucible` | Runs all five governance agents in sequence and synthesizes a binding panel verdict. | `NO-GO \| CONDITIONAL GO \| GO` |

**Panel sequence:** Compliance → Risk → Macro → Signal → Systems. Compliance runs first because a mandate violation is not a risk management question.

---

## Layer 1 — Operations

Continuous monitoring. These agents run in parallel to the rest of the stack — daily, intra-day, or at end-of-month as noted.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Drawdown Monitor | `/drawdown-monitor` | Tracks drawdown velocity, depth, and correlation profile to trigger circuit breakers at four escalation levels. | `DRAWDOWN STATUS: MONITOR \| WARN \| SUSPEND \| HALT` |
| Vendor Monitor | `/vendor-monitor` | Monitors data feed health, staleness, silent failure patterns, and switchover risk across all market data sources. | `FEED STATUS` per instrument: `LIVE \| STALE \| FAILED \| SWITCHOVER` |
| Audit Logger | `/audit-logger` | Enforces five required elements of a complete pre-trade record and gates trades on completeness. | `COMPLETE \| INCOMPLETE` |
| Cash Manager | `/cash-manager` | Tracks margin utilization, per-position headroom, cash drag, and margin call triggers across the portfolio. | `MARGIN STATUS: OK \| WARNING \| CRITICAL` |
| NAV Calculator | `/nav-calculator` | Verifies daily NAV integrity by checking price sources, staleness, corporate actions, and cross-source consistency. | `STAMP: VERIFIED \| VERIFIED WITH NOTES \| UNVERIFIED` |
| LP Reporter | `/lp-reporter` | Drafts the LP letter with period return attribution, drawdown narrative, risk metrics, and disclosure scan. | `DRAFT` stamp + disclosure checklist |
| Tax Tracker | `/tax-tracker` | Monitors tax lot holding periods, wash sale exposure, harvest opportunities, and after-tax return impact. | `TAX STATUS` with lot-level harvest flags |
| Macro Scanner | `/macro-scanner` | Produces a daily four-dimension regime state digest with Kalshi overlay and portfolio implications. | Regime state machine output + `REGIME CHANGE DETECTED` flag |
| Event Calendar | `/event-calendar` | Builds a 30-day event risk calendar with ATR-based impact models and sizing recommendations for critical windows. | `EVENT RISK — REVIEW POSITION \| EVENT RISK — MONITOR \| NO MATERIAL EVENT RISK` |
| Kalshi Reader | `/kalshi-reader` | Reads prediction market signals, flags consensus divergence ≥15pp, and converts to regime-weighted signals. | `HIGH SIGNAL \| NO SIGNAL`; `POLICY SHIFT SIGNAL` |

---

## Layer 2 — Intelligence

Market context generation. These agents produce structured outputs consumed by Governance agents — particularly the Regime Classifier's `REGIME_STATE` block, which feeds the Macro Analyst directly.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Flow Analyst | `/flow-analyst` | Analyzes CFTC COT data for net positioning percentile, OI rate-of-change, and mechanical squeeze severity. | `CROWDED \| ELEVATED \| NEUTRAL \| CONTRARIAN` per instrument |
| Sentiment Tracker | `/sentiment-tracker` | Scores news sentiment against a 30-day baseline and flags price-sentiment divergence and rapid narrative shifts. | `NARRATIVE SHIFT \| STABLE \| DIVERGENCE` |
| Earnings Watcher | `/earnings-watcher` | Monitors corporate event risk using implied vs. historical move, vol premium, and beat/miss rates. | `EARNINGS RISK HIGH \| MODERATE \| LOW` |
| Regime Classifier | `/regime-classifier` | Produces a machine-readable four-dimension regime state and confidence score, consumed by Governance agents. | `REGIME_STATE` block + `REGIME CLASSIFICATION` with confidence |

---

## Layer 3 — Research

Signal development and portfolio sizing. These agents validate new alpha ideas before they reach Governance, and produce target allocations that feed the Execution layer's Rebalancer.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Signal Generator | `/signal-generator` | Proposes regime-consistent, non-redundant alpha hypotheses grounded in mechanism — explicitly not validated. | `HYPOTHESIS — NOT VALIDATED` stamp |
| Backtest Designer | `/backtest-designer` | Runs a seven-check spec review covering universe, regime coverage, cost model, timing, holdout, benchmark, and power. | `SPEC APPROVED \| SPEC REQUIRES REVISION` |
| Correlation Mapper | `/correlation-mapper` | Audits eight-factor loadings, pairwise correlations under normal and stress regimes, and portfolio diversification score. | `APPROVED \| REDUNDANT \| CONCENTRATION WARNING` |
| Capacity Estimator | `/capacity-estimator` | Calculates AUM ceiling using the square-root impact model at 1/5/10% ADV and flags when AUM approaches that ceiling. | `CAPACITY CONSTRAINED` flag when AUM is within 3× of ceiling |
| Decay Tracker | `/decay-tracker` | Compares rolling 3m/6m/12m live vs. backtest Sharpe and classifies the signal's decay curve shape. | Health score 0–100 + decay curve: `linear \| exponential \| episodic` |
| Portfolio Optimizer | `/portfolio-optimizer` | Computes target allocations via risk parity or mean-variance, enforces hard constraints, and identifies binding constraints. | `ALLOCATION COMPLETE \| REBALANCE TRIGGER \| URGENT REBALANCE \| BINDING CONSTRAINT ACTIVE` |

---

## Layer 4 — Execution

Order management and fill quality. These agents receive verdicts from Governance and target allocations from Research, and produce the actual trade instructions.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Order Router | `/order-router` | Selects venue and order type by instrument class, applies VWAP window, and halts orders that exceed 10% ADV. | `APPROVED \| OUTSIZED ORDER — HALT` |
| Slippage Monitor | `/slippage-monitor` | Benchmarks fills against arrival price, computes realized vs. modeled slippage ratio, and classifies broker performance. | `ACCEPTABLE \| ELEVATED \| INVESTIGATE`; `FILL DEGRADATION` flag at ratio >1.5 for 3 consecutive trades |
| Position Reconciler | `/position-reconciler` | Runs three-way reconciliation across broker, OMS, and signal register and flags breaks by type and severity. | `CLEAN \| BREAKS DETECTED`; `ORDER ROUTING GATE: CLEARED \| SUSPENDED` |
| Rebalancer | `/rebalancer` | Generates the optimal trade list from Portfolio Optimizer targets, nets trades, sequences exits first, and flags uneconomic rebalances. | `REBALANCE APPROVED — FULL \| REBALANCE APPROVED — PARTIAL \| REBALANCE UNECONOMIC \| NO REBALANCE REQUIRED` |
| Roll Manager | `/roll-manager` | Maintains a 90-day futures expiry calendar, monitors roll cost vs. 30-day average, and issues urgent roll alerts within 3 days of first notice. | `URGENT ROLL \| ROLL NOW \| ROLL COST ELEVATED` |

---

## Verdict Reference

| Verdict / Stamp | Agent | Meaning |
|---|---|---|
| `NO-GO` | Full Panel | Hard block — do not proceed |
| `CONDITIONAL GO` | Full Panel | Proceed with specified conditions |
| `GO` | Full Panel | Cleared — mandatory post-trade monitoring required |
| `VIOLATION` | Compliance | Mandate or regulatory breach — hard stop |
| `BLOCKED` | Risk / Systems | Hard stop at risk or infrastructure layer |
| `HALT` | Drawdown Monitor | Maximum circuit breaker — suspend all activity |
| `SUSPEND` | Drawdown Monitor | Reduce all positions, no new trades |
| `UNVERIFIED` | NAV Calculator | Do not distribute or report until resolved |
| `OUTSIZED ORDER — HALT` | Order Router | Order exceeds 10% ADV — do not route |
| `BREAKS DETECTED` | Position Reconciler | Reconciliation gate suspended pending resolution |
| `REBALANCE UNECONOMIC` | Rebalancer | Cost > 50% of expected Sharpe benefit — partial rebalance only |
| `SPEC REQUIRES REVISION` | Backtest Designer | Backtest may not proceed until spec deficiencies resolved |
| `HYPOTHESIS — NOT VALIDATED` | Signal Generator | Idea only — no capital allocation until /signal clears |
| `FILL DEGRADATION` | Slippage Monitor | Broker on formal review — consider reducing order flow |
| `NARRATIVE SHIFT` | Sentiment Tracker | 5-day sentiment drift > 0.3 — escalate for positioning review |
| `EARNINGS RISK HIGH` | Earnings Watcher | Hedge required before expiry |
| `CROWDED` | Flow Analyst | Extreme same-direction speculative positioning — squeeze risk elevated |
| `CAPACITY CONSTRAINED` | Capacity Estimator | AUM within 3× of ceiling — do not raise without impact model revision |
| `URGENT ROLL` | Roll Manager | ≤3 days to first notice — execute immediately |
