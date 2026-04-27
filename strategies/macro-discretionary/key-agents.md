# Key Crucible Agents — Macro Discretionary

All five governance agents (risk, signal, systems, compliance, macro) are relevant to macro discretionary — more so than to any other strategy type. The adversarial framework is most valuable here because discretionary decision-making has the highest failure rate from cognitive biases and post-hoc rationalization. Each agent plays a specific role in countering a specific failure mode.

---

## Critical — Run on Every Trade

### `/macro-analyst` — Regime Identification and Thesis Validation

For macro discretionary, the macro analyst is not a pre-flight check — it is the primary research tool. Run before every new theme is initiated.

**What to use it for:**

- **Regime classification:** Is the current macro regime consistent with the thesis? A trade betting on rates declining is valid in Contraction + Decelerating inflation + Easing policy regime; it is a bet against the regime in Expansion + Accelerating inflation + Tightening.
- **Cross-asset consistency check:** Does the macro thesis hold across the expected move in multiple asset classes? If you are long gold for inflation reasons, is the gold/TIPS real yield relationship consistent with your view? Are other inflation-sensitive assets confirming or contradicting?
- **Historical analog validity:** Is the "this looks like [year]" historical analog actually comparable on the regime dimensions that matter? The macro analyst has been trained to decompose historical analogs by regime state, not just by surface-level similarities.
- **Duration of expected regime:** How long has this regime historically lasted? Is the trade sized for a regime that could persist for 6 months, or is the PM implicitly assuming a 6-week holding period for a structural change that takes 12 months to develop?

**Always invoke with the full trade thesis, not just the instrument:**
```
/macro-analyst Long 10Y Treasuries — thesis is that the Fed is behind the curve on recession risk, 
expecting cuts beginning Q2. Inflation decelerating. Credit spreads widening. Review consistency 
with current regime and historical analogs.
```

---

### `/audit-logger` — Pre-Trade Record Enforcement

The audit logger is the discipline mechanism that separates systematic macro discretionary from undisciplined macro discretionary. It enforces the five-element pre-trade checklist.

**What it checks for macro discretionary specifically:**

1. **Thesis completeness.** Is the thesis stated in terms of a regime condition, not just a directional view? "Long yen because I think yen will rise" fails. "Long yen because carry differentials are collapsing as BoJ normalizes policy, consistent with current Tightening + Risk-off regime" passes.

2. **Falsifiability of invalidation condition.** "Exit if my view changes" is not an invalidation condition. "Exit if 10-year JGB yield exceeds 1.5% (indicating BoJ is not normalizing as expected) or if yen weakens past 155 on fundamentals-driven USD strength" is an invalidation condition.

3. **Holding period consistency with sizing.** A position sized for a 3-month structural hold should have a wider stop than a position sized for a 1-week tactical entry around an event. The logger checks internal consistency.

4. **Concentration check.** If the new position would bring any theme above 12% NAV, the logger flags it before execution.

The audit logger is a hard gate for macro discretionary: **no execution until record is COMPLETE.**

```
/audit-logger — pre-trade record for: Long EUR/USD, 4% NAV, [paste full rationale]
```

---

### `/kalshi-reader` — Prediction Market Signal Integration

Prediction markets are a primary signal source for macro discretionary, not just a supplement. They aggregate information from participants who have skin in the game in real time.

**Critical uses for macro discretionary:**

- **Fed policy path.** Kalshi Fed rate probabilities are more forward-looking than Fed Funds futures because they aggregate probabilistic forecasts about discrete outcomes. If your thesis requires the Fed to cut twice in the next 6 months and Kalshi puts the probability at 20%, you are betting against the consensus with 4:1 odds against. Either your edge is very clear, or you are wrong.

- **Consensus divergence signal.** The Kalshi reader flags when your view diverges from prediction market consensus by ≥ 15 percentage points. This is not a reason to abandon the trade — contrarian macro trades can be the best trades — but it requires the PM to explicitly articulate why the market consensus is wrong. This articulation must be in the pre-trade record.

- **Event outcome probabilities.** Before any election, referendum, or major policy announcement, check Kalshi probabilities and ensure the portfolio is sized to survive the consensus-wrong scenario, not just the consensus-right scenario.

**Example invocation:**
```
/kalshi-reader — Fed rate path probabilities for next 3 FOMC meetings; compare to my thesis 
that two 25bp cuts occur before end of year
```

---

## High Value — Run Before Position Sizing and Quarterly

### `/quant-researcher` — Distributional Assumption Validation

Macro discretionary PMs often believe that being "discretionary" exempts them from quantitative scrutiny. It does not. Every trade has implicit distributional assumptions — about correlation, about tail risk, about the probability of the thesis being correct. The quant researcher surfaces these.

**What it challenges for macro discretionary:**

- **"The setup looks like [year]" — is the sample size real?** If the historical analog has 3 instances in 50 years, the statistical inference is extremely weak. The quant researcher will quantify this and force the PM to acknowledge the sample size limitation.
- **Correlation assumptions during stress.** A trade that is "hedged" with an offsetting position relies on a correlation assumption. If that correlation breaks under stress (as many macro hedges do in 2020-style crises), the hedge fails. The quant researcher explicitly stress-tests the hedge correlation.
- **P&L attribution consistency.** After each trade closes, did the P&L come from the mechanism the PM described, or from an unrelated factor? If gold was held for inflation reasons but gold's move was driven by USD weakness, the thesis was wrong even if the trade was profitable. The quant researcher helps decompose realized P&L.
- **Parameter sensitivity of the thesis.** What happens to the expected return if the interest rate differential narrows by 50 bps vs. your base case? If the trade only works under a narrow range of outcomes, that is a different risk profile than the PM described.

**Run before every new position above 4% NAV, and whenever a large position is added to.**

---

### `/general-counsel` — Legal and Sanctions Review

Macro discretionary has higher regulatory risk than systematic strategies because:

1. **Geopolitical macro trades involve EM and frontier markets.** Sanctions laws change faster than a fund's operational cadence. A position entered legally can become a sanctions violation within weeks if a new executive order is issued.

2. **Information edge questions.** Macro discretionary PMs often have access to expert networks, government contacts, and industry sources. The general counsel should be consulted if any piece of information is received that could be construed as material non-public information, even if the PM believes it is publicly available.

3. **OTC instrument documentation.** Macro discretionary funds often use OTC instruments (swaps, options, forwards). Each new instrument type requires confirming ISDA documentation is in place and Dodd-Frank/EMIR reporting obligations are met.

4. **New market access.** Before the first trade in a new country's markets, confirm that the fund entity is permitted to trade there, that reporting obligations are understood, and that there are no licensing requirements.

**Standard invocations:**
```
/general-counsel — sanctions screening for proposed position in [EM country] via [instrument type]
/general-counsel — ISDA documentation review before first use of interest rate swaps
/general-counsel — information source review for macro thesis based on [source type]
```

---

### `/chief-risk-officer` — Portfolio Stress Test Before New Theme

Before initiating a new macro theme that would bring the portfolio above 50% gross exposure or any theme above 8% NAV, run a full portfolio stress test.

**Macro-specific stress scenarios to request:**

| Scenario | Why It Matters for Macro |
|----------|--------------------------|
| 2008 GFC | All correlations go to 1; safe-haven trades overwhelm everything else |
| 2013 Taper Tantrum | Rates and EM simultaneously sell off; no hiding place in fixed income |
| 2020 COVID (March) | Liquidity crisis; even safe-haven gold sold off briefly |
| 2022 rates shock | Rates and equity correlated selling; no classic 60/40 protection |
| USD stress rally | USD up 10% in 30 days; affects all non-USD positions, EM, commodities |
| Geopolitical shock | Oil spike + equity selloff + safe-haven bond rally simultaneously |

The CRO should produce a single number: estimated portfolio loss in each scenario. If any scenario breaches the 20% max drawdown hard limit at current positioning, resize before proceeding.

---

## All Five Governance Agents — Quarterly Review

For macro discretionary, running all five governance agents quarterly is standard operating procedure, not optional. The quarterly review cycle:

1. **`/chief-risk-officer`** — Board Risk Report: full portfolio stress test, VaR, drawdown attribution
2. **`/compliance`** — Mandate compliance check: are all positions within mandate? Any exemption currencies drifted?
3. **`/quant-researcher`** — Model validation: P&L attribution for the quarter, are realized returns consistent with stated thesis mechanisms?
4. **`/general-counsel`** — Legal and regulatory horizon scan: any new rules or sanctions affecting current positions?
5. **`/investor-relations`** — LP communication readiness: can the quarterly P&L and attribution be explained clearly to LPs?

---

## Secondary Agents (Use as Flagged)

- **`/signal-researcher`** — When evaluating a systematic component to add to the macro process (e.g., adding a TSMOM signal as a filter for trend confirmation). Not needed for pure discretionary position decisions.
- **`/macro-scanner`** — Daily regime digest during high-uncertainty periods. Run daily when VIX > 20 or when a major macro transition is in progress.
- **`/sentiment-tracker`** — When news flow is a significant driver of near-term position timing. Particularly useful for event-driven macro trades.
- **`/flow-analyst`** — Before taking a contrarian macro position. If COT positioning is at the 95th percentile in the same direction as your intended trade, you are not contrarian — you are consensus.
