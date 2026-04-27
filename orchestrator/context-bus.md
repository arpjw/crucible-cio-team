# Crucible Context Bus

## Purpose

The context bus is the single source of truth shared between all agents in the Crucible pipeline. It is a structured document that agents write their outputs into and downstream agents read from. No agent passes information to another agent directly — all inter-agent communication flows through this bus.

The bus is initialized at pipeline start from `context/portfolio-state.md` and `context/risk-limits.md`. Each agent appends or updates its designated section. The final bus state is included verbatim in the Pipeline Report.

---

## Bus Schema

### Section: REGIME_STATE

Written by: **regime-classifier**  
Read by: macro-analyst, kalshi-reader, macro-scanner, risk-officer, signal-generator, signal-researcher, portfolio-optimizer

```
REGIME_STATE {
  timestamp:                      [YYYY-MM-DDTHH:MM:SSZ]
  data_as_of:                     [YYYY-MM-DD]

  growth.state:                   [EXPANSION | SLOWDOWN | CONTRACTION | RECOVERY]
  growth.score:                   [0.00–1.00]
  growth.trend_4w:                [+/-0.00]
  growth.confidence:              [0.00–1.00]
  growth.transition_risk:         [TRUE | FALSE]
  growth.nearest_boundary:        [0.45 | 0.60]
  growth.distance_to_boundary:    [0.00]

  inflation.state:                [RISING | ELEVATED | FALLING | ANCHORED]
  inflation.score:                [0.00–1.00]
  inflation.trend_4w:             [+/-0.00]
  inflation.confidence:           [0.00–1.00]
  inflation.transition_risk:      [TRUE | FALSE]

  financial_conditions.state:     [LOOSE | NORMAL | TIGHTENING | TIGHT]
  financial_conditions.score:     [0.00–1.00]
  financial_conditions.trend_4w:  [+/-0.00]
  financial_conditions.confidence:[0.00–1.00]
  financial_conditions.transition_risk: [TRUE | FALSE]

  policy.state:                   [DOVISH | NEUTRAL | PIVOTING | HAWKISH]
  policy.score:                   [0.00–1.00]
  policy.rate_path_shift_4w_bps:  [+/-0]
  policy.confidence:              [0.00–1.00]
  policy.transition_risk:         [TRUE | FALSE]

  quadrant:                       [GOLDILOCKS | LATE_CYCLE | OVERHEATING | DISINFLATION | STAGFLATION_RISK | DEFLATION_RISK | STAGFLATION | EARLY_CYCLE]
  quadrant_modifiers:             [comma-separated modifiers, or NONE]
  full_regime_label:              [quadrant + modifiers]

  overall_confidence:             [0.00–1.00]
  regime_transition_risk:         [TRUE | FALSE]
  dimensions_at_boundary:         [comma-separated list, or NONE]
  stale_indicators:               [comma-separated list, or NONE]
}
```

**Downstream read contract:** Any agent reading `REGIME_STATE` must extract `full_regime_label`, `overall_confidence`, `regime_transition_risk`, and the four dimension states as minimum. Agents may read additional fields for domain-specific use.

---

### Section: PORTFOLIO_STATE

Written by: **bus initializer** (from context/portfolio-state.md), then updated by **portfolio-optimizer**, **rebalancer**, **order-router**  
Read by: all agents

```
PORTFOLIO_STATE {
  as_of:                          [YYYY-MM-DD]

  # Initialized from context/portfolio-state.md
  nav:                            [number, USD or base currency]
  nav_currency:                   [USD | EUR | GBP | ...]
  mtd_return_pct:                 [+/-0.00]
  ytd_return_pct:                 [+/-0.00]
  drawdown_from_hwm_pct:          [0.00]
  gross_leverage:                 [0.00x]
  net_leverage:                   [+/-0.00x]
  daily_var_95_pct:               [0.00]

  current_positions: [
    {
      instrument:                 [string]
      direction:                  [LONG | SHORT]
      size_pct_nav:               [0.00]
      entry_date:                 [YYYY-MM-DD]
      signal:                     [string]
      unrealized_pnl_pct:         [+/-0.00]
    }
  ]

  active_signals_pending: [
    {
      instrument:                 [string]
      direction:                  [LONG | SHORT]
      signal:                     [string]
      proposed_size_pct_nav:      [0.00]
      pending_since:              [YYYY-MM-DD]
    }
  ]

  known_risk_clusters: [
    {
      cluster_label:              [string]
      positions:                  [comma-separated instrument list]
      combined_exposure_pct_nav:  [0.00]
    }
  ]

  # Written by portfolio-optimizer (Stage 5)
  target_weights: {
    [instrument]:                 [0.00]   # % NAV, positive = long, negative = short
  }
  rebalance_triggers: [
    {
      instrument:                 [string]
      current_pct:                [0.00]
      target_pct:                 [0.00]
      drift_pct:                  [0.00]
      urgency:                    [REBALANCE_TRIGGER | URGENT_REBALANCE]
    }
  ]
  binding_constraints: [string]            # list of constraints that limited optimal allocation
  portfolio_sharpe:               [0.00]   # expected Sharpe of target portfolio

  # Written by rebalancer (Stage 6)
  trade_list: [
    {
      instrument:                 [string]
      direction:                  [BUY | SELL | COVER | SHORT]
      size_pct_nav:               [0.00]
      sequence:                   [integer]   # lower = executes first; exits always before entries
      rationale:                  [string]
    }
  ]
  rebalance_cost_benefit:         [ECONOMIC | UNECONOMIC]
  rebalance_cost_bps:             [0.0]
  rebalance_benefit_bps:          [0.0]

  # Written by order-router (Stage 6)
  routing_instructions: [
    {
      instrument:                 [string]
      venue:                      [EXCHANGE_DIRECT | BROKER_ALGO | DMA]
      order_type:                 [MARKET | LIMIT | ICEBERG]
      vwap_window:                [string, e.g. "09:30–11:00 ET"]
      slippage_budget_bps:        [0.0]
      size_pct_adv:               [0.00]
      outsized_flag:              [TRUE | FALSE]
    }
  ]
  outsized_orders: [string]                # instruments where size > 10% ADV
}
```

---

### Section: RISK_HEADROOM

Written by: **bus initializer** (from context/risk-limits.md), then updated by **drawdown-monitor** and **risk-officer**  
Read by: all agents

```
RISK_HEADROOM {
  # Initialized from context/risk-limits.md
  gross_leverage_limit:           [0.00x]
  net_leverage_limit:             [0.00x]
  daily_var_limit_pct:            [0.00]
  monthly_drawdown_halt_pct:      [0.00]
  portfolio_drawdown_reduce_pct:  [0.00]
  max_single_position_pct:        [0.00]
  max_adv_pct:                    [0.00]
  max_loss_per_trade_pct:         [0.00]

  # Written by drawdown-monitor (Stage 2)
  drawdown_status:                [MONITOR | WARN | SUSPEND | HALT]
  drawdown_velocity:              [+/-0.00 % NAV/day]
  drawdown_days_to_threshold:     [integer, or N/A]
  drawdown_classification:        [CORRELATED | IDIOSYNCRATIC | MIXED | N/A]

  # Written by risk-officer (Stage 3)
  officer_verdict:                [APPROVED | FLAGGED | BLOCKED]
  officer_flags: [
    {
      flag_type:                  [LIMIT_BREACH | APPROACHING_LIMIT | CORRELATION | TAIL_RISK | OTHER]
      description:                [string]
      severity:                   [YELLOW | ORANGE | RED]
      limit_pct_used:             [0.00]
    }
  ]
  var_headroom_pct:               [0.00]   # remaining VaR budget (limit minus current)
  gross_leverage_headroom:        [0.00x]
  net_leverage_headroom:          [+/-0.00x]
  position_headroom: {
    [instrument]:                 [0.00]   # remaining % NAV capacity per instrument
  }
}
```

---

### Section: COMPLIANCE_STATUS

Written by: **compliance** (Stage 2)  
Read by: rebalancer, audit-logger, and pipeline halt logic

```
COMPLIANCE_STATUS {
  verdict:                        [CLEAR | WARNING | VIOLATION]
  reviewed_at:                    [YYYY-MM-DDTHH:MM:SSZ]
  reviewer:                       compliance-officer

  flags: [
    {
      rule:                       [string, e.g. "Single position limit"]
      finding:                    [string]
      severity:                   [WARNING | VIOLATION]
      limit_pct_used:             [0.00]
    }
  ]

  mandate_check:                  [PASS | FAIL]
  regulatory_check:               [PASS | FAIL]
  lp_agreement_check:             [PASS | FAIL]
  disclosure_check:               [PASS | FAIL]
  audit_trail_check:              [PASS | FAIL]

  pre_trade_checklist: {
    rationale_documented:         [TRUE | FALSE]
    warnings_addressed:           [TRUE | FALSE]
    limits_verified:              [TRUE | FALSE]
  }

  halt_triggered:                 [TRUE | FALSE]
  halt_reason:                    [string, or N/A]
}
```

---

### Section: AUDIT_STATUS

Written by: **audit-logger** (Stage 7)  
Read by: pipeline halt logic, Pipeline Report assembly

```
AUDIT_STATUS {
  status:                         [COMPLETE | INCOMPLETE]
  record_id:                      [string, unique pre-trade record identifier]
  recorded_at:                    [YYYY-MM-DDTHH:MM:SSZ]

  five_element_check: {
    trade_rationale:              [PRESENT | MISSING]
    risk_parameters:              [PRESENT | MISSING]
    compliance_clearance_ref:     [PRESENT | MISSING]
    portfolio_optimizer_ref:      [PRESENT | MISSING]
    pm_authorization:             [PRESENT | MISSING]
  }

  missing_elements: [string]      # list of missing elements; empty if COMPLETE

  override_log: [
    {
      agent:                      [string]
      override_reason:            [string]
      authorized_by:              [PM | CRO]
      timestamp:                  [YYYY-MM-DDTHH:MM:SSZ]
    }
  ]

  halt_triggered:                 [TRUE | FALSE]
  halt_reason:                    [string, or N/A]
}
```

---

### Section: ACTIVE_SIGNALS

Written by: **macro-analyst**, **kalshi-reader**, **signal-researcher**  
Read by: signal-researcher, portfolio-optimizer

```
ACTIVE_SIGNALS {
  submission_type:                [SIGNAL | REBALANCE | ROLL | OPERATIONAL]

  # Written by macro-analyst (Stage 3)
  macro_context:                  [string, regime-grounded macro assessment, max 3 sentences]
  macro_verdict:                  [SUPPORTS | NEUTRAL | CONTRADICTS]
  macro_flags: [string]           # list of macro concerns specific to the submission

  # Written by kalshi-reader (Stage 3)
  kalshi_signals: [
    {
      market:                     [string]
      kalshi_probability_pct:     [0.0]
      consensus_probability_pct:  [0.0]
      divergence_pp:              [+/-0.0]   # positive = Kalshi more bullish than consensus
      signal_direction:           [BULLISH | BEARISH | NEUTRAL]
      signal_strength:            [HIGH | MODERATE | LOW]   # HIGH if |divergence| >= 15pp
    }
  ]
  kalshi_regime_weight:           [0.00–1.00]   # prediction market confidence as regime overlay

  # Written by signal-researcher (Stage 4, conditional)
  signal_verdicts: {
    [signal_name]: {
      validity:                   [PASS | FLAG | BLOCK]
      overfitting_risk:           [LOW | MODERATE | HIGH]
      regime_robustness:          [ROBUST | CONDITIONAL | FRAGILE]
      live_sharpe_3m:             [0.00 | N/A]
      live_sharpe_6m:             [0.00 | N/A]
      backtest_sharpe:            [0.00 | N/A]
    }
  }
  signal_overall:                 [PASS | FLAG | BLOCK | NOT_EVALUATED]
}
```

---

## Bus Initialization Template

At pipeline start, the orchestrator reads the source context files and populates the bus. Any field that cannot be populated from the source files is marked `[MISSING]` and triggers a context gap flag visible in the Pipeline Report. No agent is blocked by missing context fields — but every missing field is surfaced explicitly.

```
BUS_INIT {
  initialized_at:                 [YYYY-MM-DDTHH:MM:SSZ]
  pipeline_run_id:                [string, e.g. "pipeline-20260427-001"]
  submission:                     [verbatim PM submission text]
  submission_type_detected:       [SIGNAL | REBALANCE | ROLL | OPERATIONAL]
  signal_researcher_triggered:    [TRUE | FALSE]
  context_gaps: [string]          # list of [MISSING] fields; empty if fully populated
}
```

---

## Bus State Versioning

Each agent write operation appends a timestamp to its section header in the form `[written: YYYY-MM-DDTHH:MM:SSZ by agent-name]`. This creates a lightweight audit trail of bus mutations without requiring a full version control system. The Pipeline Report includes all timestamps so the PM can reconstruct the sequence of agent writes.

---

## Reading from the Bus

Agents read by referencing their upstream section key. The pipeline instructions in `.claude/commands/run-pipeline.md` embed the relevant bus sections into each agent's prompt at invocation time. Agents do not read the bus file directly — the orchestrator injects the relevant sections as structured context into each agent call.

This means the bus is write-once per section per pipeline run. An agent that discovers a problem does not rewrite upstream sections — it writes its own verdict to its designated section, and the halt protocol handles propagation.
