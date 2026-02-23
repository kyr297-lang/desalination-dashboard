# Phase 5: Polish and Deployment - Context

**Gathered:** 2026-02-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Final polish pass on the wind-powered desalination dashboard. Adds scorecard export for lab reports, improves visual consistency across all charts and components, ensures the dashboard is self-explanatory for first-time students, adds comparison description text for the hybrid system, and confirms clean single-command startup. No new features or capabilities — this phase refines what phases 1–4 built.

</domain>

<decisions>
## Implementation Decisions

### Scorecard export
- Print-to-PDF via browser print dialog triggered by an export button
- Print view includes RAG scorecard table plus all comparison charts (cost over time, land area, turbine count, energy breakdown)
- Does NOT include hybrid builder slot selections — results only, not inputs
- Export button placed at the top of the scorecard section, near the heading

### Student onboarding
- No explicit instructions, walkthrough, or step indicators — rely on clear visual hierarchy to guide students
- Landing view opens on the overview with the scorecard visible so students see all three systems at a glance
- Sidebar tabs are text-only labels (no icons) — clean and academic
- Hybrid builder gets a single instruction line above the slots: "Select one piece of equipment for each process stage"

### Visual consistency
- Full visual audit across all charts and components — no specific priority, equal pass on everything
- Dollar values abbreviated with K/M suffixes ($1.2M, $45K) on chart axes and labels
- Tooltips show full precision ($1,234,567) even when chart labels are abbreviated
- Subtle cards (light borders or shadows) around content groups for clean separation
- RAG scorecard uses colored dots/icons next to values instead of colored cell backgrounds
- Standard readable font sizing (default Bootstrap) — no compacting
- Claude conducts thorough audit since user hasn't done a visual pass yet

### Comparison description text
- Academic neutral tone: factual, no opinion ("The hybrid system ranks second in cost efficiency, trailing Mechanical by 12%")
- Summary sentence format — one or two sentences covering ranking and biggest differentiator, not per-metric breakdown
- Placement at Claude's discretion based on existing layout flow
- Updates live whenever hybrid configuration changes (all 5 slots filled)

### Claude's Discretion
- Chart layout density (2x2 grid vs stacked) — pick based on chart readability
- Comparison description text placement
- Exact print CSS styling for export view
- Specific spacing, alignment, and padding values during visual audit

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-polish-and-deployment*
*Context gathered: 2026-02-22*
