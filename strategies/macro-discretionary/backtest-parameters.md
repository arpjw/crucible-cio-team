# Backtest Parameters — Macro Discretionary

Macro discretionary backtests are inherently fragile. Unlike systematic strategies where the backtest can be mechanically replicated, macro discretionary backtests involve reconstructing historical "decisions" from historical data — a process that almost always introduces survivorship bias, hindsight bias, and selection bias simultaneously. These requirements are designed to make that fragility explicit rather than hidden.

Use `/backtest-designer` to validate any proposed backtest. The bar for approval is higher here than for TSMOM or carry.

---

## Fundamental Problem with Macro Discretionary Backtests

Before specifying parameters, acknowledge the problem:

**Macro discretionary position decisions cannot be reliably backtested.** The signal that caused the PM to make a decision in real time (a Bloomberg headline, a Fed speech, a private conversation with an economist) is not fully recoverable from historical data. Any backtest of a discretionary strategy is necessarily a reconstruction, not a replication.

The appropriate uses of a macro discretionary backtest:
1. **Regime-conditional performance attribution:** How does the strategy *type* (e.g., long duration in easing cycles) perform across macro regimes?
2. **Analog period analysis:** What happened to this specific asset class during past historical periods with similar macro conditions?
3. **Signal hypothesis testing:** Does a specific quantifiable signal (yield curve slope, COT positioning) have predictive value?

The inappropriate use: claiming a smooth backtest equity curve represents what the strategy would have returned, because it doesn't.

---

## Walk-Forward Optimization Only

**No full-sample parameter fitting is permitted.**

Any parameter in the strategy model — lookback windows, regime thresholds, position size scaling — must be fit on historical data only up to the point of the "decision," then tested forward. This is walk-forward optimization and it produces much messier, less impressive results than full-sample fitting — which is exactly the point.

**Implementation:**
- Fit regime classifier parameters on data through 2010; test on 2010–2015; refit on 2010–2015; test on 2015–2020; etc.
- Never fit a parameter on the full sample and then report in-sample performance as if it were predictive
- If the walk-forward results are much worse than full-sample results, that gap is the overfitting penalty — it must be disclosed

---

## Regime-by-Regime Performance Attribution

Aggregate Sharpe ratio for a macro discretionary strategy is not informative. Required attribution:

| Regime State | Required Metrics |
|-------------|-----------------|
| Each of the four growth states | Annualized return, vol, Sharpe, max drawdown, number of periods |
| Each of the four inflation states | Same metrics |
| Risk-on vs. Risk-off | Same metrics |
| Tightening vs. Easing | Same metrics |

**If the strategy shows positive Sharpe across all regime combinations, it is almost certainly an artifact of backtest construction.** Macro strategies have regime-dependent returns; a strategy that works in all regimes simultaneously is either diversified to the point of having no edge, or the backtest is wrong.

---

## Minimum Macro Cycle Coverage

**Minimum 3 independent macro cycles in sample.**

A "macro cycle" is defined as a full peak-to-trough-to-peak in the economic growth cycle (typically 5–10 years in length). Three independent cycles provides a sample large enough to make limited statistical inferences about regime-conditional performance.

At 25-year lookback, most strategies will have approximately 3 full cycles. Do not attempt macro discretionary backtesting with less than 20 years of data.

**Required cycles for US macro strategies:**
1. 1995–2002 (late-cycle boom, tech bust, recession, recovery)
2. 2002–2009 (housing boom, GFC, acute crisis)
3. 2009–2020 (long expansion, COVID shock)
4. 2020–present (COVID recovery, inflation, rates normalization)

---

## Analog Period Analysis

For macro discretionary, historical analog analysis is more valuable than a single long backtest — but only if done rigorously. Requirements:

**For each proposed macro thesis, run analog period analysis:**

1. Define the macro conditions of the current regime (e.g., "Inflation decelerating from peak, Fed beginning to ease, growth slowing but not contracting")
2. Find all historical periods that match on at least 3 of the 4 regime dimensions (growth, inflation, policy, risk appetite)
3. Document performance of the proposed trade in each analog period
4. Compute average, minimum, and maximum return across analogs
5. If there are fewer than 3 analog periods, explicitly state this limitation — statistical inference is not valid

**Red flag:** If the analog analysis only includes periods where the trade worked, it is not analysis — it is confirmation bias.

---

## Red Flags Unique to Macro Discretionary

The following characteristics in a backtest should trigger immediate rejection from `/backtest-designer`:

### 1. Smooth Equity Curve

Real macro strategies have lumpy, irregular returns. Monthly returns cluster around a few big hits and many small losses. If a macro discretionary backtest shows a smooth equity curve with consistent small monthly gains, the backtest is constructed from a signal that can be mechanically fitted to the data — not from the discretionary decision process the PM describes.

Acceptable: high month-to-month return variance, concentrated gains in specific regime transitions.
Red flag: smooth, consistent upward slope with Sharpe > 1.5 and max monthly loss < 1.5%.

### 2. High Sharpe Ratio Without Economic Mechanism

A macro backtest that produces Sharpe > 1.0 without a clearly stated economic mechanism for why this regime-based strategy should work is almost certainly overfitted. The mechanism must be stated first (before seeing the backtest results) and must be testable.

Acceptable: "We expect long duration to outperform in Easing cycles because falling rates benefit bond prices — and the backtest confirms this mechanism produces X% per cycle on average."
Red flag: "We tested many parameters and found this combination produced Sharpe 1.2."

### 3. No Drawdowns During Known Stress Periods

If the backtest shows the strategy performing well during 2008, 2020, and 2022 simultaneously, something is wrong. Real macro strategies have specific regimes where they work and regimes where they do not. A strategy that avoids drawdown in all three crisis periods has either found a genuine holy grail (extremely unlikely) or has been fitted to avoid exactly those periods.

### 4. Transaction Costs Not Applied or Estimated Below 2 Bps

Macro discretionary strategies with event-driven components can have variable turnover — some periods require rapid repositioning. Transaction costs must be applied at actual trade frequency, not averaged. For OTC instruments, spread costs must be estimated from prime broker quotes, not Bloomberg mid-price.

---

## Backtest Approval Checklist

Before submitting to `/backtest-designer`:

- [ ] Walk-forward optimization methodology documented (no full-sample fitting)
- [ ] Regime-by-regime performance attribution table complete
- [ ] Minimum 3 full macro cycles in sample (minimum 20-year lookback)
- [ ] Analog period analysis run for each primary thesis; minimum 3 analogs or limitation explicitly stated
- [ ] Transaction costs applied at actual trade frequency
- [ ] T+1 open execution assumed for listed instruments (never same-day at signal price)
- [ ] OTC instrument costs estimated from prime broker spreads, not mid-price
- [ ] In-sample vs. out-of-sample results reported separately
- [ ] Red flags section reviewed — no smooth equity curve, no high Sharpe without mechanism
- [ ] Economic mechanism for each regime thesis stated in advance of results
- [ ] Drawdown during all four labeled crisis periods documented
- [ ] Correlation to equities, rates, and other factor exposures computed and disclosed
- [ ] Limitations of the backtest explicitly stated in a separate "Limitations" section

A macro discretionary backtest with an explicit Limitations section that honestly describes what it can and cannot tell you is more credible, not less. The goal is not a convincing backtest — it is a honest one.
