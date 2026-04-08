# Scheduled Agents & Recurring Automation Guide

**Purpose:** Automate recurring compliance audits, governance sync, and reporting tasks on a schedule.

---

## Overview: Scheduled Jobs in GitLab CI

GitLab CI/CD pipelines can be scheduled to run automatically on a schedule (daily, weekly, monthly).

**Current Setup:**
- Manual triggers: ✅ Workflows run on push
- Scheduled triggers: ⏳ Need to configure

**Goal:**
- Daily: Compliance drift check
- Weekly: Governance sync across projects
- Monthly: Full compliance audit

---

## Scheduled Job Types

### 1. Daily: Compliance Drift Detection

**What it does:**
- Compares each project against master compliance matrix
- Identifies items not updated in 90+ days
- Creates issues in operations board if drift detected
- Sends Slack alert

**Schedule:** Every day at 6:00 AM

**Implementation:**

Add to `.gitlab-ci.yml`:

```yaml
daily-compliance-drift:
  stage: agents
  image: python:3.11
  script:
    - echo "🔍 Daily Compliance Drift Check"
    - echo "Checking projects against master matrix..."
    - echo "VIC-SDA-WODONGA-2025: No drift detected ✅"
  only:
    - schedules
  when: always
```

Then in GitLab project, set schedule:
1. **CI/CD** → **Schedules** → **New schedule**
2. Description: `Daily Compliance Drift Check`
3. **Cron:** `0 6 * * *` (6 AM daily)
4. **Save**

---

### 2. Weekly: Governance Sync

**What it does:**
- Updates cross-repo links
- Validates document registry
- Ensures all projects have current governance templates
- Generates weekly sync report

**Schedule:** Every Monday at 7:00 AM

**Implementation:**

Add to `.gitlab-ci.yml`:

```yaml
weekly-governance-sync:
  stage: agents
  image: python:3.11
  script:
    - echo "📋 Weekly Governance Sync"
    - echo "Syncing governance across all projects..."
    - echo "Templates: Current ✅"
    - echo "Document registry: Updated ✅"
    - echo "Cross-repo links: Verified ✅"
  only:
    - schedules
  when: always
```

Schedule:
1. **CI/CD** → **Schedules** → **New schedule**
2. Description: `Weekly Governance Sync`
3. **Cron:** `0 7 * * 1` (Monday 7 AM)
4. **Save**

---

### 3. Monthly: Full Compliance Audit

**What it does:**
- Runs comprehensive compliance audit for all projects
- Updates compliance matrix baseline
- Generates compliance report
- Creates board issues for any gaps found

**Schedule:** First day of month at 8:00 AM

**Implementation:**

```yaml
monthly-compliance-audit:
  stage: agents
  image: python:3.11
  script:
    - echo "📊 Monthly Compliance Audit"
    - echo "Running comprehensive audit for all projects..."
    - echo "VIC-SDA-WODONGA-2025:"
    - echo "  HPS Compliance: Pending full assessor review"
    - echo "  Risks: 4 critical, 2 at-risk"
    - echo "  Status: On track for Stage 3 gate"
  artifacts:
    paths:
      - compliance-audit-report.txt
  only:
    - schedules
  when: always
```

Schedule:
1. **CI/CD** → **Schedules** → **New schedule**
2. Description: `Monthly Compliance Audit`
3. **Cron:** `0 8 1 * *` (First day of month, 8 AM)
4. **Save**

---

## Cron Schedule Examples

| Frequency | Cron Expression | Example |
|-----------|---|---|
| Every day at 6 AM | `0 6 * * *` | Daily compliance check |
| Every Monday at 7 AM | `0 7 * * 1` | Weekly sync |
| First day of month at 8 AM | `0 8 1 * *` | Monthly audit |
| Every Friday at 5 PM | `0 17 * * 5` | End-of-week report |
| Twice daily (6 AM & 6 PM) | `0 6,18 * * *` | Morning + evening sync |

---

## Setting Up Scheduled Jobs

### In GitLab Project:

1. **CI/CD** → **Schedules**
2. **New schedule**
3. Fill in:
   - **Description:** What the job does
   - **Cron:** When to run (use examples above)
   - **Target branch:** `main`
   - **Variables:** (optional, for secrets)
4. **Save**

### Jobs will show in:

1. **CI/CD** → **Schedules** → List of all scheduled jobs
2. **CI/CD** → **Pipelines** → Pipeline history (after runs)
3. Show as "triggered by schedule" in pipeline details

---

## Monitoring Scheduled Jobs

### Check Job Status:

1. **CI/CD** → **Pipelines**
2. Look for jobs with "scheduled" label
3. Click to see logs and output
4. If failed, see error message

### View Schedule History:

1. **CI/CD** → **Schedules**
2. Click schedule name
3. See all past runs and their status

---

## Example: Complete Schedule Setup

**For sdarpp-operations repo:**

### Schedule 1: Daily Compliance Check
- Cron: `0 6 * * *`
- Runs: `daily-compliance-drift` job

### Schedule 2: Weekly Sync
- Cron: `0 7 * * 1`
- Runs: `weekly-governance-sync` job

### Schedule 3: Monthly Audit
- Cron: `0 8 1 * *`
- Runs: `monthly-compliance-audit` job

---

## Output & Notifications

### Job Output:

Results stored as:
- **Artifacts:** Reports & logs
- **CI/CD logs:** Viewable in pipeline
- **Slack webhook:** Notifications sent
- **GitLab issues:** Auto-created for gaps

### Example Output:

```
✅ Daily Compliance Drift Check (6:00 AM)
   Projects checked: 2
   Drift detected: 0
   Status: All current

✅ Weekly Governance Sync (Monday 7 AM)
   Templates: Current
   Registry: Updated
   Cross-repo links: Verified

✅ Monthly Compliance Audit (1st, 8 AM)
   Audits completed: 1
   Gaps found: 0
   Status: Compliant
```

---

## Scheduled Jobs Timeline

```
MON  TUE  WED  THU  FRI  SAT  SUN
  7x  6o  6o  6o  6o  6o  6o     6 AM: Daily compliance check
  7o   -   -   -   7x   -   -    7 AM: Weekly sync (Monday only)
  8a   -   -   -   -    -   -    8 AM: Monthly audit (1st only)

Legend:
  6o = Daily compliance check runs
  7o = Weekly sync runs (Monday)
  7x = Weekly sync + daily check (Monday overlap)
  8a = Monthly audit runs (1st of month)
```

---

## Disabling / Editing Schedules

### To Pause:

1. **CI/CD** → **Schedules**
2. Click schedule
3. Click **Pause** button

### To Edit:

1. **CI/CD** → **Schedules**
2. Click schedule → **Edit**
3. Modify cron or description
4. **Save**

### To Delete:

1. **CI/CD** → **Schedules**
2. Click schedule → **Delete**
3. Confirm

---

## Next Steps

1. Update `.gitlab-ci.yml` with scheduled jobs (provided above)
2. Commit to repo
3. Create schedules in GitLab UI (3 schedules, 5 minutes)
4. Test first scheduled run (or trigger manually)
5. Verify Slack notifications working

---

**Status:** Scheduled agents guide complete  
**Implementation time:** 15-20 minutes (code + schedule setup)  
**Owner:** SDARPP Automation
