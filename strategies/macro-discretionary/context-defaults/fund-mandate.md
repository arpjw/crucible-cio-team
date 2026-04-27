# Fund Mandate — Macro Discretionary (Template)

> This file is a pre-filled template for a systematic macro discretionary fund. Replace all bracketed fields with your actual fund details before using in production. Copy to `context/fund-mandate.md`.

---

## Fund Identity

**Fund Name:** [FUND NAME]
**Legal Entity:** [e.g., Delaware LP / Cayman Islands exempted fund]
**Domicile:** [e.g., Delaware, Cayman, Ireland]
**Manager / GP:** [MANAGEMENT COMPANY NAME]
**Inception Date:** [DATE]
**Target AUM at Launch:** [e.g., $25M]
**Hard Capacity Ceiling:** Review at $500M (no hard ceiling at launch)

---

## Strategy Description

Systematic macro discretionary: regime-based, concentrated directional positioning across global asset classes. Positions are driven by macro regime identification and judgment-based thesis construction. Every position requires a written pre-trade rationale with five required elements: thesis, entry trigger, invalidation condition, expected holding period, and risk/return parameters.

**The PM retains full discretion on position decisions.** The system enforces that the decision-making process is documented, falsifiable, and auditable.

**Not a systematic signal-following strategy.** This fund does not follow mechanical rules for entries and exits. It follows a rigorous analytical process with documented judgment calls.

**Holding periods:** Days to months. Shorter holding periods (days) for event-driven trades around scheduled announcements; longer holding periods (weeks to months) for structural macro regime trades.

**Instrument selection:** The PM selects the instrument that best expresses the macro thesis at the lowest cost and with the most appropriate risk profile. The same thesis may be expressed via equity index futures, rates, FX, or commodities depending on where the best risk/reward resides.

---

## Permitted Instruments

### Listed Futures (primary vehicle)
All instruments in the TSMOM and carry fund mandates are permitted here, plus:
- Single-country equity index futures (IBEX, MIB, CAC — useful for European macro differentiation)
- Short-term interest rate futures (SOFR, Euribor, SONIA) for central bank rate path expression
- VIX futures (for explicit vol positioning when the thesis involves risk appetite change)
- Cryptocurrency futures (CME BTC, ETH) only with explicit pre-trade approval from CIO; subject to 2% NAV maximum

### OTC Derivatives (if prime broker agreements are in place)
- FX forwards and cross-currency swaps (requires ISDA Master Agreement)
- Interest rate swaps (requires CSA / variation margin documentation)
- Credit default swaps — Investment-grade only, specific names require legal pre-clearance
- FX and rates options (for asymmetric expression of macro views; preferred over outright futures when event timing is uncertain)

**OTC instruments require:**
1. ISDA Master Agreement with counterparty
2. CSA with variation margin terms
3. Dodd-Frank/EMIR reporting compliance (see General Counsel)
4. Pre-trade approval from CIO + General Counsel for any OTC instrument not previously used

### Prohibited without explicit CIO + Board approval
- Single-stock positions (mandate is macro, not equity selection)
- Private equity, private credit, or any illiquid instrument
- Crypto spot (only CME-listed crypto futures permitted)
- Any instrument with underlying exposure to OFAC-designated entities

---

## Geographic Scope

Opportunistic global. No geographic restrictions except:
- OFAC-sanctioned countries are fully prohibited (current list applies; check before any EM trade)
- Russia, Belarus, Iran, North Korea, Cuba — prohibited regardless of instrument structure
- Any country with primary sanctions exposure requires General Counsel pre-clearance

**EM exposure guidance:**
- EM trades are permitted and can be a significant source of alpha in macro discretionary
- Each EM position requires explicit sanctions screening at entry (not just at fund inception)
- EM positions are capped at 20% of NAV gross exposure (higher concentration risk profile)
- EM liquidity must be assessed at entry; PM must identify exit path under a liquidity stress scenario

---

## Liquidity Terms

- **Redemption frequency:** Quarterly (monthly at PM discretion during normal markets)
- **Notice period:** 60 days (macro positions may have holding periods of 1–3 months; 60-day notice allows orderly unwind)
- **Side pockets:** Permitted for OTC positions that become illiquid (requires investor consent in LPA)
- **Lock-up:** 1-year soft lock (2% redemption fee if redeemed within first year) — macro strategies need time to develop
- **Management fee:** [1.5–2%] per annum
- **Performance fee:** [20%] above [hurdle rate / high-water mark]
- **High-water mark:** Perpetual, not reset

---

## Pre-Trade Documentation Requirement (Mandatory)

Every position, before execution, requires a logged entry with all five elements:

1. **Thesis:** The macro regime condition and mechanism that justifies the position
2. **Entry trigger:** The specific observation or event that prompted this trade now
3. **Invalidation condition:** The specific price level, data point, or event that would prove the thesis wrong
4. **Expected holding period:** Days / weeks / months (determines position size and stop width)
5. **Risk/return parameters:** Target return, stop loss, position size as % NAV

Positions without all five elements logged will be flagged by `/audit-logger` and must not be executed until the record is complete.

---

## Mandate Review

Review this mandate:
- Annually (standard)
- When considering adding OTC instrument types not previously used
- When AUM crosses $100M, $250M, $500M (capacity review)
- When geopolitical events change the sanctions landscape for instruments in the universe
- When hiring a new PM or analyst with different instrument expertise
