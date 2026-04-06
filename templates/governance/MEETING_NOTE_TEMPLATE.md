# Consultant Meeting Note Template

**Purpose**: Standardised format for all consultant meeting notes. This template ensures meeting output is machine-parseable for automated report generation and action item tracking.

**IMPORTANT**: Use the exact section headers below (including the `##`). The automation scripts parse these headers to extract structured data.

---

## MEETING METADATA

- **Consultant Name**: [Full name]
- **Consultant Type**: [Town Planner / Architect / Structural Engineer / Services Engineer / Landscape Architect / Grants Consultant / SDA Provider]
- **Organization**: [Company name]
- **Contact Email**: [Email address]
- **Contact Phone**: [Phone number]
- **Meeting Date**: [YYYY-MM-DD]
- **Meeting Duration**: [X minutes]
- **Location/Format**: [In-person / Video call / Site visit]
- **Attendees**: [Names from your side]

---

## EXECUTIVE SUMMARY

[1–2 paragraphs summarizing the overall meeting tone, key themes, and confidence level. Omit details — those go in later sections.]

---

## DECISION OUTCOME

**Decision**: [APPROVED / CONDITIONAL / REJECTED / PENDING]

**Rationale**: [Why this decision was reached. 2–3 sentences.]

**Confidence Score (Overall)**: [1–10] out of 10

---

## CRITICAL SUCCESS FACTORS — ASSESSMENT

List each critical success factor and mark as ✅ (met), ⚠️ (at risk), or ❌ (not met):

- ✅ [Factor 1]: [Brief assessment]
- ✅ [Factor 2]: [Brief assessment]
- ⚠️ [Factor 3]: [Brief assessment — what needs to change]
- ❌ [Factor 4]: [Brief assessment — why it was not met]

---

## CONFIDENCE SCORES (All Controls)

Rate each control on a 1–10 scale. Scores ≥7 indicate green; 5–6 amber; ≤4 red.

| Control / Assessment Area | Score | Notes |
|---|---|---|
| Planning Feasibility | [1-10] | [Assessment notes] |
| Design Excellence | [1-10] | [Assessment notes] |
| Compliance (NCC / DA) | [1-10] | [Assessment notes] |
| Structural Adequacy | [1-10] | [Assessment notes] |
| Cost Feasibility | [1-10] | [Assessment notes] |
| Team Capability | [1-10] | [Assessment notes] |
| Timeline Achievable | [1-10] | [Assessment notes] |

**Average Score**: [Calculate: sum / count] / 10

**Threshold**: ≥ 7.0 = Green | 5.5–6.9 = Amber | ≤ 5.4 = Red

---

## ACTION ITEMS

List all action items with owner, description, and due date. Format: `- [ ] [Owner]: [Action] — Due: YYYY-MM-DD`

- [ ] [Owner]: [Action] — Due: YYYY-MM-DD
- [ ] [Owner]: [Action] — Due: YYYY-MM-DD

---

## DECISIONS MADE IN THIS MEETING

Document each decision with its rationale and any cross-references to other decisions:

1. **[Decision Title]** — [Rationale]. Cross-ref: [governance/decision_log.md](decision_log.md)

---

## RISKS IDENTIFIED

List any new risks identified or escalations to existing risks. Include risk ID reference if applicable.

- **Risk ID**: [XXX-##] — [Risk description and mitigation]
- **New Risk**: [Risk description and mitigation]

---

## NEXT STEPS & CRITICAL PATH

Summarise what happens next and the immediate next actions:

1. **By [Date]**: [Action]
2. **[Date range]**: [Action]

---

## STRENGTHS IDENTIFIED

What did the consultant do well? What are their key strengths for this engagement?

- [Strength 1]: [How this benefits the project]
- [Strength 2]: [How this benefits the project]

---

## CONCERNS / GAPS

What needs attention? What are the risks or gaps in their approach?

- [Concern 1]: [Why it matters; mitigation]
- [Concern 2]: [Why it matters; mitigation]

---

## FOLLOW-UP REQUIRED

List all items requiring follow-up:

- [Action item]
- [Action item]

---

## ADDITIONAL NOTES

[Any other context, quotes, or observations not captured above.]

---

## How This Template Is Used

1. **After the meeting**: Complete all sections using this exact format.
2. **Push to GitHub**: Commit the file to `consultants/[CONSULTANT_TYPE]-[DATE].md`.
3. **Trigger automation**: GitHub Actions will parse this template and:
   - Extract action items → auto-populate follow-up register
   - Parse confidence scores → populate DOCX decision memo
   - Detect risks → cross-check against risk register
   - Generate professional DOCX reports automatically
4. **No manual report writing**: The DOCX is generated from this structured markdown.
