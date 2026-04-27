# Fund Mandate — Time-Series Momentum (Template)

> This file is a pre-filled template for a TSMOM fund. Replace all bracketed fields with your actual fund details before using in production. Copy to `context/fund-mandate.md`.

---

## Fund Identity

**Fund Name:** [FUND NAME]
**Legal Entity:** [e.g., Delaware LP / Cayman Islands exempted fund]
**Domicile:** [e.g., Delaware, Cayman, Ireland]
**Manager / GP:** [MANAGEMENT COMPANY NAME]
**Inception Date:** [DATE]
**Target AUM at Launch:** [e.g., $25M]
**Hard Capacity Ceiling:** $1.5B (strategy-level constraint; review at $500M)

---

## Strategy Description

Systematic trend-following using time-series price momentum signals. The fund takes long and short positions in liquid futures contracts across multiple asset classes and geographies, sized proportionally to target a fixed volatility contribution per instrument. All positions are derived mechanically from the signal; no discretionary overrides.

**Signal:** 12-month minus 1-month total return, recomputed weekly. EWMA variant may be used as an alternate specification with prior written approval from the Risk Committee.

**Position sizing:** Volatility-scaled targeting 15% annualized volatility contribution per instrument; 15–20% target at portfolio level.

**Rebalancing frequency:** Weekly (or monthly if explicitly specified in the investment guidelines).

---

## Permitted Instruments

### Equity Index Futures (target 25–35% of risk budget)
- S&P 500 (ES), Nasdaq-100 (NQ), Russell 2000 (RTY)
- Euro Stoxx 50 (FESX), DAX (FDAX), FTSE 100 (Z), Nikkei 225 (NK), Hang Seng (HSI)
- MSCI Emerging Markets (only if daily liquidity > $200M average; review quarterly)

### Fixed Income Futures (target 25–35% of risk budget)
- US Treasury 2Y (ZT), 5Y (ZF), 10Y (ZN), 30Y (ZB)
- Euro-Bund (FGBL), Euro-Bobl (FGBM), Gilt (R), JGB (JBU)
- Eurodollar / SOFR short-term rates (front 4 contracts maximum)

### FX Futures (target 15–25% of risk budget)
- G10 FX: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF, NZD/USD
- No EM FX unless average daily volume exceeds $500M in the futures contract

### Commodity Futures (target 15–25% of risk budget)
- Energy: WTI (CL), Brent (BRN), Natural Gas (NG) — caution: NG has extreme volatility, cap at 2% NAV
- Metals: Gold (GC), Silver (SI), Copper (HG)
- Agricultural: Corn (ZC), Soybeans (ZS), Wheat (ZW) — combined ag cap 10% gross exposure
- Soft commodities only with CIO approval (illiquid roll profile)

**Minimum liquidity requirement:** Any instrument must have average daily volume exceeding $50M (notional) to remain in the universe. Review universe quarterly.

**Total instruments at launch:** 20–30 futures contracts. Start at 20 for operational simplicity; expand as operational infrastructure matures.

---

## Geographic Scope

Global. Primary markets: North America, Europe, Japan. Secondary: Australia, Canada, Hong Kong. Emerging markets only via highly liquid futures contracts as specified above.

---

## Liquidity Terms

- **Redemption frequency:** Monthly
- **Notice period:** 30 days (consistent with weekly rebalancing; portfolio can be substantially liquidated in under 5 trading days at normal sizing)
- **Gates:** Side pocket provisions at PM discretion if a market-wide liquidity event prevents orderly liquidation
- **Lock-up:** None (open-end structure appropriate given liquid instrument universe)
- **Management fee:** [1–2%] per annum
- **Performance fee:** [10–20%] above [hurdle rate / high-water mark]

---

## Prohibited Activities

- Discretionary overrides of signal-derived positions without documented rationale and risk committee approval
- Concentration in any single instrument exceeding 5% NAV (see risk limits)
- OTC derivatives without explicit written approval from General Counsel (futures-only mandate by default)
- Leverage exceeding 3× gross notional exposure
- Holding positions through earnings or index rebalance events if they were not driven by the trend signal

---

## Mandate Review

Review this mandate annually or when:
- AUM crosses $250M, $500M, or $1B (capacity review required)
- A new asset class is being considered for inclusion
- Signal specification change is proposed
- Regulatory status changes (new exemptions, registrations, or filing obligations)
