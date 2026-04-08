# GitLab Project Boards Setup — Company Operations

**Purpose:** Company-level board for cross-project governance, compliance tracking, and operational oversight.

---

## Master Board: SDARPP Operations

### Setup Steps

1. **Go to GitLab Project** → `sdarpp-operations`
2. **Left Sidebar** → **Planning** → **Boards**
3. **Create board:**
   - Board name: **`SDARPP Operations Master`**
   - Scope: **Project board**
   - Click **Create**

---

## Workflow Lists (Company-Level)

### List 1: 📊 Governance Updates
```
Label: governance
WIP Limit: 10
```

### List 2: 🔄 Compliance Audits
```
Label: compliance-audit
WIP Limit: 3
```

### List 3: 👥 Project Registration
```
Label: project-registration
WIP Limit: 5
```

### List 4: 📋 Template Updates
```
Label: template-update
WIP Limit: 5
```

### List 5: ✅ Completed
```
Label: complete
WIP Limit: ∞
```

---

## Company-Level Labels

| Label | Purpose |
|-------|---------|
| `governance` | Governance doc updates |
| `compliance-audit` | Compliance matrix reviews |
| `project-registration` | New project onboarding |
| `template-update` | Template creation/revision |
| `cross-project-sync` | Issues affecting multiple projects |
| `critical` | Urgent company-level decisions |
| `documentation` | Docs and guides |
| `complete` | Finished items |

---

## Company Milestones

| Milestone | Purpose |
|-----------|---------|
| **Q2 2026 Operations** | Apr-Jun quarterly review |
| **Project Registration: VIC-SDA-WODONGA-2025** | Day Street project setup |
| **Template Library v1.0** | Complete governance templates |
| **Compliance Matrix v1.1** | SDA compliance framework |
| **Multi-Project Sync** | Cross-repo synchronization |

---

## Example Issues for Operations Board

### Governance
```
Title: [Governance] Update cross-repo sync documentation
Label: governance
Milestone: Q2 2026 Operations
```

### Compliance
```
Title: [Compliance] Audit VIC-SDA-WODONGA-2025 baseline
Label: compliance-audit
Milestone: Q2 2026 Operations
Assignee: Compliance Officer
```

### Project Registration
```
Title: [Registration] Onboard WA-SDA-PERTH-2024 project
Label: project-registration
Milestone: Project Registration: WA-SDA-PERTH-2024
```

### Template Updates
```
Title: [Templates] Create planning validation template
Label: template-update
Milestone: Template Library v1.0
```

---

## Board Features

### WIP Limits (Work in Progress)

Limits on how many items can be in each stage:
- Prevents overload
- Encourages completion
- Board shows warning when limit exceeded

Example:
- **In Progress**: Max 3 items (focus)
- **In Review**: Max 5 items (prevents bottleneck)
- **Done**: Unlimited (completed work)

### Milestones

Filter board by milestone:
1. Board top bar → **Milestone**
2. Select company milestone
3. Shows only issues for that milestone

### Assignees

Assign company-level owners:
- Compliance Officer → Compliance audits
- Project Director → Project registration
- Documentation Owner → Template updates

---

## Sync with Day Street Board

### Cross-Project Links:

Day Street issues can reference company board:
```
Company Epic: sdarpp-operations#[issue-number]
```

Example:
```
Day Street Issue: Massing study validation
Related: sdarpp-operations#42 (Compliance baseline audit)
```

---

## Monthly Review Cycle

### Every Month:

1. **Week 1:** Update company milestones based on project status
2. **Week 2:** Review compliance audit board
3. **Week 3:** Complete governance updates
4. **Week 4:** Close completed items, plan next month

---

## Access & Permissions

### Board Visibility:

- **Private**: Only team members see board
- **Public**: Anyone can view (good for transparency)

Recommend: **Private** for company ops, **Public** for Day Street (client transparency)

---

## Integrations

### GitHub Issues

GitLab boards can link to GitHub issues:
```
In GitLab issue description:
GitHub: sdarpp-development-os/project_day_st_wodonga#123
```

### Slack Integration (Optional)

Enable Slack notifications for board updates:
1. **Project Settings** → **Integrations** → **Slack**
2. Connect Slack workspace
3. Enable notifications for board updates

---

**Status:** Company board setup ready  
**Time to complete:** 10-15 minutes  
**Next:** Create both boards and populate with example issues
