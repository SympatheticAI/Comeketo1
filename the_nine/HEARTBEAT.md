# Heartbeat — What Must Be Checked Proactively

This file defines the standing obligations of the master loop's heartbeat cycle.

---

## Heartbeat Cycle

**Frequency:** Every 5 minutes (realtime sweep)
**Responsibility:** Master loop maintains pulse

---

## What Gets Checked

### 1. Master Loop Health
- Is the loop still running?
- Is continuity preserved?
- Are sub-loops closing properly?
- Are open obligations being tracked?

### 2. Trigger Monitoring
- Are time-based triggers firing on schedule?
- Are event-based triggers being received?
- Is the trigger engine healthy?

### 3. Corridor States
- Are active corridors maintaining state?
- Are corridor configurations current?
- Are corridor-specific rules being enforced?

### 4. Memory Integrity
- Is The Nine accessible and current?
- Is working memory (TODAY.md) being updated?
- Is durable memory promotion happening appropriately?

### 5. Tool Availability
- Are integrations reachable? (Google, ClickUp, Close, etc.)
- Is VY operational?
- Are required services running?

### 6. Queue Health
- Are task queues processing?
- Are there stalled items?
- Is Symphony executing properly?

### 7. Approval Queue
- Are there pending approvals?
- Are approvals being processed in reasonable time?
- Are high-stakes actions properly gated?

### 8. Self-Maintenance
- Has the medic run within expected window?
- Has the watchdog checked the medic?
- Are recovery actions succeeding?

---

## Heartbeat Actions

Based on checks, the heartbeat may:

- **Update corridor states** — Refresh active corridor status
- **Record to state** — Write heartbeat signature
- **Flag stale obligations** — Mark items needing attention
- **Trigger medic** — If health check interval reached
- **Escalate critical issues** — Alert human if serious degradation detected

---

## Failure Response

If heartbeat itself fails:
1. **Watchdog detects** — Monitors for heartbeat silence
2. **Alert sent** — Human notified of heartbeat failure
3. **Recovery attempted** — Medic tries to restore heartbeat
4. **Escalation if persistent** — Human intervention required

---

## Success Criteria

Heartbeat is successful when:
- ✅ All checks complete within timeout
- ✅ State is written successfully
- ✅ Critical issues are escalated if found
- ✅ Sub-loops are tracked accurately
- ✅ No silent failures detected

---

**Last Updated:** 2026-03-22
**Next Review:** After first week of operation
