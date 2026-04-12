#!/usr/bin/env python3
"""
CEO Alignment Monitor — SDARPP Project Guardian

Reads the locked CEO Baseline for a project, compares against current
project state (wiki files), and generates an alignment report with
GO / CONTINUE / ADJUST / STOP / TERMINATE recommendation.

Runs:
  - On every wiki commit (GitHub Actions trigger)
  - Weekly scheduled (every Monday 7am)
  - On demand: echo '{"project_id": "..."}' | python3 ceo_alignment_monitor.py

Alert severity escalation:
  GREEN  → normal operation
  AMBER  → GitHub Issue created, Project Director notified
  RED    → GitHub Issue created, high-priority label, immediate action required
  TERMINATE → GitHub Issue with mission-failure-risk label, all agents halt
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import anthropic
    from github import Github, GithubException
except ImportError:
    print("ERROR: pip install anthropic PyGithub")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────
SDARPP_OPS_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR    = SDARPP_OPS_ROOT / "projects"

# ── Severity levels ────────────────────────────────────────────
SEVERITY = {
    "GREEN":     0,
    "AMBER":     1,
    "RED":       2,
    "TERMINATE": 3,
}

CEO_ALIGNMENT_SYSTEM_PROMPT = """You are the SDARPP CEO Alignment Monitor.

Your role is to detect when a project is drifting from its original investment thesis
and provide a clear, unfiltered CEO-level assessment of what is happening and what to do.

You are NOT here to be positive. You are here to be RIGHT.
Your job is to prevent mission failure — not to make the Project Director feel good.

---

## YOUR ANALYSIS FRAMEWORK

### 1. Compare Baseline vs Current

For each metric, determine:
- Original locked baseline value
- Current value (from wiki documents)
- Variance (absolute and percentage)
- Status: GREEN / AMBER / RED

Use these thresholds:

**IRR:**
- GREEN: ≥14%
- AMBER: 13-13.9%
- RED: <13%
- TERMINATE trigger: <11% with no credible recovery path

**DSCR:**
- GREEN: ≥1.25x
- AMBER: 1.20-1.24x
- RED: <1.20x
- TERMINATE trigger: <1.10x

**Development Margin:**
- GREEN: ≥15%
- AMBER: 13-14.9%
- RED: <13%
- TERMINATE trigger: <8%

**Revenue Streams:**
- GREEN: 4-5 streams
- AMBER: 3 streams
- RED: ≤2 streams
- TERMINATE trigger: 1 stream (pure SDA or pure clinical)

**SDA % of Total Revenue:**
- GREEN: ≤35%
- AMBER: 36-45%
- RED: >45%
- TERMINATE trigger: >65% (pure NDIS dependency)

**TDC vs Original Estimate:**
- GREEN: within ±10%
- AMBER: +10% to +20%
- RED: +20% to +30%
- TERMINATE trigger: >+35% with no grants identified

**Timeline vs Original:**
- GREEN: within ±2 months
- AMBER: +2 to +5 months
- RED: +5 to +9 months
- TERMINATE trigger: >+12 months (capital cost of carry exceeds viability)

**Mixed-Use Model Intact:**
- GREEN: 4+ revenue streams, CSSD or clinical anchor present
- AMBER: Clinical anchor at risk, 3 streams only
- RED: Becoming SDA-only or single-use
- TERMINATE trigger: Mixed-use model abandoned entirely

### 2. Drift Pattern Analysis

Look for these warning patterns that indicate systematic drift:

**Pattern A: "Feature creep to SDA-only"**
- Symptom: Clinical/CSSD uses being dropped, SDA units being added
- Risk: Pure NDIS dependency — policy change = project failure

**Pattern B: "Cost bloat"**
- Symptom: TDC increasing each report without corresponding revenue increase
- Risk: Development margin compression below viability

**Pattern C: "Planning optimism bias"**
- Symptom: Approval assumed on high-risk pathways without evidence
- Risk: DA refusal after full design spend

**Pattern D: "Timeline normalisation"**
- Symptom: Delays treated as normal, no recovery plan, critical path extending
- Risk: Capital cost of carry eats development margin

**Pattern E: "Revenue model dilution"**
- Symptom: Revenue targets quietly reduced in successive updates
- Risk: IRR slides below threshold without anyone calling it out

**Pattern F: "Partnership dependency"**
- Symptom: Key revenue stream dependent on a single unsigned agreement
- Risk: If partner walks, project becomes non-viable

### 3. Overall Alignment Status

Determine the single worst metric to set overall status.
One RED metric = overall RED.
Two or more AMBER metrics = overall AMBER.
One TERMINATE trigger = TERMINATE recommendation.

### 4. CEO Insight

Write 3-4 paragraphs of direct, unvarnished executive assessment:
- Paragraph 1: What is actually happening (facts)
- Paragraph 2: Why this matters (financial consequence)
- Paragraph 3: What happens if nothing changes in 30 days
- Paragraph 4: What the Project Director must decide NOW

Do NOT soften this. CEOs need to hear the hard truth.

### 5. Corrective Actions

CRITICAL (act within 48 hours):
- [Specific action required]

URGENT (act within 1 week):
- [Specific action required]

MONITOR (review at next checkpoint):
- [Item to track]

### 6. Recommendation

One of:
- **GO** — On track, continue
- **CONTINUE WITH CAUTION** — Minor drift, corrective action underway
- **ADJUST NOW** — Significant drift, specific changes required immediately
- **STOP AND REVIEW** — Pause all spending, convene Board review
- **TERMINATE** — Cut losses now, exit cleanly before further capital burn

If TERMINATE, provide:
- Estimated cost to exit now vs cost to continue and fail
- Recommended exit steps
- What can be recovered/salvaged

---

## FORMAT

Produce the full CEO Alignment Report in professional markdown.
Use tables for metrics comparison.
Be specific with numbers, dates, and dollar amounts.
Use Australian English.
"""


def load_wiki_files(project_id: str) -> dict:
    """Load all wiki documents for analysis"""
    wiki_dir = PROJECTS_DIR / project_id / "wiki"
    content  = {}

    if not wiki_dir.exists():
        return content

    for md_file in sorted(wiki_dir.glob("*.md")):
        with open(md_file, encoding="utf-8", errors="ignore") as f:
            content[md_file.name] = f.read()

    return content


def load_ceo_baseline(project_id: str) -> Optional[dict]:
    """Load the locked CEO baseline for this project"""
    baseline_path = PROJECTS_DIR / project_id / "ceo-baseline.json"

    if not baseline_path.exists():
        return None

    with open(baseline_path) as f:
        return json.load(f)


def load_previous_alignment(project_id: str) -> Optional[str]:
    """Load most recent prior alignment report to detect severity change"""
    wiki_dir = PROJECTS_DIR / project_id / "wiki"
    if not wiki_dir.exists():
        return None

    reports = sorted(wiki_dir.glob("ceo-alignment_*.md"), reverse=True)
    if len(reports) < 2:
        return None

    # Second most recent (most recent is what we just produced)
    with open(reports[1], encoding="utf-8") as f:
        return f.read()


def extract_overall_status(report_text: str) -> str:
    """Extract overall alignment status from a report"""
    for line in report_text.split("\n"):
        if "Overall Alignment" in line or "**Overall:**" in line:
            if "TERMINATE" in line.upper():
                return "TERMINATE"
            elif "RED" in line.upper():
                return "RED"
            elif "AMBER" in line.upper():
                return "AMBER"
    return "GREEN"


def create_github_alert(project_id: str, status: str, report_summary: str,
                         repo_name: str = "sdarpp-operations"):
    """Create GitHub Issue alert for alignment degradation"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("WARNING: GITHUB_TOKEN not set — skipping GitHub alert")
        return

    try:
        g    = Github(token)
        repo = g.get_repo(f"sdarpp-development-os/{repo_name}")

        severity_config = {
            "AMBER": {
                "labels":  ["alignment-amber", "project-alert"],
                "prefix":  "⚠️ ALIGNMENT AMBER",
                "urgency": "Action required within 3 business days"
            },
            "RED": {
                "labels":  ["alignment-red", "project-alert", "urgent"],
                "prefix":  "🚨 ALIGNMENT RED — URGENT",
                "urgency": "Immediate action required — respond within 24 hours"
            },
            "TERMINATE": {
                "labels":  ["mission-failure-risk", "alignment-red", "urgent", "board-review"],
                "prefix":  "🛑 MISSION FAILURE RISK — TERMINATE SIGNAL",
                "urgency": "STOP ALL WORK — Board review mandatory before proceeding"
            },
        }

        cfg = severity_config.get(status, severity_config["AMBER"])

        title = f"{cfg['prefix']}: {project_id} — CEO Alignment Monitor"
        body  = f"""## {cfg['prefix']}

**Project:** `{project_id}`
**Detected:** {datetime.now().strftime('%d/%m/%Y %H:%M AEST')}
**Urgency:** {cfg['urgency']}

---

{report_summary}

---

## Required Actions

1. Review full CEO Alignment Report in `projects/{project_id}/wiki/`
2. Assess corrective actions listed in report
3. Update project state within required timeframe
4. Close this issue only after corrective actions are implemented

---

*Generated by CEO Alignment Monitor (CAM v1.0)*
*This alert cannot be dismissed without documented corrective action.*
"""

        issue = repo.create_issue(
            title=title,
            body=body,
            labels=cfg["labels"]
        )
        print(f"✅ GitHub Alert created: {issue.html_url}")

    except GithubException as e:
        print(f"WARNING: Failed to create GitHub alert: {e}")


def build_alignment_prompt(project_id: str, wiki_content: dict,
                            baseline: Optional[dict], previous_report: Optional[str]) -> str:

    wiki_sections = "\n\n---\n\n".join(
        f"### {filename}\n\n{content}"
        for filename, content in wiki_content.items()
        if not filename.startswith("ceo-alignment")  # exclude prior alignment reports
    )

    baseline_section = ""
    if baseline:
        baseline_section = f"""
## LOCKED CEO BASELINE (DO NOT MODIFY)

These are the original investment thesis targets locked at project inception.
Compare every current metric against these — not against any intermediate update.

```json
{json.dumps(baseline, indent=2)}
```
"""
    else:
        baseline_section = """
## CEO BASELINE

No locked baseline file found. Extract the original investment thesis from the earliest
project state document and use those as the baseline targets for this analysis.
Flag that the baseline file should be created immediately after this report.
"""

    previous_section = ""
    if previous_report:
        previous_section = f"""
## PREVIOUS ALIGNMENT REPORT

For context, here is the most recent prior alignment assessment.
Identify if the situation has improved, deteriorated, or stalled since then.

{previous_report[:3000]}...
"""

    return f"""Please produce a full CEO Alignment Report for project: **{project_id}**

---

{baseline_section}

---

## CURRENT PROJECT WIKI DOCUMENTS

{wiki_sections}

---

{previous_section}

---

## REQUIRED OUTPUT

Produce the complete CEO Alignment Report covering:

1. **Executive Status Dashboard** — traffic light for each dimension
2. **Drift Detection Table** — baseline vs current vs variance vs status for each metric
3. **Drift Pattern Analysis** — which of the 6 warning patterns are present?
4. **CEO Insight** — 3-4 paragraphs, direct and unvarnished
5. **Corrective Actions** — CRITICAL / URGENT / MONITOR
6. **GO / CONTINUE / ADJUST / STOP / TERMINATE Recommendation**

Be direct. Do not soften the assessment.
If the project is drifting toward mission failure, say so clearly.
The Project Director's job is to make good decisions — your job is to give them the facts.
"""


def save_alignment_report(report: str, project_id: str) -> Path:
    wiki_dir  = PROJECTS_DIR / project_id / "wiki"
    wiki_dir.mkdir(parents=True, exist_ok=True)
    date_str  = datetime.now().strftime("%Y%m%d_%H%M")
    out_file  = wiki_dir / f"ceo-alignment_{date_str}.md"

    header = f"""# CEO Alignment Report — {project_id}
**Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M AEST')}
**Agent:** CEO Alignment Monitor (CAM v1.0)
**Classification:** CONFIDENTIAL — Project Director Only

---

"""
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(header + report)

    print(f"✅ CEO Alignment Report saved: {out_file}")
    return out_file


def main():
    stdin_data = sys.stdin.read().strip()
    if stdin_data:
        payload = json.loads(stdin_data)
    else:
        print("ERROR: No project_id on stdin")
        sys.exit(1)

    project_id = payload.get("project_id")
    if not project_id:
        print("ERROR: project_id required")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    print(f"Running CEO Alignment Monitor for: {project_id}")

    # ── Load data ──────────────────────────────────────────────
    wiki_content     = load_wiki_files(project_id)
    baseline         = load_ceo_baseline(project_id)
    previous_report  = load_previous_alignment(project_id)

    if not wiki_content:
        print(f"WARNING: No wiki files found for {project_id} — skipping")
        sys.exit(0)

    # ── Build prompt ───────────────────────────────────────────
    user_prompt = build_alignment_prompt(project_id, wiki_content, baseline, previous_report)

    # ── Call Claude ────────────────────────────────────────────
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=6000,
        system=CEO_ALIGNMENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    report = message.content[0].text

    # ── Save report ────────────────────────────────────────────
    out_file = save_alignment_report(report, project_id)

    # ── Detect severity & alert if degraded ────────────────────
    current_status  = extract_overall_status(report)
    previous_status = extract_overall_status(previous_report) if previous_report else "GREEN"

    print(f"Alignment: {previous_status} → {current_status}")

    # Alert if severity has worsened OR is already RED/TERMINATE
    if SEVERITY.get(current_status, 0) > SEVERITY.get(previous_status, 0) or \
       current_status in ("RED", "TERMINATE"):

        # Extract first 1500 chars of CEO Insight for alert
        lines        = report.split("\n")
        ceo_start    = next((i for i, l in enumerate(lines) if "CEO Insight" in l), 0)
        summary_text = "\n".join(lines[ceo_start:ceo_start + 30])

        create_github_alert(project_id, current_status, summary_text)

    # ── Output result ──────────────────────────────────────────
    result = {
        "agent":         "CEO Alignment Monitor",
        "status":        "success",
        "project_id":    project_id,
        "alignment":     current_status,
        "previous":      previous_status,
        "changed":       current_status != previous_status,
        "output_file":   str(out_file),
        "alert_created": current_status in ("AMBER", "RED", "TERMINATE"),
    }

    print(json.dumps(result, indent=2))

    # Exit with error code if TERMINATE to halt downstream agents
    if current_status == "TERMINATE":
        print("\n🛑 TERMINATE signal — all downstream agents should halt")
        sys.exit(2)


if __name__ == "__main__":
    main()
