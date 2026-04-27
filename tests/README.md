# Manual Testing Guide

Before submitting a new agent, run it against all three scenarios below and document the results in your PR description. There is no automated test runner — these are manual runs in Claude Code using the slash command you've created.

The goal is not to produce a specific content output. The goal is to verify that your agent produces correctly structured output across the full range of inputs: clean, ambiguous, and clearly bad.

---

## How to run

1. Populate `context/fund-mandate.md`, `context/risk-limits.md`, and `context/portfolio-state.md` with representative (not necessarily real) parameters. The agent must be tested against a populated context — testing against placeholder files is not valid.
2. Invoke your agent's slash command with the scenario input.
3. Check the output against the structural requirements below.

---

## Scenario 1 — Clean input (should produce a passing verdict)

**Input:** A trade or signal that clearly satisfies all of your agent's checks. Size within limits, instrument permitted, no threshold breaches.

**Example for a hypothetical vol-surface-monitor agent:** "Long 1% NAV SPX straddle, 30-day expiry, implied vol at 18%, 30-day historical vol at 16%, term structure in contango."

**What a good response looks like structurally:**
- Opens with a brief parse of the input (what the agent understood)
- Runs each named check in sequence, each producing a finding
- Every check clears — each finding states why, not just "CLEAR"
- Closes with the stamped verdict: `[AGENT NAME] VERDICT: [PASSING VALUE]`
- No hedging language ("you might want to consider..."), no open questions to the user

---

## Scenario 2 — Borderline input (should produce soft flags)

**Input:** A trade or signal that approaches but does not breach hard thresholds. Something real enough to trigger a warning but not a hard block.

**Example for a hypothetical vol-surface-monitor agent:** "Long 1% NAV SPX straddle, 30-day expiry, implied vol at 22%, 30-day historical vol at 16%, term structure flat. Fund's vol budget is 20% implied vol."

**What a good response looks like structurally:**
- Parses input correctly
- At least one check produces a WARNING or FLAG finding — not CLEAR, not VIOLATION
- The warning is tied to a specific threshold stated in the agent file (e.g., "22% implied vol exceeds the 20% budget threshold")
- The finding states what the PM must address before execution, or states that PM may override with documented rationale
- Stamped verdict reflects the soft flag: `[AGENT NAME] VERDICT: [WARNING VALUE]`
- The agent does not block — it escalates with conditions

---

## Scenario 3 — Clear violation (should produce a hard block)

**Input:** A trade or signal that breaches a hard threshold with no ambiguity.

**Example for a hypothetical vol-surface-monitor agent:** "Long 5% NAV SPX straddle, 30-day expiry, implied vol at 35%, position would exceed the fund's 3% NAV options limit."

**What a good response looks like structurally:**
- Identifies the breach immediately in the findings section
- States the exact threshold breached and by how much
- Makes clear this is a hard block — no PM override, no exceptions without a formal governance process
- Stamped verdict is the most severe value in the agent's verdict set: `[AGENT NAME] VERDICT: [BLOCK VALUE]`
- Does not continue running lower-priority checks after a hard block finding (or clearly labels them as informational only)
- No softening language. A VIOLATION is a VIOLATION.

---

## Structural requirements that apply to all three scenarios

These apply regardless of what the agent does or what verdict it produces:

1. **Verdict stamp is the last line of the output** (or the last thing before a brief action summary). It is not buried mid-response.
2. **Every finding is tagged** with the finding type (VIOLATION / WARNING / CLEAR, or the agent's equivalent).
3. **Threshold references are explicit** — the agent states the number, not just the direction.
4. **No clarifying questions** in the output. The agent runs on what it has.
5. **Context files are referenced** — the agent should name which context file a limit came from (e.g., "Per `context/risk-limits.md`, max single-position NAV is 5%").
