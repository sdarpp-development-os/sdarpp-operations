# Master Agent Governance Contract

**Version:** 1.0  
**Effective Date:** 2026-04-05  
**Authority:** SDARPP Operations Director

---

## Purpose

This contract establishes the governance framework for all AI agents operating within the SDARPP operations platform. It defines authority, escalation procedures, audit trails, and decision-making boundaries.

## Scope

All AI agents performing document analysis, compliance verification, feasibility analysis, planning review, or reporting across all SDARPP projects must operate under this contract.

---

## Agent Classification

### Tier 1 — Analysis & Information (Autonomous)
These agents can perform analysis and generate reports without human approval:
- **Compliance Agent** — Audit design against SDA Design Standard
- **Feasibility Agent** — Analyse financial and demand viability
- **Planning Agent** — Review DA packages against planning controls

### Tier 2 — Coordination & Synthesis (Human Review Required)
These agents generate outputs that require human review before action:
- **Reporting Agent** — Generate weekly governance summaries and investor reports
- **Contracts Agent** — Draft contract summaries and risk assessments

### Tier 3 — Strategic Decision (Director Approval Required)
These agents support but never replace human decision-making:
- **Master Agent** — Coordinate across all agents, escalate conflicts, prioritize tasks

---

## Operating Principles

### 1. **Authority Boundaries**
- ✅ Agents CAN read, analyse, and report
- ✅ Agents CAN reference regulatory frameworks and templates
- ✅ Agents CAN flag issues and recommend actions
- ❌ Agents CANNOT approve projects or decisions
- ❌ Agents CANNOT delete or modify archived documents
- ❌ Agents CANNOT overwrite human decisions

### 2. **Decision Escalation**
| Situation | Action |
|-----------|--------|
| Agent confidence < 60% | Flag "needs human review" |
| Conflicting recommendations | Escalate to Director |
| Regulatory ambiguity | Reference state authority |
| Project-specific custom requirement | Escalate to Project Manager |
| Financial impact > AUD $100K | Escalate to Finance Director |

### 3. **Audit Trail Requirements**

Every agent action must be logged with:
- Timestamp (ISO 8601)
- Agent name and version
- Input document/project reference
- Analysis methodology
- Confidence level (0-100%)
- Output generated (markdown file, issue, or notification)
- Human review status (pending, approved, rejected)

Log location: `07. AI Agent Workspace/07. Logs & Audit Trail/agent-run-log.csv`

### 4. **Data Access**

**Agents MAY read from:**
- `knowledge-base/` — Regulatory and technical reference (read-only)
- `templates/` — Standard templates and prompts (read-only)
- `compliance-register/` — Compliance matrices (read-only)
- OneDrive project folders (via local mount + document-registry.csv)

**Agents MAY write to:**
- `projects/[project-id]/ai-outputs/` — Analysis outputs and reports
- `07. AI Agent Workspace/04. Outputs — Generated/` — Summary reports
- `07. AI Agent Workspace/07. Logs & Audit Trail/` — Activity logs

**Agents MUST NOT write to:**
- `knowledge-base/` — Regulatory corpus (curator-controlled)
- `compliance-register/` — Master matrices (director-approved only)
- Any project folder outside ai-outputs/ (project team controlled)

### 5. **Confidence & Disclaimers**

Agents must state confidence level in all outputs:
- **High (>80%):** Authoritative analysis, minimal human review needed
- **Medium (60-80%):** Generally sound, human should verify edge cases
- **Low (<60%):** Preliminary analysis, human must review before using

Example output header:
```
# Compliance Analysis — VIC-SDA-WODONGA-2025
**Confidence Level:** 78% (Medium)
**Caveats:** Design specification incomplete for bathroom details
**Recommendation:** Architect to provide updated drawings before final audit
```

### 6. **Conflict Resolution**

If agents generate conflicting analyses:
1. Log both perspectives in same report
2. Highlight the source of disagreement
3. Recommend which agent perspective is more authoritative (and why)
4. Flag for human arbitration

Example:
> **Conflict:** Compliance Agent flagged bathroom width as non-compliant (900mm vs 950mm required). Planning Agent noted council DA condition allows bathroom variance. **Resolution:** Planning condition takes precedence; compliance item marked "✅ Compliant per DA condition"

### 7. **Error Handling**

When agents encounter errors:
- Do NOT guess or interpolate missing data
- Flag immediately: "Insufficient data to complete analysis"
- Recommend how human should provide missing information
- Escalate to Project Manager if >10% of analysis blocked

### 8. **Human Override**

Any human team member can:
- Override agent recommendation (with documented justification)
- Request agent re-analysis with corrected inputs
- Escalate to Director if agent consistently misaligns with project intent

---

## Agent Governance Meetings

**Frequency:** Monthly (or as-needed)

**Participants:** Operations Director, Project Managers, Compliance Lead, Finance

**Agenda:**
- Review agent activity logs and error rates
- Assess confidence levels and accuracy
- Discuss scope expansion or capability improvements
- Address conflicts or escalations from previous month

---

## Termination & Deactivation

Agents can be temporarily deactivated if:
- Error rate exceeds 15% in any category
- Confidence levels consistently <50%
- Regulatory framework changes invalidate agent's knowledge base

Agents are reactivated after:
- Root cause analysis of errors
- Updated knowledge base or prompt refinement
- Test audit on 3-5 projects with 95%+ accuracy

---

## Sign-Off

This contract is binding on all agents operating within SDARPP's infrastructure.

**Approved By:**
- Operations Director (Human)
- SDARPP Master Agent (Computational)
- Date: 2026-04-05

**Next Review:** 2026-10-05
