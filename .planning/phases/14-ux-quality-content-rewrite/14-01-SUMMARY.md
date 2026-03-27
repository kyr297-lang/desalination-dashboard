---
phase: 14-ux-quality-content-rewrite
plan: 01
subsystem: ui
tags: [dash, dcc.Slider, dcc.Loading, dbc.Alert, dcc.Store, callbacks]

# Dependency graph
requires:
  - phase: 12-data-layer-hybrid-builder-removal
    provides: chart callback structure and slider IDs in charts.py
  - phase: 13-system-layout-images-creative-differentiation
    provides: shell.py store pattern with sidebar-collapsed and active-system stores
provides:
  - All four sliders fire chart callbacks only on mouse release (mouseup updatemode)
  - No text input boxes on any slider (allow_direct_input=False)
  - Battery slider endpoint labels and always-visible tooltip
  - dcc.Loading spinner wrapping the chart grid (row1 + row2)
  - First-visit guidance banner above control panel with slider-dismiss callback
  - store-banner-dismissed dcc.Store in shell.py
affects:
  - 14-02 (landing page rewrite may share shell.py pattern awareness)
  - 14-03 (mechanical content update — unrelated to slider/banner changes)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - dcc.Loading wraps output children list, not individual dcc.Graph components
    - Banner dismiss via prevent_initial_call=True callback reading all four slider Input values
    - Banner store initialized in shell.py alongside other session stores to satisfy suppress_callback_exceptions=True

key-files:
  created: []
  modified:
    - src/layout/shell.py
    - src/layout/charts.py

key-decisions:
  - "Banner store (store-banner-dismissed) added to shell.py alongside sidebar-collapsed and active-system — required by suppress_callback_exceptions=True so the store exists in DOM before any callback references it"
  - "Banner text uses em-dash unicode \\u2014 matching existing charts.py pattern for slider helper text — NOT double-hyphen as written in CONTEXT.md"
  - "dcc.Loading wraps [row1, row2] as a list — not legend_row or control_panel — per D-05"
  - "prevent_initial_call=True on dismiss_banner is mandatory — prevents page-load default slider values from immediately dismissing the banner"

patterns-established:
  - "Session-scoped banner pattern: dbc.Alert with is_open controlled by dcc.Store flag, dismiss via slider Input callback with prevent_initial_call=True"

requirements-completed: [UX-01, UX-02, UX-03, UX-04, UX-05]

# Metrics
duration: 5min
completed: 2026-03-27
---

# Phase 14 Plan 01: Slider UX Fixes, Loading Spinner, and First-Visit Banner Summary

**Four slider behaviors fixed (mouseup, no direct input, battery endpoint labels), chart grid wrapped in dcc.Loading spinner, and session-scoped guidance banner added above control panel with slider-dismiss callback**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-27T06:23:00Z
- **Completed:** 2026-03-27T06:28:39Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- All four sliders (time-horizon, battery, tds, depth) now fire chart callbacks only on mouse release via `updatemode="mouseup"` — eliminates per-pixel chart recalculations during drag
- `allow_direct_input=False` added to all four sliders — suppresses Dash 4.0 text input boxes
- Battery slider updated with `marks={0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}` and `tooltip={"always_visible": True, "placement": "bottom"}`
- `dcc.Loading(children=[row1, row2], type="default")` wraps the chart grid — spinner visible during chart recalculation
- `dbc.Alert` guidance banner (`id="banner-guidance"`, `color="info"`, `dismissable=False`) inserted above control panel
- `dismiss_banner` callback with `prevent_initial_call=True` hides banner on any slider interaction; `store-banner-dismissed` store added to `shell.py`

## Task Commits

Each task was committed atomically:

1. **Task 1: Slider fixes, dcc.Loading wrapper, first-visit guidance banner** - `ab35ba2` (feat)

## Files Created/Modified
- `src/layout/shell.py` - Added `store-banner-dismissed` dcc.Store alongside existing session stores
- `src/layout/charts.py` - All four slider fixes, banner component, dcc.Loading wrapper, dismiss_banner callback

## Decisions Made
- Banner store added to `shell.py` (not `charts.py`) to satisfy `suppress_callback_exceptions=True` — store must exist in DOM before callback references it on any tab
- Em-dash `\u2014` used in banner text (matches existing charts.py pattern), not double-hyphen from CONTEXT.md
- `dcc.Loading` wraps `[row1, row2]` as children list — does not wrap `legend_row` or `control_panel` per D-05

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Slider UX and spinner complete — Phase 14 Plan 02 (landing page rewrite) can proceed independently
- Phase 14 Plan 03 (mechanical content update in config.py) can also proceed independently
- No blockers

---
*Phase: 14-ux-quality-content-rewrite*
*Completed: 2026-03-27*
