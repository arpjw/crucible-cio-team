# Crucible Playbook

**From day zero to a running fund — what to do, in what order, and why.**

This document assumes you have already run `/setup` and have a completed `SETUP_REPORT.md` in your repo root. If you haven't, stop here and run `/setup` first. Nothing in this playbook is actionable until the context files are populated.

---

## Part 1 — Before You Trade (Weeks 1–4)

The goal of the first four weeks is to be ready. Ready means: legal entity exists and is compliant, data pipeline is live and writing to the agents, you are fluent with the pipeline workflow, and your first LP conversation is scheduled. Not one trade touches real capital until all four are true.

---

### Week 1 — Legal Foundation

Open `SETUP_REPORT.md` and work through **Appendix A**. This is your legal formation checklist, tailored to the jurisdiction and structure you chose during `/setup`. The sequence matters — nothing downstream (bank account, broker account, NFA exemption) can happen until the entity exists.

**Delaware LLC** (most common for US managers):
- File Articles of Organization with the Delaware Division of Corporations. $90 filing fee, same-day approval available for $50 expedite. Use `legal/formation/delaware-llc-checklist.md` for the complete sequence.
- Appoint a registered agent in Delaware. Expect $100–300/year. You need a physical Delaware address on file — your registered agent provides this.
- Apply for an EIN from the IRS (irs.gov, takes ten minutes online).
- Execute an Operating Agreement. Use `legal/templates/operating-agreement-outline.md` as your starting point. Have an attorney review before signing if you have outside capital coming in.

**NFA CPO Exemption 4.13(a)(3)**:
If your AUM and investor count qualify (generally: trading commodity pools with qualified eligible persons only, below certain thresholds), file the exemption this week via NFA's BASIC system. See `legal/formation/nfa-cpo-exemption-guide.md` for eligibility criteria and the exact filing sequence. This exemption is not perpetual — you must re-file annually and notify NFA within 30 days of any change that affects eligibility.

**Business bank account**:
Open a business checking account in the LLC's name. You need the EIN and Operating Agreement. SVB is no longer an option — Mercury, First Republic (now JPMorgan), or a regional bank that serves investment managers. This is not the fund account — it is the management company operating account for expenses.

**Target for end of Week 1:** Legal entity exists, EIN is issued, NFA exemption filed (if applicable), business bank account open. No capital moves until this is complete.

---

### Week 2 — Infrastructure

Open `SETUP_REPORT.md` and work through **Appendix B**. This is your broker and vendor setup checklist, tailored to the selections you made during `/setup`.

**IBKR Pro fund account**:
Open an Interactive Brokers Pro account in the fund entity's name (not your personal account). This requires the LLC formation documents, EIN, and a description of your investment strategy. Expect 3–5 business days for approval. While waiting for approval, complete the remaining infrastructure steps.

**Data pipeline**:
`scripts/update-context.py` is the script that pulls market data, regime signals, and portfolio state and writes them to the context files the agents read. Run it manually now to confirm it connects and writes output:

```bash
python scripts/update-context.py
```

If it fails, check the data vendor credentials you configured during `/setup`. The three context files — `context/fund-mandate.md`, `context/risk-limits.md`, `context/portfolio-state.md` — should be populated by `/setup` already. The script's job is to update `portfolio-state.md` as positions and signals change.

**Establish baseline regime reading**:
Once the data pipeline is writing, run:
```
/regime-classifier
```
This establishes your baseline. Read the full output — the four-dimension composite scores (growth, inflation, monetary, risk appetite) and the confidence level. Save this reading. You will compare against it weekly to detect regime transitions before they show up in P&L.

**First daily brief**:
```
/macro-scanner
```
This is the daily four-dimension regime state digest. Read it as if you are the PM opening the day. Note the REGIME CHANGE DETECTED flag — if it fires, that is the most important thing in the briefing.

**Target for end of Week 2:** IBKR account open, data pipeline running, first `/regime-classifier` and `/macro-scanner` outputs in hand.

---

### Week 3 — Paper Trading

This week is entirely about becoming fluent with the pipeline workflow before real capital is at risk. You will make mistakes with paper trades that you should not make with live trades — this is the purpose of Week 3.

**First paper trade**:
Pick a trade you would actually consider. It should be specific: instrument, direction, size as percent of NAV, and a one-paragraph thesis. Then describe it to the pipeline:

```
/run-pipeline Long 2% NAV ES futures, thesis: 20-day breakout in rising growth regime, momentum signal fires, ATR stop at 1.5× entry
```

**Read the full Pipeline Report.** Do not skim. Every agent's output is relevant. The agents most likely to generate friction on your first trade are:
- **Compliance** — flags if the instrument or size violates the mandate you set up during `/setup`
- **Risk Officer** — flags if VaR contribution or drawdown headroom is tight
- **Audit Logger** — flags if your pre-trade rationale is missing required elements (signal, thesis, size rationale, risk limit, approval authority)

If any agent issues a hard block, work through why before moving on. The block is almost always surfacing a real gap in your setup.

**Daily pipeline practice**:
Run `/run-pipeline` every day this week on something real — a hypothetical position, a sizing question, a regime check. If you don't have a trade idea, run it on an existing market dislocation and work through what you would do. The goal is that by Week 4 you are not thinking about the tool — you are thinking about the trade.

**Target for end of Week 3:** You have run at least five full pipeline reviews. You have resolved at least one hard block. You know exactly what information each agent needs before it will clear.

---

### Week 4 — LP Preparation

A fund without LPs is a personal account. Week 4 is about getting your first institutional conversation scheduled and being ready for it.

**Run `/investor-relations`** against your current state. Describe the fund, the strategy, and where you are in the setup process. The IR agent will simulate a DDQ review and identify the gaps that a serious allocator would find. Address every gap it surfaces before you have a real conversation.

**Complete the DDQ**:
`legal/templates/ddq-template.md` is a standard institutional DDQ template. Fill in every answer — there are no optional sections. Gaps in a DDQ signal to an allocator that you have not thought through the question. If you genuinely do not have an answer (e.g., administrator — you haven't engaged one yet), say "we are in the process of engaging X" and name the vendors you are evaluating.

**Draft your pitch deck**:
`fundraising/pitch-deck-outline.md` gives you the structure. A first-close pitch deck should be short — ten to twelve slides. The structure: (1) firm overview, (2) investment thesis, (3) strategy description with signal mechanism, (4) backtest results with full methodology disclosure, (5) risk management framework, (6) team, (7) terms. Do not put anything in the pitch deck that contradicts your DDQ.

**Identify first LP candidates**:
`fundraising/lp-targeting-guide.md` gives you a framework for LP outreach organized by tier. For a first close, target the emerging manager tier: family offices, smaller endowments, high-net-worth individuals who are sophisticated enough to qualify but who are willing to take emerging manager risk. Do not cold-outreach institutional allocators (pensions, large endowments, FOFs) before you have a 12-month track record — it will not work and it will burn a relationship you want to have later.

Identify three candidates specifically. Write a one-paragraph description of why each is the right fit for the fund — strategy alignment, risk tolerance, check size expectations, existing relationship. If you cannot write that paragraph, that LP is not the right first call.

**Target for end of Week 4:** DDQ complete, pitch deck drafted, three LP candidates identified, first conversation scheduled.

---

## Part 2 — First Capital (Months 2–3)

---

### Month 2, Week 1 — First LP Close

LP subscription documents are executed. If you used the LP Subscription Agreement outline from `legal/templates/lp-subscription-agreement-outline.md`, have an attorney confirm the completed document before the LP signs. Fund formation attorneys who do this regularly (Seward & Kissel, Schulte Roth, K&L Gates emerging manager practice) will have seen more edge cases than you have.

Capital received into the fund bank account. This is a separate account from the management company operating account — it is titled in the name of the fund entity.

**Initialize the books**:
```
/fund-accountant
```
Describe the opening state: capital received, expense accruals (if any), management fee rate, performance fee structure, and the opening date. The Fund Accountant will initialize the trial balance structure and flag any accounting treatment questions that need to be resolved before the first NAV calculation.

**Establish opening NAV**:
```
/nav-calculator
```
The opening NAV is the capital received. Run this now to establish the baseline and stamp it VERIFIED. Every subsequent NAV calculation will compare against this.

**Record opening state**:
```
/audit-logger
```
Document the fund's opening state as the first entry in the audit log: capital received, initial portfolio state (cash, no positions), mandate confirmed, risk limits active. The audit logger should return COMPLETE. If it returns INCOMPLETE, the missing elements will be listed — fill them in before proceeding.

**Target for end of Month 2, Week 1:** Fund is live, books initialized, opening NAV stamped VERIFIED, audit log records COMPLETE opening state.

---

### Month 2, Week 2 — First Live Trade

This is the one-way door. Everything you did in Weeks 1–4 was preparation. This is execution.

**Run the pipeline**:
```
/run-pipeline [your first real trade, specific and complete]
```

Wait for a GO or CONDITIONAL GO verdict before submitting to IBKR. A CONDITIONAL GO requires you to document each condition — what it is, how you will monitor it, what would cause you to exit — before the order goes in. That documentation becomes part of the audit record.

A NO-GO verdict means the trade does not happen. This is not a failure — it is the system working. Understand which agent blocked and why before deciding whether to revise the trade or abandon it.

**After execution**:
```
/slippage-monitor
```
Compare your actual fill against the modeled slippage from the Order Router's pre-trade estimate. On your first trade this is establishing a baseline, not auditing a pattern. Note the realized vs. modeled ratio. This number will matter when you have enough trades to see a pattern.

Record everything in the audit log. The audit record for a live trade includes: pre-trade rationale, agent verdicts, fill details, slippage vs. model, and the monitoring conditions from any CONDITIONAL GO.

**Target for end of Month 2, Week 2:** First trade executed, audit record COMPLETE, slippage baseline established.

---

### Month 2, ongoing — Daily Rhythm

This is the operating cadence you will run indefinitely. It becomes automatic within a few weeks.

**Morning (before market open)**

`scripts/update-context.py` should be scheduled to run automatically before you sit down. If you have not automated it, run it manually as the first thing you do.

```
/macro-scanner
```
Four-dimension regime state digest. The REGIME CHANGE DETECTED flag is the first thing to look for. If it fired, read the full output before looking at your positions.

```
/event-calendar
```
Any position flagged EVENT RISK — REVIEW POSITION requires an explicit sizing decision before the open. Do not leave it to chance.

If major macro data was released overnight (CPI, NFP, FOMC), run:
```
/regime-classifier
```
to see if the release materially changed the regime reading.

**Midday (trade ideas and position changes)**

Any trade idea — enter, exit, resize, roll — goes through:
```
/run-pipeline [trade description]
```
No exceptions. The pipeline is not a burden — it is the reason you will be able to explain every decision a year from now.

**End of day**

```
/drawdown-monitor
```
Daily drawdown status. MONITOR is fine. WARN requires you to read the velocity and depth analysis carefully. SUSPEND or HALT means position reduction before tomorrow's open.

```
/vendor-monitor
```
Data feed health check. Any STALE or FAILED feed affects tomorrow's regime reading and position valuation. Address feed issues before market open the next day.

**Weekly (Friday or Monday morning)**

```
/flow-analyst
```
CFTC COT data updates every Friday at 3:30 PM ET (for the previous Tuesday's positioning). Run this Friday afternoon or Monday morning after the update. CROWDED on any portfolio instrument is a risk factor to incorporate into next week's sizing decisions.

```
/portfolio-optimizer
```
Computes target allocations from current risk parameters. If drift from targets exceeds 30%, the agent issues a REBALANCE TRIGGER. Feed the output to `/rebalancer` to generate the trade list.

```
/cash-manager
```
Margin utilization and cash runway. Weekly is sufficient unless the market is moving fast, in which case run it daily.

**Monthly (first week of the following month)**

```
/nav-calculator
```
Month-end NAV verification. UNVERIFIED means no LP communication until resolved.

```
/fund-accountant
```
P&L attribution, fee calculation verification, expense allocation review.

```
/lp-reporter
```
Draft the monthly LP letter.

```
/tax-tracker
```
Tax lot review. Any position approaching the 12-month holding period needs an explicit harvest-or-hold decision.

```
/audit-logger
```
Full audit trail review for the month. Every trade should have a COMPLETE record. Resolve any INCOMPLETE records before sending the LP letter.

---

### Month 3 — First LP Report

**Run `/lp-reporter`** to draft the monthly letter. Describe the month: strategy performance, attribution, risk posture, any notable events or decisions. The agent will produce a DRAFT-stamped letter with a disclosure checklist. Work through every item on the checklist.

**Cross-check with `/fund-accountant`**. The P&L number in the LP letter must match the P&L number from fund accounting. If they diverge, resolve it before sending. Even a small discrepancy that has an innocent explanation will undermine LP confidence if they notice it independently.

Use `fundraising/lp-letter-template.md` (normal-month variant) as the structural guide. The letter should be short — two to three pages maximum. Return, attribution, risk metrics, any notable decisions with rationale. LPs do not want prose — they want clarity.

**Run `/investor-relations`** before sending. The IR agent will preview the letter from an LP perspective and flag anything that will generate a follow-up question you are not prepared to answer. Better to find those now.

Send by the 15th of the following month. If you miss it, send it anyway and note the delay. A late letter is better than no letter. Consistency matters more than perfection.

**Target for end of Month 3:** First LP letter sent, track record has begun, LP feedback incorporated into Q2 planning.

---

## Part 3 — Scaling (Months 4–12)

Scaling introduces three new problems: regulatory threshold monitoring as AUM grows, institutional infrastructure requirements that emerge after a track record exists, and organizational complexity that one person cannot absorb. The sequence below is approximately right for most systematic managers. Individual timelines will vary depending on strategy, instruments, and LP type.

---

### $1M → $5M

**Third-party fund administrator**: At $1M–2M, self-administered NAV is defensible. Above $2M, serious allocators will ask who your administrator is. The administrator takes NAV calculation off your plate and provides a third-party verification that LPs rely on. NAV Subscriptions, SS&C, and Gemini Fund Services all have emerging manager programs with minimums in the $1M–2M range.

**Auditor engagement**: Most institutional LP agreements require an annual audit by a registered firm. Engage an auditor in Month 4 or 5 so you have time to get organized before the first year-end audit. PCAOB-registered firms with alternative investment practices include Deloitte, EY (smaller funds use local affiliates), and mid-market firms like Spicer Jeffries, Cohen & Company, and Anchin.

**Data vendor upgrade**: If your instrument count has grown past what your initial data setup covers, upgrade now. Better to upgrade with $3M than to discover data gaps with $10M.

**Regulatory monitoring**: Run `/general-counsel` quarterly to check your CPO exemption currency and whether NFA membership or other filings are triggered as AUM grows. The 4.13(a)(3) exemption has hard thresholds — crossing them without filing the appropriate upgrade creates retroactive exposure.

---

### $5M → $25M

**Series 3 exam**: If you have not already passed the Series 3, do it before you scale past the CPO Exemption thresholds. The exam is administered by FINRA; study materials are available through Kaplan and Knopman. It is not a difficult exam if you prepare, but it takes 4–6 weeks of preparation time that you will not have if you are also running a fund in drawdown.

**Prime broker upgrade**: IBKR Pro is excellent at sub-$10M. At $10M–25M, you may benefit from a full prime — better financing rates on leverage, enhanced reporting, and relationship-based execution services. Consider Bank of America, Jefferies, or Cantor Fitzgerald's emerging manager programs. Do not switch prime brokers during a drawdown or at year-end.

**Institutional LP outreach**: The emerging manager programs at large allocators (CDPQ, CalPERS emerging manager program, University endowments) become relevant at $10M–15M with a 12-month track record. Use `fundraising/lp-targeting-guide.md` institutional tier as the roadmap. Expect a 6–12 month decision cycle from first meeting to commitment.

**Board Risk Report**: Run `/chief-risk-officer` monthly and produce the Board Risk Report output. If you have an LP advisory board, send it to them. If you do not, send it to yourself — the discipline of producing it monthly is the point, not the distribution. A fund manager who can produce a Board Risk Report on demand, at any time, is operating at a different level of risk oversight than one who cannot.

---

### $25M+

**IA registration evaluation**: At $25M AUM, run `/general-counsel` with the explicit question of whether state investment adviser registration is required in your state of operation. At $100M+, SEC registration is mandatory. The registration process takes 3–6 months and requires an ADV filing. Do not cross registration thresholds without the filing in place — the penalties are material and the SEC has taken enforcement action against managers who did this.

**CTO hire**: At $25M you need a full-time engineer. Not a quant — an engineer. Someone who builds and maintains infrastructure, owns the data pipeline, and treats system reliability as a non-negotiable. The `/infrastructure-auditor` assessment will tell you exactly what that person inherits and what they will need to fix first. Hire for rigor and reliability, not for sophistication. You already have the quant capability.

**COO upgrade**: A fractional COO can get you from $5M to $25M. Above $25M, the operational complexity of fund administration, LP reporting, regulatory monitoring, and vendor management requires dedicated bandwidth. Budget for a full-time COO or a COO-caliber fractional with significant hours.

**Formal ISDA**: If you trade OTC derivatives (FX forwards, interest rate swaps, credit instruments), you need an ISDA Master Agreement with your prime broker before you exceed the notional thresholds that require it. Run `/general-counsel` with your current OTC exposure to get the threshold analysis.

**Non-negotiable at this scale**: Run `/run-pipeline` before every trade. At $25M+, a single large bad trade is a material event in your fund's history. The pipeline review takes twenty minutes. The downside of skipping it is measured in years of track record erosion.

---

## Part 4 — Reference

---

### Daily Checklist

Print this. Put it where you see it before market open.

**Morning — Before Market Open**
- [ ] Run `scripts/update-context.py` (or confirm it ran automatically)
- [ ] Run `/macro-scanner` — check REGIME CHANGE DETECTED flag first
- [ ] Run `/event-calendar` — any EVENT RISK — REVIEW POSITION positions require explicit sizing decision now
- [ ] If macro data released overnight: run `/regime-classifier`
- [ ] Review open positions against overnight moves

**Intraday — Trade Workflow**
- [ ] Any new position, resize, exit, or roll: run `/run-pipeline [description]`
- [ ] Wait for GO or documented CONDITIONAL GO before submitting
- [ ] After execution: run `/slippage-monitor` to compare fill to model
- [ ] Update audit log with fill details

**End of Day**
- [ ] Run `/drawdown-monitor` — any WARN or above requires a written response
- [ ] Run `/vendor-monitor` — any STALE or FAILED feed requires resolution before tomorrow
- [ ] Confirm context files reflect today's trades (run `scripts/update-context.py` if needed)

**Weekly — Friday or Monday**
- [ ] Run `/flow-analyst` (COT data updates Friday 3:30 PM ET)
- [ ] Run `/portfolio-optimizer` — act on REBALANCE TRIGGER by running `/rebalancer`
- [ ] Run `/cash-manager` — flag any WARNING or CRITICAL margin status
- [ ] Review roll calendar — any URGENT ROLL from `/roll-manager` must be acted on

**Monthly — First Week of Following Month**
- [ ] Run `/nav-calculator` — UNVERIFIED blocks LP letter
- [ ] Run `/fund-accountant` — verify P&L attribution and fee calculations
- [ ] Run `/lp-reporter` — draft letter, work through disclosure checklist
- [ ] Run `/tax-tracker` — harvest-or-hold decisions on positions near 12-month mark
- [ ] Run `/audit-logger` full review — all trades for the month must be COMPLETE
- [ ] Send LP letter by the 15th

---

### Agent Quick Reference

**I want to enter a new position.**
→ `/run-pipeline [instrument, direction, size, thesis]`

**I have a new signal idea.**
→ `/signal-generator [concept]` → `/backtest-designer [spec]` → `/correlation-mapper` → `/capacity-estimator` → `/decay-tracker` → `/signal [validated spec + results]`

**I'm in drawdown.**
→ `/drawdown-monitor` first (get the escalation level) → `/cash-manager` (check margin headroom) → `/flow-analyst` (check positioning) → `/position-reconciler` (confirm book before adjusting) → `/chief-risk-officer` (full portfolio risk assessment)

**It's month end.**
→ `/nav-calculator` → `/position-reconciler` → `/slippage-monitor` → `/tax-tracker` → `/audit-logger` → `/lp-reporter` → `/fund-accountant`

**I want to roll a futures position.**
→ `/roll-manager` → if approved, `/run-pipeline [roll description]`

**I want to know if the regime has shifted.**
→ `/regime-classifier` → `/macro-scanner` → `/kalshi-reader`

**I'm preparing for an LP meeting.**
→ `/investor-relations` → work through the DDQ gaps it surfaces

**I want to rebalance the portfolio.**
→ `/portfolio-optimizer` → `/rebalancer` → if REBALANCE APPROVED, `/run-pipeline [rebalance trade list]`

**I want to deploy a new strategy.**
→ `/backtest-designer [final spec]` → `/decay-tracker` → `/capacity-estimator` → `/signal` → `/systems` → `/compliance` → `/audit-logger` → `/run-pipeline [first trade]`

**I want to check the fund's legal and regulatory status.**
→ `/general-counsel`

---

### The Philosophy

Crucible exists to answer one question before it is too late: what would make this wrong?

Every agent in the framework is a skeptic — not an assistant, not a validator, not a consensus-builder. They are designed to find the failure mode in a decision before the market finds it for you. The pipeline is not a checklist to complete and move past. It is an adversarial review that challenges the decision from five different expert perspectives simultaneously, then routes the output through operations, execution, and a final audit gate before any capital moves.

The practical result is a fund that can answer "why did you do that" for every trade, every month, every year. Not "because the signal fired" — because the regime was X, the risk contribution was Y, the macro thesis was Z, compliance cleared it, and the audit log records all of it. That level of defensibility is not bureaucracy. It is survival. Funds that cannot explain their decisions to LPs, regulators, or themselves after a drawdown are the ones that close. Funds that can answer every question with precision are the ones that attract institutional capital, survive the hard stretches, and compound over time. The agents do not make decisions. They make sure every decision is defensible. The rest is yours.

---

*Crucible CIO Team — v2.0.0*
