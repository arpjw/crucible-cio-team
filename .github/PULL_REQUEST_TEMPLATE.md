## What this PR adds

<!-- One sentence: what agent, what layer, what it does -->


## Agent Proposal issue

<!-- Link the Agent Proposal issue this was discussed in. PRs without a prior proposal issue will be asked to open one. -->

Closes #


## Checklist

- [ ] Agent file created at `agents/<agent-name>.md`
- [ ] Command file created at `.claude/commands/<agent-name>.md`
- [ ] Agent produces a named verdict stamp from a defined set of values
- [ ] Agent computes from inputs and context files — does not ask clarifying questions mid-run
- [ ] Agent is strategy-agnostic (no hardcoded asset classes, jurisdictions, or fund-specific numbers)
- [ ] Agent reads relevant `context/` files (mandate, risk-limits, portfolio-state) where applicable
- [ ] Hard block threshold vs. soft flag threshold are explicitly stated in the agent file
- [ ] Tested against all three scenarios in `tests/README.md` (results documented below)
- [ ] `AGENTS.md` updated with new entry (layer, command, function, key output)
- [ ] No hardcoded fund-specific parameters in agent or command files

## Test results

<!-- Paste a brief summary of your three test runs. For each scenario: what you provided, what the agent produced, whether that matched the expected verdict. -->

**Scenario 1 — Clean (should produce GO / CLEAR / APPROVED):**


**Scenario 2 — Borderline (should produce soft flags):**


**Scenario 3 — Violation (should produce hard block):**
