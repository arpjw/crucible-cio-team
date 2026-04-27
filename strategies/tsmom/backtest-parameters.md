# Backtest Parameters — Time-Series Momentum

A backtest specification checklist for TSMOM strategies. Use `/backtest-designer` to validate any backtest against these requirements before trusting the results.

---

## Required Lookback Period

**Minimum: 20 years.**

The following crisis periods must be included in-sample:

| Period | Why It Must Be Included |
|--------|------------------------|
| 2000–2002 (dot-com bust) | Large equity short positions — TSMOM performs well; validates the mechanism |
| 2007–2009 (GFC) | TSMOM's best historical period; also tests commodity roll behavior at extreme vol |
| 2013 (Taper Tantrum) | Short-duration rates reversal — tests whipsaw loss behavior |
| 2015–2016 (China/oil rout) | Range-bound commodity environment — stress period for TSMOM |
| 2018 Q4 (equity selloff) | Tests mixed-signal environment |
| 2020 (COVID crash and V-recovery) | V-shaped recovery is TSMOM's worst-case scenario — mandatory inclusion |
| 2022 (rates/equity correlation breakdown) | Unusual regime where both stocks and bonds sold off simultaneously |

A backtest with data only from 2010 onward will show artificially low volatility and will miss the most important validation period (2008) and the most damaging failure mode (2020 recovery).

---

## Signal Variants to Test

Test the following specifications and report results separately — do not average or select the best:

| Variant | Specification | Purpose |
|---------|---------------|---------|
| 12-1 binary | `sign(r_{t-12, t-1})` | Canonical published specification |
| 3-12 | `sign(r_{t-12, t-3})` | Shorter lookback; less crisis exposure |
| EWMA (λ=63d) | EWMA signal, 63-day span | Faster response, higher turnover |
| EWMA (λ=126d) | EWMA signal, 126-day span | Balanced speed vs. stability |

**Decision rule:** The 12-1 binary specification is the default. Any other variant must produce a Sharpe ratio within 0.1 of the 12-1 specification during the out-of-sample period, or it will not be approved. Selecting a variant because it performed better in-sample is overfitting.

---

## Transaction Cost Model

Apply transaction costs at each rebalancing event. Costs must be applied **before** computing performance metrics.

| Cost Component | Minimum Assumption | Notes |
|---------------|-------------------|-------|
| Commission | 1 bp per side | Exchange fees + clearing |
| Bid-ask spread | 1 bp per side | Liquid futures; larger for EM |
| Market impact | Size-dependent | Use square-root model for positions > 1% ADV |
| Total baseline | **2 bps per side** | Minimum acceptable assumption |

For backtests at simulated AUM above $200M, apply market impact scaling using:
```
Impact(bps) = 0.5 × σ_daily × sqrt(trade_size / ADV)
```

Any backtest using zero transaction costs or "approximate" costs below 1 bp/side will be rejected by `/backtest-designer`.

---

## Slippage Assumption

For realistic execution modeling:

```
Slippage = 1 ATR per 10% ADV participation rate
```

Where ATR is the 20-day Average True Range of the instrument. This scales linearly — a trade representing 5% of ADV incurs 0.5 ATR of slippage.

For the canonical backtest, assume execution at T+1 open (trade is signaled at close, executed next open). Never assume same-day execution at signal price.

---

## Out-of-Sample Holdout

**Holdout period: 2018–present.**

The in-sample period for parameter estimation ends December 31, 2017. The signal lookback (12-1) is fixed and was published before 2018; it does not require fitting. However, any secondary parameters (vol estimation window, rebalancing frequency, position size multiplier) must be fixed on data through 2017 only.

Report in-sample Sharpe and out-of-sample Sharpe separately. If out-of-sample Sharpe is below 0.3 (after costs), the backtest fails — do not scale up into a strategy that is not working live.

---

## Benchmark

**Primary benchmark: SG Trend Index** (publicly available, replicates the aggregate performance of the largest CTA trend funds).

Report the following relative to the SG Trend Index:
- Annualized alpha (after costs)
- Correlation to index
- Maximum drawdown vs. index drawdown at the same time

If the backtest cannot meaningfully beat the SG Trend Index, the strategy is replicating what can be accessed via a managed-account platform at lower cost and fee. A correlation > 0.85 to the SG Trend Index with no measurable alpha is insufficient justification for launching as a standalone fund.

Secondary benchmark: MSCI World (to verify the negative equity correlation claim).

---

## Known Data Pitfalls

### Survivorship Bias in Futures Contracts

Futures contracts that became illiquid, had delivery failures, or were delisted are often excluded from commercial data providers' continuous back-adjusted price series. This creates survivorship bias — you only see the instruments that survived.

**Mitigation:** Document the exact data provider and methodology for handling delisted contracts. Preferred approach: maintain an explicit universe that includes historically-available contracts even if they are no longer trading.

### Back-Adjustment Method Materially Affects Results

The three common methods for creating continuous futures price series produce meaningfully different TSMOM signals:

| Method | Effect on TSMOM |
|--------|-----------------|
| Panama (add/subtract roll gap) | Introduces artificial trends; inflates momentum signal strength |
| Ratio adjustment (multiply by roll ratio) | More accurate price levels; removes artificial carry |
| Raw (use nearby only, splice at roll) | Cleanest but creates large price gaps at splices |

**Recommended:** Ratio adjustment for signal calculation. Panama method will overstate TSMOM returns — if your backtest uses Panama adjustment, results must be treated with skepticism until verified with ratio adjustment.

### Volatility Estimation Window Choice

The position sizing formula uses realized volatility. The estimation window significantly affects position stability:
- 20-day window: Reactive, high turnover, position sizes swing widely
- 60-day window: Stable, lower turnover, slower to respond to vol regime changes
- 252-day window: Very stable, but lags vol regime changes by up to a year

**Recommended:** 60-day exponentially weighted volatility for live trading. Do not fit this parameter to the backtest.

---

## Backtest Approval Checklist

Before submitting to `/backtest-designer`, confirm:

- [ ] Data covers 2000–present (minimum)
- [ ] All five crisis periods listed above are in-sample
- [ ] Transaction costs ≥ 2 bps per side applied
- [ ] T+1 open execution assumed (not same-day)
- [ ] Back-adjustment method documented (ratio preferred)
- [ ] Survivorship bias mitigation documented
- [ ] Lookback fixed at 12-1 (or justified alternative with prior approval)
- [ ] Out-of-sample holdout from 2018 onward
- [ ] Results reported vs. SG Trend Index benchmark
- [ ] In-sample and out-of-sample Sharpe reported separately
