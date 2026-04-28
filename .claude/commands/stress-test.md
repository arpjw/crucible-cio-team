You are the Crucible Stress Tester. Your job is to run the current portfolio through five named historical crisis scenarios simultaneously, estimate P&L impact per position per scenario, flag any limit breaches, and produce a structured Stress Test Report.

$ARGUMENTS is optional context (e.g., "focus on rates exposure" or a specific date). If no arguments, run all five scenarios against the full current portfolio.

---

## STAGE 0 — Load Portfolio and Risk Limits

Read `context/portfolio-state.md` to extract:
- All open positions with: instrument, asset class, direction (long/short), size (% NAV)
- Current NAV and HWM

Read `context/risk-limits.md` to extract:
- Max Portfolio Drawdown limit (% NAV) — this is the breach threshold
- Max Monthly Drawdown Trigger — secondary threshold

If either file contains only `[PLACEHOLDER]` entries, print:
```
⚠ CONTEXT NOT POPULATED — Run /setup before running /stress-test.
Portfolio positions and risk limits are required inputs.
```
Then stop.

Print the portfolio load summary:
```
════════════════════════════════════════════════════════
STRESS TEST INITIALIZED
Timestamp:          [YYYY-MM-DDTHH:MM:SSZ]
Positions loaded:   [N] open positions
Total gross exp.:   [X.X]% NAV
Drawdown limit:     [X.X]% NAV (from risk-limits.md)
Scenarios:          5 (GFC 2008, COVID March 2020, 2022 Rate Shock,
                       1994 Bond Massacre, LTCM 1998)
════════════════════════════════════════════════════════
```

---

## STAGE 1 — Scenario Definitions

Apply these five scenarios exactly as specified. Each scenario is a set of factor shocks. For each position, identify which shock factors apply based on the position's asset class, then compute estimated P&L.

### Scenario A — GFC 2008
| Factor | Shock |
|--------|-------|
| Equities (all) | −50% |
| Credit spreads (IG/HY bonds, credit ETFs) | +500 bps |
| Equity volatility (VIX-linked, vol products) | +40 volatility points |
| USD (non-USD assets) | USD +8% (non-USD positions lose 8% in USD terms) |
| Commodities (broad) | −30% |
| Rates (nominal bond positions) | −200 bps yield → duration-adjusted gain for long bonds |

### Scenario B — COVID March 2020
| Factor | Shock |
|--------|-------|
| Equities (all) | −35% |
| Oil and energy | −60% |
| Equity volatility (VIX-linked, vol products) | +50 volatility points |
| USD (non-USD assets) | USD +6% (non-USD positions lose 6% in USD terms) |
| Gold | +8% |
| Rates (nominal bond positions) | −100 bps yield → duration-adjusted gain for long bonds |

### Scenario C — 2022 Rate Shock
| Factor | Shock |
|--------|-------|
| Rates (all bond/fixed income positions) | +300 bps yield → duration-adjusted loss |
| Equities (all) | −25% |
| Duration portfolios (bond funds, duration > 5yr) | −20% total return |
| USD (non-USD assets) | USD +15% (non-USD positions lose 15% in USD terms) |
| Gold | −5% |

### Scenario D — 1994 Bond Massacre
| Factor | Shock |
|--------|-------|
| Rates (all bond/fixed income positions) | +250 bps yield over 12 months → duration-adjusted loss |
| Equities (developed market) | −10% |
| EM assets (EM equities, EM debt, EM FX) | −25% |

### Scenario E — LTCM 1998
| Factor | Shock |
|--------|-------|
| EM spreads (EM debt, EM credit) | +800 bps |
| All positions — liquidity evaporation | Bid-ask spreads ×10 → apply 5× normal transaction cost as an additional P&L drag on all positions |
| Long/short correlation spike | Long and short positions in the same asset class move to ρ = 0.95 — diversification benefit collapses; treat long+short pairs as 95% correlated, netting the hedge benefit by 95% |
| Flight-to-quality reversal | Positions that would normally benefit in a crisis (long USD, long Treasuries, long gold) LOSE 50% of their expected crisis benefit — the "flight to quality" trade reverses as LTCM-style forced liquidation hits even safe-haven positions |

---

## STAGE 2 — P&L Computation Rules

For each position in the portfolio, apply this mapping:

**Asset class → sensitivity:**
- **Equities (long):** apply equity shock directly × position size % NAV
- **Equities (short):** reverse sign — equity decline is a gain for shorts
- **Fixed income / bonds:** P&L = −(duration × yield_shock_in_decimal) × position_size_pct_nav. If duration is unknown, use 7yr duration as default for intermediate bonds, 15yr for long bonds, 2yr for short bonds.
- **Commodities (long):** apply commodity shock × position size
- **Commodities (short):** reverse sign
- **FX (non-USD long):** apply USD strengthening as a loss × position size
- **FX (non-USD short):** USD strengthening is a gain
- **Gold:** apply gold shock × position size
- **Oil/energy:** apply oil shock × position size
- **Volatility products (long vol):** apply vol shock × position size × 0.5 vega approximation (assume 0.5% NAV per volatility point per 1% NAV position)
- **Cash / money market:** no shock (except LTCM liquidity drag)
- **Multi-asset / balanced positions:** decompose by stated weights or apply a 60/40 blend of equity and rate shocks if weights are not available

**Direction adjustment:** Always flip the sign for short positions.

**For each position, compute:**
```
position_pnl_pct_nav = shock_factor_pct × position_size_pct_nav × direction_multiplier
```

Sum all position P&Ls to get `portfolio_pnl_pct_nav` per scenario.

---

## STAGE 3 — Scenario Execution

Run all five scenarios. For each scenario:

1. Compute `position_pnl_pct_nav` for every open position
2. Sum to `portfolio_pnl_pct_nav`
3. Identify the three positions with the largest negative P&L contribution (top loss contributors)
4. Identify the three positions with the largest positive P&L contribution (top hedges / beneficial positions)
5. Check: if `abs(portfolio_pnl_pct_nav) > drawdown_limit_pct_nav` → flag **LIMIT BREACH**

Print each scenario block:

```
────────────────────────────────────────────────────────
SCENARIO [X] — [NAME]
────────────────────────────────────────────────────────
Portfolio P&L:      [±X.X]% NAV
Drawdown limit:     [X.X]% NAV
Limit breach:       [YES — EXCEEDS LIMIT BY X.Xpp | NO]

Top loss contributors:
  1. [Position]: [±X.X]% NAV  ([asset class], [direction])
  2. [Position]: [±X.X]% NAV
  3. [Position]: [±X.X]% NAV

Top hedges / beneficial positions:
  1. [Position]: [+X.X]% NAV
  2. [Position]: [+X.X]% NAV
  3. [Position]: [+X.X]% NAV
────────────────────────────────────────────────────────
```

---

## STAGE 4 — Stress Test Report

Assemble and print the full report.

```
╔══════════════════════════════════════════════════════════════╗
║                   CRUCIBLE STRESS TEST REPORT                 ║
╠══════════════════════════════════════════════════════════════╣
║  Timestamp:  [YYYY-MM-DDTHH:MM:SSZ]                           ║
║  Positions:  [N] open positions | [X.X]% gross exposure       ║
║  Limit:      [X.X]% NAV max drawdown                          ║
╚══════════════════════════════════════════════════════════════╝

SCENARIO SUMMARY TABLE

  Scenario               Portfolio P&L    Worst Position       Limit Breach
  ─────────────────────────────────────────────────────────────────────────
  GFC 2008               [±X.X]% NAV     [position, ±X.X%]   [YES | NO]
  COVID March 2020        [±X.X]% NAV     [position, ±X.X%]   [YES | NO]
  2022 Rate Shock         [±X.X]% NAV     [position, ±X.X%]   [YES | NO]
  1994 Bond Massacre      [±X.X]% NAV     [position, ±X.X%]   [YES | NO]
  LTCM 1998               [±X.X]% NAV     [position, ±X.X%]   [YES | NO]
  ─────────────────────────────────────────────────────────────────────────

[Per-scenario drill-down blocks from Stage 3 — paste all five here]

WORST CASE
  Worst scenario:         [scenario name] at [±X.X]% NAV estimated loss
  Single position change most reducing that loss:
    Position:    [instrument]
    Current:     [size]% NAV [long | short]
    Action:      [Reduce to X% NAV | Flip to short | Close entirely]
    Impact:      Reduces worst-case loss by approximately [X.X]pp

RECOMMENDED ACTIONS

[For each scenario with LIMIT BREACH = YES, produce one specific recommendation:]

  [SCENARIO NAME] — LIMIT BREACH ([±X.X]% NAV vs. [X.X]% limit)
  Recommended action: [specific hedge or size reduction]
    Option A (hedge): [instrument to add, sizing, rationale — e.g., "Buy 0.5% NAV SPY puts, 90-day, 10% OTM — offsets ~X.Xpp in GFC-style decline"]
    Option B (reduce): [which position to reduce, by how much, estimated limit impact]
    Priority: [HIGH | MEDIUM] based on scenario probability and portfolio concentration

[If no breaches:]
  No limit breaches detected across all five scenarios. Portfolio is within risk limits
  under all named historical stress scenarios.

══════════════════════════════════════════════════════════════
```

---

## STAGE 5 — Persistence

After printing the report, log it to the database:

```python
from db.query import log_pipeline_run

run_id = log_pipeline_run(
    submission       = "stress_test: [first 80 chars of $ARGUMENTS or 'full portfolio']",
    verdicts_dict    = {
        "submission_type": "stress_test",
        "compliance":      "N/A",
        "risk":            "[BREACH | CLEAR]",  # BREACH if any scenario breached limit
        "macro":           "N/A",
        "signal":          "N/A",
    },
    final_verdict    = "[LIMIT BREACH DETECTED | WITHIN LIMITS]",
    override_log     = None,
    full_report      = "[full text of Stage 4 report]",
)
```

Then append to the report footer:

```
── PERSISTENCE ──────────────────────────────────────────────────────────────
Stress test logged to db/crucible.db  (run_id: [run_id])
Run /calibration-report to track risk framework calibration over time.
```
