# Risk Limits — Time-Series Momentum (Template)

> Pre-filled risk limits appropriate for a TSMOM strategy. Soft warnings trigger at 80% of each hard limit. Copy to `context/risk-limits.md` and adjust to your specific fund parameters.

---

## Portfolio-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Target annualized volatility | 15% | 20% | Increase position sizes only up to hard limit |
| Maximum drawdown from HWM | 20% | 25% | HALT at hard limit — see halt protocol |
| Gross leverage | 2.4× NAV | 3.0× NAV | Notional futures exposure / NAV |
| Net leverage | 1.6× NAV | 2.0× NAV | Long exposure minus short exposure / NAV |
| VaR (95%, 1-day, historical) | 1.6% NAV | 2.0% NAV | Based on 252-day rolling window |
| VaR (99%, 1-day, historical) | 2.4% NAV | 3.0% NAV | Tail risk check |
| Expected shortfall (CVaR 95%) | 2.4% NAV | 3.0% NAV | Average loss beyond VaR |

---

## Instrument-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Single instrument — % NAV | 4% | 5% | Notional exposure |
| Single instrument — % ADV | 8% | 10% | Order size as % of avg daily volume |
| Single sector (equity indices) | 16% | 20% | Combined gross exposure |
| Single asset class | 32% | 40% | E.g., combined FX exposure |
| Correlated pair (ρ > 0.8) | — | 8% combined | Both positions combined |

---

## Drawdown Thresholds and Actions

| Drawdown Level | Status | Required Action |
|---------------|--------|-----------------|
| < 10% | NORMAL | No action |
| 10–15% | MONITOR | Daily P&L review, notify IB |
| 15–20% | WARN | Reduce gross leverage by 20%, CIO review |
| 20–25% | SUSPEND | Reduce to 50% position size, investor notification required |
| > 25% | HALT | Liquidate to cash, convene risk committee within 24 hours |

Drawdown measured from most recent NAV high-water mark, not inception.

---

## Volatility Regime Adjustments

TSMOM uses dynamic position sizing. When realized portfolio volatility exceeds targets, positions are automatically scaled down. Manual override requires CIO sign-off.

| Realized 20-day Vol | Position Scale Factor |
|--------------------|-----------------------|
| < 10% | 1.5× (scale up, max 1.5) |
| 10–15% | 1.0× (target) |
| 15–20% | 0.75× |
| 20–25% | 0.6× |
| > 25% | 0.5× (floor) |

---

## Roll and Liquidity Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| Front-month roll — begin rolling | 30 days before FND | Earlier for illiquid contracts |
| Maximum OI in expiring contract | 20% of open interest | Must roll if above this level |
| Roll cost alert | 120% of 30-day average | Flag to PM, log reason if proceeding |
| Illiquid instrument hold limit | 2% NAV | Instruments falling below $50M ADV |

---

## Concentration and Correlation Limits

| Scenario | Limit |
|----------|-------|
| Maximum instruments in single country | 4 |
| Maximum instruments correlated > 0.7 in portfolio | 6 (in aggregate) |
| Maximum instruments in one sector with same signal direction | 5 |

---

## Margin and Cash Requirements

| Metric | Minimum | Target | Notes |
|--------|---------|--------|-------|
| Cash buffer above initial margin | 20% of initial margin | 35% | Cushion for adverse moves |
| Unencumbered cash / T-bills | 30% NAV | 40% NAV | Available for margin calls |
| Maximum margin utilization | 85% | 70% | Of prime broker credit facility |

---

## Soft Warning Protocol

When any metric crosses the soft warning threshold:
1. Automated alert generated and logged to audit record
2. PM notified within 1 business hour
3. PM must acknowledge alert in writing (email or audit log entry)
4. If metric not back below soft warning within 3 business days, hard limit response procedures begin

---

## Limit Review Schedule

- **Daily:** VaR, drawdown from HWM, margin utilization
- **Weekly:** Gross leverage, instrument concentration, vol regime check
- **Monthly:** Correlation matrix, sector concentrations, ADV liquidity check for all instruments
- **Quarterly:** Full risk limit review — adjust if AUM, instrument universe, or market structure has materially changed
