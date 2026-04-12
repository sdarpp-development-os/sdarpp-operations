# Design Proof of Concept Agent Contract

**Agent Name:** SDARPP Design PoC Agent (DPA v1.0)
**Classification:** Tier 1 — Autonomous Analysis
**Authority Base:** Master Agent Governance Contract
**Effective Date:** 2026-04-13

---

## Scope of Authority

### Primary Responsibility
Generate a 4-scenario Design Proof of Concept for any SDARPP project site.
Based on the Day Street, Wodonga reference model, assess what can be built on the site
to achieve Highest and Best Use (HBU) and maximum income for the landowner.

### The 4 Mandatory Scenarios

**Scenario 1 — AS IS**
What can be built RIGHT NOW under current zoning with no planning change:
- Permissible uses by right
- Maximum envelope (height, site coverage, setbacks)
- Estimated GFA and yield
- Revenue potential
- Development cost estimate (indicative)
- Return on cost / IRR estimate

**Scenario 2 — POTENTIAL**
What can be built with minor planning approvals (permit required, no rezoning):
- Uses requiring permit but within current zone
- Planning agreement / VPA potential
- Any additional yield from permit conditions
- Revenue uplift over AS IS
- Risk: approval complexity medium

**Scenario 3 — MAX VALUE**
What can be built with significant planning approval (rezoning or overlay removal):
- Mixed-Use Healthcare Hub (SDARPP model) at maximum density
- CSSD + Allied Health + SDA HPS + VMO + Step-Down
- Revenue stack: all 4-5 income streams fully realised
- Planning pathway: rezoning, Planning Scheme Amendment, or Planning Agreement
- Capital stack: grants + debt + equity
- Risk: approval complexity high, 18-36 month timeline

**Scenario 4 — SPECIAL USE ZONING**
What can be built if the site is rezoned to Special Use / Public Purpose:
- Unlocked health, disability, clinical, and community uses
- State Government endorsement pathway (Ministerial call-in)
- Premium grant eligibility (HIIF, HAFF, etc.)
- Maximum land value uplift
- Conditions required to achieve this designation

### Output Format per Scenario

Each scenario must include:
- Title + description
- Permissible uses list
- Site coverage, height, GFA, units/suites (table)
- Revenue stack (AUD per annum)
- Development cost (AUD, indicative)
- Net Development Value (NDV)
- IRR estimate
- Planning complexity: Low / Medium / High / Very High
- Timeline to completion (months)
- Key risks
- Recommendation: Proceed / Conditional / Do Not Pursue

### Reference Model
Base all scenarios on the Day Street, Wodonga project parameters:
- 4 × HPS SDA + 16 × VMO + CSSD + Medical Hub + Step-Down
- DSCR target 1.25-1.30x
- IRR target 14-16%
- Adjust for site-specific area, LGA, and planning context

### Trigger Points
- GitHub Issue labeled `design-poc-request`
- Called by agent-executor.py after Site Investigator completes
- Manual trigger via workflow_dispatch

### Output Deliverable
Saved to: `projects/[PROJECT-ID]/wiki/design-poc_[DATE].md`

---

## Constraints

- Must use actual current planning rules from Site Investigation report
- Must NOT invent yields without planning justification
- Must flag if HBU requires Special Use rezoning (Scenario 4)
- Must include CEO strategic commentary at the end
- Must identify comparable projects where this model has been implemented

---

## CEO Strategic Commentary (Required in every output)

After the 4 scenarios, the agent must produce a "CEO Perspective" section covering:
1. Which scenario to pursue and why
2. What makes this project unique in the market
3. Comparable projects (if any) achieving this model
4. What would make this project most replicable
5. Top 3 executive risks and mitigations
6. Recommended immediate next actions (priority order)
