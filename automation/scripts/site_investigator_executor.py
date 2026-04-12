#!/usr/bin/env python3
"""
Site Investigator Agent Executor

Performs deep site-specific planning and constraint investigation.
Implements smart caching — reuses state-level knowledge if <12 months old,
always fetches LGA-specific and First Nations data fresh.

Usage:
  echo '{"project_id": "...", "address": "...", "state": "VIC", "lga": "..."}' | python3 site_investigator_executor.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────
SDARPP_OPS_ROOT = Path(__file__).parent.parent.parent
KB_DIR          = SDARPP_OPS_ROOT / "knowledge-base"
STATE_PLAN_DIR  = KB_DIR / "state-planning"
FIRST_NATIONS_DIR = KB_DIR / "first-nations"
ESG_DIR         = KB_DIR / "esg"

# ── Cache thresholds (days) ────────────────────────────────────
CACHE_THRESHOLDS = {
    "state_planning":      365,   # 12 months
    "ndis_sda_policy":     180,   # 6 months
    "esg_frameworks":      365,   # 12 months
    "first_nations_national": 365, # 12 months — state framework only
    "lga_specific":        0,     # always refresh
    "first_nations_local": 0,     # always refresh
    "infrastructure":      0,     # always refresh
    "environmental":       0,     # always refresh
}

SITE_INVESTIGATOR_SYSTEM_PROMPT = """You are a SDARPP Site Investigator Agent.

You are a specialist urban planning and site analysis expert combining:
- Registered Town Planner (Victorian and Australian planning law)
- Environmental consultant
- Infrastructure engineer
- Aboriginal cultural heritage advisor

Your role is to conduct a comprehensive site investigation for a new SDARPP development project.

---

## INVESTIGATION FRAMEWORK

Produce a structured report covering all 8 sections:

### Section 1: Planning & Zoning Summary
- Current zone under the relevant Planning Scheme
- Zone purpose and objectives
- Permit requirements for proposed uses (healthcare, SDA, clinical, accommodation)
- Uses by right (no permit needed)
- Uses requiring permit
- Uses prohibited
- Decision guidelines the council must apply

### Section 2: Overlay Analysis
For each applicable overlay:
- Heritage Overlay (HO) — STOP: full heritage assessment required
- Design & Development Overlay (DDO) — height limits, design standards
- Development Plan Overlay (DPO) — triggers development plan requirement
- Flood Overlay (LSIO, SBO, FO) — restricts development envelope
- Environmental Significance Overlay (ESO) — vegetation, waterway buffers
- Development Contributions Overlay (DCO) — infrastructure levy obligations
- Any other relevant overlays

### Section 3: Infrastructure & Servicing
- Water and sewer capacity (SA Water / City West Water / etc.)
- Electrical supply (kVA demand for clinical/CSSD)
- Gas supply
- NBN and telecommunications
- Road access and traffic generation triggers
- Car parking requirements (LGA DCP or Planning Scheme standards)
- Emergency vehicle access (turning circles, frontage)
- Stormwater management obligations

### Section 4: Environmental Constraints
- Contamination risk (former use, AS4482 Phase 1 triggers)
- Bushfire Attack Level (BAL) risk if applicable
- Coastal / flooding / inundation
- Significant vegetation
- Noise / amenity sources nearby
- Any state-listed environmental significance

### Section 5: Aboriginal Cultural Heritage & First Nations
**ALWAYS research fresh for each project — never reuse from prior site.**

Identify:
- State (VIC: Aboriginal Heritage Act 2006; NSW: AHIP under NPW Act; WA: AHA 1972 etc.)
- Relevant Registered Aboriginal Party (RAP) or Local Aboriginal Land Council (LALC) for this specific LGA
- Any existing Cultural Heritage Management Plans (CHMP) in the area
- Whether a CHMP or Cultural Heritage Permit is triggered by the proposed development activity level
- First Nations groups with connection to country in this specific area
- Recommended engagement approach ("Designing with Country" framework)
- First Nations economic participation opportunities (employment, subcontracting, ownership)

### Section 6: Comparable Precedents
- 3 similar SDARPP or Mixed-Use Healthcare Hub projects in VIC/AU
- Planning outcomes achieved
- What these precedents mean for this site's approval prospects

### Section 7: Smart Cache Reuse Log
Be transparent about what was reused vs freshly researched:

| Data Category | Source | Age | Action |
|---------------|--------|-----|--------|
| State planning rules (VIC) | knowledge-base/state-planning/vic/ | [X months] | Reused / Refreshed |
| NDIS SDA policy | knowledge-base/ndis-sda-design-standard/ | [X months] | Reused / Refreshed |
| ESG frameworks | knowledge-base/esg/ | [X months] | Reused / Refreshed |
| First Nations (national framework) | knowledge-base/first-nations/ | [X months] | Reused / Refreshed |
| LGA planning scheme controls | Web search | Fresh | Always fresh |
| Local Aboriginal Land Council | Web search | Fresh | Always fresh |
| Infrastructure constraints | Web search | Fresh | Always fresh |
| Environmental data | Web search | Fresh | Always fresh |

### Section 8: Critical Constraints Summary

**GREEN — No issues, proceed:**
[List clear items]

**AMBER — Requires attention / investigation:**
[List items needing action before DA]

**RED — STOP — Must resolve before proceeding:**
[List blocking constraints]

---

## AUSTRALIAN STANDARDS

- Use Australian English spelling and terminology
- Reference Victorian Planning Provisions (VPP) for VIC projects
- Reference correct LGA Planning Scheme (not generic)
- Use AUD ($) for all costs
- Use correct Australian planning terminology (permit, scheme, overlay — not permit application, zoning code, etc.)
- Identify the correct Registered Aboriginal Party (RAP) for VIC projects using DATSIP / Heritage Victoria records

---

## PROHIBITIONS

Do NOT:
- Use US planning terminology
- Use generic state-level heritage data instead of site-specific RAP/ALCC
- Confuse council boundaries or apply wrong DCP/Planning Scheme
- Assume a CHMP is not required without checking the Cultural Heritage Act thresholds
"""


def check_cache(data_type: str, state: str) -> dict:
    """
    Check if cached knowledge base data is still valid.
    Returns: {"use_cache": bool, "cache_path": Path|None, "age_days": int|None}
    """
    threshold = CACHE_THRESHOLDS.get(data_type, 0)

    if threshold == 0:
        return {"use_cache": False, "cache_path": None, "age_days": None}

    # Map data type to KB path
    path_map = {
        "state_planning": STATE_PLAN_DIR / state.lower(),
        "ndis_sda_policy": KB_DIR / "ndis-sda-design-standard",
        "esg_frameworks": ESG_DIR,
        "first_nations_national": FIRST_NATIONS_DIR,
    }

    kb_path = path_map.get(data_type)
    if not kb_path or not kb_path.exists():
        return {"use_cache": False, "cache_path": None, "age_days": None}

    # Check for freshness marker file
    freshness_file = kb_path / ".last_updated"
    if not freshness_file.exists():
        return {"use_cache": False, "cache_path": kb_path, "age_days": None}

    with open(freshness_file) as f:
        last_updated_str = f.read().strip()

    try:
        last_updated = datetime.fromisoformat(last_updated_str)
        age_days = (datetime.now() - last_updated).days

        if age_days <= threshold:
            return {"use_cache": True, "cache_path": kb_path, "age_days": age_days}
        else:
            return {"use_cache": False, "cache_path": kb_path, "age_days": age_days}
    except ValueError:
        return {"use_cache": False, "cache_path": kb_path, "age_days": None}


def load_cached_data(cache_path: Path) -> str:
    """Load all .md files from a knowledge base directory"""
    if not cache_path:
        return ""

    content = []
    for md_file in sorted(cache_path.glob("**/*.md")):
        with open(md_file, encoding="utf-8", errors="ignore") as f:
            content.append(f"## {md_file.name}\n\n{f.read()}")

    return "\n\n---\n\n".join(content) if content else ""


def build_investigation_prompt(project_data: dict, cache_report: dict, cached_content: str) -> str:
    project_name  = project_data.get("project_name", "Unknown Project")
    address       = project_data.get("address", project_data.get("site_address", "Unknown"))
    state         = project_data.get("state", "VIC")
    lga           = project_data.get("lga", "Unknown LGA")
    zoning        = project_data.get("zoning", "Unknown")
    proposed_use  = project_data.get("proposed_use", "Mixed-Use Healthcare Hub")
    land_area     = project_data.get("land_area", "Unknown")

    cache_summary = "\n".join([
        f"- {k}: {'REUSE (cached)' if v['use_cache'] else 'FETCH FRESH'} "
        f"(age: {v['age_days']} days)" if v['age_days'] else
        f"- {k}: {'REUSE' if v['use_cache'] else 'FETCH FRESH'}"
        for k, v in cache_report.items()
    ])

    prompt = f"""Please conduct a full Site Investigation for the following project:

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

## DATA CACHE STATUS

The following data categories have been assessed for cache validity:

{cache_summary}

**Instructions:**
- For categories marked REUSE: Use the existing data provided below — do NOT re-research
- For categories marked FETCH FRESH: You must research current data (use your training knowledge + note if web search needed)
- **ALWAYS research fresh:** LGA-specific planning controls, local Aboriginal Land Council/RAP, infrastructure constraints, environmental data

---

## CACHED KNOWLEDGE BASE DATA (reuse as instructed above)

{cached_content if cached_content else "No cached data available — research all categories fresh."}

---

## INVESTIGATION REQUIRED

Produce the complete 8-section Site Investigation Report.

Pay particular attention to:
1. The SPECIFIC Planning Scheme for {lga} (not generic VIC rules)
2. The SPECIFIC Registered Aboriginal Party (RAP) for {lga} in {state}
3. Whether a Cultural Heritage Management Plan (CHMP) is triggered for the proposed works
4. Whether the site has any overlays that would restrict the Mixed-Use Healthcare Hub model
5. What planning pathway would unlock the FULL SDARPP model (CSSD + Medical Hub + SDA + VMO)

End with a clear Section 8 traffic light summary (GREEN/AMBER/RED constraints).
"""
    return prompt


def save_investigation(report: str, project_data: dict) -> Path:
    project_id = project_data.get("project_id", "unknown")
    date_str   = datetime.now().strftime("%Y%m%d")

    output_dir = SDARPP_OPS_ROOT / "projects" / project_id / "wiki"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"site-investigation_{date_str}.md"

    frontmatter = f"""# Site Investigation Report
**Project**: {project_data.get('project_name', project_id)}
**Address**: {project_data.get('address', project_data.get('site_address', 'Unknown'))}
**LGA**: {project_data.get('lga', 'Unknown')}
**Generated**: {datetime.now().strftime('%d/%m/%Y %H:%M AEST')}
**Agent**: Site Investigator Agent (SIA v1.0)
**Status**: Draft — Requires Project Director Review

---

"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(frontmatter + report)

    print(f"✅ Site Investigation saved: {output_file}")
    return output_file


def main():
    # Read payload
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

    state = project_data.get("state", "VIC").lower()

    # ── Check cache ──────────────────────────────────────────
    cache_report = {
        "state_planning":         check_cache("state_planning", state),
        "ndis_sda_policy":        check_cache("ndis_sda_policy", state),
        "esg_frameworks":         check_cache("esg_frameworks", state),
        "first_nations_national": check_cache("first_nations_national", state),
    }

    # ── Load cached content ──────────────────────────────────
    cached_parts = []
    for data_type, cache_info in cache_report.items():
        if cache_info["use_cache"] and cache_info["cache_path"]:
            content = load_cached_data(cache_info["cache_path"])
            if content:
                cached_parts.append(f"### CACHED: {data_type}\n\n{content}")

    cached_content = "\n\n".join(cached_parts)

    print(f"Cache status: {sum(1 for c in cache_report.values() if c['use_cache'])}/{len(cache_report)} categories reused")

    # ── Build prompt ─────────────────────────────────────────
    user_prompt = build_investigation_prompt(project_data, cache_report, cached_content)

    # ── Call Claude ──────────────────────────────────────────
    client = anthropic.Anthropic(api_key=api_key)

    print(f"Running Site Investigation for {project_data.get('project_name', 'project')}...")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8192,
        system=SITE_INVESTIGATOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    report = message.content[0].text

    # ── Save ─────────────────────────────────────────────────
    output_file = save_investigation(report, project_data)

    result = {
        "agent": "Site Investigator",
        "status": "success",
        "message": "Site investigation complete",
        "output_file": str(output_file),
        "cache_reuse": {k: v["use_cache"] for k, v in cache_report.items()},
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
