You are running a structured trade postmortem for Crucible. Your job is to feed a losing trade outcome back through the agents that originally reviewed it, identify what each agent missed, and produce a logged finding that /calibration-report can consume to surface systemic gaps.

The submission: $ARGUMENTS

Parse the submission as: [original trade description] | [actual outcome] | [date of trade]
If the pipe-delimited format is not present, infer as best you can and state your interpretation at the top.

---

## STAGE 1 — Retrieve Original Review

Search `db/pipeline_runs` for the most recent pipeline run whose `submission` column most closely matches the original trade description. Use this query pattern:

```python
from db.query import get_recent_runs

runs = get_recent_runs(n=50)
# Find the run whose submission text overlaps most with the original trade description
# Match on key tokens: instrument, direction, sizing, signal type
```

Display the matched run in full:

```
════════════════════════════════════════════════════════
ORIGINAL REVIEW RETRIEVED
Run ID:         [id]
Timestamp:      [timestamp]
Submission:     [submission text]
────────────────────────────────────────────────────────
Compliance:     [compliance_verdict]
Risk Officer:   [risk_verdict]
Macro Analyst:  [macro_verdict]
Signal:         [signal_verdict]
Final Verdict:  [final_verdict]
Override log:   [override_log or NONE]
════════════════════════════════════════════════════════
```

If no matching run is found in the database, print:

```
⚠ NO MATCHING RUN FOUND in db/pipeline_runs
```

Then ask the PM: "Please describe what the original review said — which agents flagged concerns, which gave CLEAR verdicts, and what the final decision was. I will use your description for the re-review."

Proceed with whatever information is available. Do not halt because the DB record is missing.

---

## STAGE 2 — Outcome Classification

Classify the actual outcome into exactly one of the following types. State your reasoning in 2–3 sentences before declaring the classification.

| Code | Type | Definition |
|------|------|-----------|
| `LOSS` | Trade went against thesis | The directional call was wrong — the instrument moved against the position |
| `STOP-OUT` | Hit stop before thesis resolved | The position was stopped out on noise before the thesis had time to play out |
| `REGIME-MISS` | Correct thesis, wrong timing | The signal or macro call was eventually correct, but a regime shift made the timing wrong |
| `EXECUTION-MISS` | Correct signal, poor fill | The trade direction was right but slippage, fill timing, or sizing eroded the edge |
| `BLACK-SWAN` | Genuinely unforeseeable | An event with no credible prior probability — not a tail risk that was visible and ignored |

Print:

```
────────────────────────────────────────────────────────
OUTCOME CLASSIFICATION
Type:      [CODE]
Reasoning: [2–3 sentences]
────────────────────────────────────────────────────────
```

**Classification matters downstream:** LOSS and REGIME-MISS implicate signal and macro agents. STOP-OUT implicates risk sizing. EXECUTION-MISS implicates order router and slippage monitor. BLACK-SWAN receives a different treatment — agents are credited, not blamed.

---

## STAGE 3 — Agent Re-Review

For each agent that produced a CLEAR, APPROVED, SUPPORTS, or GO verdict on the original run, re-run that agent with the actual outcome as additional context.

Each re-review uses this prompt structure:

> "You are the [Agent]. You previously reviewed this trade and gave it a [VERDICT] verdict. The trade has since resulted in: [actual outcome].
>
> Given this outcome, run your full framework again and answer the following specifically:
> 1. What specific check in your framework should have caught this? Name the exact check by its framework label.
> 2. What threshold or criterion was too loose? State the current value and what it should have been.
> 3. What question did you fail to ask? Frame it as a question you would add to your checklist.
>
> Produce a MISS ANALYSIS. Be specific — generalities are not actionable."

**Agents to re-run** (only those with CLEAR/APPROVED/GO/SUPPORTS verdicts from the original run):
- Compliance Officer → load `agents/compliance-officer.md`
- Risk Officer → load `agents/risk-officer.md`
- Macro Analyst → load `agents/macro-analyst.md`
- Signal Researcher → load `agents/signal-researcher.md` (if signal_verdict was evaluated)

For each agent that produced a FLAG, BLOCKED, or CONTRADICTS verdict: credit them. Print:

```
✓ [Agent] flagged this — verdict was [VERDICT]. Concern: [flags from original run or summary of what they caught]
```

Format each agent's MISS ANALYSIS block as:

```
────────────────────────────────────────────────────────
[AGENT NAME] — MISS ANALYSIS
────────────────────────────────────────────────────────
Check missed:        [specific framework check label]
Current threshold:   [the value that was in force]
Recommended change:  [specific new value or additional criterion]
Question to add:     [the question that would have surfaced this]
────────────────────────────────────────────────────────
```

If the outcome type is BLACK-SWAN, skip re-review for all agents and instead print:

```
════════════════════════════════════════════════════════
OUTCOME TYPE: BLACK-SWAN — Agent re-review not applicable
No agent framework could have been expected to catch a genuinely
unforeseeable event. Agents are credited for the verdicts they gave.
════════════════════════════════════════════════════════
```

---

## STAGE 4 — Postmortem Report

Assemble the full postmortem report and log it.

```
╔══════════════════════════════════════════════════════════════╗
║                   CRUCIBLE POSTMORTEM REPORT                  ║
╠══════════════════════════════════════════════════════════════╣
║  Trade:      [original trade description, ≤80 chars]          ║
║  Outcome:    [actual outcome]                                  ║
║  Date:       [date of trade]                                   ║
║  Run ID:     [matched pipeline_run_id or NONE]                 ║
╚══════════════════════════════════════════════════════════════╝

OUTCOME CLASSIFICATION
  Type:       [CODE]
  Reasoning:  [2–3 sentences]

AGENT SCORECARD
  [For each agent involved — verdict, miss or credit, one line each]
  e.g.:
  Compliance Officer    CLEAR     → MISS: [what was missed]
  Risk Officer          FLAGGED   → CREDIT: [what was caught]
  Macro Analyst         SUPPORTS  → MISS: [what was missed]
  Signal Researcher     PASS      → MISS: [what was missed]

PER-AGENT MISS ANALYSIS
  [Paste each agent's MISS ANALYSIS block from Stage 3]

SYSTEMIC GAP DETECTION
```

**After listing all miss analyses:** If two or more agents missed the same root cause — for example, both Risk Officer and Macro Analyst failed to weight regime transition risk — flag it as a SYSTEMIC GAP:

```
  ⚠ SYSTEMIC GAP: [root cause description]
     Agents that missed it: [list]
     Implication: [what this gap means for the overall framework]
```

If no systemic gap is detected, print: `No systemic gap detected — misses appear agent-specific.`

```
RECOMMENDED ACTION
  [ ] Update agent threshold: [which agent] → [specific change]
  [ ] Add new check: [which agent] → [the check to add]
  [ ] Accept as unforeseeable: [reasoning why no change warranted]

══════════════════════════════════════════════════════════════
```

**After printing the report**, log the outcome to the database:

```python
from db.query import update_outcome

# Use the pipeline_run_id matched in Stage 1 (or skip if no match was found)
if pipeline_run_id is not None:
    update_outcome(
        pipeline_run_id = pipeline_run_id,
        actual_outcome  = "[actual outcome text]",
        miss_type       = "[LOSS | STOP-OUT | REGIME-MISS | EXECUTION-MISS | BLACK-SWAN]",
    )
```

Then append to the report footer:

```
── PERSISTENCE ──────────────────────────────────────────────────────────────
Outcome logged to db/crucible.db  (run_id: [run_id], miss_type: [CODE])
Run /calibration-report to see miss pattern trends over time.
```

If no DB match was found, print:

```
── PERSISTENCE ──────────────────────────────────────────────────────────────
No matching run found — outcome not logged. Submit again with the exact
original trade text to enable DB matching.
```
