# Backtest Parameters — Carry

A backtest specification checklist for carry strategies. Carry backtests have unique failure modes compared to TSMOM — most importantly, the correlation structure in normal-market data will overstate diversification benefit in the scenarios that matter. Use `/backtest-designer` to validate against these requirements.

---

## Required Lookback Period

**Minimum: 25 years.**

Carry backtests require a longer history than TSMOM because carry premia are highly regime-dependent and a 20-year sample may not include all relevant macro cycles. The following crash and stress periods must be in-sample:

| Period | Why It Must Be Included |
|--------|------------------------|
| 1998 LTCM crisis | First major documented carry crash; FX and rates carry simultaneously |
| 2000–2002 (dot-com bust) | Low-vol carry environment; validates normal-regime carry premium |
| 2007–2009 (GFC) | The defining carry crash — 2008 FX carry crash is the most severe on record |
| 2013 (Taper Tantrum) | Rapid rates repricing; rates carry and EM FX carry both suffered |
| 2015 (China devaluation) | EM FX carry unwind; CNY peg break risk scenario |
| 2018 Q4 (EM selloff) | EM FX carry crash |
| 2020 (COVID) | Multi-asset carry crash in March; V-recovery partially offsets |
| 2022 (rates shock) | Yield curve inversion; rates carry turned negative |

A backtest starting in 2010 will show excellent carry returns (post-GFC normalization was very favorable for carry) with none of the major crash history that is needed to calibrate drawdown limits properly.

---

## Signal Construction Variants to Test

Report each variant separately:

### FX Carry Variants
| Variant | Specification | Notes |
|---------|--------------|-------|
| Raw interest rate differential | `r_high - r_low` | Simplest; may include country risk premium |
| CIP deviation | Forward premium minus interest differential | More precise; filters out arbitrage-able component |
| Forward rate implied | Use forward points directly | Operationally cleanest; matches live implementation |

### Rates Carry Variants
| Variant | Specification | Notes |
|---------|--------------|-------|
| Curve slope only | `y_10Y - y_2Y` | Simple; misses roll-down |
| Roll-down only | Expected price appreciation as bond ages | Better for stable curves |
| Combined | Slope + roll-down | Most complete; use as primary |

### Commodity Carry Variants
| Variant | Specification | Notes |
|---------|--------------|-------|
| Front minus second contract | `(F1 - F2) / F2 × 365/30` | Monthly annualized roll yield |
| Front minus 12-month | `(F1 - F12) / F12` | Longer-dated curve; less noisy |

---

## Transaction Costs

Apply costs per side at each rebalancing event:

| Instrument | Cost per Side | Notes |
|------------|--------------|-------|
| G10 FX futures | 0.5–1 bp | Very liquid; lowest costs |
| G10 FX forwards | 1–2 bps | Prime broker spread; benchmark against interbank |
| EM FX futures | 2–5 bps | Liquidity-dependent; use 5 bps for EM |
| US rates futures | 0.25–0.5 bps | Deepest market; sub-bp costs |
| European rates futures | 0.5–1 bp | Slightly wider than US |
| JGB futures | 1–2 bps | Less liquidity in certain tenors |
| Commodity futures | 1–2 bps | Similar to TSMOM; 2 bps baseline |

Carry strategies have lower turnover than TSMOM (monthly vs. weekly for most components), which partially offsets the wider EM bid-ask spreads.

---

## Benchmark

**Primary benchmark: Deutsche Bank G10 Carry Index** (long the three highest-yielding G10 currencies, short the three lowest; equal-weighted; publicly available).

Also compare to:
- **Barclays FX Carry Index** (alternative construction; useful for robustness check)
- **T-Bill rate** (carry strategies should comfortably beat cash over a full cycle)
- **60/40 portfolio** (to verify carry provides genuine diversification, not just equity beta)

If FX carry returns have correlation > 0.7 to the MSCI World equity index over the full backtest period, the strategy is not providing the diversification claimed — decompose the beta before attributing carry premium.

---

## Out-of-Sample Holdout

**Holdout period: 2019–present.**

Slightly different from TSMOM because rates carry dynamics changed significantly in 2022. The holdout period must include:
- 2020 COVID crash (carry crash scenario)
- 2022 rates shock (yield curve inversion; negative rates carry)
- 2023–2024 normalization (recovery period)

Report in-sample Sharpe (pre-2019) and out-of-sample Sharpe separately. If out-of-sample Sharpe is below 0.25 after costs (lower threshold than TSMOM because carry runs at lower vol), the strategy is not working live.

---

## Critical Pitfall: Correlation Decomposition

**The most common carry backtest failure:** Reporting average correlation across the full sample period and using it as the diversification claim.

Carry positions are approximately uncorrelated in normal markets and highly correlated during crashes. A 25-year average correlation of 0.25 between FX carry and commodity carry is not meaningful — what matters is:

1. Correlation during the 2008 FX carry crash: likely 0.7–0.9
2. Correlation during 2020 COVID: likely 0.6–0.8
3. Correlation during normal markets: 0.1–0.3

Any backtest that reports a single portfolio Sharpe ratio without decomposing normal-regime vs. crisis-regime correlation is hiding the most important risk of the strategy.

**Required decomposition:**
- Regime-conditional Sharpe ratios: Sharpe during RISK_ON vs. RISK_OFF periods
- Crisis-conditional drawdown: maximum drawdown during each of the labeled crisis periods above
- Equity beta decomposition: carry return = α + β₁ × equity return + β₂ × vol return + ε; report all three components

---

## Backtest Approval Checklist

Before submitting to `/backtest-designer`, confirm:

- [ ] Data covers 1998–present (minimum; 2000 acceptable if 1998 data unavailable)
- [ ] All eight stress periods listed above are in-sample
- [ ] Transaction costs applied per the table above
- [ ] FX carry: specify whether raw differential, CIP deviation, or forward-implied
- [ ] Rates carry: roll-down component explicitly included
- [ ] Commodity carry: annualized roll yield correctly computed (days-to-expiry scaling)
- [ ] Correlation decomposition provided (normal vs. stress regimes)
- [ ] Out-of-sample holdout from 2019 onward
- [ ] Results compared to Deutsche Bank G10 Carry Index
- [ ] Equity beta explicitly decomposed and reported
- [ ] In-sample and out-of-sample Sharpe reported separately
- [ ] Crash scenarios reported with period-specific drawdown figures
