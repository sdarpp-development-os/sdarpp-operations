# SDARPP Operations Platform

Fortune 100-grade operations infrastructure for multi-jurisdictional NDIS Specialist Disability Accommodation (SDA) and healthcare real estate development across NSW, Victoria, Western Australia, and South Australia.

## 🏢 Company

**SDARPP** (Specialist Disability Accommodation Real Estate Portfolio Platform)
- NDIS SDA provider registration: NSW, VIC, WA, SA
- Project types: NDIS SDA accommodation, hospital outpatient facilities, VMO clinics, aged care
- Operating model: AI-driven compliance, feasibility analysis, and project governance

---

## 📁 Repository Structure

### knowledge-base/
Curated regulatory and technical reference corpus for all projects:
- **ndis-sda-design-standard/** — SDA Design Standard 2021 implementation guidance
- **state-planning/** — State-specific planning control matrices (NSW, VIC, WA, SA)
- **aged-care/** — Aged Care Quality Standards reference
- **document-registry.csv** — Master index of all project documents on OneDrive

### templates/
Production-ready templates and prompts:
- **agent-prompts/** — AI agent instruction sets (compliance, feasibility, planning, reporting)
- **governance/** — Risk register, decision log, weekly summary templates
- **project-setup/** — New project checklist and folder structure specification

### automation/
AI agent contracts and operational scripts:
- **agents/** — Agent contracts and governance rules (master, compliance, feasibility, planning, reporting)
- **scripts/** — Python/Bash automation (OneDrive indexer, document router, validator)
- **hooks/** — Pre-commit and post-push Git hooks

### compliance-register/
Compliance matrices and status tracking:
- **ndis-sda-compliance-matrix.md** — SDA Design Standard checklist
- **provider-registration-status.md** — NDIS provider conditions tracking
- **state-planning-conditions-status.md** — Planning approval conditions by project

### projects/
Per-project governance and coordination:
- Each active project has a sub-folder with governance, planning, SDA, and AI output folders
- README.md in each project links to the GitHub project repo and OneDrive folder for detailed documents

---

## 📊 Active Projects

| Project ID | Location | Status | Repository | Director |
|-----------|----------|--------|-----------|----------|
| **VIC-SDA-WODONGA-2025** | Wodonga VIC | Stage 3 (Design & Cost Alignment) | [project_day_st_wodonga](https://github.com/sdarpp-development-os/project_day_st_wodonga) | Sugi Gunamijaya |

**Project Details:** See [`projects/VIC-SDA-WODONGA-2025/README.md`](projects/VIC-SDA-WODONGA-2025/README.md)

---

## 🤖 AI Agent Automation

### Weekly Governance Summary
Runs **Monday 07:00 AEDT** via GitHub Actions:
- Aggregates risk register, decision log, and project status changes
- Generates human-readable weekly summary
- Opens PR for review before merge

### Compliance Drift Detection
Runs **weekly** via GitHub Actions:
- Compares each project's SDA checklist to master compliance matrix
- Flags items not updated in 90+ days
- Raises GitHub Issues for remediation

### Knowledge Base Sync
Triggers **on push** to knowledge-base/:
- Validates document-registry.csv structure
- Updates project index
- Notifies relevant agents of content updates

### Document Registry Validation
Triggers **on push** to knowledge-base/:
- Validates OneDrive paths and document metadata
- Checks for broken links or missing files
- Flags stale or superseded documents

---

## 🗂️ File Structure Reference

```
sdarpp-operations/
├── .github/workflows/              ← GitHub Actions
├── knowledge-base/                 ← Regulatory & technical reference
├── templates/                      ← AI prompts & governance templates
├── automation/                     ← Agent contracts & scripts
├── compliance-register/            ← Status matrices
├── projects/                       ← Per-project coordination
└── README.md
```

---

## 🚀 Quick Start

### For New Projects
1. Copy `templates/project-setup/new-project-checklist.md`
2. Follow checklist to create `projects/[project-id]/` folder
3. Reference `templates/project-setup/project-folder-structure-spec.md`
4. Trigger document indexing: `scripts/build-onedrive-index.py`

### For AI Agents
1. Read relevant agent contract in `automation/agents/`
2. Access knowledge base at `knowledge-base/`
3. Reference templates in `templates/agent-prompts/`
4. Write outputs to designated OneDrive folder via document router

### For Compliance Review
1. Check `compliance-register/` matrices
2. Reference `knowledge-base/ndis-sda-design-standard/`
3. Review project checklists in `projects/[project-id]/sda/`

---

## 📋 Key Abbreviations

| Abbreviation | Meaning |
|---|---|
| SDA | Specialist Disability Accommodation |
| NDIS | National Disability Insurance Scheme |
| DA | Development Application |
| LEP | Local Environmental Plan (NSW) |
| DCP | Development Control Plan (NSW) |
| EPA Act | Environmental Planning & Assessment Act 1979 (NSW) |
| NCC | National Construction Code |
| ASIC | Australian Securities & Investments Commission |
| VMO | Visiting Medical Officer |
| TGA | Therapeutic Goods Administration |
| AHPRA | Australian Health Practitioner Regulation Agency |

---

## 🔐 Security & Access

- **Public:** Knowledge base, templates, compliance matrices
- **Private:** Project details, agent outputs, financial summaries (stored on OneDrive, not GitHub)
- **GitHub Actions:** Credential-free automation using OneDrive local mount path
- **Document Registry:** CSV index links GitHub content to OneDrive storage

---

## 📞 Support

For project-specific questions: Check `projects/[project-id]/README.md`  
For regulatory questions: Check `knowledge-base/` and `compliance-register/`  
For automation issues: Check `automation/` folder and relevant agent contract

---

**Last Updated:** 2026-04-05  
**Version:** 1.0  
**Managed by:** SDARPP Operations Team
