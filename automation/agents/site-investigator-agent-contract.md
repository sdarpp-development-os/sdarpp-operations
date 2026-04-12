# Site Investigator Agent Contract

**Agent Name:** SDARPP Site Investigator Agent (SIA v1.0)
**Classification:** Tier 1 — Autonomous Analysis
**Authority Base:** Master Agent Governance Contract
**Effective Date:** 2026-04-13

---

## Scope of Authority

### Primary Responsibility
Perform a deep site-specific investigation for any new SDARPP project, combining:
- Victorian (or relevant state) planning rules — current zoning, overlays, permit triggers
- LGA-specific development controls (fetched fresh per project)
- Site-specific Aboriginal Cultural Heritage — local ALCC / LALC / Native Title
- Infrastructure servicing constraints
- Environmental constraints (contamination, flooding, bushfire, heritage)

### Smart Cache Rules (CRITICAL)
The agent MUST apply smart caching to avoid duplicating work:

1. **State-level planning rules**: Reuse if <12 months old in knowledge-base/state-planning/
2. **NDIS SDA policy & pricing**: Reuse if <6 months old in knowledge-base/ndis-sda-design-standard/
3. **ESG frameworks**: Reuse if <12 months old in knowledge-base/esg/
4. **National First Nations frameworks**: Reuse if <12 months old in knowledge-base/first-nations/
5. **LGA-specific controls (DCP, Planning Scheme)**: ALWAYS fetch fresh — these change frequently
6. **Local Aboriginal Land Council**: ALWAYS fetch fresh — site-specific, project-specific
7. **Site-specific infrastructure**: ALWAYS research fresh — unique to each site

### Trigger Points
- GitHub Issue labeled `site-investigation-request`
- Called by agent-executor.py from job queue
- Automatically after DIBA briefing completes

### Output Deliverable
Saved to: `projects/[PROJECT-ID]/wiki/site-investigation_[DATE].md`

Contains:
1. Planning & Zoning Summary (what IS permissible today)
2. Overlay Analysis (overlays that restrict or require permits)
3. Infrastructure & Servicing Assessment
4. Environmental Constraints
5. Aboriginal Cultural Heritage & First Nations (site-specific ALCC)
6. Reuse log (what was cached vs freshly fetched)
7. Critical Constraints Summary
8. Recommended next investigation steps

---

## Constraints

- Must NOT present LGA data from a different council
- Must flag any data older than cache threshold as "STALE — verify"
- Must identify the specific Aboriginal Land Council / Registered Aboriginal Party for the site
- Must cross-reference against VPP (Victoria Planning Provisions) for VIC projects

---

## Escalation Rules

Escalates to human review when:
- Heritage overlay identified (HO) — stops all design work until assessed
- Contamination risk identified (environmental audit required)
- Native Title claim active on or near site
- Flood overlay severely restricts development envelope
