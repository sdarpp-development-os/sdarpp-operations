# Cross-Repository Synchronization Guide

**Purpose:** Define how templates, compliance baselines, and standards flow between `sdarpp-operations` (company-level master) and individual project repositories (e.g., `project_day_st_wodonga`).

---

## Architecture Overview

```
sdarpp-operations/ (MASTER — Source of Truth)
├── templates/governance/         ← Company-level governance templates
├── templates/agent-prompts/      ← AI agent instruction sets
├── compliance-register/          ← Master compliance baselines
├── knowledge-base/              ← Regulatory and technical reference
└── projects/[PROJECT_ID]/       ← Per-project governance links

project_[NAME]/ (PROJECT — Implements Templates)
├── governance/                  ← Uses templates from operations
│   ├── MEETING_NOTE_TEMPLATE.md (inherited from operations)
│   ├── FOLLOW_UP_REGISTER.md    (instance of operations template)
│   ├── RISK_REGISTER.md         (instance of operations template)
│   ├── DECISION_LOG.md          (instance of operations template)
│   └── [project-specific docs]  (e.g., governance_overview.md)
├── compliance/                  ← Feeds back to operations baseline
│   └── NDIS_SDA_STANDARDS.md    (→ updates operations matrix)
└── [other folders]/
```

---

## Template Flow: Operations → Projects

### 1. Governance Templates

**Source:** `sdarpp-operations/templates/governance/`

| Template | Usage | Where Copied |
|----------|-------|--------------|
| `MEETING_NOTE_TEMPLATE.md` | Standardized meeting note format | Project: `governance/MEETING_NOTE_TEMPLATE.md` |
| `FOLLOW_UP_REGISTER_TEMPLATE.md` | Action item tracking | Project: `governance/FOLLOW_UP_REGISTER.md` |
| `RISK_REGISTER_TEMPLATE.md` | Risk tracking structure | Project: `governance/RISK_REGISTER.md` |
| `DECISION_LOG_TEMPLATE.md` | Strategic decision logging | Project: `governance/DECISION_LOG.md` |

**How to Use:**
1. Project is initialized or added to operations `projects/[PROJECT_ID]/`
2. Operations owner copies template → Project repo
3. Project team customizes with project-specific data
4. GitHub Actions in each project validates against template structure

### 2. AI Agent Prompts

**Source:** `sdarpp-operations/templates/agent-prompts/`

| Agent Prompt | Purpose | Project Usage |
|---|---|---|
| `compliance-check-prompt.md` | NDIS SDA compliance audit framework | Used in project governance prompts |
| `feasibility-analysis-prompt.md` | Financial modeling guidance | Used in feasibility documents |

**How to Use:**
1. Project team accesses operations repo for current agent prompts
2. Prompts referenced in project `governance/copilot_prompts.md`
3. When operations updates prompts, projects adopt updates in next sprint

### 3. Knowledge Base References

**Source:** `sdarpp-operations/knowledge-base/`

Projects reference (but do not copy) these resources:
- `ndis-sda-design-standard/` — Design Standard implementation
- `state-planning/[STATE]/` — State-specific planning controls
- `document-registry.csv` — Cross-project document index

**How Projects Access:**
- Via GitHub links: `https://github.com/sdarpp-development-os/sdarpp-operations/blob/main/knowledge-base/...`
- Via git submodule (optional): Clone knowledge-base as read-only reference
- Via local copy (for offline access): Copy static reference docs to project

---

## Data Flow: Projects → Operations

### 1. Compliance Baseline Population

**Flow:** Project SDA compliance work → Operations master matrix

**Process:**
1. Project completes initial SDA compliance assessment (e.g., `compliance/NDIS_SDA_STANDARDS.md`)
2. Operations owner reviews project compliance findings
3. Updates `sdarpp-operations/compliance-register/ndis-sda-compliance-matrix.md` with project baseline
4. Adds project entry under "Project Baselines" section with:
   - Category/model evaluated
   - Known gaps or risks
   - Timeline for full audit
   - Link back to project repo

**Example (Day Street Baseline):**
```
### VIC-SDA-WODONGA-2025
Category: HPS (High Physical Support)
Status: ⭕ Pending full accredited assessor audit
Known Issues: 
- Communal kitchen does not meet HPS standard (❌)
- Step-free access requires validation (⚠️)
Next Steps: Engage SDA Assessor by 01 May 2026
```

### 2. Decision Log Integration

**Flow:** Project decisions → Operations decision log (where applicable)

**Process:**
1. Project makes strategic decision → Logs in `governance/decision_log.md`
2. For company-level decisions (e.g., "Approved SDA Provider Engagement"), add entry to operations decision log
3. Cross-reference: Project decision log links to operations, operations links back to project

**Governance Drift Check Enforcement:**
- CI in project repo validates that domain file changes (pm/, feasibility/, sda/) are accompanied by decision_log.md updates
- Same rule applies in operations repo: compliance-register changes require decision_log.md entry

### 3. Consultant & Expert Engagement

**Flow:** Project consultant briefs, templates, meeting notes → Operations case library

**Process:**
1. Project engages consultant (e.g., architect, planner)
2. Project documents engagement in `consultants/[CONSULTANT_TYPE]-[DATE].md` using meeting note template
3. Operations owner (monthly) reviews multi-project consultant performance patterns
4. Patterns inform updates to operations `templates/project-setup/` recommendations

**Example:** If three projects independently report consultant delays, operations updates the "Consultant Selection" playbook.

---

## Adding a New Project to Operations

### Step-by-Step

1. **Create project folder** in `sdarpp-operations/projects/[PROJECT_ID]/`
   ```bash
   mkdir -p sdarpp-operations/projects/VIC-SDA-WODONGA-2025
   ```

2. **Create project README** with:
   - Project name, location, entity
   - Current stage & status
   - Critical path (next 3 milestones)
   - Key consultants
   - Link to project GitHub repo

3. **Copy governance templates** to project repo:
   - `MEETING_NOTE_TEMPLATE.md` → Project `governance/`
   - `FOLLOW_UP_REGISTER_TEMPLATE.md` → Project `governance/FOLLOW_UP_REGISTER.md`
   - `RISK_REGISTER_TEMPLATE.md` → Project `governance/RISK_REGISTER.md`
   - `DECISION_LOG_TEMPLATE.md` → Project `governance/DECISION_LOG.md`

4. **Add project to document registry** (`sdarpp-operations/knowledge-base/document-registry.csv`):
   ```csv
   [PROJECT_ID],projects/[PROJECT_ID],README.md,project,1.0,[DATE],current
   [PROJECT_ID],[GITHUB_URL],governance/DECISION_LOG.md,governance,1.0,[DATE],current
   [PROJECT_ID],[GITHUB_URL],compliance/[COMPLIANCE_FILE].md,compliance,1.0,[DATE],current
   ```

5. **Add cross-repo link** in project `README.md`:
   ```markdown
   **Part of:** [SDARPP Operations Platform](https://github.com/sdarpp-development-os/sdarpp-operations)
   ```

6. **Commit to both repos** with audit trail

---

## Maintenance Responsibilities

### Operations Owner (Company-Level)

- **Quarterly:** Review all projects' governance documents for template violations
- **Monthly:** Audit `compliance-register/` for stale project baselines
- **As-needed:** Update master templates when best practices evolve
- **Monthly:** Synthesize cross-project lessons into operations README and playbooks

### Project Team (Project-Level)

- **After each meeting:** Update `governance/FOLLOW_UP_REGISTER.md` and trigger action item extraction
- **When decisions made:** Log in `governance/DECISION_LOG.md`
- **Weekly:** Scan `governance/RISK_REGISTER.md` for status changes
- **Monthly:** Notify operations if compliance baseline assessment updates

### Both

- **Governance Drift Check (Automatic):** Both repos run CI that ensures governance docs are updated when domain files change
- **Bi-directional Linking:** Maintain active cross-references between operations and projects
- **Version Control:** All updates committed with clear messages and audit trail

---

## FAQ

### Q: What if a project repo has different governance needs?

**A:** Extend operations templates, don't replace them. Example:
```
Project needs "Executive Briefing" template
→ Create: governance/EXECUTIVE_BRIEFING_TEMPLATE.md in project
→ If successful in multiple projects, push back to operations
→ Add to operations/templates/governance/
```

### Q: How often should projects sync with operations templates?

**A:** 
- **Mandatory:** When CI detects template structure violations
- **Recommended:** Monthly, during compliance audit cycle
- **Check-ins:** When major project milestone is reached (stage gate)

### Q: What if operations templates are updated?

**A:**
1. Operations notifies project teams (GitHub issue or email)
2. Projects adopt updated templates in next cycle
3. If backward-compatible: existing project docs stay current
4. If breaking change: operations provides migration guide

### Q: Can a project override a template?

**A:** Yes, if documented and approved:
1. Project creates variation (e.g., `RISK_REGISTER_EXTENDED.md`)
2. Commits decision to `governance/decision_log.md` with rationale
3. Operations owner approves deviation (CI check)
4. If multiple projects need variation → elevate to operations template

---

## Tools & Integration

### GitHub Actions

**In Operations:**
- `compliance-drift-check.yml` — Validates compliance matrix coherence
- `document-registry-validate.yml` — Ensures all listed documents exist

**In Projects:**
- `governance_check.yml` — Validates mandatory governance files present
- `governance_drift.yml` — Ensures domain file changes → decision_log updates
- `extract_action_items.yml` — Parses meeting notes → populates FOLLOW_UP_REGISTER

### CI Enforcements

| Rule | Trigger | Action |
|------|---------|--------|
| **Governance Sync** | Push to `governance/` | Check decision_log.md exists |
| **Template Structure** | Change to governance docs | Validate YAML/Markdown structure matches template |
| **Compliance Link** | Change to `compliance/` | Verify entries exist in compliance-register baseline |
| **Registry Currency** | Update document-registry.csv | Validate all listed docs exist and are current |

---

## Versioning

**Template versions** follow `MAJOR.MINOR` format:
- `1.0` — Initial release
- `1.1` — Non-breaking update (added optional field)
- `2.0` — Breaking change (renamed section, removed field)

**Projects use latest template version** unless explicitly frozen for a reason (documented in decision_log.md).

---

## Contact & Governance

- **Operations Owner:** [Project Director]
- **Compliance Audit:** Monthly, by SDARPP Compliance Officer
- **Template Review:** Quarterly, with input from all active projects
- **Escalations:** Cross-repo issues logged as GitHub issues in operations repo with `[PROJECT_ID]` label

---

*Last Updated:* 6 April 2026  
*Version:* 1.0
