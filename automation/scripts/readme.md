# SDARPP Automation Scripts

Production-ready scripts for SDARPP operations automation, document management, and compliance monitoring.

## Scripts

### 1. build-onedrive-index.py
**Purpose:** Scan OneDrive and generate master document registry

**Usage:**
```bash
python build-onedrive-index.py [--onedrive-path PATH] [--output FILE]
```

**What it does:**
- Recursively scans `05. SDARPP Operations` folder
- Extracts document metadata (path, type, version, date)
- Generates/updates `knowledge-base/document-registry.csv`
- Classifies documents by type (compliance, regulatory, template, etc.)

**Output:** `knowledge-base/document-registry.csv`

**Example:**
```bash
python build-onedrive-index.py \
  --onedrive-path ~/Library/CloudStorage/OneDrive-SDArpp \
  --output knowledge-base/document-registry.csv
```

---

### 2. document-intake-router.py
**Purpose:** Route documents from intake queue to project folders

**Usage:**
```bash
python document-intake-router.py [--watch] [--intake-path PATH]
```

**What it does:**
- Monitors `07. AI Agent Workspace/01. Inputs/document-queue/`
- Extracts project ID from filename (e.g., `VIC-SDA-WODONGA-2025_compliance-audit.md`)
- Routes document to correct project `ai-outputs/` folder
- Falls back to `07. AI Agent Workspace/04. Outputs — Generated/` for system documents
- Updates document registry with location

**Input:** Documents placed in `document-queue/` with naming convention:
- `[PROJECT-ID]_[description].md` → routes to project
- `[description].md` → routes to general outputs

**Output Destinations:**
- Project documents: `projects/[PROJECT-ID]/ai-outputs/`
- General outputs: `07. AI Agent Workspace/04. Outputs — Generated/`

**Example:**
```bash
python document-intake-router.py
```

---

### 3. validate-project-structure.sh
**Purpose:** Validate all projects follow universal folder template

**Usage:**
```bash
./validate-project-structure.sh [--fix] [--project-path PATH]
```

**What it does:**
- Scans all projects in `03–06. Projects — [STATE]/`
- Verifies all 9 lifecycle stages exist:
  - 00. Project Administration
  - 01. Acquisition
  - 02. Due Diligence
  - 03. Planning — DA & Approvals
  - 04. Design
  - 05. Procurement & Contracts
  - 06. Construction
  - 07. Operations & SDA Management
  - 08. Financials — Development
- Verifies Project Administration subfolders (Brief, Contacts, Decision Log, Risk Register, Meeting Notes)
- Reports missing folders

**Flags:**
- `--fix` → Automatically create missing folders
- `--project-path PATH` → Validate specific project

**Output:**
```
✅ Project is VALID
❌ MISSING: [Stage Name]
⚠️  Project has MISSING folders (run with --fix to create)
```

**Example:**
```bash
# Check all projects
./validate-project-structure.sh

# Fix missing folders
./validate-project-structure.sh --fix
```

---

### 4. generate-weekly-summary.sh
**Purpose:** Generate weekly governance summary (Monday 07:00 AEDT)

**Usage:**
```bash
./generate-weekly-summary.sh
```

**What it does:**
- Scans all projects for changes in past 7 days
- Extracts:
  - Decision log entries
  - Risk register updates
  - Project status changes
- Generates `weekly-summary-YYYY-MM-DD.md` in each project
- Creates GitHub PR for human review (via GitHub Actions)

**Output:** `projects/[PROJECT-ID]/governance/weekly-summary-YYYY-MM-DD.md`

**Runs Automatically:** Monday 07:00 AEDT via `.github/workflows/weekly-governance-summary.yml`

**Example:**
```bash
./generate-weekly-summary.sh
```

---

### 5. compliance-drift-check.sh
**Purpose:** Detect stale compliance checklists (weekly)

**Usage:**
```bash
./compliance-drift-check.sh
```

**What it does:**
- Scans all projects' `sda/sda-compliance-checklist.md`
- Identifies items not updated in 90+ days
- Detects missing checklist items
- Reports findings

**Thresholds:**
- **Stale:** Not modified in 90+ days
- **Missing:** Fewer than 30 items when standard has ~30

**Output:** GitHub Issues (raised automatically when drift detected)
```
[COMPLIANCE DRIFT] SDA Design Standard Compliance — YYYY-MM-DD
Stale items: N
Missing items: M
```

**Runs Automatically:** Weekly (Wednesday 09:00 AEDT) via `.github/workflows/compliance-drift-check.yml`

**Example:**
```bash
./compliance-drift-check.sh
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ONEDRIVE_PATH` | OneDrive mount path | `~/Library/CloudStorage/OneDrive-SDArpp/05. SDARPP Operations` |
| `INTAKE_PATH` | Document intake queue path | `[ONEDRIVE]/07. AI Agent Workspace/01. Inputs/document-queue` |

**Example:**
```bash
export ONEDRIVE_PATH=~/Library/CloudStorage/OneDrive-SDArpp
python build-onedrive-index.py
```

---

## Automation Schedule

| Script | Trigger | Frequency | Time | Status |
|--------|---------|-----------|------|--------|
| **Weekly Summary** | GitHub Actions | Weekly | Monday 07:00 AEDT | Active |
| **Compliance Drift** | GitHub Actions | Weekly | Wednesday 09:00 AEDT | Active |
| **Knowledge Base Sync** | GitHub Actions | On push | Immediate | Active |
| **Document Registry Validate** | GitHub Actions | On push | Immediate | Active |
| **Build OneDrive Index** | Manual | As needed | — | Manual |
| **Document Router** | Manual | As needed | — | Manual |
| **Validate Structure** | Manual | Monthly | — | Manual |

---

## Error Handling

### Common Issues

**"OneDrive path not found"**
```bash
# Check your OneDrive mount path
ls ~/Library/CloudStorage/
# Update ONEDRIVE_PATH environment variable
export ONEDRIVE_PATH=~/Library/CloudStorage/[YourOneDrivePath]
```

**"Permission denied" on scripts**
```bash
# Make scripts executable
chmod +x *.sh *.py
```

**"Registry CSV not found"**
```bash
# Run index builder first
python build-onedrive-index.py
```

**"Project folder not found for routing"**
```bash
# Validate project structure
./validate-project-structure.sh --fix
```

---

## Development & Testing

### Local Testing

```bash
# Test with specific project
./validate-project-structure.sh --project-path ~/Library/CloudStorage/OneDrive-SDArpp/'05. SDARPP Operations/04. Projects — VIC/VIC-SDA-WODONGA-2025'

# Generate test summary
./generate-weekly-summary.sh

# Check compliance drift
./compliance-drift-check.sh
```

### Logging

All scripts output results to stdout. Redirect to log file:

```bash
./validate-project-structure.sh >> project-validation-$(date +%Y-%m-%d).log 2>&1
```

---

## Next Steps

1. **Schedule scripts** in your cron/task scheduler
2. **Test manually** before relying on automation
3. **Monitor logs** for errors or drift detection
4. **Review outputs** from GitHub Actions workflows

---

**Version:** 1.0  
**Last Updated:** 2026-04-05  
**Managed By:** SDARPP Operations Team
