---
phase: 05-polish-and-deployment
plan: 01
subsystem: ui
tags: [dash, plotly, css, print, export, clientside_callback]

# Dependency graph
requires:
  - phase: 04-hybrid-builder
    provides: scorecard-container, comparison-text, store-hybrid-slots, system_view layout
provides:
  - Export / Print button (id="export-btn") with clientside window.print() callback
  - "@media print CSS hiding sidebar, navbar, controls, hybrid builder inputs"
  - "@page { size: auto; } fix for Chrome print Layout option"
  - ".chart-controls and .hybrid-builder-section CSS class assignments"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "clientside_callback at module level (not app.clientside_callback) — consistent with project callback pattern"
    - "no-print CSS class on interactive UI elements for print hiding"
    - "className-based print hiding (chart-controls, hybrid-builder-section) to avoid Plotly reflow"

key-files:
  created: []
  modified:
    - src/layout/system_view.py
    - src/layout/scorecard.py
    - assets/custom.css
    - src/layout/charts.py
    - src/layout/hybrid_builder.py

key-decisions:
  - "export-btn placed above scorecard-container in CardBody (not inside it) so scorecard callback re-renders do not destroy the button"
  - "@page { size: auto; } added as top-level rule (not inside @media print) to fix Chrome print dialog Layout option disappearing (dbc GitHub #269)"
  - "dcc-graph and js-plotly-plot NOT hidden with display:none to avoid Plotly layout reflow issues — only non-chart UI elements hidden"
  - "clientside_callback imported at module level from dash alongside existing callback import"

patterns-established:
  - "no-print class: add to any UI element that should be hidden in print view"
  - "chart-controls class: control panel wrapper class for print hiding"
  - "hybrid-builder-section class: hybrid builder wrapper class for print hiding"

requirements-completed: [EXP-01]

# Metrics
duration: 5min
completed: 2026-02-22
---

# Phase 5 Plan 01: Polish and Deployment — Export / Print Summary

**Browser print-to-PDF export via clientside window.print() with @media print CSS hiding all non-report UI elements, satisfying EXP-01**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-23T02:31:10Z
- **Completed:** 2026-02-23T02:36:00Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Export / Print button added above scorecard table on all system tabs, wired to browser print dialog via clientside_callback
- @media print block hides navbar, sidebar, tab bar, breadcrumb, export button, chart sliders, legend badges, and hybrid builder dropdowns
- @page fix resolves Chrome print dialog Layout option disappearance (Bootstrap/dbc known issue)
- No new pip dependencies added

## Task Commits

Each task was committed atomically:

1. **Task 1: Add export button, scorecard card wrapper, and print clientside_callback** - `1ebbb6e` (feat)
2. **Task 2: Add @media print CSS and no-print class assignments** - `be94f7a` (feat)

## Files Created/Modified

- `src/layout/system_view.py` - Added export-btn (dbc.Button, id="export-btn", className="no-print") inside new dbc.Card wrapping the scorecard section; button placed above scorecard-container so scorecard callback re-renders do not destroy it
- `src/layout/scorecard.py` - Added clientside_callback import; added module-level clientside_callback firing window.print() on export-btn click
- `assets/custom.css` - Added top-level @page { size: auto; } and full @media print block hiding non-report UI
- `src/layout/charts.py` - Added className="chart-controls" to control panel card for print hiding
- `src/layout/hybrid_builder.py` - Added className="hybrid-builder-section" to outermost wrapper for print hiding

## Decisions Made

- export-btn placed as a sibling above scorecard-container inside a CardBody — the scorecard callback replaces scorecard-container children on every hybrid slot change, so the button cannot live inside scorecard-container or it would be destroyed on each update
- @page { size: auto; } added as a standalone top-level rule (not inside @media print) — this is the fix for the well-documented dbc/Bootstrap Chrome print dialog issue where the Layout option disappears
- dcc.Graph and .js-plotly-plot are NOT hidden with display:none — Plotly re-renders with zero dimensions when hidden this way; only non-chart UI elements are hidden in print
- Used module-level clientside_callback (from dash import clientside_callback) not app.clientside_callback — consistent with the project's existing callback registration pattern throughout all layout modules

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- EXP-01 satisfied: Export / Print button on all system tabs opens browser print dialog
- Print preview shows RAG scorecard table and all four comparison charts
- Print preview hides sidebar, navbar, tab bar, breadcrumb, hybrid builder dropdowns, sliders, legend badges, and export button itself
- Chrome print dialog shows Layout option (portrait/landscape) — @page fix working
- Phase 5 Plan 01 is the only new-functionality plan in this phase; remaining plans (if any) can focus on final polish and deployment

## Self-Check: PASSED

- All 5 modified files confirmed on disk
- SUMMARY.md confirmed on disk
- Commits 1ebbb6e and be94f7a confirmed in git log

---
*Phase: 05-polish-and-deployment*
*Completed: 2026-02-22*
