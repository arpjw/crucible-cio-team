# Crucible Halt Protocol

## Purpose

This document defines exactly what happens when the Crucible pipeline halts mid-execution. Every halt is either a HARD HALT or a SOFT HALT. The type determines what stops, who is notified, and what is required to resume.

No agent may override a halt unilaterally. All overrides require PM authorization, documented rationale, and an automatic audit log entry.

---

## Halt Types

### HARD HALT

**Definition:** The pipeline stops completely. All pending agent calls are cancelled. No execution instructions are issued under any circumstances. The pipeline cannot be resumed — a new pipeline run must be started after the underlying condition is resolved.

**Triggers:**

| Condition | Triggering Agent | Bus Field |
|---|---|---|
| Compliance violation | compliance (Stage 2) | `COMPLIANCE_STATUS.verdict = VIOLATION` |
| Drawdown breach | drawdown-monitor (Stage 2) | `RISK_HEADROOM.drawdown_status = HALT` |

**What stops immediately:**
- All queued agent invocations (Stage 3 onward)
- Any pending trade instructions
- Any rebalance or roll execution in progress

**What happens:**

1. **Halt record written to bus:**
   ```
   HARD_HALT {
     halt_id:          [pipeline_run_id + "-HALT"]
     triggered_at:     [YYYY-MM-DDTHH:MM:SSZ]
     triggering_agent: [compliance | drawdown-monitor]
     trigger_field:    [COMPLIANCE_STATUS.verdict | RISK_HEADROOM.drawdown_status]
     trigger_value:    [VIOLATION | HALT]
     halt_reason:      [verbatim from agent verdict]
     pending_agents_cancelled: [list of agents not yet run]
   }
   ```

2. **Pipeline Report issued immediately** — abbreviated report containing:
   - HARD HALT notice at the top, formatted as:
     ```
     ██████████████████████████████████████████████████
     HARD HALT — [TRIGGERING AGENT] — [TIMESTAMP]
     Reason: [halt_reason verbatim]
     No execution instructions will be issued.
     All pending agents cancelled: [list]
     ██████████████████████████████████████████████████
     ```
   - Context bus state as of halt (all sections written before the halt)
   - Agents not yet run and what analysis is therefore missing

3. **PM notified with:**
   - The triggering agent name
   - The exact rule breached (for compliance) or the exact drawdown metric (for drawdown)
   - The current bus state for any completed stages
   - Required resolution steps before a new pipeline run is permitted

4. **No override path exists.** A HARD HALT cannot be overridden. To resume:
   - **Compliance VIOLATION:** resolve the violation (amend the proposed trade, obtain required approvals, or confirm the rule does not apply) then re-run `/run-pipeline` with the amended submission
   - **Drawdown HALT:** the drawdown-monitor's HALT escalation requires risk reduction before new positions are permitted; the PM must reduce gross exposure per the protocol defined in `context/risk-limits.md` before re-running the pipeline

---

### SOFT HALT

**Definition:** The pipeline pauses at a specific stage. The issue is surfaced to the PM, who may choose to override with documented rationale or abandon the pipeline run. The override is automatically logged to the audit record.

**Triggers:**

| Condition | Triggering Agent | Bus Field |
|---|---|---|
| Officer blocks a position | risk-officer (Stage 3) | `RISK_HEADROOM.officer_verdict = BLOCKED` |
| Signal blocked | signal-researcher (Stage 4) | `ACTIVE_SIGNALS.signal_overall = BLOCK` |
| Rebalance uneconomic | rebalancer (Stage 6) | `PORTFOLIO_STATE.rebalance_cost_benefit = UNECONOMIC` |
| Audit record incomplete | audit-logger (Stage 7) | `AUDIT_STATUS.status = INCOMPLETE` |

**What stops:** Agents downstream of the triggering stage. Agents already completed are not re-run.

**What happens:**

1. **Soft halt record written to bus:**
   ```
   SOFT_HALT {
     halt_id:               [pipeline_run_id + "-SOFTHALT-n"]
     triggered_at:          [YYYY-MM-DDTHH:MM:SSZ]
     triggering_agent:      [string]
     trigger_field:         [string]
     trigger_value:         [string]
     halt_reason:           [verbatim from agent output]
     pending_agents_paused: [list of agents not yet run]
     override_required:     TRUE
   }
   ```

2. **Pipeline pauses and surfaces to PM:**
   ```
   ──────────────────────────────────────────────────────
   SOFT HALT — [TRIGGERING AGENT] — [TIMESTAMP]
   Issue: [halt_reason]
   Pending agents paused: [list]

   Options:
     [A] Override — provide rationale below, pipeline resumes
     [B] Abandon — pipeline terminated, no execution instructions issued
   ──────────────────────────────────────────────────────
   ```

3. **If PM selects Override:**
   - PM provides written rationale (minimum one sentence explaining why the flag does not apply or is accepted)
   - Override entry is automatically written to `AUDIT_STATUS.override_log`:
     ```
     {
       agent:           [triggering agent]
       override_reason: [PM rationale verbatim]
       authorized_by:   PM
       timestamp:       [YYYY-MM-DDTHH:MM:SSZ]
     }
     ```
   - Pipeline resumes from the paused stage
   - Override is included in the Pipeline Report and flagged for post-trade review

4. **If PM selects Abandon:**
   - Pipeline terminates
   - No execution instructions are issued
   - Bus state is preserved for diagnostic reference
   - A new pipeline run can be started from scratch

---

## Escalation Levels Within SOFT HALT

Not all soft halts have equal weight. The pipeline categorizes them by severity so the PM can quickly assess whether an override is routine or exceptional.

| Severity | Trigger | Default PM Guidance |
|---|---|---|
| **HIGH** | risk-officer BLOCKED | Override requires written rationale reviewed by CRO before execution |
| **HIGH** | signal-researcher BLOCK | Override requires explicit acknowledgment of overfitting or regime mismatch risk |
| **MEDIUM** | rebalancer UNECONOMIC | Override acceptable if PM judges strategic value outweighs cost |
| **LOW** | audit-logger INCOMPLETE | Override acceptable only if all five elements will be completed within 1 business day |

---

## Multiple Simultaneous Halts

If multiple soft halt conditions fire in the same pipeline run (e.g., risk-officer BLOCKED and signal-researcher BLOCK), the pipeline aggregates them into a single pause event rather than presenting them sequentially. The PM sees all flags at once and provides a single override decision covering all of them. Each override is logged separately in `AUDIT_STATUS.override_log`.

If a soft halt and a hard halt fire in the same run, the hard halt takes precedence. The soft halt is noted in the halt record but does not require separate override action.

---

## Post-Halt Review

After any halt (hard or soft), the following review steps are expected:

1. **Same-day:** PM reviews the halt reason and determines root cause
2. **Within 3 business days:** Any compliance VIOLATION that triggered a HARD HALT is reviewed by the Compliance Officer for systemic pattern (is this a recurring violation or a one-off?)
3. **Monthly:** All SOFT HALT overrides from the month are reviewed in aggregate — high override frequency on a given agent suggests the agent's thresholds may need recalibration
4. **Audit trail:** All halt records, override decisions, and rationales are preserved in the audit log indefinitely

---

## Halt-Related Bus Fields Reference

The following fields are checked by the halt logic after each stage. Agents must write these fields in the exact format specified or the halt check will fail to trigger.

| Bus Field | Written By | Halt Type | Halt Value |
|---|---|---|---|
| `COMPLIANCE_STATUS.verdict` | compliance | HARD | `VIOLATION` |
| `RISK_HEADROOM.drawdown_status` | drawdown-monitor | HARD | `HALT` |
| `RISK_HEADROOM.officer_verdict` | risk-officer | SOFT (HIGH) | `BLOCKED` |
| `ACTIVE_SIGNALS.signal_overall` | signal-researcher | SOFT (HIGH) | `BLOCK` |
| `PORTFOLIO_STATE.rebalance_cost_benefit` | rebalancer | SOFT (MEDIUM) | `UNECONOMIC` |
| `AUDIT_STATUS.status` | audit-logger | SOFT (LOW) | `INCOMPLETE` |
