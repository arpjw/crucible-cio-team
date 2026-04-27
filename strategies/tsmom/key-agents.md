# Key Crucible Agents — Time-Series Momentum

Not all agents are equally relevant to every strategy. For TSMOM, five agents provide the highest signal-to-noise ratio. Run these first; add others when the pipeline flags a specific concern.

---

## Priority 1 — Run on Every Signal Review

### `/signal-researcher` — Trend Signal Validity

TSMOM has well-documented failure modes that look-ahead bias and overfitting errors frequently mask. The signal researcher is the primary defense.

**What to check for TSMOM specifically:**

- **Look-ahead bias in return calculation.** The 1-month skip is critical. Many implementations accidentally include the most recent month, which introduces a reversal effect that partially offsets the real signal. Ask the agent to verify the exact index dates used in the return calculation.
- **Survivorship bias in the instrument universe.** Futures contracts that failed or became illiquid are often excluded from historical data by default. This inflates the apparent Sharpe ratio. Confirm the universe definition is point-in-time.
- **Transaction cost contamination.** Backtests that use mid-price execution without explicit transaction costs are unreliable. Verify 2 bps minimum cost per side is applied.
- **Lookback overfitting.** The 12-1 lookback is the published, validated specification. If the backtest tests multiple lookbacks and selects the best, the in-sample result is inflated. One lookback, fixed.

**Parameters to specify when invoking:**
```
/signal Long [instrument] — TSMOM 12-1 signal, weekly rebalancing, vol-scaled sizing
```

---

### `/decay-tracker` — Live Signal Health

TSMOM edge has documented post-2009 decay. The strategy went from ~0.8 Sharpe (pre-2009 full-sample) to ~0.3–0.5 Sharpe in live trading post-2009 as the strategy became crowded. Monitoring live vs. backtest performance divergence is mandatory.

**What to watch for TSMOM specifically:**

- **Decay classification:** TSMOM typically shows **gradual linear decay** in Sharpe since 2009, not episodic decay. Exponential decay would be a more serious signal to investigate capacity and crowding.
- **Regime-conditional decay:** Decay is concentrated in low-vol range-bound regimes (2014–2016, 2017, parts of 2021). Check if decay is regime-specific or broad-based — regime-specific decay is manageable; broad-based decay suggests structural erosion.
- **Health score threshold for action:** Below 60/100 on the decay tracker's health score, consider reducing position sizes by 25–50% until health recovers. Below 40/100, escalate to CIO for strategy review.

**Parameters to specify:**
```
/decay-tracker TSMOM 12-1 signal, review past 12 months live vs. backtest
```

---

## Priority 2 — Run Before Sizing Up or Adding Instruments

### `/regime-classifier` — Current Regime State

TSMOM performance is highly regime-dependent. Before entering a new position or increasing gross leverage, confirm the current regime.

**TSMOM regime performance map:**

| Regime | TSMOM Expected Performance | Action |
|--------|---------------------------|--------|
| Trending + elevated vol | Excellent — full size | Normal operation |
| Trending + low vol | Good — full size | Normal operation |
| Range-bound + low vol | Poor — worst case for TSMOM | Reduce size 25–50% |
| Crisis / high vol spike | Mixed — initially good, reversal risk | Tight stop, monitor daily |
| Post-crisis recovery | Very poor — V-shaped reversals destroy TSMOM | Reduce size significantly |

**Decision rule:** If the regime classifier returns `RANGE_BOUND` with confidence > 60%, reduce gross exposure by 30% before executing new TSMOM signals. Document the override in the audit log if proceeding at full size.

**Parameters to specify:**
```
/regime-classifier — looking for TSMOM regime compatibility check
```

---

### `/flow-analyst` — COT Positioning and Crowding

TSMOM is a crowded strategy. When systematic funds all hold similar positions, unwinds are simultaneous and violent. COT data reveals when this risk is elevated.

**What to watch for TSMOM specifically:**

- **Net positioning percentile > 90th:** All systematic funds are long this instrument in the same direction as the TSMOM signal. Crowding risk is high — the instrument is susceptible to a momentum crash if any macro catalyst triggers concurrent liquidation.
- **OI rate-of-change:** Rapid increase in open interest confirms new money entering the trend. Rapid decline confirms early unwind — consider tightening stop or reducing position ahead of potential cascade.
- **Squeeze severity > 2 ATR:** Signals that a reversal is underway that is large enough to force systematic stops. In this case, TSMOM signal may be about to flip short; wait for the signal to confirm rather than adding to the losing direction.

**Crowding alert thresholds for TSMOM:**
- COT net percentile > 85th: ELEVATED — reduce position by 20%
- COT net percentile > 95th: CROWDED — reduce position by 40% regardless of signal strength

---

### `/roll-manager` — Futures Roll Cost Management

TSMOM rebalances weekly, which generates significant futures roll turnover. Roll costs compound over time and are one of the primary drags on realized vs. backtest returns.

**What to watch for TSMOM specifically:**

- **Roll cost vs. annualized backtest assumption.** If live roll costs exceed the 2 bps/side assumption, the strategy's net return will underperform. Flag any instrument where average roll cost exceeds 3 bps/side.
- **OI migration timing.** For high-turnover strategies, rolling too early wastes capital in the less liquid contract; rolling too late risks holding through delivery. TSMOM should initiate roll when OI in the expiring contract drops below 40% of peak (not the 20% floor the roll manager uses as the default hard trigger).
- **Contango vs. backwardation affect on carry.** Roll costs in contango markets erode TSMOM returns in commodity futures specifically. If a commodity is in steep contango, the trend signal must be proportionally stronger to justify the position after roll costs.

**Recommended roll schedule for TSMOM:**
```
/roll-manager — weekly roll review, flag any instrument where roll cost > 3 bps/side or OI in expiry < 40%
```

---

## Secondary Agents (Use When Flagged by Pipeline)

- **`/risk`** — Run when gross leverage approaches 2.4× or drawdown exceeds 10%. TSMOM's leverage is normally well-controlled by the vol-scaling mechanism; manual review is only needed at extremes.
- **`/compliance`** — Run when adding new instruments (confirm instrument-level permissions in mandate) or crossing $100M AUM (review reporting thresholds).
- **`/correlation-mapper`** — Run quarterly or when adding more than 2 new instruments. Correlation between TSMOM positions spikes during crises — routine review prevents silent concentration buildup.
- **`/capacity-estimator`** — Run when AUM doubles or when adding instruments below the $100M ADV threshold. Capacity ceiling review at $250M, $500M, $1B.
