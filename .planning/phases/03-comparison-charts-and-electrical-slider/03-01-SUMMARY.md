---
phase: 03-comparison-charts-and-electrical-slider
plan: 01
subsystem: ui
tags: [plotly, dash, numpy, pandas, dbc, graph_objects, charts, sliders]

# Dependency graph
requires:
  - phase: 02-system-selection-and-scorecard
    provides: "system_view.py layout shell, scorecard table, equipment grid, set_data() pattern"
  - phase: 01-foundation
    provides: "load_data(), loader.py, processing.py formatting helpers, config.py SYSTEM_COLORS"
provides:
  - "compute_cost_over_time(): replacement-cycle cumulative cost array via numpy.cumsum"
  - "interpolate_battery_cost(): numpy.interp against 11-row battery_lookup table"
  - "battery_ratio_label(): formatted percent string for slider live label"
  - "compute_chart_data(): single aggregation function returning all chart data for all three systems"
  - "build_cost_chart(): Plotly Figure with 3 line traces, dollar hovertemplate, uirevision=static"
  - "build_land_chart(): grouped bar Figure comparing land area across systems"
  - "build_turbine_chart(): grouped bar Figure comparing wind turbine counts"
  - "build_pie_chart(): Figure with 3 domain-positioned pie traces, grey No-data for hybrid"
  - "make_chart_section(): complete Dash layout with control panel, legend badges, dcc.Store, 2x2 chart grid"
affects:
  - 03-02-callbacks (wires slider inputs to these figure builders)
  - 04-hybrid-builder (will populate hybrid data in compute_chart_data placeholder)

# Tech tracking
tech-stack:
  added: [numpy (already installed, now imported in processing.py)]
  patterns:
    - "Pure data layer: compute_chart_data() returns all chart data in one dict — callbacks stay fast"
    - "Battery override: override_costs dict in compute_cost_over_time() zeroes base cost and injects slider-interpolated cost for correct replacement cycles"
    - "Hybrid placeholder: zeros/empty dicts throughout Phase 3, TODO comments for Phase 4"
    - "uirevision=static + layout.transition: prevents chart blink on slider drag"
    - "Domain-positioned go.Pie traces: 3 pies in one dcc.Graph without make_subplots overhead"

key-files:
  created:
    - src/layout/charts.py
  modified:
    - src/data/processing.py

key-decisions:
  - "Battery override passes interpolated cost via override_costs dict so compute_cost_over_time handles all replacement cycles (year 0, 12, 24, 36, 48) at the current slider value"
  - "Hybrid system is placeholder zeros/empty throughout Phase 3 — no KeyError risk from data dict"
  - "Empty energy dict for hybrid pie renders as single grey No-data slice to avoid go.Pie(values=[]) error"
  - "External HTML legend row (dbc.Badge) is authoritative for visibility state — no reliance on restyleData (Dash bug #2037)"
  - "dcc.Store(id=store-legend-visibility) holds canonical visibility dict; callbacks in Plan 02 wire badge clicks to store updates"

patterns-established:
  - "Chart figure builders: pure functions taking data arrays + visibility dict, returning go.Figure — no side effects"
  - "compute_chart_data(): single aggregation function called once per slider event, precomputes all arrays"
  - "_visibility() helper: maps store dict key to True or legendonly string"
  - "Control panel: dbc.Card with light #f8f9fa background grouping both sliders"

requirements-completed: [CHART-01, CHART-02, CHART-03, CHART-04, CHART-05, CTRL-01, VIS-03]

# Metrics
duration: 3min
completed: 2026-02-22
---

# Phase 3 Plan 01: Comparison Charts — Data Layer and Figure Builders Summary

**Plotly figure builders for all 4 comparison charts plus numpy-based cost computation with battery interpolation and replacement cycle modeling**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-02-22T05:12:38Z
- **Completed:** 2026-02-22T05:15:16Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added 4 new functions to processing.py: `interpolate_battery_cost`, `battery_ratio_label`, `compute_cost_over_time`, `compute_chart_data`
- Created charts.py with 4 figure builders (`build_cost_chart`, `build_land_chart`, `build_turbine_chart`, `build_pie_chart`) and `make_chart_section` layout factory
- Battery interpolation correctly uses slider-interpolated cost for all replacement cycles (avoids double-counting pitfall from RESEARCH.md)
- All figures verified: 3 traces each, `uirevision="static"`, 300ms transition, no in-chart legend
- `make_chart_section` verified to contain all 13 required component IDs (sliders, labels, legend badges, store, graph ids)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add chart data computation functions to processing.py** - `d94c85d` (feat)
2. **Task 2: Create charts.py with figure builders and chart section layout** - `71c3558` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified
- `src/data/processing.py` - Added numpy import + 4 new functions: interpolate_battery_cost, battery_ratio_label, compute_cost_over_time, compute_chart_data
- `src/layout/charts.py` - New file: build_cost_chart, build_land_chart, build_turbine_chart, build_pie_chart, make_chart_section

## Decisions Made
- Battery override via `override_costs={"Battery (1 day of power)": interpolated_cost}` pattern ensures replacement cycles at years 0, 12, 24, 36, 48 all use the current slider value — not the spreadsheet's $1.8M base cost
- Hybrid placeholder is zeros/empty throughout (no KeyError risk) with TODO comments marking Phase 4 integration points
- Empty energy dict for hybrid pie uses `["No data"]` / `[1]` with grey marker to avoid `go.Pie(values=[])` error
- Used `pd.to_numeric(..., errors="coerce")` for all numeric conversions, consistent with existing processing.py patterns

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None - all functions verified on first attempt. Computed values match expected benchmarks from RESEARCH.md:
- Battery cost at 50/50: $700,000 (expected ~$700K)
- Mechanical year 50: $79,376,798 (expected ~$79M)
- Electrical total cost at 50/50: $14,262,241 (expected ~$14.2M)
- Turbine counts: Mechanical=4, Electrical=1 (correct)

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All figure builders and data computation functions ready for Plan 02 callback wiring
- `make_chart_section()` returns complete layout with all required component IDs
- `compute_chart_data()` is the single aggregation function Plan 02 callbacks will call
- No changes needed to Plan 02 scope — clean interface boundary maintained

---
*Phase: 03-comparison-charts-and-electrical-slider*
*Completed: 2026-02-22*
