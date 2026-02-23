---
phase: 03-comparison-charts-and-electrical-slider
plan: 02
subsystem: ui
tags: [dash, plotly, callbacks, dcc.Store, charts, sliders]

# Dependency graph
requires:
  - phase: 03-01
    provides: Figure builder functions (build_cost_chart, build_land_chart, build_turbine_chart, build_pie_chart), make_chart_section layout, compute_chart_data, battery_ratio_label, fmt_cost
  - phase: 02-02
    provides: set_data() module pattern, shell.py render_content callback, dcc.Store infrastructure
provides:
  - Dash callbacks wiring both sliders and legend store to all four chart figures
  - update_charts() master callback returning 4 figures + 3 live labels
  - toggle_legend() callback managing system visibility via dcc.Store
  - update_badge_styles() callback dimming badge when system toggled off
  - Chart section integrated into system_view.py below scorecard and equipment grid
affects: [04-hybrid-builder, 05-export-and-polish]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "set_data() module pattern extended to charts.py — module-level _data populated from app.py, not inside callbacks"
    - "ctx.triggered_id for multi-input callbacks — identifies which legend badge was clicked without if/else per Input"
    - "uirevision='static' on all figures — prevents chart blink/reset on slider drag"
    - "dcc.Store as authoritative visibility state — avoids restyleData Dash bug #2037"
    - "opacity + text-decoration: line-through for dimmed badge — consistent toggle-off visual signal"

key-files:
  created: []
  modified:
    - src/layout/charts.py
    - src/layout/system_view.py
    - app.py

key-decisions:
  - "update_charts() fires on both slider inputs and legend store change — single callback for all four figures avoids state fragmentation"
  - "toggle_legend() uses ctx.triggered_id with a dict map to system key — eliminates per-badge if/else branching"
  - "Badge dimming uses opacity 0.4 + text-decoration: line-through rather than hiding — user can see what is toggled off"
  - "set_data() pattern mirrored exactly from shell.py — consistent module-level data access across all layout modules"

patterns-established:
  - "Callback outputs: return all figures + labels in a single master callback, not split per-figure"
  - "Legend visibility store: dict with mechanical/electrical/hybrid bool keys, updated atomically"
  - "Live labels: three separate Output targets (label-years, label-battery-ratio, label-elec-cost) updated in same callback that updates charts"

requirements-completed: [CHART-01, CHART-02, CHART-03, CHART-04, CHART-05, CTRL-01, CTRL-02, VIS-03]

# Metrics
duration: 15min
completed: 2026-02-22
---

# Phase 3 Plan 02: Comparison Charts Callbacks Summary

**Four Dash callbacks wired into charts.py connecting both sliders and legend store to all four comparison charts with live label updates and badge visibility toggling**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-02-21T23:05:00Z
- **Completed:** 2026-02-22T05:24:17Z
- **Tasks:** 2 (1 auto + 1 human-verify checkpoint)
- **Files modified:** 3

## Accomplishments

- Master update_charts() callback fires on time horizon slider, battery slider, and legend store — returns 4 chart figures plus 3 live label strings in one shot
- toggle_legend() callback uses ctx.triggered_id with a lookup dict to flip the correct visibility key in dcc.Store without if/else per badge
- update_badge_styles() callback dims toggled-off badges with opacity 0.4 and line-through text decoration for clear visual feedback
- Chart section appended to system_view.py below equipment grid via make_chart_section() import
- set_charts_data(DATA) wired in app.py so callbacks have module-level data access
- Human verified full interactive experience: sliders update in real time, legend toggles propagate across all four charts, tooltips show formatted values, hybrid shows placeholder data

## Task Commits

Each task was committed atomically:

1. **Task 1: Add callbacks to charts.py and integrate chart section into system_view.py** - `eb2ba0a` (feat)
2. **Task 2: Verify interactive chart section** - Human-verify checkpoint, approved by user (no code commit)

**Plan metadata:** *(this commit — docs)*

## Files Created/Modified

- `src/layout/charts.py` — Added _data / set_data(), update_charts() callback, toggle_legend() callback, update_badge_styles() callback (+199 lines)
- `src/layout/system_view.py` — Added make_chart_section import and appended chart section to layout return
- `app.py` — Added set_charts_data(DATA) call after existing set_data(DATA)

## Decisions Made

- `update_charts()` master callback consolidates all four chart outputs and three labels into a single callback — avoids state fragmentation that would occur with separate per-figure callbacks
- `ctx.triggered_id` with a `{id: key}` dict lookup in `toggle_legend()` — cleaner than if/else per Input, extends easily if a fourth system is added
- Badge dimming uses `opacity: 0.4` plus `text-decoration: line-through` — opacity alone is subtle; line-through makes toggle-off state unambiguous
- `set_data()` pattern mirrored exactly from shell.py — keeps all layout modules consistent and avoids callback-time data loading

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All four comparison charts fully interactive with real data from data.xlsx
- Time horizon slider, battery/tank slider, and shared legend all working
- Hybrid placeholder (zeros / grey "No data" pie slice) correctly handled
- Phase 4 (Hybrid Builder) can now integrate real hybrid data into the existing chart callbacks — chart section is already wired and ready to receive real hybrid values via compute_chart_data()
- No blockers for Phase 4

---
*Phase: 03-comparison-charts-and-electrical-slider*
*Completed: 2026-02-22*
