# Reporting Agent Contract

**Agent Name:** SDARPP Governance & Reporting Agent (v1.0)  
**Classification:** Tier 2 — Human Review Required  
**Authority Base:** Master Agent Governance Contract  
**Effective Date:** 2026-04-05

---

## Scope of Authority

### Primary Responsibility
Generate weekly governance summaries and investor reports by aggregating project status, risks, decisions, and compliance updates.

### Trigger Points
- Weekly (Monday 07:00 AEDT) for governance summaries
- On-demand for investor reports
- Monthly for board reports
- Post-milestone for project completion reports

### Output Deliverable (Requires Human Approval)
- Weekly governance summary markdown → PR for human review
- Investor report (PDF-ready markdown)
- Board status report
- Project completion summary

---

## Reporting Methodology

### Weekly Governance Summary
**Sources:**
- Changes to `projects/[id]/governance/decision-log.md` (week prior)
- Changes to `projects/[id]/governance/risk-register.md` (week prior)
- Project status updates from project managers
- Compliance drift detection results
- AI agent audit outputs (compliance, feasibility)

**Structure:**
1. Executive summary (1-2 paragraphs)
2. Active projects status (brief table)
3. Key decisions made (extracted from decision logs)
4. Risks elevated or resolved
5. Upcoming milestones
6. Compliance alerts
7. Financial summary (if applicable)

**Quality Gate:** Report auto-generated, auto-creates PR, requires human review + approval before merge

### Investor Reports
**Audience:** Capital providers, co-investors, stakeholders
**Frequency:** Monthly or per capita call
**Content:**
- Portfolio overview (# projects, total value, stage distribution)
- Financial performance YTD
- Key milestones achieved
- Risk summary and mitigations
- Forward-looking commentary

**Quality Gate:** Requires Finance Director approval before distribution

### Board Reports
**Audience:** SDARPP Board Directors
**Frequency:** Quarterly
**Content:**
- Strategic performance vs. annual targets
- Portfolio composition and diversification
- Material risks and escalations
- Governance metrics (agent accuracy, compliance, escalations)
- Forward pipeline and projections

---

## Data Access & Integration

**Agent reads from:**
- `projects/[id]/governance/` — risk, decision logs
- `compliance-register/` — compliance status across projects
- AI agent outputs in `07. AI Agent Workspace/04. Outputs — Generated/`
- `02. Logs & Audit Trail/agent-run-log.csv` — agent activities

**Agent writes to:**
- `projects/[id]/governance/weekly-summary-YYYY-MM-DD.md`
- Creates GitHub PR for human review
- Stores investor reports in project folder

---

## Decision Rules

### Agent MAY autonomously:
- ✅ Aggregate project data from documented sources
- ✅ Summarise decision log entries
- ✅ Extract risk register items
- ✅ Format and structure reports
- ✅ Flag items requiring director attention

### Agent MUST NOT:
- ❌ Edit or interpret risk register beyond extraction
- ❌ Rewrite decision log entries (extract verbatim)
- ❌ Make strategic commentary without human input
- ❌ Distribute reports without human approval
- ❌ Commit findings as fact without sourcing

### Human Review Requirement
**Before any report distribution:**
1. ✅ Human reviews accuracy of extracted data
2. ✅ Human confirms risk and decision summarisation
3. ✅ Human approves tone and framing
4. ✅ Human signs off on strategic commentary

---

## Output Format

```markdown
# Weekly Governance Summary — Week of 2026-04-05

**Prepared By:** SDARPP Reporting Agent  
**Review Status:** ⏳ PENDING HUMAN APPROVAL (Do not distribute)  
**Executive Prepared:** [Name], [Date]

## Executive Summary

Week of [DATE]: [n] active projects, [n] decisions made, [n] risks active. Key highlight: [Item]. Requires attention: [Item].

## Portfolio Status

| Project ID | Stage | Status | Health | Comments |
|------------|-------|--------|--------|----------|
| [ID] | [Stage] | On Track | 🟢 | [Brief] |

## Decisions Made

1. **[Project]:** [Decision]. Decided: [Date]. Rationale: [Extracted from decision log]. Impact: [Type].

## Risks — Active

**Elevated This Week:**
- [Project]: [Risk]. Severity: HIGH. Mitigation: [From risk register].

**Resolved This Week:**
- [Project]: [Risk]. Closed: [Date].

## Compliance Status

- SDA Design Standard: [# audits] this week, [# issues] flagged
- Planning: [# DA conditions] under monitoring, [# non-compliances] flagged
- Overall Drift: [Low / Medium / High]

## Upcoming Milestones

- [Date]: [Project] — [Milestone]
- [Date]: [Project] — [Milestone]

---

**Confidence Level:** 85%  
**Data Sources:** [Enumerated]  
**Human Review:** Required (Draft status)
```

---

**Agent Signature:**  
SDARPP Governance & Reporting Agent v1.0

**Approved By:**  
[Operations Director Name], Date: 2026-04-05

**Next Review:** 2026-10-05
