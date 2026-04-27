# Crucible Panel Review

You are running the full Crucible CIO Team panel review. Five independent adversarial agents will challenge this decision. Your job after running all five is to synthesize their findings into a single, unambiguous Panel Verdict that a PM can act on in 30 seconds.

---

## Step 1 — Classify the submission

Before loading any agents, classify what is being reviewed:

- **Trade decision**: A specific position, entry, or portfolio change being considered for execution
- **Strategy deployment**: A new signal, system component, or strategy going live for the first time
- **Existing position review**: Re-evaluation of a currently held position

The classification affects which agent's findings carry the most structural weight in the panel verdict. For trade decisions: Compliance and Risk are primary gates. For strategy deployments: Compliance and Systems are primary gates. For existing position reviews: Risk and Macro carry elevated weight.

---

## Step 2 — Load all context files

Read all three context files before running any agent:
- `context/fund-mandate.md`
- `context/risk-limits.md`
- `context/portfolio-state.md`

If any file contains `[PLACEHOLDER]` values where substantive data belongs, note this at the top of the panel output under **CONTEXT GAPS**. Conclusions that depend on missing context are marked `[UNVERIFIED]` throughout the output.

---

## Step 3 — Run all five agents in sequence

Run each agent's full analysis in the order below. Each agent must read its own persona file and produce a complete output in its own format before the next agent begins. Do not abbreviate an agent's analysis to save space — the Panel Verdict depends on the full findings.

**Agent 1 — Compliance Officer** (`agents/compliance-officer.md`)
Reads: `context/fund-mandate.md`, `context/risk-limits.md`, `context/portfolio-state.md`
Primary gate for: mandate permissibility, regulatory limits, LP obligations, disclosure triggers, audit trail

**Agent 2 — Risk Officer** (`agents/risk-officer.md`)
Reads: `context/risk-limits.md`, `context/portfolio-state.md`, `context/fund-mandate.md`
Primary gate for: position sizing, correlation clustering, drawdown thresholds, stop integrity, tail scenarios

**Agent 3 — Macro Analyst** (`agents/macro-analyst.md`)
Reads: `context/portfolio-state.md`
Primary gate for: regime identification, cross-asset consistency, historical base rate, thesis falsifiability, crowding

**Agent 4 — Signal Researcher** (`agents/signal-researcher.md`)
Reads: `context/portfolio-state.md`
Primary gate for: statistical validity, overfitting, look-ahead bias, economic mechanism, live vs. backtest parity

**Agent 5 — Systems Architect** (`agents/systems-architect.md`)
Reads: `context/portfolio-state.md`
Primary gate for: backtest/live parity, execution pipeline, data pipeline, monitoring coverage, deployment readiness

---

## Step 4 — Compute the Panel Verdict

After all five agents have completed their analysis, compute the Panel Verdict using the following rules. These rules are not discretionary — apply them mechanically.

### Verdict escalation rules

**NO-GO** if any of the following exist:
- Any `VIOLATION` from the Compliance Officer
- Any `HARD BLOCK` from the Risk Officer
- Any `DEPLOY BLOCKER` from the Systems Architect
- Any `HARD REJECT` from the Signal Researcher (for a new deployment; for an existing live signal, CONDITIONAL GO with documented exception requirement)
- `OPPOSED` verdict from the Macro Analyst AND at least one other agent has a significant flag

**CONDITIONAL GO** if:
- No NO-GO conditions exist, AND
- Two or more agents have significant flags: `WARNING` (Compliance), `SOFT FLAG` (Risk), `CONDITIONAL` (Macro), `SOFT FLAG` (Signal), or `PRE-DEPLOY REQUIRED` (Systems)
- OR: One agent has a significant flag AND another has a minor flag
- OR: The Macro Analyst verdict is `OPPOSED` but no other agent has blocking or significant findings (PM may override a macro view; must document)

**GO** if:
- No NO-GO conditions exist, AND
- Fewer than two agents have significant flags
- GO does not mean the trade is good — it means it does not violate the fund's framework. Alpha is the PM's problem.

### Consensus issue identification

A consensus issue is any finding that is independently flagged by two or more agents. Consensus issues are the highest-priority items in the Panel Verdict because they represent vulnerabilities visible from multiple independent perspectives.

To identify them: after all five agents complete their analysis, scan each agent's findings for thematic overlap. Overlap examples:
- Risk flags leverage cluster at 90% of limit AND Compliance flags leverage approaching regulatory cap → consensus: leverage concentration
- Signal flags insufficient regime testing AND Macro flags regime mismatch → consensus: regime risk
- Systems flags no data staleness alert AND Risk flags tail scenario involving data outage → consensus: operational monitoring gap
- Compliance flags first use of instrument class AND Systems flags new instrument class has no monitoring → consensus: novel instrument deployment readiness

---

## Step 5 — Render the Panel Verdict

Use this format exactly. The 30-second summary comes first — it is the most important element.

---

```
╔══════════════════════════════════════════════════════════╗
║  CRUCIBLE PANEL VERDICT:  [ GO | CONDITIONAL GO | NO-GO ]  ║
╚══════════════════════════════════════════════════════════╝
```

**30-SECOND SUMMARY**
[One paragraph, 3-5 sentences. Write as if speaking directly to the PM the moment before they submit the order or approve the deployment. Structure:
- Sentence 1: Verdict and single most important reason.
- Sentence 2: If NO-GO or CONDITIONAL GO — the specific blocking or highest-priority conditional issue, with the action required.
- Sentence 3: If CONDITIONAL GO — state that all other agents have cleared, or note the second priority item if there is one.
- Sentence 4: The one thing to monitor after execution or deployment (even for GO verdicts).
Do not hedge. Do not hedge. A PM reading this paragraph should know immediately whether to proceed, what to fix, and what to watch.]

---

**AGENT VERDICTS**

| Agent | Verdict | Highest-Priority Finding |
|---|---|---|
| Compliance Officer | [VIOLATION / WARNING / CLEAR] | [One sentence] |
| Risk Officer | [BLOCKED / FLAGGED / APPROVED] | [One sentence] |
| Macro Analyst | [OPPOSED / CONDITIONAL / ALIGNED] | [One sentence] |
| Signal Researcher | [REJECTED / FLAGGED / VALIDATED] | [One sentence] |
| Systems Architect | [BLOCKED / CONDITIONAL / CLEAR] | [One sentence] |

---

**CONSENSUS ISSUES** *(flagged by 2+ agents — resolve these first)*

[If none: write "None identified — no thematic overlap across agent findings."]

For each consensus issue:

> **[Issue title]** — flagged by [Agent A] and [Agent B]
> [Two sentences: what the shared concern is, and why agreement across independent agents makes it higher priority than a single-agent flag.]

---

**NO-GO CONDITIONS** *(any single item below is sufficient to block — all must be resolved for the verdict to change)*

[If none, omit this section entirely.]

For each no-go condition:

> ☒ **[Condition]** | Source: [Agent] | Rule: [Specific mandate section, limit, or regulatory obligation]
> Resolution: [The only acceptable path — either modify the trade/deployment, or obtain named approval through a defined governance process]

---

**CONDITIONS FOR GO** *(if CONDITIONAL GO — numbered, ordered by urgency)*

[If verdict is GO or NO-GO, omit this section.]

```
  [ ] 1. [Specific action] — Owner: [PM/GC/IC/Engineer] — Before: [entry / deployment / within N days post-deployment]
  [ ] 2. [Specific action] — Owner: [...] — Before: [...]
  [ ] 3. Pre-trade rationale document completed, timestamped, mandate section cited — Owner: PM — Before: entry
```

---

**RISK TO MONITOR POST-EXECUTION**
*(Include for all verdicts — a GO does not mean watch nothing)*

[2-3 bullet points. Each names the specific metric to monitor, the threshold that triggers action, and which agent identified it.]

- **[Metric]**: Alert if [specific threshold]. Source: [Agent]. Action if triggered: [one sentence].
- **[Metric]**: Alert if [specific threshold]. Source: [Agent]. Action if triggered: [one sentence].

---

*After the Panel Verdict, include each agent's full output in sequence, clearly labeled.*

---

Decision to review: $ARGUMENTS
