# Crucible CIO Team

**An adversarial multi-agent framework for systematic fund managers.**

Five AI agents that challenge your decisions before you execute. Not assistants — adversaries. Each one is looking for the reason your trade, strategy, or deployment should not proceed.

---

## Why Crucible

Most AI tools help you build the case *for* a decision. Crucible is built to tear that case apart.

Before you execute a trade, deploy a strategy, or take on a new position, five independent agents stress-test your decision from five distinct institutional perspectives. Each agent has explicit formulas, pass/fail criteria, and escalation thresholds — not generic questions. The final `/crucible` command synthesizes all five into a single Panel Verdict: **GO**, **CONDITIONAL GO**, or **NO-GO**.

---

## The Panel

| Agent | Invocation | Jurisdiction |
|---|---|---|
| Risk Officer | `/risk` | Position sizing, VaR contribution, correlation clustering, drawdown headroom, tail scenarios |
| Signal Researcher | `/signal` | Statistical significance, look-ahead bias, multiple comparisons, regime decomposition, live/backtest parity |
| Systems Architect | `/systems` | Execution pipeline integrity, data reliability, backtest/live parity, deployment readiness |
| Compliance Officer | `/compliance` | Mandate permissibility, regulatory limits, LP alignment, disclosure obligations, audit trail |
| Macro Analyst | `/macro` | Regime identification, cross-asset consistency, historical analogs, thesis falsifiability, crowding |

Run all five at once:

```
/crucible [trade or deployment description]
```

The Panel Verdict surfaces in 30 seconds. Every blocking issue is ranked by severity and cross-referenced across agents. Consensus findings — vulnerabilities flagged independently by multiple agents — are elevated to highest priority.

---

## How It Works

Crucible runs inside [Claude Code](https://claude.ai/code). Each agent is a structured persona file that instructs Claude to reason from a specific institutional vantage point, using formulas and falsifiable criteria rather than open-ended questions.

Agents are grounded in three context files you populate with your fund's actual parameters:

- `context/fund-mandate.md` — permitted instruments, geographies, strategies, liquidity terms
- `context/risk-limits.md` — leverage, VaR, drawdown, concentration, and regulatory limits
- `context/portfolio-state.md` — current NAV, open positions, active signals, risk clusters

**The agents are only as good as the context you give them.** Fill these files out before your first session.

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/crucible-cio-team.git
cd crucible-cio-team
```

**2. Install Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
```

**3. Populate your context files**

Fill in `context/fund-mandate.md`, `context/risk-limits.md`, and `context/portfolio-state.md` with your fund's actual parameters. Placeholder structure is included in each file.

**4. Open Claude Code**
```bash
claude
```

**5. Run your first review**
```
/crucible Long EUR/USD via June futures, 2% NAV risk, thesis is ECB-Fed policy divergence widening through Q3
```

---

## Verdict Logic

| Verdict | Condition |
|---|---|
| **NO-GO** | Any HARD BLOCK (Risk), VIOLATION (Compliance), or DEPLOY BLOCKER (Systems) |
| **CONDITIONAL GO** | Any soft flags, warnings, or Macro OPPOSED without a hard block elsewhere |
| **GO** | All five agents clear with no unresolved flags |

A GO verdict includes a mandatory post-execution monitoring section. A clean panel review does not mean watch nothing.

---

## Panel Sequence

`/crucible` runs agents in this order:

1. **Compliance** — hard gate. A VIOLATION stops the review.
2. **Risk** — sizing and limits gate.
3. **Macro** — regime and thesis gate.
4. **Signal** — edge validity gate.
5. **Systems** — execution readiness gate.

Compliance runs first because a mandate violation is not a risk management question.

---

## Adapting to Your Fund

Crucible is jurisdiction-agnostic and strategy-agnostic. It is designed for systematic managers but works for any fund with documented risk limits and a mandate.

To adapt:
- Update `context/fund-mandate.md` with your actual permitted instruments and strategy scope
- Update `context/risk-limits.md` with your actual limits — the agents enforce the numbers you give them
- Extend or trim individual agents in `agents/` to match your fund's specific requirements

---

## Structure

```
crucible-cio-team/
├── agents/
│   ├── risk-officer.md
│   ├── signal-researcher.md
│   ├── systems-architect.md
│   ├── compliance-officer.md
│   └── macro-analyst.md
├── .claude/
│   └── commands/
│       ├── risk.md
│       ├── signal.md
│       ├── systems.md
│       ├── compliance.md
│       ├── macro.md
│       └── crucible.md
├── context/
│   ├── fund-mandate.md
│   ├── risk-limits.md
│   └── portfolio-state.md
└── documentation/
```

---

## License

MIT. Use it, fork it, adapt it to your fund.

---

*Built with Claude Code. Inspired by the principle that the most important question before any trade is not "why should I do this" — it is "what would make this wrong."*
