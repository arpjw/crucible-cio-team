# Time-Series Momentum — Strategy Overview

## What It Is

Time-series momentum (TSMOM) goes long instruments with positive recent returns and short instruments with negative recent returns. Unlike cross-sectional momentum (which ranks instruments against each other), TSMOM treats each instrument independently — the only comparison is the instrument against its own history.

The canonical signal: if the past 12-month return (excluding the most recent month to avoid short-term reversal) is positive, go long; if negative, go short. Every instrument is always either long or short — there is no neutral.

---

## Signal Construction

### Classic Specification (Moskowitz, Ooi & Pedersen 2012)

```
Signal(t) = sign(r_{t-12, t-1})
```

Where `r_{t-12, t-1}` is the total return from 12 months ago to 1 month ago (the 1-month skip prevents short-term reversal contamination).

### Exponentially Weighted Moving Average Variant (EWMA)

```
Signal_strength(t) = EWMA(daily_return, span=λ) / realized_vol(t)
```

The EWMA variant responds faster to trend reversals and reduces whipsaw losses slightly at the cost of more turnover. Span (λ) is typically 2–6 months. Back-tested Sharpe ratio differences between variants are small; choose based on operational preference for turnover.

### Volatility-Scaled Position Sizing

Target annualized volatility per instrument: **15%**

```
Position(i, t) = (Target_Vol / Realized_Vol_i) × Signal(i, t) × (Capital / N)
```

Where:
- `Realized_Vol_i` = 60-day exponentially weighted standard deviation of daily returns
- `N` = number of instruments in universe
- The signal is either +1 (long) or -1 (short) in the binary specification, or a continuous value in [−1, +1] in the EWMA variant

This sizing ensures each instrument contributes equally to portfolio-level volatility regardless of its native volatility regime.

---

## Rebalancing

**Weekly** rebalancing is standard. Monthly is acceptable for cost reduction.

- Signal recomputed at each rebalancing date
- Position targets updated based on new signal and current volatility estimate
- Trades executed at next day's open to avoid look-ahead bias in live trading

Cost of weekly vs. monthly: approximately 2–3 bps/trade difference in turnover-driven costs. At $100M AUM and 25 instruments, weekly rebalancing adds roughly $150–300K/year in additional transaction costs.

---

## Why the Edge Exists

**1. Behavioral underreaction.** Investors and markets underreact to information, causing prices to drift in the direction of the initial move before eventually correcting. TSMOM harvests this drift.

**2. Structural CTA demand.** Systematic trend-following funds collectively reinforce trends. A rising asset attracts buying from momentum funds, which pushes prices further, which attracts more buying. This is a self-reinforcing loop until it reverses.

**3. Risk premium for crisis drawdowns.** TSMOM underperforms badly in rapid trend reversals (2009 bounce, 2020 V-shaped recovery). Investors are compensated for bearing this reversal risk with a positive expected return over full cycles.

**4. Risk-parity and rebalancing flows.** Large risk-parity funds rebalance toward fixed volatility targets, creating predictable buying and selling pressure that TSMOM strategies can front-run.

---

## Known Failure Modes

**Whipsaws in ranging markets.** When price oscillates without trend, TSMOM generates frequent signal reversals and losses. Low-volatility, range-bound regimes (2014–2016, 2017) produce the worst drawdowns.

**Crowding during unwinds.** When many CTAs hold similar positions and sentiment shifts, the unwind is simultaneous. CTA positioning data (COT reports) can detect this risk — see `/flow-analyst`.

**Post-2009 alpha decay.** The edge has partially eroded as the strategy became crowded. Rolling Sharpe ratios post-2009 are materially lower than the historical record. Monitor with `/decay-tracker`.

**Parameter overfitting.** The 12-1 lookback is published and validated. Adding lookback optimization to the backtest will inflate in-sample Sharpe significantly with no live benefit. Use fixed lookback.

---

## Capacity Ceiling

Square-root market impact model at 1% ADV:

| AUM | Estimated Slippage Drag |
|-----|------------------------|
| $100M | ~5 bps/year |
| $500M | ~10–15 bps/year |
| $1B | ~20–30 bps/year |
| $2B | ~40–60 bps/year |

**Ceiling estimate: $500M–$2B** depending on universe breadth.
- 10-instrument concentrated universe: ceiling ~$300–500M
- 20-instrument diversified universe: ceiling ~$750M–1.2B
- 30-instrument global futures universe: ceiling ~$1.5–2B

Beyond the ceiling, the strategy can still operate but alpha erosion from market impact is significant relative to expected return.

---

## References

- Moskowitz, T., Ooi, Y.H., & Pedersen, L.H. (2012). "Time Series Momentum." *Journal of Financial Economics*, 104(2), 228–250.
- Hurst, B., Ooi, Y.H., & Pedersen, L.H. (2017). "A Century of Evidence on Trend-Following Investing." *AQR White Paper*.
- Levine, A., & Pedersen, L.H. (2016). "Which Trend Is Your Friend?" *Financial Analysts Journal*, 72(3), 51–66.
- AQR Capital Management. "Demystifying Time-Series Momentum Strategies." AQR Insight Award Paper.
