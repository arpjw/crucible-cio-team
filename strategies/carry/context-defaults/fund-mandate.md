# Fund Mandate — Carry (Template)

> This file is a pre-filled template for a multi-asset carry fund. Replace all bracketed fields with your actual fund details before using in production. Copy to `context/fund-mandate.md`.

---

## Fund Identity

**Fund Name:** [FUND NAME]
**Legal Entity:** [e.g., Delaware LP / Cayman Islands exempted fund]
**Domicile:** [e.g., Delaware, Cayman, Ireland]
**Manager / GP:** [MANAGEMENT COMPANY NAME]
**Inception Date:** [DATE]
**Target AUM at Launch:** [e.g., $25M]
**Hard Capacity Ceiling:** $2B (strategy-level constraint; review at $500M)

---

## Strategy Description

Systematic carry harvesting across three asset classes: FX, fixed income, and commodities. The fund takes long positions in high-carry instruments funded by short positions in low-carry instruments within each asset class, weighted by carry signal strength and volatility-scaled to target a constant risk contribution per instrument.

All positions are signal-derived and mechanically sized. Discretionary overrides require written approval from the Risk Committee and are logged to the audit record.

**FX carry signal:** Interest rate differential (or CIP deviation where measurable), updated daily.

**Rates carry signal:** Yield curve slope and roll-down return, computed weekly.

**Commodity carry signal:** Annualized roll yield from front-month to second-month futures spread, updated weekly.

**Position sizing:** Volatility-scaled. Target 10% annualized volatility contribution per instrument; 10–12% target at portfolio level. Carry strategies run at lower vol than TSMOM because the left-tail exposure is compensated for by the carry premium — excess leverage amplifies crash risk disproportionately.

**Rebalancing frequency:** Weekly for FX; monthly for rates and commodities. FX positions require more frequent rebalancing because interest rate differentials can shift quickly with central bank communication.

---

## Permitted Instruments

### FX Futures / Forwards (target 35–45% of risk budget)

**G10 FX (primary):**
- EUR/USD, GBP/USD, AUD/USD, NZD/USD, USD/CAD, USD/CHF, USD/JPY, USD/NOK, USD/SEK
- Implementation: CME FX futures preferred; prime broker forwards permitted with ISDA in place

**EM FX (secondary — 20% of FX allocation maximum):**
- USD/BRL, USD/MXN, USD/ZAR, USD/TRY (only the most liquid EM pairs)
- EM FX requires daily liquidity check; if average daily volume drops below $200M, reduce to zero immediately
- EM FX limited to 8% of total NAV gross exposure

### Fixed Income Futures (target 30–40% of risk budget)
- US Rates: ZT (2Y), ZF (5Y), ZN (10Y), ZB (30Y) — curve carry across the tenor spectrum
- European Rates: Schatz (2Y), Bobl (5Y), Bund (10Y) — eurozone curve carry
- UK Gilts: Short, medium, long gilt futures
- Japan: JGB futures (with awareness of BOJ policy interventions)
- Australia: 3Y and 10Y bond futures
- No EM rates unless instrument has > $500M average daily volume
- Maximum rates exposure: 50% gross NAV

### Commodity Futures (target 15–25% of risk budget)
- Energy: WTI (CL), Brent (BRN) — roll yield signal only; no directional bets
- Metals: Gold (GC), Silver (SI), Copper (HG) — gold typically in contango; include only when roll yield is positive
- Agriculture: Corn (ZC), Soybeans (ZS), Wheat (ZW) — combined ag cap 10% gross exposure
- Carry signal strength minimum: roll yield must exceed 3% annualized for a long position; no short commodity positions based on carry alone (short carry in commodities has different risk profile)

---

## Geographic Scope

Global developed markets primarily. G10 currencies and their associated rate markets. EM exposure limited to FX only (no EM fixed income futures — illiquid with high jump risk). Commodity carry is global by nature.

---

## Liquidity Terms

- **Redemption frequency:** Monthly
- **Notice period:** 45 days (longer than TSMOM because FX forward positions may require advance notice to unwind; 30-day minimum even if operational capacity permits faster)
- **Gates:** Redemption gate at 20% of fund NAV per quarter, triggered by PM declaration of liquidity impairment
- **Lock-up:** None (carry strategies should be liquid; lock-ups for illiquid underlying would misrepresent strategy)
- **Management fee:** [1–1.5%] per annum (carry has lower vol than TSMOM; fee should reflect this)
- **Performance fee:** [10–20%] above [hurdle rate / high-water mark]
- **High-water mark:** Perpetual (not reset)

---

## Prohibited Activities

- Short commodity carry positions without explicit CIO approval (crash risk is asymmetric for short carry)
- EM fixed income futures exposure (jump-to-default and central bank intervention risk)
- FX spot trading as a substitute for futures/forwards (creates unhedged settlement risk)
- Carrying positions through known risk events (FOMC, major elections, central bank policy reviews) without explicit pre-trade risk review — see `/event-calendar`
- Leverage exceeding 4× gross notional exposure
- Concentration in any single currency pair exceeding 3% NAV

---

## Mandate Review

Review this mandate annually or when:
- AUM crosses $250M, $500M, or $1B
- A central bank policy regime changes materially (e.g., BoJ abandons YCC, Fed pivot to cuts)
- EM FX exposure is being considered beyond the 8% NAV cap
- OTC instruments (swaps, cross-currency basis) are proposed for the rates carry implementation
