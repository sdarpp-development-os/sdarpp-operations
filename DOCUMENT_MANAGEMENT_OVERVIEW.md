# Document Management Overview — SDARPP Operations

**Prepared:** 08 April 2026  
**Owner:** Sugi Gunamijaya  
**Purpose:** Define a single, lean document management system — eliminate duplication, clarify where everything lives, and reduce AI processing overhead.

---

## The Problem (Current State)

You currently have **4 parallel systems** all receiving the same information:

```
📁 OneDrive/05. SDARPP Operations/    ← Operational documents
📁 GitHub/sdarpp-operations/          ← Platform code + ops
📁 GitHub/project_day_st_wodonga/     ← Project-specific wiki + Hermes
📁 GitLab (mirror)                    ← Duplicate of GitHub
```

**Duplication identified:**
| Content | Where It Exists (Duplicate) |
|---------|---------------------------|
| Project documents (VIC-SDA-WODONGA-2025) | OneDrive AND GitHub/sdarpp-operations AND GitHub/project_day_st_wodonga |
| Governance/decisions | OneDrive AND GitHub/governance/ AND GitHub/wiki/decisions.md |
| AI Automation inbox | OneDrive/AI Automation/In/ AND local /raw/ (just created) |
| Templates | OneDrive/02. Templates Library AND GitHub/sdarpp-operations/templates/ |
| Knowledge base | OneDrive/01. Knowledge Base AND GitHub/sdarpp-operations/knowledge-base/ |

**Result:** You process every document 3–4 times. AI agents don't know which copy is current.

---

## The Solution (Target State) — 3-Layer System

```
LAYER 1: FILES        → OneDrive (all rich documents)
LAYER 2: CODE + WIKI  → GitHub (all code, config, structured text)
LAYER 3: VISUAL       → Planner + Sheets (view only — not a source of truth)
```

**One rule:** Every document has exactly ONE home. Everything else is a link or a reference to that home.

---

## Layer 1: OneDrive — Master Document Store

**What lives here:** Word, Excel, PDF, PowerPoint, drawings, photos, scanned documents  
**Who accesses it:** You, consultants (via shared folder links), financial partners  
**Why here and not GitHub:** Rich file formats, consultant-friendly sharing (no GitHub account needed), M365 Business backup and version history

### Canonical OneDrive Structure

```
📁 05. SDARPP Operations/
├── 📁 00. Company Administration/     ← ACN, ASIC, legal entity docs
├── 📁 01. Knowledge Base/             ← Reference library (NDIS, planning, healthcare)
│   ├── 01. Design Excellence
│   ├── 02. NDIS Regulatory Framework
│   ├── 03. State Planning Frameworks
│   ├── 04. Healthcare & Care Regulations
│   ├── 05. Building & Construction Standards
│   ├── 06. Market Intelligence
│   └── 07. AI Agent Reference Corpus    ← Source docs for AI context
├── 📁 02. Templates Library/          ← Master templates (never project-specific)
│   ├── 01. Project Initiation
│   ├── 02. Feasibility & Financial
│   ├── 03. Legal & Agreements
│   ├── 04. Planning & Design
│   ├── 05. Governance & Reporting
│   ├── 06. Correspondence
│   └── 07. AI Agent Prompts Library
├── 📁 03. Projects — NSW/
├── 📁 04. Projects — VIC/
│   └── 📁 VIC-SDA-WODONGA-2025/
│       ├── 📁 00. Project Administration/
│       ├── 📁 01. Acquisition/
│       ├── 📁 02. Due Diligence/
│       ├── 📁 03. Planning — DA & Approvals/
│       │   ├── 01. Pre-DA
│       │   ├── 02. DA Preparation
│       │   ├── 03. DA Lodgement
│       │   ├── 04. Approval & Conditions
│       │   └── 05. Post-DA Modifications
│       ├── 📁 04. Design & Construction/
│       ├── 📁 05. Finance & Feasibility/
│       └── 📁 06. Consultant Deliverables/   ← Massing study, structural audit, etc.
└── 📁 _AI_AUTOMATION/                ← Hermes document inbox/outbox
    ├── 📁 IN/                         ← Drop files here for Hermes to process
    └── 📁 OUT/                        ← Hermes-processed archive
```

### AI Automation Folder — The Single /raw/ Inbox

**Stop using:** Local `/raw/` folder (created today — to be retired)  
**Use instead:** OneDrive `_AI_AUTOMATION/IN/`

This is accessible from any device, syncs to your Mac automatically via OneDrive desktop app, and consultants can drop files directly if you share the folder link with them.

**Naming convention (same as /raw/):**
```
YYYY-MM-DD_type_source_description.ext
```

**Hermes trigger:** "Hermes, process OneDrive/_AI_AUTOMATION/IN/"

---

## Layer 2: GitHub — Code, Config & Wiki

**What lives here:** Markdown wiki, AGENTS.md, automation scripts, CI/CD, structured project state  
**Who accesses it:** You, AI agents (Hermes, Claude), automation pipelines  
**Why here and not OneDrive:** Version control, AI-readable markdown, automation triggers, GitLab sync

### Two-Repo Rule

You have two GitHub repos that touch the same project. Each has ONE distinct job:

#### Repo 1: `sdarpp-operations` — Platform & Operations

**Job:** Cross-project platform. Templates, automation, knowledge base metadata, governance standards.  
**Does NOT contain:** Project-specific decisions, meeting notes, budgets.

```
📁 sdarpp-operations/
├── automation/
│   ├── agents/        ← AI agent configurations (platform-level)
│   ├── scripts/       ← Shared automation scripts
│   └── hooks/         ← Git hooks
├── governance/        ← Cross-project governance policies
├── knowledge-base/    ← Metadata index pointing to OneDrive/01. Knowledge Base/
├── templates/         ← Markdown template files (mirrors OneDrive/02. Templates Library/)
├── compliance-register/
├── projects/
│   └── VIC-SDA-WODONGA-2025/  ← Pointer only (README + link to project repo)
├── AGENTS.md          ← Platform-level Hermes config (if applicable)
└── DOCUMENT_MANAGEMENT_OVERVIEW.md   ← This file
```

#### Repo 2: `project_day_st_wodonga` — Project-Specific Wiki

**Job:** Single source of truth for Day Street Wodonga project state.  
**Does NOT contain:** Rich files (PDFs, Word docs) — those live in OneDrive.

```
📁 project_day_st_wodonga/
├── wiki/
│   ├── index.md              ← Navigation hub
│   ├── project_state.md      ← Current status, milestones, active decisions
│   ├── schedule.md           ← Timeline, critical path
│   ├── decisions.md          ← Decision log with IDs and rationale
│   ├── risks.md              ← Risk register
│   ├── budget.md             ← Pro-forma, actuals, variances
│   ├── planning_constraints.md
│   └── stakeholder_list.md
├── AGENTS.md                 ← Hermes configuration
├── raw/ → RETIRE (redirect to OneDrive/_AI_AUTOMATION/IN/)
└── archive/ → RETIRE (redirect to OneDrive/_AI_AUTOMATION/OUT/)
```

### GitLab — Mirror Only (Passive)

**Job:** Automated mirror of GitHub. Nothing is created or edited directly in GitLab.  
**Action required:** None. Ensure the GitLab mirror webhook is active and stop thinking of it as a separate source.

---

## Layer 3: Visual Management — View Only

**What lives here:** Task status, Gantt bars, dashboard charts  
**Who accesses it:** You, co-investors (read-only dashboard link)  
**Rule:** These tools NEVER contain unique information. They are visual representations of what's already in OneDrive (Layer 1) or GitHub (Layer 2).

| Tool | Visual Purpose | Data Source |
|------|---------------|-------------|
| Microsoft Planner | Kanban + Task List + Timeline | Manually synced from wiki/schedule.md |
| Google Sheets | Detailed Gantt | Manually entered from wiki/schedule.md |
| Looker Studio | Dashboard | Connected to Google Sheets |

---

## The New Document Flow (Lean)

### Incoming Document (Invoice, Report, Meeting Notes)

```
📧 Consultant sends document
         ↓
📁 Save to OneDrive/_AI_AUTOMATION/IN/
   (naming: YYYY-MM-DD_type_source_description.ext)
         ↓
🤖 Hermes: "process _AI_AUTOMATION/IN/"
         ↓
┌─────────────────────────────────────────┐
│  Hermes Audit:                           │
│  • Cross-ref against wiki/budget.md      │
│  • Update wiki/ sections on GitHub       │
│  • Move file to _AI_AUTOMATION/OUT/      │
│  • Report findings (approved/flagged)    │
└─────────────────────────────────────────┘
         ↓
📝 GitHub wiki updated (project_state.md, decisions.md, etc.)
         ↓
📊 Manually update Planner task + Sheets (visual sync)
```

### Creating a New Project Document

```
❓ Need a brief / memo / letter?
         ↓
Open OneDrive/02. Templates Library/  ← Start from template
         ↓
Save to correct project folder:
   OneDrive/04. Projects — VIC/VIC-SDA-WODONGA-2025/{category}/
         ↓
If it contains a decision → also update GitHub wiki/decisions.md
If it contains a milestone → also update GitHub wiki/schedule.md
```

### Reference Material (Knowledge Base)

```
New regulation / planning code / market report
         ↓
Save to OneDrive/01. Knowledge Base/{category}/
         ↓
Update GitHub knowledge-base/index.md with pointer
(do NOT duplicate content — just reference the OneDrive path)
```

---

## What to STOP Doing

| Stop | Replace With |
|------|-------------|
| ❌ Saving project docs to both OneDrive AND GitHub | ✅ OneDrive = rich files; GitHub = markdown wiki only |
| ❌ Using local `/raw/` folder | ✅ OneDrive `_AI_AUTOMATION/IN/` |
| ❌ Editing anything directly in GitLab | ✅ GitLab is mirror only — edit in GitHub |
| ❌ Duplicating templates in OneDrive AND GitHub | ✅ OneDrive = master templates; GitHub templates/ = markdown versions only |
| ❌ Treating Planner/Sheets as a source of truth | ✅ Visual layer only — wiki is truth |
| ❌ Creating meeting notes in multiple places | ✅ One place: OneDrive → processed by Hermes → wiki updated |

---

## What to KEEP Doing

| Keep | Why |
|------|-----|
| ✅ OneDrive curated folder structure | Already well-organised — just clarify the AI_AUTOMATION inbox |
| ✅ GitHub `project_day_st_wodonga/wiki/` | Hermes source of truth is working |
| ✅ GitLab mirror | Good CI/CD safety net |
| ✅ AGENTS.md + Hermes workflow | The compound loop is the right architecture |
| ✅ Naming convention on raw files | Already defined — extend to OneDrive |

---

## Duplicate Cleanup Actions (One-Time)

### Immediate (This Week)
- [ ] **Retire local `/raw/`** — redirect Hermes to `OneDrive/_AI_AUTOMATION/IN/`
- [ ] **Retire local `/archive/`** — redirect Hermes output to `OneDrive/_AI_AUTOMATION/OUT/`
- [ ] **Clean `sdarpp-operations/projects/VIC-SDA-WODONGA-2025/`** — replace content with a README that points to `project_day_st_wodonga` repo

### Short Term (This Month)
- [ ] **Decide on templates:** Keep markdown templates in `sdarpp-operations/templates/` OR OneDrive only — not both
- [ ] **Merge knowledge-base metadata:** `sdarpp-operations/knowledge-base/` should be an index of OneDrive paths, not duplicate content
- [ ] **Fix OneDrive duplicates** visible in screenshot:
  - Remove `01.\ Project\ Administration` (duplicate of `00. Project Administration`)
  - Remove one of the two `Due Diligence` folders (02 and 03 both appear)

### Ongoing
- [ ] Before saving any document, ask: "Is this Layer 1 (OneDrive) or Layer 2 (GitHub wiki)?"
- [ ] One-sentence test: **Rich file (PDF/Word/Excel) = OneDrive. Structured text (markdown) = GitHub.**

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  WHERE DOES THIS DOCUMENT LIVE?                              │
│                                                             │
│  PDF / Word / Excel / Drawing?  → OneDrive                  │
│  Invoice / Report from consultant? → OneDrive/_AI_AUTO/IN/  │
│  Decision / Risk / Milestone? → GitHub wiki (markdown)       │
│  Automation script / Agent config? → GitHub sdarpp-ops/     │
│  Template? → OneDrive/02. Templates Library/                 │
│  Regulation / Planning code? → OneDrive/01. Knowledge Base/ │
│  Visual task tracking? → Planner / Sheets (view only)        │
│  GitLab? → Never edit here. Mirror only.                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary: Each Tool's Single Job

| Tool | Single Job | Contains | Does NOT Contain |
|------|-----------|----------|-----------------|
| **OneDrive** | Document archive & inbox | All rich files, consultant deliverables, AI inbox | Markdown wiki, code |
| **GitHub / project repo** | Project wiki + agent config | Markdown decisions, risks, schedule, AGENTS.md | PDFs, Word docs |
| **GitHub / sdarpp-operations** | Platform code + ops | Scripts, automation, cross-project governance | Project-specific content |
| **GitLab** | Mirror backup | Exact copy of GitHub | Anything original |
| **Microsoft Planner** | Visual task board | Task status (manually synced) | Nothing unique |
| **Google Sheets** | Gantt chart | Timeline data (manually entered) | Nothing unique |
| **Looker Studio** | Dashboard | Charts (auto from Sheets) | Nothing unique |

---

**Document Owner:** Sugi Gunamijaya / SDArpp PMO  
**Version:** 1.0  
**Next Review:** 30 April 2026 (post-structural audit)
