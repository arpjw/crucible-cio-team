# Crucible CIO Team

An adversarial multi-agent framework for systematic fund managers. Five AI agents that challenge fund decisions before execution, modeled after the role structure of a systematic macro CTA.

## Framework Overview

Each agent is a skeptic, not an assistant. They exist to surface failure modes, not validate decisions. When you present a trade idea, signal, or portfolio change, the Crucible agents attack it from their domain.

## Agents

| Agent | Slash Command | Domain |
|---|---|---|
| Risk Officer | `/risk` | Position sizing, drawdown, tail risk, correlation |
| Signal Researcher | `/signal` | Signal validity, overfitting, regime robustness |
| Systems Architect | `/systems` | Execution infrastructure, data pipelines, latency |
| Compliance Officer | `/compliance` | Regulatory, mandate, risk limits, reporting |
| Macro Analyst | `/macro` | Macro thesis, regime identification, cross-asset |
| Full Panel | `/crucible` | All five agents in sequence |

## Directory Structure

```
agents/               # Agent persona definitions
context/              # Shared fund context (mandate, limits, portfolio state)
.claude/commands/     # Slash commands that invoke each agent
```

## Usage

1. Update `context/` files with your fund's actual mandate, limits, and current portfolio state.
2. Invoke an agent with a slash command followed by your decision or question.
3. The agent challenges the decision from its domain perspective.

Example:
```
/risk Long 2% NAV ES futures as trend signal fires on 20-day breakout
/crucible Adding EM FX carry basket, 3% NAV, 6 positions equally weighted
```

## Agent Personas

Agent personas live in `agents/`. Each file defines:
- Role identity and adversarial mandate
- Domain-specific challenge framework
- What inputs to expect and what outputs to produce
- Escalation criteria (when to hard block vs. flag)

## Context Files

`context/` files are read by agents at invocation time to ground their challenges in the fund's actual constraints. Keep them current.
