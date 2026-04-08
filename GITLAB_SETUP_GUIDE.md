# SDARPP Operations — GitHub ↔ GitLab Bidirectional Sync

**Master Repository for Multi-Project Operations**

```
GitHub (PRIMARY SOURCE)
    ↓ Mirror + Sync
GitLab (OPERATING ENGINE)
    ├── Company-level agents
    ├── Cross-project compliance
    ├── Governance automation
    └── Project coordination boards
```

---

## Quick Setup

### 1. GitHub Actions Secrets

**Settings → Secrets and Variables → Actions**

Add three secrets:
- `GITLAB_TOKEN`: Personal access token from GitLab
- `GITLAB_USERNAME`: Your GitLab username
- `GITLAB_PROJECT_ID`: Numeric ID of GitLab project (from project settings)

### 2. GitLab Project Setup

**In GitLab.com:**
1. Create project: `sdarpp-operations`
2. **Settings → Repository → Mirroring**
3. Pull mirror from GitHub: `https://github.com/sdarpp-development-os/sdarpp-operations.git`
4. Trigger "Mirror now"

### 3. GitLab CI/CD Variables

**Settings → CI/CD → Variables**

Add:
- `GITHUB_TOKEN`: GitHub Personal Access Token (repo + workflow scope)

---

## Architecture

| Component | Location | Purpose |
|-----------|----------|---------|
| **Source Code** | GitHub (primary) | Version control, PRs, code review |
| **Templates** | GitHub + GitLab sync | Governance templates for all projects |
| **Compliance** | GitLab (master) | Master compliance matrix + project baselines |
| **Agents** | GitLab CI | Company-level automation (compliance, governance sync) |
| **Boards** | GitLab | Cross-project tracking, project coordination |

---

## Synchronization Flow

```
1. Developer commits to GitHub main
   ↓
2. GitHub Actions triggers sync-to-gitlab.yml
   ↓
3. Commit pushed to GitLab main
   ↓
4. GitLab CI/CD pipeline runs (agents, validation)
   ↓
5. Results pushed back to GitHub (if any updates)
```

---

## Company-Level Agents

**In GitLab CI, runs automatically on push to main:**

1. **Compliance Validation** — Audit all projects against master compliance matrix
2. **Governance Sync** — Ensure templates and cross-repo links are current
3. **Project Coordination** — Update boards and milestone tracking

---

## Project Registration

**When adding new project:**

1. Create folder: `projects/[PROJECT_ID]/README.md`
2. Add to document registry: `knowledge-base/document-registry.csv`
3. Update compliance matrix with baseline
4. Create GitLab project with pull mirror from GitHub

**Example: Day Street**
- Folder: `projects/VIC-SDA-WODONGA-2025/README.md`
- Registry entry: ✓
- Compliance baseline: ✓
- GitLab project: `project_day_st_wodonga`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Mirror not syncing | Check GitHub token has `repo` scope; verify URL format |
| GitLab → GitHub sync fails | Verify GITHUB_TOKEN has `repo` + `workflow` scopes |
| Circular sync conflicts | Workflows already have `paths-ignore` for `.gitlab-ci.yml` |

---

**Status:** Production ready  
**Last Updated:** 2026-04-08  
**Owner:** SDARPP Automation
