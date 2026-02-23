# Phase 1: Foundation - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Data layer, app shell, and project scaffolding. The app launches via `python app.py`, reads data.xlsx correctly (all three sheets), provides startup validation, assigns consistent system colors, and delivers the structural shell that all future features build into. No feature content yet — just the working skeleton.

</domain>

<decisions>
## Implementation Decisions

### System colors
- Academic muted palette — soft, professional tones suitable for academic paper charts
- Cohesive palette — colors should look good together and be distinguishable, no specific semantic associations required
- Colorblind accessibility is nice to have but not a hard requirement
- RAG scorecard indicators (red/yellow/green) use separate standard traffic-light colors, independent from system palette

### App shell structure
- Sidebar navigation layout — dashboard-style with sidebar and main content area
- Sidebar only shows nav items for features that are actually built (grows as phases complete)
- Sidebar is collapsible — toggle button to show/hide, giving more room for charts
- Top header bar with project title (e.g., "Wind-Powered Desalination Dashboard")

### Data validation UX
- Silent success — if data loads fine, just show the app with no success message
- Full-page error on failure — if data.xlsx is missing or a sheet fails to parse, show a clear error page and render nothing else
- Error messages show both levels: high-level message for students, expandable "Details" section with specifics (which sheet, which column/row)
- Also log validation info to the terminal/console for whoever launched `python app.py`

### Tech stack
- Dash (Plotly) framework — interactive dashboard with callback-driven chart interactions
- dash-bootstrap-components with FLATLY theme — clean, flat, professional academic styling
- Auto-open browser tab when `python app.py` is run

### Claude's Discretion
- Exact muted color values for the three systems
- Sidebar width and toggle button design
- Error page layout and styling
- Project file structure and module organization
- Dash app configuration details

</decisions>

<specifics>
## Specific Ideas

- FLATLY Bootstrap theme specifically chosen for its clean, muted academic feel
- Dashboard should feel professional — think academic data visualization tool, not flashy startup
- Sidebar grows organically as features are built across phases

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-foundation*
*Context gathered: 2026-02-21*
