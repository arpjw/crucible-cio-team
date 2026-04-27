# Contributing to Crucible

Crucible is an adversarial multi-agent framework for systematic fund managers. The framework only works if every agent is genuinely adversarial — specific formulas, hard thresholds, real verdicts. Contributions that add vague questions or generic checklists will not be merged.

---

## Before You Build Anything — Open an Issue

The fastest path to a merged contribution is **opening an Agent Proposal issue before writing a single line**.

Use the [Agent Proposal template](.github/ISSUE_TEMPLATE/agent-proposal.md). The template takes five minutes to fill out. It forces you to state the key formulas and the exact escalation threshold your agent uses — if you can't fill that out before building, the agent isn't ready to be built yet.

Agents that arrive as PRs without a prior proposal issue will be asked to open one before review begins.

---

## The Quality Bar

Every Crucible agent must meet five criteria before it gets merged. These are not guidelines — they are gates.

**1. Named verdict system.** Every agent produces a stamped verdict from a defined set. Examples: `CAPACITY CONSTRAINED / CONSTRAINED / UNCONSTRAINED`, `FILL DEGRADATION / ELEVATED / ACCEPTABLE`. A response that ends with "you should consider..." is not a verdict.

**2. Computes rather than asks.** Agents derive findings from inputs and context files. They do not ask the user clarifying questions mid-run. If an agent needs position size, it reads `context/portfolio-state.md`. If it needs risk limits, it reads `context/risk-limits.md`. Questions belong in the proposal issue, not the agent output.

**3. Explicit formulas or criteria.** Every flag must trace to a named threshold. "High correlation" is not a check. "Pairwise ρ > 0.70 in stress periods flags CONCENTRATION WARNING" is a check. If your agent can't be argued with on the basis of its own stated criteria, it's too vague.

**4. Strategy-agnostic.** Agents read fund-specific parameters from `context/` files — they do not hardcode them. An agent that assumes equity long/short or a specific regulatory jurisdiction is not a Crucible agent. The context files carry the fund's identity; the agent carries the logic.

**5. Clear escalation threshold.** Every agent must specify the exact condition that triggers a hard block versus a soft flag. Reviewers must be able to read the agent file and reproduce the escalation decision for any given input without ambiguity.

---

## Directory Structure for a New Agent

Two files. That's it.

```
agents/agent-name.md          # Agent persona: identity, methodology, formulas, output format
.claude/commands/agent-name.md # Slash command definition that invokes the agent
```

Look at `agents/compliance-officer.md` and `.claude/commands/compliance.md` as reference implementations. The persona file should define: identity, step-by-step methodology, explicit formulas or criteria, and the exact output format including the verdict stamp. The command file should be short — it invokes the persona and routes the user's input.

No other files are required to start. AGENTS.md gets updated in the PR.

---

## Review Checklist

Before submitting a PR, run through these five questions. If any answer is no, fix it before opening the PR.

1. **Does it have a named verdict system?** The agent's output section must show a stamped verdict from a defined set of values.
2. **Does it compute rather than ask?** The agent must not ask the user for information it could derive from context files or the input.
3. **Is it strategy-agnostic?** No hardcoded asset classes, jurisdictions, or fund-specific numbers. All parameters come from `context/` files.
4. **Does it reference context files?** At minimum, the agent should read whichever context files are relevant — mandate, risk limits, portfolio state — before running its checks.
5. **Does it have a clear escalation threshold?** The exact condition that triggers a hard block (no override) versus a soft flag (PM may override with documented rationale) must be stated explicitly in the agent file.

---

## Testing Before Submission

Every new agent must be tested against the three scenarios in `tests/README.md` before the PR is opened. The test guide describes the scenario structure and what a well-formed agent response looks like. There is no automated test runner — these are manual runs that you document in the PR description.

---

## Where Crucible Has Gaps

The highest-value contributions are agents for fund types and roles not yet covered. Currently underrepresented:

- **Options trading** — vol surface analysis, gamma exposure, pin risk, term structure signals
- **Crypto / digital assets** — on-chain flow signals, exchange counterparty risk, stablecoin liquidity
- **Equity long/short** — factor exposure decomposition, crowding, short availability, borrow cost
- **Family office** — illiquid allocation, co-investment diligence, manager selection, concentration vs. dynasty risk
- **Fixed income / credit** — duration, spread DV01, default correlation, liability-matching mandates
- **Systematic equity** — alpha decay by factor type, style rotation, rebalancing frequency optimization

If your agent covers a domain or role that Crucible doesn't have, that's a contribution worth making.

---

## GitHub Discussions

GitHub Discussions is enabled for this project. Use it for:

- **Ideas** — proposing an agent concept before you're ready to open a formal issue
- **Show and Tell** — sharing how you've adapted Crucible to your fund's structure, strategy, or regulatory context
- **Q&A** — asking questions about the framework, agent design, or how to extend the pipeline

Discussions are the right venue for "I'm thinking about building X — does it fit?" before the Agent Proposal issue. Opening a discussion first costs nothing and often surfaces whether someone else is already building the same thing.

Suggested categories to enable: **Ideas**, **Show and Tell**, **Q&A**.
