# NFA CPO Exemption 4.13(a)(3) — Filing Guide

> **Regulatory context:** Any person who operates a commodity pool (a fund that trades futures, swaps, or commodity options) is a Commodity Pool Operator (CPO) under the Commodity Exchange Act. CPOs must either register with the CFTC and become NFA members, or claim an exemption. Exemption 4.13(a)(3) is the primary exemption used by small systematic funds. This guide covers the full exemption lifecycle.

---

## What Is the Exemption?

CFTC Regulation 4.13(a)(3) allows a fund manager to operate a commodity pool without registering as a CPO, provided the fund meets two de minimis trading tests and does not market itself through general solicitation. The exemption does not eliminate all regulatory obligations — you still must join NFA and file an annual affirmation — but it avoids the full CPO registration burden, including the Disclosure Document, CTA registration for individual traders, and CFTC reporting requirements.

**Practical meaning:** If you run a systematic fund that primarily trades equities or credit but uses futures or swaps as overlays or hedges, you almost certainly need to know whether you qualify for this exemption.

---

## Who Qualifies?

To claim 4.13(a)(3), all of the following must be true:

1. **Sophisticated investors only:** Each participant in the pool must be either:
   - A "qualified eligible person" (QEP) as defined in CFTC Rule 4.7, OR
   - An "accredited investor" as defined in SEC Rule 501(a) under Regulation D.
   - *Most institutional LP structures satisfy this. Retail investors disqualify the pool.*

2. **De minimis trading — Initial margin test:** The aggregate initial margin and premiums required for commodity interest positions established by the pool do not exceed **5% of the liquidation value** of the portfolio. Margin is measured at establishment; subsequent market moves do not cause retroactive disqualification, but new position additions are measured at the time of addition.

3. **De minimis trading — Net notional test:** The aggregate net notional value of commodity interest positions held by the pool does not exceed **100% of the liquidation value** of the portfolio. Net notional is measured gross by direction (long vs. short) within each asset class, not portfolio-level netted.

4. **No general solicitation:** The pool is not marketed through general solicitation or advertising. Under 4.13(a)(3), you cannot use mass emails, social media posts, public webinars, or public pitch events to raise capital. All fundraising must be through pre-existing substantive relationships.

5. **Claim must be filed:** The operator must file a notice claim on NFA's BASIC system before beginning trading activity.

---

## The Two De Minimis Tests — Detail

### Test 1: Initial Margin and Premiums ≤ 5%

**What counts:**
- Exchange initial margin on futures positions
- Premiums paid for commodity options (not equity options on securities)
- Swap initial margin requirements (variation margin does not count)

**What does not count:**
- Unrealized gains or losses on open positions
- Proceeds from commodity option premium receipts (selling options — only net premium paid counts if short)
- Margin on security futures products regulated solely by SEC

**How to measure:** At the time each new commodity interest position is established, calculate: (aggregate initial margin + net premiums paid) ÷ (pool liquidation value). This ratio must be ≤ 5%.

**Buffer management:** Build in a buffer. If your strategy targets 3% margin utilization, a drawdown compresses the denominator and pushes the ratio up. Model the 5% limit at 70–80% drawdown depth scenarios.

### Test 2: Net Notional ≤ 100%

**What counts:**
- Futures: net notional = face value of futures position (contract size × price × number of contracts), measured separately long and short
- Swaps: notional as defined in the swap confirmation
- Options: delta-adjusted notional is not used — CFTC uses face value of underlying

**How to measure:** Sum the absolute value of all long commodity interest positions. Sum the absolute value of all short commodity interest positions. Take the larger number. That number must be ≤ 100% of pool liquidation value.

**Note on netting:** Within a commodity interest type, long and short in the same contract can be netted. Across different commodity types, positions are not netted.

---

## What the Exemption Permits and Prohibits

### Permitted

- Operating a commodity pool with commodity interest trading at or below the de minimis thresholds
- Trading listed futures on U.S. or non-U.S. exchanges
- Trading OTC swaps (note: swap dealers require ISDA, LEI, and counterparty qualification)
- Using commodity options as hedges or overlays
- Accepting capital from accredited investors and QEPs
- Charging management fees and performance allocations
- Remaining exempt from CPO registration, CTA registration, and CFTC Disclosure Document requirements

### Prohibited

- Exceeding either de minimis threshold (triggers registration requirement)
- General solicitation or advertising to market the pool
- Accepting non-accredited, non-QEP investors
- Using exemption for a pool that primarily trades commodity interests (this is the spirit of "de minimis")
- Failing to file annual affirmation (triggers loss of exemption)

---

## How to File on NFA BASIC — Step by Step

**Prerequisites:**
- Management company LLC formed (see Delaware LLC Checklist)
- EIN obtained
- NFA membership application submitted and approved

### Step 1: Apply for NFA Membership

Navigate to nfa.futures.org. Select "NFA Registration / Membership" → "Apply for Membership." You are applying as a "Commodity Pool Operator — Exempt."

Complete the NFA membership application:
- Entity information (name, EIN, address, state of formation)
- Principal information (individual who will be listed as principal — typically the fund manager)
- Background disclosure questions (criminal history, regulatory history, bankruptcies)
- Fingerprints required for principals (NFA will send instructions)

**NFA membership fee:** $750 for new members; annual renewal $200. Additional per-principal fees apply.

**Timeline:** 2–6 weeks for NFA to process and approve membership.

### Step 2: File the Exemption Claim on BASIC

Once NFA membership is approved, log into BASIC at nfa.futures.org/BasicNet/.

Navigate to: Organization → Filing → Exemption Claims → CPO Exemption 4.13(a)(3).

Complete the claim form:
- Pool name and principal place of business
- Pool formation date
- Confirm each qualification criterion (the form presents each test as a checkbox with a representation)
- Investor qualification (accredited investor / QEP)
- Confirm no general solicitation

**Submit the claim.** It is effective upon filing — NFA does not pre-approve exemption claims, it processes and posts them to the public BASIC database.

**Verify:** Search BASIC for your entity name within 2–3 business days. The exemption should appear under your NFA ID.

### Step 3: Retain Records

Maintain documentation supporting each representation:
- Investor qualification records (accredited investor questionnaires, subscription agreements)
- Trading records showing margin and notional calculations at each new position establishment
- Evidence of no general solicitation (no mass emails, no public advertising)

CFTC and NFA can examine these records. The exemption is self-certified — NFA does not audit you at filing, but audits can occur later.

---

## Annual Affirmation Requirement

**Deadline:** The exemption must be affirmed annually. NFA sends reminder notices, but the obligation is yours. The annual affirmation deadline is **within 60 days after the pool's fiscal year end.**

**How to affirm:** Log into BASIC → Organization → Filing → Affirmations → Affirm CPO Exemption.

The affirmation confirms that the pool still qualifies — all conditions are still met, thresholds have not been exceeded, no general solicitation has occurred, and investors still meet qualification requirements.

**Consequence of missing affirmation:** The exemption is automatically withdrawn. You are then operating an unregistered commodity pool — a CFTC violation. File immediately if you miss the deadline and consult counsel.

---

## What Triggers Loss of the Exemption

| Trigger | What Happens |
|---|---|
| Margin exceeds 5% of pool value | Must cease adding commodity interest positions until back in compliance; if structural, must register as CPO |
| Notional exceeds 100% of pool value | Same as above |
| Non-qualified investor admitted | Must remediate or register |
| General solicitation occurs | Exemption may be voided retroactively; SEC Reg D may also be implicated |
| Annual affirmation missed | Exemption automatically withdrawn |
| NFA membership lapses | Exemption no longer has a valid underlying membership |

---

## When You Exceed the Thresholds — The Upgrade Path

If your strategy scales and you exceed the de minimis thresholds, you must register as a full CPO. The steps:

1. Stop adding commodity interest positions immediately upon recognizing the threshold will be exceeded.
2. Notify fund counsel and begin CPO registration process.
3. File for CPO registration on NFA BASIC (NFA Form 7-R for the organization, 8-R for principals).
4. Prepare a CFTC-compliant Disclosure Document (the CPO equivalent of a prospectus).
5. Each individual acting as a commodity trading advisor (CTA) for the fund may need CTA registration or a CTA exemption separately.
6. Budget 60–120 days for NFA to review and approve the CPO registration.

**Do not continue trading commodity interests beyond the thresholds without registration.** CFTC enforcement actions for unregistered CPO activity can include disgorgement, civil penalties up to $1 million per violation, and trading bans.

---

## Series 3 vs. Series 65 — Relevance to Exemption

**Series 3 (National Commodity Futures Examination):**
- Required for registered CPOs and CTAs and their associated persons.
- NOT required if you are using the 4.13(a)(3) exemption — you are exempt from CPO registration, so the associated person registration requirement does not apply.
- If you upgrade to full CPO registration, principals and APs who solicit or accept funds for commodity pools must pass Series 3 or qualify for an exemption.

**Series 65 (Uniform Investment Adviser Law Examination):**
- Required for Investment Adviser Representatives in most states.
- Relevant to you if you also register as an investment adviser (for securities advice).
- Has no direct relationship to CPO exemption status.
- See the [Series 65 Study Plan](series-65-study-plan.md) for details.

**Practical guidance:** A fund manager running a systematic futures strategy who claims 4.13(a)(3) and also advises on securities (equities, ETFs) will typically need Series 65 (for the IA side) but not Series 3 (CPO exemption covers the commodity side).

---

## Key NFA Resources

| Resource | URL |
|---|---|
| NFA BASIC system | nfa.futures.org/BasicNet/ |
| CPO registration requirements | nfa.futures.org (search "CPO registration") |
| CFTC Regulation 4.13 full text | eCFR.gov → Title 17 → Part 4 |
| NFA compliance rules | nfa.futures.org/rulebook |
| CFTC guidance on de minimis tests | CFTC.gov → Policy Statements |
