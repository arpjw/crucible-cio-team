# Macro Discretionary — Strategy Overview

## What It Is

Systematic macro discretionary combines a structured analytical framework with judgment-based position decisions. The "systematic" component is the regime identification process and the pre-trade decision protocol — not the positions themselves. Every trade must pass through a documented checklist before execution. The PM retains discretion on whether and how to trade; the system enforces that the reasoning is explicit and falsifiable.

The word "discretionary" does not mean unconstrained. It means the position decisions are not mechanically derived from a single signal — they integrate multiple signals and qualitative judgment. The system's job is to make that judgment auditable.

---

## Strategy Architecture

### Layer 1 — Regime Identification

The regime framework classifies the macro environment along four dimensions:

| Dimension | States |
|-----------|--------|
| Growth | Expansion / Slowdown / Contraction / Recovery |
| Inflation | Accelerating / Stable / Decelerating / Deflationary |
| Policy | Tightening / Neutral / Easing |
| Risk appetite | Risk-on / Transitioning / Risk-off |

The four-dimension composite determines which asset classes have positive expected carry, which trends are likely to persist, and which hedges are most cost-effective. See `/regime-classifier` for the full specification.

**Key principle:** Every position must be stated in terms of a regime thesis. "I am long gold because I think it will go up" is not a valid thesis. "I am long gold because the regime is Slowdown + Decelerating inflation + Easing policy, which has historically been gold's best macro environment" is a valid thesis.

### Layer 2 — Signal Stack

Macro discretionary uses a hierarchy of signal types, weighted by conviction:

**Structural signals (highest conviction, slowest-moving):**
- FRED macro indicators: unemployment, ISM, CPI, yield curve slope, credit spreads
- Central bank balance sheet trends
- Long-cycle debt dynamics (Dalio-style debt cycle positioning)
- Cross-country growth differential

**Event-driven signals (medium conviction, medium speed):**
- FOMC meetings and communications — assess whether the Fed is ahead of or behind the curve
- CPI surprises — inflation print vs. expectation, not just level
- GDP revisions — often have more information than the initial print
- Geopolitical events — regime-relevant, not just headline-relevant

**Sentiment signals (lower conviction, fastest-moving):**
- CFTC COT positioning — crowding indicator, not directional signal
- News sentiment via `/sentiment-tracker`
- Prediction market probabilities via `/kalshi-reader`
- Survey data: AAII, BofA Global Fund Manager Survey

**Position construction:** A structural signal provides the direction and initial sizing. An event-driven signal confirms or delays entry timing. A sentiment signal adjusts size (reduce if crowded, add if contrarian). All three must be documented in the pre-trade rationale.

### Layer 3 — Falsifiability Requirements

This is the most important discipline in macro discretionary. Before entering any position, the PM must state in writing:

1. **The thesis:** What regime condition justifies this position?
2. **The entry trigger:** What specific observation prompted this to be done now rather than next week?
3. **The invalidation condition:** What would prove this thesis wrong? At what price or data point would I exit?
4. **The expected holding period:** Days, weeks, or months? (determines position sizing and stop width)
5. **The expected return and risk:** What is the target, and what is the stop?

A thesis without an invalidation condition is not a thesis — it is a hope. The `/audit-logger` enforces that all five elements are present before the order is routed.

### How to Distinguish Genuine Thesis from Post-Hoc Rationalization

Post-hoc rationalization is the primary pathology of discretionary macro funds. It produces smooth backtest curves that completely fail to predict live performance.

Indicators of a genuine thesis:
- The thesis is written down **before** the position is taken
- The invalidation condition is stated as a specific observable (price level, data print, central bank action) — not "if my view changes"
- The thesis makes a falsifiable prediction: "if my thesis is correct, 10Y yields will decline within 3 months"
- The PM has a history of sometimes being invalidated and exiting — if every trade is held to a profit, the invalidation conditions are not being enforced

Indicators of post-hoc rationalization:
- The rationale is written after price has moved in the intended direction
- The invalidation condition is vague ("if macro deteriorates further")
- The position is never reduced even when data contradicts the thesis
- The PM cannot articulate what would change their mind

---

## Capacity Ceiling

| AUM Range | Notes |
|-----------|-------|
| $0–100M | Unconstrained. The fund can express any macro view in liquid futures markets without moving prices. |
| $100M–500M | Practically unconstrained in liquid instruments. Concentrated single-country positions begin to require more careful execution. |
| $500M–1B | Liquidity limitations emerge for concentrated themes in smaller markets. EM currency and EM rates require careful execution to avoid being front-run. OTC access becomes important. |
| $1B+ | Listed futures alone are insufficient for many macro themes. Significant OTC derivatives access (swaps, options, forwards) required. Banks must be willing to take the other side. Execution becomes a primary alpha-eroding factor. |

There is no hard strategy-level capacity ceiling for macro discretionary the way TSMOM and carry have one — macro discretionary positions are more concentrated and more idiosyncratic. However, the larger the fund, the more important execution quality becomes relative to the thesis quality.

---

## Known Failure Modes

**Conviction masquerading as edge.** High conviction is not the same as being right. The most dangerous macro PMs are those who are confident and persuasive — they are also the ones who hold losing positions too long because they have narratives justifying staying in.

**Regime persistence overfitting.** Historical analog analysis ("this looks like 1994" or "this is similar to 2001") can be useful, but the number of macro cycles in any dataset is small — typically 3–5 per 20 years. Statistical inference from 3 data points is unreliable.

**Geopolitical macro trades without sanctions screening.** Macro funds are particularly exposed to sanctions risk because geopolitical macro trades often involve exposure to countries under US/EU sanctions regimes. See `/general-counsel` before entering any EM or geopolitical-driven position.

**Holding through expected-value-negative events.** Central bank decisions, elections, and geopolitical events have highly uncertain outcomes. Holding a full-size position through a binary event because "I believe the Fed will cut" is a different risk than a trending market position. Scale down before events.

---

## References

- Dalio, R. "A Template for Understanding Big Debt Crises." Bridgewater Associates.
- Soros, G. (1987). *The Alchemy of Finance*. Wiley. (Reflexivity framework)
- Druckenmiller, S. Multiple interviews on macro process. (Asymmetric bet construction)
- Bridgewater Associates. "The All Weather Story." (Regime-based portfolio construction)
- Ilmanen, A. (2011). *Expected Returns*. Wiley. (Cross-asset macro framework, Chapters 1–5)
- Kaminsky, G., & Reinhart, C. (1999). "The Twin Crises." *American Economic Review*, 89(3), 473–500.
