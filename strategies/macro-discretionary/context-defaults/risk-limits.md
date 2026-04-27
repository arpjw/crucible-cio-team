# Risk Limits — Macro Discretionary (Template)

> Pre-filled risk limits for a macro discretionary strategy. Macro discretionary runs higher single-position concentration than systematic strategies — this is intentional and part of the strategy. Limits reflect that profile. Copy to `context/risk-limits.md` and adjust to your specific fund parameters.

---

## Portfolio-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Target annualized volatility | 12% | 18% | Variable by regime — higher in high-conviction environments |
| Maximum drawdown from HWM | 16% | 20% | Tighter ceiling than TSMOM vol would suggest due to concentration |
| Gross leverage | 1.6× NAV | 2.0× NAV | Much lower than systematic strategies — macro positions are concentrated |
| Net leverage | 1.2× NAV | 1.5× NAV | Higher net directional exposure expected vs. systematic |
| VaR (95%, 1-day, historical) | 2.0% NAV | 2.5% NAV | Higher than carry; macro positions have fatter tails |
| VaR (99%, 1-day, historical) | 3.0% NAV | 3.5% NAV | |
| Expected shortfall (CVaR 95%) | 2.5% NAV | 3.0% NAV | |
| Number of active themes | 5 | 8 | Macro funds that spread too thin lose the edge of concentrated conviction |

---

## Instrument-Level Limits

| Metric | Soft Warning | Hard Limit | Notes |
|--------|-------------|------------|-------|
| Single instrument — % NAV | 6.4% | 8.0% | Higher concentration is part of the strategy |
| Single macro theme (multiple instruments) | 12% | 15% | Theme-level limit; all instruments expressing same thesis count together |
| EM exposure — total gross | 16% | 20% | Higher jump risk in EM |
| Single EM position | 4% | 5% | EM positions have sharper tails |
| VIX futures — % NAV | 1.6% | 2.0% | Vol is a separate tool; limit prevents it from becoming the portfolio |
| OTC derivatives notional — % NAV | 32% | 40% | OTC positions have less operational oversight; cap accordingly |
| Options (net premium at risk) | — | 3% NAV | Maximum total premium at risk for long option positions |

---

## Drawdown Thresholds and Actions

| Drawdown Level | Status | Required Action |
|---------------|--------|-----------------|
| < 8% | NORMAL | No action |
| 8–12% | MONITOR | Daily review of all positions; identify which themes are driving loss |
| 12–16% | WARN | Reduce gross leverage by 30%; all new positions require dual approval (PM + Risk Officer); investor notice |
| 16–20% | SUSPEND | Reduce to 50% gross exposure; convene risk committee; no new positions without committee approval |
| > 20% | HALT | Liquidate all positions to cash; board-level review required before re-entry |

---

## Event Risk Protocol

Macro discretionary funds are specifically exposed to scheduled events. Before each high-impact event:

| Event Type | Required Action | Timing |
|-----------|----------------|--------|
| FOMC rate decision | Review all rates, FX, and equity positions — reduce by 30% if near high-conviction entry | 3 business days prior |
| CPI / PCE print | Review inflation-sensitive positions; document expected outcome vs. current pricing | 2 business days prior |
| NFP report | Review USD-sensitive positions | 2 business days prior |
| Central bank speeches (Chair/President) | No new positions in affected markets on same day | Day of event |
| Elections (any G7 country) | All positions in that country's assets subject to 50% size cap until result | 1 week prior |
| Geopolitical events (acute) | Immediate CIO review of all EM and commodity positions | Within 4 hours of event |

The `/event-calendar` agent provides the 30-day forward schedule and sizing recommendations. Run it weekly.

---

## Concentration Limits

| Concentration Type | Soft Warning | Hard Limit |
|-------------------|-------------|------------|
| Single country gross exposure | 16% | 20% |
| Single asset class | 40% | 50% |
| Duration risk (DV01 × rate change) | 1.2% NAV per 25 bps | 1.5% NAV per 25 bps |
| FX exposure (USD equivalent of all non-USD) | 32% | 40% |
| Commodity gross exposure | 20% | 25% |

---

## Regime-Based Limit Adjustments

Macro discretionary limits should flex with the regime. These adjustments apply when the regime classifier provides a clear signal:

| Regime State | Adjustment |
|-------------|------------|
| RISK_OFF, high confidence (> 70%) | Reduce single position cap to 5% NAV; increase cash buffer to 30% |
| HIGH_VOL (realized vol > 25%) | Halve all position size caps; no new entries until vol normalizes below 20% |
| TRANSITION (regime classifier low confidence) | No new macro theme entries until regime clarity improves |
| RISK_ON, high confidence (> 70%), low vol | Standard limits apply; may use options to add convexity |

---

## Stop Loss Protocol

All positions must have a stop loss defined at entry and logged in the audit record. For macro discretionary, stop losses are at the theme level (not just the instrument level):

| Holding Period | Stop Loss Width |
|----------------|-----------------|
| Days (event-driven) | 0.5–1.0% NAV |
| Weeks (tactical) | 1.5–2.0% NAV |
| Months (structural) | 2.5–3.0% NAV |

**Stop loss discipline:** A stop does not automatically trigger a forced exit — it triggers a mandatory review. The PM must explicitly decide to hold through the stop. That decision must be logged with a revised invalidation condition. Holding through stops without documentation is an audit violation.

---

## Margin and Cash Requirements

| Metric | Minimum | Target | Notes |
|--------|---------|--------|-------|
| Unencumbered cash / T-bills | 40% NAV | 50% NAV | Macro funds need dry powder; cash is the option to act |
| Cash buffer above initial margin | 30% of initial margin | 50% | Macro positions can require sudden additional margin |
| OTC derivative collateral posted | Per CSA terms | Buffer: 10% above minimum | |
| Maximum margin utilization | 70% | 55% | Conservative — macro positions can move against you violently |

---

## Limit Review Schedule

- **Daily:** Drawdown from HWM, single-position size checks, event risk calendar review
- **Weekly:** Theme-level concentration, leverage, VaR, stop loss compliance review
- **Monthly:** Regime-based limit adjustment review (are limits consistent with current regime?), EM sanctions screening re-run for all active EM positions
- **Quarterly:** Full mandate review, OTC documentation audit, General Counsel review of any new instrument types
