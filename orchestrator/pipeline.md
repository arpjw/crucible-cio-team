# Crucible Orchestration Pipeline

## Purpose

This document defines the execution graph for the Crucible Orchestration Layer. It specifies the order in which agents run, what each agent reads from the shared context bus, what each agent writes to it, and which edges in the graph are hard dependencies vs. soft sequencing.

The pipeline replaces human copy-paste. Outputs from one agent become inputs to the next automatically via the context bus (`orchestrator/context-bus.md`). No agent should be invoked without its upstream dependencies satisfied.

---

## Execution Graph

```
Stage 0: Bus Initialization
  └── Load context/portfolio-state.md → PORTFOLIO_STATE
  └── Load context/risk-limits.md     → RISK_HEADROOM

Stage 1: Regime Classification (always first)
  └── regime-classifier
        READS:  context/portfolio-state.md, context/risk-limits.md
        WRITES: REGIME_STATE → context bus
        FANS OUT TO: macro-analyst, kalshi-reader, macro-scanner,
                     risk-officer, signal-generator (all read REGIME_STATE)

Stage 2: Hard Gates (sequential, fail-fast)
  ├── compliance
  │     READS:  REGIME_STATE, PORTFOLIO_STATE, RISK_HEADROOM
  │             context/fund-mandate.md
  │     WRITES: COMPLIANCE_STATUS → context bus
  │     GATE:   if COMPLIANCE_STATUS.verdict = VIOLATION → HARD HALT
  │
  └── drawdown-monitor
        READS:  PORTFOLIO_STATE, RISK_HEADROOM
        WRITES: DRAWDOWN_STATUS → context bus (embedded in RISK_HEADROOM)
        GATE:   if DRAWDOWN_STATUS.escalation = HALT → HARD HALT

Stage 3: Parallel Intelligence Layer
  ├── risk-officer
  │     READS:  REGIME_STATE, PORTFOLIO_STATE, RISK_HEADROOM
  │     WRITES: RISK_HEADROOM.officer_verdict, RISK_HEADROOM.flags[]
  │
  ├── macro-analyst
  │     READS:  REGIME_STATE, PORTFOLIO_STATE
  │     WRITES: bus.MACRO_VERDICT (embedded in ACTIVE_SIGNALS context)
  │
  └── kalshi-reader
        READS:  REGIME_STATE
        WRITES: bus.KALSHI_SIGNALS (embedded in ACTIVE_SIGNALS context)

  [All three run concurrently — no inter-dependencies]

Stage 4: Signal Research (conditional on submission type)
  └── signal-researcher  [only if submission is signal-related]
        READS:  REGIME_STATE, ACTIVE_SIGNALS, RISK_HEADROOM
        WRITES: ACTIVE_SIGNALS.signal_verdict per signal

Stage 5: Portfolio Optimization
  └── portfolio-optimizer
        READS:  REGIME_STATE, PORTFOLIO_STATE, RISK_HEADROOM, ACTIVE_SIGNALS
        WRITES: PORTFOLIO_STATE.target_weights[]
                PORTFOLIO_STATE.rebalance_triggers[]
                PORTFOLIO_STATE.binding_constraints[]

Stage 6: Execution Layer (reads from portfolio-optimizer output)
  ├── rebalancer
  │     READS:  PORTFOLIO_STATE.target_weights, PORTFOLIO_STATE.current_weights,
  │             RISK_HEADROOM, COMPLIANCE_STATUS
  │     WRITES: PORTFOLIO_STATE.trade_list[]
  │
  └── order-router
        READS:  PORTFOLIO_STATE.trade_list, PORTFOLIO_STATE.target_weights,
                RISK_HEADROOM
        WRITES: PORTFOLIO_STATE.routing_instructions[]

Stage 7: Audit Gate (final gate before any execution instruction is issued)
  └── audit-logger
        READS:  PORTFOLIO_STATE.trade_list, PORTFOLIO_STATE.routing_instructions,
                COMPLIANCE_STATUS, RISK_HEADROOM
        WRITES: AUDIT_STATUS → context bus
        GATE:   if AUDIT_STATUS.status = INCOMPLETE → SOFT HALT
                Execution instructions withheld until COMPLETE

Stage 8: Pipeline Report
  └── [orchestrator assembles unified Pipeline Report from full bus state]
```

---

## Dependency Rules

### Hard Dependencies (agent cannot start until upstream is complete)

| Agent | Must Wait For |
|---|---|
| compliance | regime-classifier |
| drawdown-monitor | compliance (sequential gate ordering) |
| risk-officer | regime-classifier |
| macro-analyst | regime-classifier |
| kalshi-reader | regime-classifier |
| signal-researcher | risk-officer, macro-analyst, kalshi-reader |
| portfolio-optimizer | signal-researcher (or Stage 3 if no signal research) |
| rebalancer | portfolio-optimizer |
| order-router | portfolio-optimizer |
| audit-logger | rebalancer, order-router |

### Parallel Execution Windows

| Window | Agents |
|---|---|
| Stage 3 | risk-officer, macro-analyst, kalshi-reader |
| Stage 6 | rebalancer, order-router |

---

## Context Bus Flow: What Each Agent Reads and Writes

### regime-classifier
- **Reads:** context/portfolio-state.md (prior regime notes), context/risk-limits.md
- **Writes:** `REGIME_STATE {}` — the full machine-readable block as defined in `agents/regime-classifier.md`

### compliance
- **Reads:** `REGIME_STATE`, `PORTFOLIO_STATE`, `RISK_HEADROOM`, context/fund-mandate.md
- **Writes:** `COMPLIANCE_STATUS.verdict` ∈ {CLEAR, WARNING, VIOLATION}
- **Writes:** `COMPLIANCE_STATUS.flags[]` — list of flagged items with limit % used
- **Writes:** `COMPLIANCE_STATUS.pre_trade_checklist` — mandatory checklist state

### drawdown-monitor
- **Reads:** `PORTFOLIO_STATE`, `RISK_HEADROOM`
- **Writes:** `RISK_HEADROOM.drawdown_status` ∈ {MONITOR, WARN, SUSPEND, HALT}
- **Writes:** `RISK_HEADROOM.drawdown_velocity` — projected days to threshold breach
- **Writes:** `RISK_HEADROOM.drawdown_classification` ∈ {CORRELATED, IDIOSYNCRATIC}

### risk-officer
- **Reads:** `REGIME_STATE`, `PORTFOLIO_STATE`, `RISK_HEADROOM`
- **Writes:** `RISK_HEADROOM.officer_verdict` ∈ {APPROVED, FLAGGED, BLOCKED}
- **Writes:** `RISK_HEADROOM.position_headroom{}` — per-position remaining capacity
- **Writes:** `RISK_HEADROOM.var_headroom` — remaining VaR budget

### macro-analyst
- **Reads:** `REGIME_STATE`, `PORTFOLIO_STATE`
- **Writes:** `ACTIVE_SIGNALS.macro_context` — regime-grounded macro assessment
- **Writes:** `ACTIVE_SIGNALS.macro_verdict` ∈ {SUPPORTS, NEUTRAL, CONTRADICTS}

### kalshi-reader
- **Reads:** `REGIME_STATE`
- **Writes:** `ACTIVE_SIGNALS.kalshi_signals[]` — signals ranked by divergence strength
- **Writes:** `ACTIVE_SIGNALS.kalshi_regime_weight` — prediction market confidence overlay

### signal-researcher
- **Reads:** `REGIME_STATE`, `ACTIVE_SIGNALS`, `RISK_HEADROOM`
- **Writes:** `ACTIVE_SIGNALS.signal_verdicts{}` — per-signal: {validity, overfitting_risk, regime_robustness}
- **Writes:** `ACTIVE_SIGNALS.signal_overall` ∈ {PASS, FLAG, BLOCK}

### portfolio-optimizer
- **Reads:** `REGIME_STATE`, `PORTFOLIO_STATE`, `RISK_HEADROOM`, `ACTIVE_SIGNALS`
- **Writes:** `PORTFOLIO_STATE.target_weights{}` — optimal allocation per instrument (% NAV)
- **Writes:** `PORTFOLIO_STATE.rebalance_triggers[]` — which positions exceed 30% drift
- **Writes:** `PORTFOLIO_STATE.binding_constraints[]` — which constraints limited the optimum
- **Writes:** `PORTFOLIO_STATE.portfolio_sharpe` — expected Sharpe of the target portfolio

### rebalancer
- **Reads:** `PORTFOLIO_STATE.target_weights`, `PORTFOLIO_STATE.current_weights`, `RISK_HEADROOM`, `COMPLIANCE_STATUS`
- **Writes:** `PORTFOLIO_STATE.trade_list[]` — netted, sequenced trades (exits before entries)
- **Writes:** `PORTFOLIO_STATE.rebalance_cost_benefit` — ECONOMIC or UNECONOMIC verdict

### order-router
- **Reads:** `PORTFOLIO_STATE.trade_list`, `PORTFOLIO_STATE.target_weights`, `RISK_HEADROOM`
- **Writes:** `PORTFOLIO_STATE.routing_instructions[]` — per-trade: venue, timing, order type, slippage budget
- **Writes:** `PORTFOLIO_STATE.outsized_orders[]` — any orders flagged at >10% ADV

### audit-logger
- **Reads:** `PORTFOLIO_STATE.trade_list`, `PORTFOLIO_STATE.routing_instructions`, `COMPLIANCE_STATUS`, `RISK_HEADROOM`
- **Writes:** `AUDIT_STATUS.status` ∈ {COMPLETE, INCOMPLETE}
- **Writes:** `AUDIT_STATUS.missing_elements[]` — which of the five required elements are absent
- **Writes:** `AUDIT_STATUS.record_id` — unique pre-trade record identifier

---

## Halt Propagation Rules

| Condition | Trigger | Effect |
|---|---|---|
| `COMPLIANCE_STATUS.verdict = VIOLATION` | compliance (Stage 2) | HARD HALT — all pending agents cancelled, no execution instructions issued |
| `RISK_HEADROOM.drawdown_status = HALT` | drawdown-monitor (Stage 2) | HARD HALT — same as above |
| `AUDIT_STATUS.status = INCOMPLETE` | audit-logger (Stage 7) | SOFT HALT — execution withheld, PM asked for override with documented rationale |
| `RISK_HEADROOM.officer_verdict = BLOCKED` | risk-officer (Stage 3) | SOFT HALT — pipeline pauses, surfaces block reason, requires PM override |
| `PORTFOLIO_STATE.rebalance_cost_benefit = UNECONOMIC` | rebalancer (Stage 6) | SOFT HALT — rebalance not recommended; PM must confirm to proceed |
| `ACTIVE_SIGNALS.signal_overall = BLOCK` | signal-researcher (Stage 4) | SOFT HALT — signal blocked; requires PM override before portfolio-optimizer runs |

See `orchestrator/halt-protocol.md` for full halt handling procedures.

---

## Signal-Related Submission Detection

The pipeline determines whether to invoke signal-researcher (Stage 4) based on submission content.

**Invoke signal-researcher if the submission contains any of:**
- Reference to a signal, model, factor, or strategy by name
- A proposed new position driven by a quantitative trigger
- A backtest result or Sharpe ratio claim
- The words "signal", "alpha", "factor", "model", "strategy", "breakout", "momentum", "carry", "value", "trend"

**Skip signal-researcher if the submission is purely:**
- A portfolio rebalance to existing target weights (no new signal)
- A roll or expiry management decision
- A compliance or operational inquiry

---

## Pipeline Timing Reference

| Stage | Agents | Expected Duration |
|---|---|---|
| 0 | Bus init | < 5 seconds |
| 1 | regime-classifier | 30–60 seconds |
| 2 | compliance, drawdown-monitor | 30–60 seconds each, sequential |
| 3 | risk-officer, macro-analyst, kalshi-reader | 30–60 seconds, parallel |
| 4 | signal-researcher (if triggered) | 30–60 seconds |
| 5 | portfolio-optimizer | 30–60 seconds |
| 6 | rebalancer, order-router | 30–60 seconds, parallel |
| 7 | audit-logger | 15–30 seconds |
| 8 | report assembly | < 10 seconds |

Total pipeline runtime (no halts, signal-related submission): approximately 5–8 minutes.
