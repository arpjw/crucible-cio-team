# Key Crucible Agents — Carry

Carry strategy risks concentrate in a small number of well-defined failure modes: crash risk, correlation breakdown, and regime shifts. The agents below map directly onto these failure modes.

---

## Priority 1 — Run Before Any New Position or Sizing Up

### `/macro-analyst` — Regime Check Before Every New Position

Carry performs worst during risk-off regime shifts. This is not just about whether the carry signal is positive — it's about whether the macro environment is supportive of carry harvesting at all.

**TSMOM can survive in many regimes. Carry cannot survive risk-off.**

**What to check for carry specifically:**

- **Central bank divergence is intact.** FX carry depends on interest rate differentials persisting. If a high-yield currency's central bank is about to cut rates aggressively, the carry signal is about to turn negative even before the price moves. The macro analyst should evaluate whether the current rate environment supports the carry positions.
- **Risk appetite indicators.** Global risk appetite (ISM, credit spreads, equity vol) is the primary macro driver of carry returns. The macro analyst should classify whether the current environment is risk-on or risk-off. Never size up carry into a risk-off regime.
- **Fed policy trajectory.** USD-funded carry (most common) depends on USD rates being lower than or stable relative to the carry currencies. A sudden hawkish shift that strengthens USD undermines all USD-short carry positions simultaneously.
- **Yield curve slope.** If the yield curve is inverted, rates carry is negative — confirm before entering new duration positions.

**Decision rule:** If macro analyst returns a risk-off regime classification with confidence > 50%, do not add new carry positions. If confidence > 70%, reduce existing positions by 30%.

---

### `/chief-risk-officer` — Carry Crash Stress Testing

Carry crashes require explicit tail scenario analysis that the standard VaR framework will underestimate — because historical VaR is computed over normal-regime data, and carry crashes are tail events.

**Mandatory stress scenarios for carry:**

| Scenario | Why It Must Be Tested |
|----------|----------------------|
| 2008 FX carry crash (Aug–Oct 2008) | AUD/JPY fell 40%, EM FX fell 30%; the defining carry crash |
| 1998 LTCM crisis | FX and rates carry unwind; carry correlation spike |
| 2015 China devaluation | EM FX carry positions suffered; CNY peg break risk |
| 2020 COVID (Feb–Mar 2020) | EM FX and commodity carry lost 15–20% in days |
| 2022 rates shock | Rates carry was negative; yield curve inversion |
| JPY unwind scenario | Yen-funded carry is the largest structural carry trade globally; rapid yen strengthening is a systemic risk |

**What to request:**
```
/chief-risk-officer — carry portfolio stress test against 2008 FX crash, 2020 COVID, JPY unwind scenario
```

The CRO should provide:
1. Estimated portfolio loss in each scenario
2. Whether current position sizing survives each scenario without breaching the 15% max drawdown limit
3. Which specific positions drive the worst-case loss

If any scenario produces a simulated loss exceeding the 15% drawdown hard limit, the portfolio must be resized down until all scenarios clear.

---

## Priority 2 — Run on Initial Construction and Quarterly

### `/correlation-mapper` — Diversification Verification

Carry strategy diversification benefit rests on the claim that FX carry, rates carry, and commodity carry are not correlated in normal markets. This claim fails during crashes. The correlation mapper must be run to verify:

1. Current normal-regime pairwise correlations are within expected range (< 0.5 pairwise)
2. Stress correlations are explicitly computed — do not use normal-regime correlations for risk management
3. No unintended concentration is building as positions move

**Carry-specific instruction for the agent:**
- Request both `ρ_normal` (60-day rolling) and `ρ_stress` (computed over 2008, 2020 crisis periods)
- The diversification score in normal markets is not meaningful for carry; it's the stress diversification score that matters
- If any two positions have `ρ_stress > 0.8`, they cannot both be held at full size — the diversification claim is false in the scenario that matters

**Run this quarterly and whenever aggregate gross exposure increases by more than 15%.**

---

### `/kalshi-reader` — Fed Rate Path and Event Risk

For carry strategies, prediction markets provide the most current assessment of central bank policy expectations — which directly drives carry signal sustainability.

**What to check:**

- **Fed rate path probability.** Kalshi and Polymarket give real-time probabilities of rate cuts/hikes at each FOMC meeting. If the probability of a 50 bps cut has risen from 10% to 40% in the past week, the USD funding environment is about to change materially. This affects all USD-short carry positions.
- **EM political/economic event risk.** Prediction markets sometimes price EM political risk (elections, central bank governor changes) before it is reflected in FX implied vols. If Kalshi shows elevated probability of a major EM political disruption, reduce EM carry exposure.
- **Key divergence signal.** If Kalshi-implied rate cut probability is materially higher than what is priced into rate futures (> 15 percentage point gap), there is a signal to reduce long-carry positions — the market may be about to reprice.

---

## Priority 3 — Run When Pipeline Flags Specific Concerns

### `/signal-researcher` — Carry Signal Quality

For carry, the signal construction is less prone to look-ahead bias than TSMOM, but has its own failure modes:

- **CIP violation methodology.** If using CIP deviation as the carry signal, ensure the calculation uses T+2 settlement for spot and the correct forward curve for the implied forward rate. Implementation errors here are common.
- **Roll yield calculation in commodities.** The annualized roll yield must use the correct days-to-expiry and account for weekend/holiday effects. Errors in the time-scaling produce signals that look better than they are.
- **Currency-hedged vs. unhedged returns.** Rates carry positions must specify whether the currency exposure is hedged. A US fund holding European Bunds has both rates carry and EUR/USD FX carry. Failing to separate these contaminates the attribution.

### `/macro-scanner` — Daily Regime Digest

Run daily during elevated risk periods (VIX > 20). The macro scanner's four-dimension state machine provides a rapid early-warning system for regime change. For carry specifically, watch the risk appetite dimension — any transition from RISK_ON to RISK_OFF_FORMING is a trigger to review carry positions.

### `/event-calendar` — 30-Day Event Risk

FOMC meetings, ECB meetings, CPI releases, and NFP reports all create short-term carry disruptions. The event calendar flags which scheduled events in the next 30 days are most likely to disrupt current carry positions and by how much. Critical for avoiding the most predictable crash triggers.

---

## Secondary Agents

- **`/compliance`** — Run when adding OTC FX forwards (ISDA documentation requirements, reporting thresholds).
- **`/fund-accountant`** — Run monthly to verify that currency P&L is correctly attributed (unrealized FX vs. realized carry income vs. roll cost).
- **`/head-of-trading`** — Run quarterly for FX execution quality audit. FX forward spreads can widen substantially at prime brokers for less-favored clients; benchmark against interbank rates.
