# Carry — Strategy Overview

## What It Is

Carry strategies earn the return from "rolling down the yield curve" or holding higher-yielding assets funded by lower-yielding ones. The core insight: across asset classes, instruments with a higher implied forward return (the "carry") tend to outperform lower-carry instruments over time, after controlling for other risk factors.

Carry is not a single signal — it is a family of signals that share a common mechanism but differ in implementation across asset classes.

---

## Signal Construction by Asset Class

### FX Carry

**Signal:** Interest rate differential between two currencies.

```
Carry(i) = r_i - r_base
```

Where `r_i` is the overnight/short-term rate in currency i, and `r_base` is the funding currency rate (typically USD or a basket). Go long high-yielding currencies, short low-yielding ones.

**Covered Interest Parity (CIP) Deviation as signal:** When forward rates deviate from the no-arbitrage CIP relationship, it indicates a compensated risk premium rather than pure arbitrage. A persistent CIP deviation is a more reliable carry signal than the raw interest rate differential because it has already been arbitraged away by banks — what remains is genuine risk premium.

**Implementation:** Use currency futures or FX forwards. Futures-based implementation avoids counterparty risk but requires rolling. Forward-based implementation incurs counterparty risk with the prime broker.

**Universe:** G10 FX minimum. EM FX carry offers higher yields but significantly higher drawdown risk (sudden devaluations). EM carry should not exceed 20% of the FX carry allocation.

### Rates Carry

**Signal:** Yield curve slope and roll-down return.

```
Carry(maturity) = y_long - y_short (slope)
Roll_down(maturity) = y_long - y_{long - 1 year} (roll-down as bond ages)
```

Go long the part of the yield curve with the highest carry (slope × roll-down combined). In a normal upward-sloping curve, this means being long the belly (5–10 year) relative to short duration funding.

**Implementation:** Treasury futures (ZN, ZB, ZF, ZT) for US rates; Bund/Bobl/Schatz for European rates; JGB for Japan. Each market's curve has different carry dynamics.

**Current regime consideration:** Flat or inverted yield curves dramatically reduce rates carry. In inverted curve environments (2022–2023 US rates), the carry signal is negative — the strategy should be underweight rates carry during inversions.

### Commodity Carry

**Signal:** Futures curve shape (backwardation vs. contango).

```
Roll_yield = (Spot_price - Futures_price) / Futures_price × (365 / days_to_expiry)
```

A positive roll yield (backwardation) means the futures price is below spot — rolling long futures earns the gap. A negative roll yield (contango) means the futures price is above spot — rolling long futures loses the gap.

**Implementation:** Go long commodities in backwardation; go short (or underweight) commodities in contango. Weight by the magnitude of the roll yield.

**Key insight:** Commodity carry has lower correlation to FX and rates carry than either have to equity beta. It is the most diversifying of the three carry components.

---

## Why the Edge Exists

**1. Compensation for crash risk.** Carry strategies earn a premium for bearing the risk of periodic sharp reversals. High-yield currencies crash during risk-off events; steep yield curves flatten in recessions; commodity backwardation collapses during supply gluts. Investors demand a return for holding these exposures through the bad times.

**2. Liquidity provision.** Carry trades involve selling volatility and providing liquidity to hedgers. Hedgers (importers, exporters, commodity producers) pay a risk premium to lock in prices; carry traders earn this premium by taking the other side.

**3. Limits to arbitrage.** Institutional constraints (funding limits, leverage restrictions, VaR limits) prevent arbitrage capital from fully eliminating carry premia. When institutional investors are constrained (2008, 2020), carry premia widen before eventually reverting.

---

## Known Failure Modes

**Carry crashes during risk-off events.** The defining failure mode: when volatility spikes and risk appetite collapses, all carry positions unwind simultaneously. 2008 FX carry crash: AUD/JPY fell 40% in 6 weeks. 2020 COVID: EM carry lost 15–20% in days. These events are correlated across asset classes — the diversification benefit across FX, rates, and commodity carry partially collapses exactly when you need it.

**Correlation spike under stress.** In normal markets, FX carry and rates carry have low correlation (~0.2–0.3). During risk-off events, correlation rises to 0.7–0.9. The stress correlation is the one that matters for tail risk management. See `/correlation-mapper`.

**Carry and equity beta are regime-dependent.** In calm markets, FX carry has low equity beta. In risk-off markets, it behaves like a leveraged equity position. This makes carry strategy performance hard to decompose from a multi-strategy portfolio perspective.

**Yield curve inversions destroy rates carry.** When the curve inverts, rates carry is negative. A strategy that mechanically holds long duration in an inverted curve environment will bleed.

---

## Capacity Ceiling

Carry capacity varies significantly by asset class:

| Component | Estimated Capacity |
|-----------|-------------------|
| G10 FX carry (futures) | $500M–1B |
| EM FX carry (futures) | $100–250M |
| US rates carry | $2B+ |
| European rates carry | $1–2B |
| Commodity carry | $200–500M |
| **Diversified multi-asset carry** | **$1–5B** |

The diversified multi-asset approach reaches the higher end because the asset classes have different liquidity profiles. Binding constraint is typically EM FX or commodity carry at larger AUM.

---

## References

- Koijen, R.S.J., Moskowitz, T.J., Pedersen, L.H., & Vrugt, E.B. (2018). "Carry." *Journal of Financial Economics*, 127(2), 197–225.
- Brunnermeier, M.K., Nagel, S., & Pedersen, L.H. (2008). "Carry Trades and Currency Crashes." *NBER Macroeconomics Annual*, 23, 313–347.
- Fama, E.F. (1984). "Forward and spot exchange rates." *Journal of Monetary Economics*, 14(3), 319–338.
- Gorton, G.B., & Rouwenhorst, K.G. (2006). "Facts and Fantasies about Commodity Futures." *Financial Analysts Journal*, 62(2), 47–68.
