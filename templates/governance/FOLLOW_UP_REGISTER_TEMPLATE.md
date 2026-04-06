# Follow-Up Register — Active Engagement & Action Items [PROJECT_NAME]

**Purpose**: Single source of truth for all outstanding consultant follow-ups, action items, and key deliverables. Updated after every meeting or decision.

**Project**: [PROJECT_NAME]  
**Last Updated**: [YYYY-MM-DD]

---

| ID | Counterparty | Action Required | Due Date | Status | Owner | Source |
|---|---|---|---|---|---|---|
| FU-001 | [Consultant Name] | [Action Required] | [YYYY-MM-DD] | 🟡 Pending | [Owner Name] | [Document Reference] |
| FU-002 | [Consultant Name] | [Action Required] | [YYYY-MM-DD] | 🟡 Pending | [Owner Name] | [Document Reference] |

---

## Status Legend

| Status | Meaning |
|---|---|
| 🟢 Active | In progress, on track |
| 🟡 Pending | Awaiting response or action from counterparty |
| 🟠 At Risk | Behind schedule or flagged concern |
| 🔴 Overdue | Past due date and not complete |
| ✅ Complete | Finished and delivered |

---

## Instructions for Use

1. **After every meeting:** Add a new row with the action item, owner, and due date.
2. **Every morning:** Scan the register for items due within the next 7 days.
3. **When following up:** Move status from Pending → At Risk (if communication stalled).
4. **When complete:** Move status → Complete with the date.
5. **When updating:** Commit the change with `git commit -m "docs: update follow-up register — [FU-XXX status]"`.

**Critical rule** (enforced by CI): Any time you update this file, you MUST also update `governance/decision_log.md` with the context of the follow-up change. The governance drift check will fail if you don't.

---

## Current Critical Path (Next 14 Days)

| Date | Item | Owner | Risk Level |
|---|---|---|---|
| [YYYY-MM-DD] | [Action] | [Owner] | 🟢 Green / 🟠 Amber / 🔴 Red |

---

## Related Governance Documents

- [Decision Log](decision_log.md) — Strategic decisions and rationale
- [Risk Register](risk_register.md) — Project risks and mitigation strategies
- [Project Schedule](../pm/PROJECT_DELIVERY_SCHEDULE.md) — Milestone timeline
