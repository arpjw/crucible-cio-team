# Crucible CIO Team

An adversarial multi-agent framework for systematic fund managers. Five AI agents that challenge fund decisions before execution, modeled after the role structure of a systematic macro CTA.

## Framework Overview

Each agent is a skeptic, not an assistant. They exist to surface failure modes, not validate decisions. When you present a trade idea, signal, or portfolio change, the Crucible agents attack it from their domain.

## Layer 0 — Decision Review Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Risk Officer | `/risk` | Position sizing, drawdown, tail risk, correlation |
| Signal Researcher | `/signal` | Signal validity, overfitting, regime robustness |
| Systems Architect | `/systems` | Execution infrastructure, data pipelines, latency |
| Compliance Officer | `/compliance` | Regulatory, mandate, risk limits, reporting |
| Macro Analyst | `/macro` | Macro thesis, regime identification, cross-asset |
| Full Panel | `/crucible` | All five agents in sequence |

## Layer 1 — Operations Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Drawdown Monitor | `/drawdown-monitor` | Circuit breaker: threshold positioning, velocity, correlated vs. idiosyncratic loss, MONITOR/WARN/SUSPEND/HALT |
| Vendor Monitor | `/vendor-monitor` | Data feed health: staleness, silent failure detection, cross-vendor consistency, switchover risk |
| Audit Logger | `/audit-logger` | Pre-trade record enforcer: five required elements, COMPLETE/INCOMPLETE gating |
| Cash Manager | `/cash-manager` | Margin and liquidity: utilization, per-position headroom, cash drag, runway, margin call trigger |
| NAV Calculator | `/nav-calculator` | Daily NAV integrity: price verification, staleness, source change, corporate actions, VERIFIED/UNVERIFIED stamp |
| LP Reporter | `/lp-reporter` | LP letter drafter: period return, attribution, drawdown narrative, risk metrics, disclosure scan, DRAFT stamp |
| Tax Tracker | `/tax-tracker` | Tax lot monitor: holding period, wash sale detection, harvest opportunities, after-tax return impact |
| Macro Scanner | `/macro-scanner` | Daily regime digest: four-dimension state machine, regime change detection, Kalshi overlay, portfolio implication |
| Event Calendar | `/event-calendar` | 30-day event risk calendar: market impact model, ATR-based event exposure, 5-day critical window, sizing recs |
| Kalshi Reader | `/kalshi-reader` | Prediction market signals: consensus divergence ≥15pp flagged, regime weight conversion, ranked by signal strength |

## Layer 2 — Intelligence Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Flow Analyst | `/flow-analyst` | CFTC COT monitor: net positioning percentile, OI ROC, squeeze severity in ATR units, CROWDED/ELEVATED/NEUTRAL/CONTRARIAN |
| Sentiment Tracker | `/sentiment-tracker` | News sentiment: headline vs. body scoring, 5-day drift vs. 30d avg, price-sentiment divergence, NARRATIVE SHIFT flag |
| Earnings Watcher | `/earnings-watcher` | Corporate event risk: implied vs. historical move, vol premium, beat/miss rate, EARNINGS RISK HIGH/MODERATE/LOW with hedge recs |
| Regime Classifier | `/regime-classifier` | Live regime state machine: four-dimension composite scores, confidence, transition risk, machine-readable REGIME_STATE block |

## Layer 3 — Research Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Signal Generator | `/signal-generator` | Alpha hypothesis proposer: regime-consistent, non-redundant, mechanism-grounded hypotheses stamped HYPOTHESIS — NOT VALIDATED |
| Backtest Designer | `/backtest-designer` | Backtest spec enforcer: seven checks (universe, regime coverage, cost model, timing, holdout, benchmark, power), SPEC APPROVED/REQUIRES REVISION |
| Correlation Mapper | `/correlation-mapper` | Factor exposure auditor: eight-factor loadings, pairwise ρ_normal and ρ_stress, diversification score, APPROVED/REDUNDANT/CONCENTRATION WARNING |
| Capacity Estimator | `/capacity-estimator` | AUM ceiling calculator: square-root impact model at 1/5/10% ADV, capacity ceiling formula, CAPACITY CONSTRAINED flag when AUM within 3× of ceiling |
| Decay Tracker | `/decay-tracker` | Signal health monitor: rolling 3m/6m/12m live vs. backtest Sharpe ratio, decay curve classification (linear/exponential/episodic), health score 0-100 |
| Portfolio Optimizer | `/portfolio-optimizer` | Position sizing arbiter: risk parity or mean-variance, hard constraint enforcement, binding constraint identification, REBALANCE TRIGGER at >30% drift |

## Layer 4 — Execution Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Order Router | `/order-router` | Venue and timing selection: exchange direct/broker algo/DMA by instrument class, VWAP window, order type (market/limit/iceberg by %ADV), slippage budget, OUTSIZED ORDER halt at >10% ADV |
| Slippage Monitor | `/slippage-monitor` | Fill quality auditor: arrival price benchmark, realized vs. modeled slippage ratio, FILL DEGRADATION flag at ratio >1.5 for 3 consecutive trades, broker/time-of-day/size attribution, ACCEPTABLE/ELEVATED/INVESTIGATE |
| Position Reconciler | `/position-reconciler` | Three-way reconciliation: broker vs. OMS (break at 1 contract or 0.01% NAV), OMS vs. signal register (UNINTENDED POSITION), execution log vs. OMS (UNBOOKED FILL), CLEAN/BREAKS DETECTED gate |
| Rebalancer | `/rebalancer` | Optimal trade generator: gap computation, trade netting, exits-before-entries sequencing, cost-benefit (REBALANCE UNECONOMIC if cost >50% of benefit), partial rebalance to 85% of gap |
| Roll Manager | `/roll-manager` | Futures roll scheduler: 90-day expiry calendar, roll cost in bps annualized, ROLL COST ELEVATED at >120% of 30d avg, OI-adjusted timing (LIQUIDITY MIGRATED <20% OI), URGENT ROLL at ≤3 days to FND |

## Directory Structure

```
agents/               # Agent persona definitions
context/              # Shared fund context (mandate, limits, portfolio state)
.claude/commands/     # Slash commands that invoke each agent
```

## Usage

1. Update `context/` files with your fund's actual mandate, limits, and current portfolio state.
2. Invoke an agent with a slash command followed by your decision or question.
3. The agent challenges the decision from its domain perspective.

Example:
```
/risk Long 2% NAV ES futures as trend signal fires on 20-day breakout
/crucible Adding EM FX carry basket, 3% NAV, 6 positions equally weighted
```

## Agent Personas

Agent personas live in `agents/`. Each file defines:
- Role identity and adversarial mandate
- Domain-specific challenge framework
- What inputs to expect and what outputs to produce
- Escalation criteria (when to hard block vs. flag)

## Context Files

`context/` files are read by agents at invocation time to ground their challenges in the fund's actual constraints. Keep them current.
