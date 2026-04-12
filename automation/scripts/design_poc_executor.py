#!/usr/bin/env python3
"""
Design Proof of Concept Agent Executor

Generates 4-scenario Design PoC for any SDARPP project site.
Based on Day Street, Wodonga reference model.
Produces AS IS / Potential / Max Value / Special Use Zoning analysis.
Includes CEO Strategic Commentary.

Usage:
  echo '{"project_id": "...", "address": "...", "state": "VIC", "lga": "..."}' | python3 design_poc_executor.py
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic")
    sys.exit(1)

SDARPP_OPS_ROOT = Path(__file__).parent.parent.parent

DESIGN_POC_SYSTEM_PROMPT = """You are a SDARPP Design Proof of Concept Agent.

You combine the expertise of:
- Accredited Architect (RAIA) — schematic and concept design
- Town Planner — planning rules and yield calculations
- Development Economist — financial feasibility modelling
- SDARPP Subject Matter Expert — Mixed-Use Healthcare Hub model

Your reference model is the Day Street, Wodonga project:
- CSSD (Central Sterile Supply Department)
- Allied Health / Medical Hub
- Clinical Step-Down / Transition Care
- 4 × HPS SDA (High Physical Support)
- 16 × VMO (Visiting Medical Officer suites)
- DSCR: 1.25-1.30x
- IRR Target: 14-16%
- Development Margin: 15-20%

---

## THE 4 MANDATORY SCENARIOS

### Scenario 1 — AS IS
**Definition:** What can be built TODAY under current zoning — no planning change required.

Report must include:
- All uses permissible by right (no permit)
- Maximum building envelope (height, site coverage %, setbacks)
- Estimated Gross Floor Area (GFA)
- Estimated number of units / suites / floors
- **Revenue Table (AUD/year)**:
  - Income Stream 1: [type] — $[amount]
  - Income Stream 2: [type] — $[amount]
  - Total Revenue: $[amount]
- Estimated Total Development Cost (TDC): $[amount]
- Net Development Value (NDV): $[amount]
- Return on Cost: [%]
- Estimated IRR: [%]
- Planning Complexity: Low
- Timeline to completion: [months]
- Key Risks (3 dot points)
- **Recommendation: Proceed / Conditional / Do Not Pursue**

### Scenario 2 — POTENTIAL
**Definition:** Best outcome achievable WITH a planning permit but WITHOUT rezoning.

Report must include same tables as Scenario 1, plus:
- Uses requiring permit but permissible in current zone
- Any Planning Agreement or VPA opportunity
- Additional yield vs Scenario 1
- Revenue uplift ($ and %)
- Planning Complexity: Medium
- Permit approval probability: [%]
- Additional cost/risk for planning permit pathway

### Scenario 3 — MAX VALUE (SDARPP Full Model)
**Definition:** Full Mixed-Use Healthcare Hub delivered via rezoning or Planning Scheme Amendment.

This is the target SDARPP model. Must include:
- Full 4-5 revenue stream stack:
  1. CSSD / institutional clinical revenue
  2. Medical Hub / allied health income
  3. Clinical Transition / step-down income
  4. NDIS SDA revenue (HPS pricing)
  5. VMO / private accommodation income
- Rezoning pathway (Planning Scheme Amendment process)
- Planning Agreement / VPA opportunity
- Capital stack: grants + debt + equity
- Grant programs applicable (name, amount, eligibility)
- DSCR at target revenues
- IRR at target structure
- Planning Complexity: High
- Timeline: [months — include rezoning duration]
- Why this is the preferred scenario

### Scenario 4 — SPECIAL USE ZONING
**Definition:** Maximum value achievable if site is rezoned to Special Use / Public Purpose.

Report must include:
- What Special Use zoning would unlock
- How to achieve Special Use designation (Ministerial call-in, gazettement)
- State Government support pathway
- Premium grant programs unlocked by Special Use
- Land value uplift ($ and %)
- Maximum GFA / yield
- Revenue at full Special Use
- IRR at maximum scenario
- Planning Complexity: Very High
- Timeline: [months — include Ministerial/Parliamentary process]
- Conditions required (partnership with health authority, NFP operator, etc.)

---

## COMPARATIVE SCENARIO TABLE

After the 4 scenarios, produce a single comparison table:

| Metric | AS IS | Potential | Max Value | Special Use |
|--------|-------|-----------|-----------|-------------|
| GFA (sqm) | | | | |
| Revenue ($/yr) | | | | |
| TDC ($) | | | | |
| NDV ($) | | | | |
| IRR (%) | | | | |
| Planning Risk | Low | Medium | High | Very High |
| Timeline (months) | | | | |
| Grants Available | | | | |
| Recommended | | | ✅ Target | ✅ Stretch |

---

## CEO STRATEGIC COMMENTARY (REQUIRED)

This is the most important section. Write from the perspective of an experienced CEO and institutional developer.

### 1. Recommended Scenario & Rationale
Which scenario to pursue first, second, and stretch target.

### 2. Market Uniqueness
Is anyone else doing this model in Australia? If yes, identify them.
If no — what does that mean strategically? First mover advantage or market signal?

### 3. Comparable Australian Projects
Identify 3-5 comparable developments achieving similar mixed-use health + disability + clinical models.
For each: Name, Location, Developer, Scale, Outcome.
Be honest — if comparable projects are limited, say so and explain why.

### 4. Replicability Assessment
Under what conditions can this model be replicated across:
- Other VIC regional centres (Bendigo, Ballarat, Shepparton, Wangaratta)
- NSW regional centres
- Metropolitan sites

Minimum viable conditions for replication:
- Land size: [sqm minimum]
- Land value threshold: [$X/sqm maximum to remain feasible]
- Population catchment: [minimum]
- Health infrastructure proximity: [metres from hospital preferred]

### 5. Top 5 Executive Risks + Mitigations

| Rank | Risk | Probability | Impact | Mitigation |
|------|------|-------------|--------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### 6. Recommended Immediate Actions (Priority Order)
Numbered list of next steps the Project Director must execute immediately.
Be specific about WHO, WHAT, and WHEN.

### 7. Strategic Opportunities the Developer Should Not Miss
Any opportunities that are time-sensitive, competitive, or counter-intuitive that most developers would overlook.

---

## FORMAT REQUIREMENTS

- Use executive-level, investment-committee language
- All costs in AUD ($)
- Use Australian English spelling
- Be specific — cite actual planning scheme zones, overlay codes (DDO, HO, etc.)
- Do not hedge excessively — provide a clear point of view
- Assume reader is: CEO, Board member, institutional investor, government partner
"""


def load_site_investigation(project_id: str) -> str:
    """Load the most recent site investigation report if available"""
    project_dir = SDARPP_OPS_ROOT / "projects" / project_id / "wiki"
    if not project_dir.exists():
        return ""

    investigations = sorted(project_dir.glob("site-investigation_*.md"), reverse=True)
    if not investigations:
        return ""

    with open(investigations[0], encoding="utf-8") as f:
        content = f.read()

    print(f"✅ Loaded site investigation: {investigations[0].name}")
    return content


def build_poc_prompt(project_data: dict, site_investigation: str) -> str:
    project_name = project_data.get("project_name", "Unknown Project")
    address      = project_data.get("address", project_data.get("site_address", "Unknown"))
    state        = project_data.get("state", "VIC")
    lga          = project_data.get("lga", "Unknown LGA")
    zoning       = project_data.get("zoning", "Unknown")
    land_area    = project_data.get("land_area", "Unknown")
    proposed_use = project_data.get("proposed_use", "Mixed-Use Healthcare Hub")

    si_section = f"""
## SITE INVESTIGATION DATA

The following site investigation has already been completed. Use this data for all planning rules, constraints, and overlays — do NOT contradict it.

{site_investigation}
""" if site_investigation else """
## SITE INVESTIGATION DATA

No prior site investigation available. Make reasonable assumptions based on the project details below and note them clearly in your report.
"""

    return f"""Please produce a complete 4-Scenario Design Proof of Concept for:

---

## PROJECT DETAILS

- **Project Name:** {project_name}
- **Address:** {address}
- **State:** {state}
- **LGA:** {lga}
- **Land Area:** {land_area}
- **Current Zoning:** {zoning}
- **Proposed Development:** {proposed_use}

---

## REFERENCE MODEL

Base your yield and revenue calculations on the Day Street, Wodonga project:
- 4 × HPS SDA units at current NDIS SDA HPS pricing (~$130,000+/unit/year)
- 16 × VMO suites at $35,000–$50,000/suite/year
- CSSD contract revenue: $800K–$1.2M/year (hospital services agreement)
- Allied Health Hub: $500K–$900K/year (room rentals + anchor tenant)
- Step-Down / Clinical Transition: $1.2M–$1.8M/year (NDIS + health dept block grant)

Adjust all yields and revenues proportionally for the actual site area.

---

{si_section}

---

## REQUIRED OUTPUT

Produce all 4 scenarios + comparative table + CEO Strategic Commentary.

Be direct. Give a clear point of view on which scenario to pursue.
Identify if anyone else is doing this model in Australia.
Provide a replication framework for portfolio scaling.
"""


def save_poc_report(report: str, project_data: dict) -> Path:
    project_id = project_data.get("project_id", "unknown")
    date_str   = datetime.now().strftime("%Y%m%d")

    output_dir = SDARPP_OPS_ROOT / "projects" / project_id / "wiki"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"design-poc_{date_str}.md"

    frontmatter = f"""# Design Proof of Concept — 4 Scenarios
**Project**: {project_data.get('project_name', project_id)}
**Address**: {project_data.get('address', project_data.get('site_address', 'Unknown'))}
**Generated**: {datetime.now().strftime('%d/%m/%Y %H:%M AEST')}
**Agent**: Design PoC Agent (DPA v1.0)
**Status**: Draft — Requires Architect + Project Director Review

---

"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(frontmatter + report)

    print(f"✅ Design PoC saved: {output_file}")
    return output_file


def main():
    stdin_data = sys.stdin.read().strip()
    if stdin_data:
        project_data = json.loads(stdin_data)
    else:
        print("ERROR: No project data on stdin")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    project_id = project_data.get("project_id", "unknown")

    # Load site investigation if available
    site_investigation = load_site_investigation(project_id)

    # Build prompt
    user_prompt = build_poc_prompt(project_data, site_investigation)

    # Call Claude
    client = anthropic.Anthropic(api_key=api_key)

    print(f"Generating Design PoC (4 scenarios) for {project_data.get('project_name', project_id)}...")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8192,
        system=DESIGN_POC_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    report = message.content[0].text

    # Save
    output_file = save_poc_report(report, project_data)

    result = {
        "agent": "Design PoC",
        "status": "success",
        "message": "4-scenario Design PoC generated",
        "output_file": str(output_file),
        "project": project_data.get("project_name"),
        "scenarios": ["AS IS", "Potential", "Max Value", "Special Use Zoning"],
        "site_investigation_used": bool(site_investigation),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
