# Risk Limits — Carry (Template)

> Pre-filled risk limits appropriate for a multi-asset carry strategy. Carry crashes are sharper and faster than TSMOM drawdowns — limits are tighter accordingly. Copy to `context/risk-limits.md` and adjust to your specific fund parameters.

---

## Portfolio-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Target annualized volatility | 10% | 12% | Lower vol than TSMOM — carry crashes amplify with leverage |
| Maximum drawdown from HWM | 12% | 15% | Carry crashes are fast — tight limit needed |
| Gross leverage | 3.2× NAV | 4.0× NAV | Carry positions are small individually but aggregate leverage can be high |
| Net leverage | 1.6× NAV | 2.0× NAV | Long carry vs. short funding |
| VaR (95%, 1-day, historical) | 1.2% NAV | 1.5% NAV | Tighter than TSMOM — crash risk is left-tail concentrated |
| VaR (99%, 1-day, historical) | 2.0% NAV | 2.5% NAV | Critical to monitor — 99% VaR expands sharply before crashes |
| Expected shortfall (CVaR 95%) | 1.8% NAV | 2.2% NAV | ES/CVaR is the most relevant metric for carry |

---

## Instrument-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Single currency pair — % NAV | 2.4% | 3.0% | More concentrated than TSMOM limit warrants; carry positions are correlated |
| Single rates instrument — % NAV | 4% | 5% | Rates carry is more liquid; slightly higher limit |
| Single commodity carry position — % NAV | 2% | 2.5% | Commodity carry has jump risk at roll |
| EM FX total exposure | 6.4% | 8.0% | Combined gross EM FX across all pairs |
| Single asset class gross exposure | 40% | 50% | FX, rates, or commodity total |

---

## Drawdown Thresholds and Actions

| Drawdown Level | Status | Required Action |
|---------------|--------|-----------------|
| < 5% | NORMAL | No action |
| 5–8% | MONITOR | Daily P&L review, review which positions are driving loss |
| 8–12% | WARN | Reduce gross leverage by 25%, identify if crash scenario is developing |
| 12–15% | SUSPEND | Reduce to 50% position size immediately, investor notification required, convene risk committee |
| > 15% | HALT | Liquidate all positions to cash; carry crashes can go to -30% rapidly once momentum is established |

**Critical note on carry crash velocity:** Carry crashes happen faster than TSMOM drawdowns. The transition from WARN to HALT can occur in 2–3 days. The drawdown monitoring frequency is daily at all levels; at 8%+ drawdown, monitor intraday.

---

## Carry Crash Detection Signals

Monitor these leading indicators separately from the drawdown metric. If two or more are triggered simultaneously, treat as an early warning of a developing crash and reduce to 50% gross exposure preemptively:

| Signal | Threshold | Notes |
|--------|-----------|-------|
| VIX level | > 25 | Carry begins to underperform at VIX > 20; > 25 is the danger zone |
| VIX 5-day change | > 8 points | Rapid VIX spike is a better indicator than level alone |
| Cross-currency basis (USD) | > 30 bps | Indicates USD funding stress — carry unwinding risk |
| EM FX implied vol (1-month) | +50% vs. 30d avg | EM carry positions are at risk |
| JPY strengthening | > 3% in 5 days | AUD/JPY and similar EM vs. JPY pairs are classic carry trades; rapid JPY strength signals unwind |

---

## Correlation-Based Limits

Carry's key risk is that positions become correlated during stress. Monitor and limit:

| Metric | Soft Warning | Hard Limit |
|--------|-------------|------------|
| Average pairwise ρ across all positions (rolling 60d) | 0.35 | 0.5 |
| Max pairwise ρ between any two large positions | 0.6 | 0.75 |
| Estimated portfolio ρ to S&P 500 (rolling 90d) | 0.3 | 0.4 |

If average pairwise correlation exceeds the soft warning, reduce total gross exposure by 20% until correlation normalizes. Carry strategy diversification is an illusion if correlations are elevated.

---

## Volatility Regime Adjustments

| Realized 20-day Portfolio Vol | Position Scale Factor |
|------------------------------|----------------------|
| < 6% | 1.3× (scale up, max 1.3) |
| 6–10% | 1.0× (target) |
| 10–12% | 0.8× |
| 12–15% | 0.6× |
| > 15% | 0.4× (floor) |

Scale-down happens faster than for TSMOM because carry has less regime persistence — once volatility spikes, carry losses can compound rapidly.

---

## Roll and Liquidity Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| FX forward maturity | Maximum 3 months | Longer maturities reduce flexibility to reduce position |
| FX futures roll | Begin 15 days before expiry | FX futures roll is cheap; do it early |
| Commodity roll — begin | 20 days before FND | Earlier than TSMOM because carry signal itself changes at roll |
| Minimum ADV for EM FX instrument | $200M | Reduce to zero if below threshold |

---

## Margin and Cash Requirements

| Metric | Minimum | Target | Notes |
|--------|---------|--------|-------|
| Cash buffer above initial margin | 25% of initial margin | 40% | Higher buffer than TSMOM — carry crashes require margin |
| Unencumbered cash / T-bills | 35% NAV | 45% NAV | Carry portfolios need more dry powder for crash scenarios |
| Maximum margin utilization | 80% | 65% | More conservative than TSMOM |

---

## Limit Review Schedule

- **Daily:** Drawdown from HWM, VIX level, carry crash detection signals, EM FX exposure
- **Weekly:** Portfolio VaR, correlation matrix, gross leverage, vol regime
- **Monthly:** Carry signal strength review (is each position still earning positive carry?), EM FX liquidity check
- **Quarterly:** Full risk limit review, capacity review, correlation regime assessment
