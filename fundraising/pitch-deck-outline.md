# Pitch Deck — Nine-Slide Structure

> **Before distributing:** Have fund counsel review this deck for compliance with applicable advertising rules and your offering exemption. Under Rule 506(b) and CPO Exemption 4.13(a)(3), this deck may only be shared with persons with whom you have a pre-existing substantive relationship and who qualify as accredited investors or QEPs. Do not post this deck publicly, send it unsolicited, or distribute it at public events.
>
> **Date:** [DATE]
> **Version:** [VERSION]
> **Recipients:** [KEEP A LOG OF WHO RECEIVES THIS DECK AND WHEN]

---

## Slide 1 — Cover

**What to include:**
- Fund legal name
- Manager legal name
- Strategy tagline (1 line, plain English — not "quantitative multi-factor systematic alpha generation")
- Date of materials
- Contact information (name, email, phone)
- Regulatory disclaimer (small print): "Confidential — For Qualified Investors Only. Not an offer to sell or solicitation of an offer to buy. Past performance does not guarantee future results."

**What not to include:**
- Performance numbers on the cover (draws attention to unverified claims)
- AUM if small (it will be addressed in the deck)
- Excessive branding or graphic design that substitutes for substance

**What an LP is looking for:** Enough to know in 10 seconds what the strategy is and whether to keep reading.

---

## Slide 2 — Executive Summary

**What to include:**
- One paragraph, plain English description of the strategy. If you cannot explain it in three sentences to a non-quant, you do not understand it well enough to defend it in an LP meeting.
- Target net return and target volatility (e.g., "Target: 12–15% net annual return, 10–12% annual volatility")
- Sharpe ratio target or historical Sharpe
- Target AUM and hard capacity ceiling
- Team: one sentence. Who you are and why you are the right person to run this strategy.
- Status: AUM, months live, current investor count

**What not to include:**
- Promises or guarantees of any kind
- Vague language like "proprietary" or "cutting-edge" without specifics
- Gross returns (LPs care about net returns after fees)

**What an LP is looking for:** Whether to spend 20 more minutes on this. If the executive summary does not answer "what is the edge and why does it persist," you lose them here.

---

## Slide 3 — Strategy and Edge

**What to include:**

*Signal construction (plain language):*
- What market or markets does the strategy trade?
- What is the primary signal type (momentum, mean reversion, carry, volatility, alternative data)?
- What is the signal frequency (daily, weekly, monthly)?
- How do signals combine into positions? Is position sizing rules-based?
- What is the average holding period?

*Why the edge exists:*
- What behavioral or structural market inefficiency does the strategy exploit?
- Why has it not been fully arbitraged? (Risk premium? Capacity constraint? Data access? Execution advantage?)
- What evidence supports the existence of the edge? (Academic literature? First-principles economic logic? Empirical observation?)

*How it has persisted:*
- Out-of-sample evidence: does the strategy work on data it was not trained on?
- Regime robustness: does the strategy work across different market environments?
- Decay analysis: how has performance trended over the most recent 12–24 months vs. the full track record?

**What not to include:**
- Proprietary model details that you do not want disclosed
- Overclaiming: "our signals predicted COVID" type statements
- Curve-fitted backtest results presented without out-of-sample validation

**What an LP will ask after reading this slide:**
- "What happens to this strategy when everyone is doing it?"
- "Why can't a larger fund replicate this?"
- "What does the strategy do in a trending vs. a ranging environment?"
- "How much of the return is explained by well-known factors?"

---

## Slide 4 — Track Record

**What to include:**

*Returns table:*
- Monthly net returns since inception (all of them — LPs will notice if months are missing)
- Clearly labeled: month, year, net return
- Format: standard monthly return grid (rows = year, columns = January through December, last column = annual return)
- Inception date and current AUM clearly labeled

*Risk metrics:*
- Annualized return (net of all fees)
- Annualized volatility
- Sharpe ratio
- Maximum drawdown (depth and duration)
- Calmar ratio (annualized return / max drawdown)
- Win rate (% of months positive)
- Average up month / average down month
- Worst month

*Benchmark comparison:*
- Compare against at least one relevant benchmark (S&P 500 total return, SG Trend Index, or relevant index)
- Show correlation to the benchmark — for systematic strategies, LPs want to see low or negative correlation to equity markets as evidence of diversification value

**What not to include:**
- Simulated or hypothetical performance mixed with live performance without clear labeling
- Gross returns without a net return equivalent — if you show gross, show net immediately below
- Selective time periods without the full track record

**What an LP will ask after reading this slide:**
- "Are these live returns or backtested?"
- "Were these returns audited?"
- "What happened in [worst month]?"
- "What was the track record at your prior firm?"

**Mandatory disclaimer on this slide:**
"Returns shown are net of management and performance fees. Past performance does not guarantee future results. [If partially simulated:] Returns prior to [date] are simulated/paper/from prior firm and have inherent limitations."

---

## Slide 5 — Risk Management

**What to include:**

*Framework overview:*
- How risk is measured: VaR? CVaR? Volatility targeting? Maximum drawdown limits?
- Position-level limits: maximum single position size as % of NAV
- Portfolio-level limits: maximum gross exposure, maximum net exposure, maximum sector concentration
- Instrument-level limits: margin utilization cap, maximum notional per instrument

*Drawdown protocol:*
- At what drawdown level does trading halt? (e.g., "Portfolio halts at 10% drawdown from high water mark")
- What is the reinstatement process after a halt?
- Who makes the halt decision — is it automated or discretionary?

*Who runs risk:*
- Is risk management the PM's responsibility alone or is there a separate risk function?
- How often is the risk framework reviewed?
- Has the risk framework been tested in a real drawdown?

**What not to include:**
- "We manage risk carefully" without specifics — this statement means nothing to a sophisticated LP
- Risk limits that do not match what the actual track record shows (LPs will back-test whether you stayed within limits)

**What an LP will ask after reading this slide:**
- "Walk me through your worst drawdown — what happened, what did you do, how did you recover?"
- "Who would override the PM if risk limits were being breached?"
- "Have you ever breached a risk limit? What happened?"

---

## Slide 6 — Portfolio Construction

**What to include:**
- How signals become positions: signal score → position size formula → execution
- Diversification approach: how many positions, how are they sized, what correlation constraints exist
- How capital is allocated across strategies or asset classes if multi-strategy
- Capacity: current AUM as % of strategy capacity; how capacity was estimated (see capacity estimator methodology)
- Leverage: current and historical leverage ranges; how leverage is managed
- Turnover: estimated annual turnover and its impact on transaction costs

**What an LP will ask after reading this slide:**
- "What is your capacity ceiling and how did you calculate it?"
- "What happens to the strategy if AUM doubles? Triples?"
- "How does portfolio construction handle a correlation spike (crisis scenario)?"

---

## Slide 7 — Operations

**What to include:**

*Service providers:*
- Prime broker: name, relationship duration, margin facility terms (you don't need to disclose the rate, but mention the facility exists)
- Fund administrator: name, what they do (NAV calculation, investor records, capital account maintenance)
- Auditor: name, whether PCAOB-registered, last audit date
- Legal counsel: name, fund formation counsel vs. ongoing regulatory

*Technology:*
- Order management system
- Data vendors
- Execution infrastructure (proprietary or third-party?)
- Brief description of reconciliation process

*Business continuity:*
- One sentence: what happens if the PM is incapacitated?

**What not to include:**
- "We use best-in-class service providers" — name them. Anonymous vendor references signal something is wrong.

**What an LP will ask:**
- "Is your auditor PCAOB-registered?" (Required if you have SEC-registered, qualified custodian audit path)
- "Does your fund administrator independently calculate NAV or do they take your numbers?"
- "What happens if Interactive Brokers goes under?" (Or whatever your prime broker is)

---

## Slide 8 — Team

**What to include:**

*For each principal:*
- Name and title
- Relevant experience: prior investment firms, strategy background, research background
- Education: degrees, institutions (one line per degree)
- Regulatory status: registered IA, CPO exemption, Series licenses held
- Time commitment to fund: full-time or part-time (be honest; LPs will find out)

*Advisors (if applicable):*
- Name, affiliation, nature of advisory relationship
- Do not list advisors who have no meaningful engagement — LPs check

**What not to include:**
- Credentials that are not relevant to investment management
- Photos of the team in formal settings that make a one-person operation look like a 20-person firm

**What an LP will ask:**
- "Is this your full-time focus or do you have other income sources?"
- "What happens to the fund if you [are disabled / leave / die]?"
- "Do you have personal capital invested in the fund?"

---

## Slide 9 — Terms

**What to include:**

| Term | [YOUR FUND] |
|---|---|
| Management fee | [e.g., 1.5% annually, charged monthly on NAV] |
| Performance fee | [e.g., 20% of net profits above HWM] |
| Hurdle rate | [e.g., None / SOFR + 200bps / 8% preferred return] |
| High-water mark | [e.g., Yes / Perpetual / Series-based] |
| Initial lock-up | [e.g., None / 6 months / 1 year] |
| Redemption notice | [e.g., 30 days prior to quarter-end] |
| Redemption frequency | [e.g., Quarterly] |
| Gate provision | [e.g., 25% of fund NAV per quarter] |
| Minimum investment | [e.g., $500,000 / $1,000,000] |
| Target close | [e.g., [DATE] for initial close; rolling closes monthly thereafter] |
| Target raise | [e.g., $10M initial close; $50M target] |
| Fund structure | [e.g., Delaware LP / LLC] |
| Investor eligibility | [e.g., Accredited investors / Qualified Eligible Persons only] |

**On fee negotiations:** Be consistent. If you offer different terms to different LPs and LPs compare notes (they will), you will lose credibility. MFN (most-favored-nation) clauses in side letters require you to offer any better terms given to one LP to all existing LPs who have MFN provisions.

**What an LP will ask after reading this slide:**
- "Are you willing to consider a separate managed account?" (Common from large LPs who want control)
- "What are your co-investment terms?" (If applicable)
- "Do you offer reduced fees for early investors or anchor commitments?"

**Regulatory footer (mandatory on every slide):**
"Confidential. For discussion purposes only with accredited investors and qualified eligible persons. Not an offer to sell or solicitation of an offer to buy securities. Interests have not been registered under the Securities Act of 1933. Any offering will be made only pursuant to a Confidential Private Placement Memorandum. Past performance does not guarantee future results. Investment in the fund involves significant risk, including possible loss of the entire investment."
