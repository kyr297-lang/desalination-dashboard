---
phase: 15-data-layer-chart-overhaul
plan: 02
subsystem: ui
tags: [plotly, dash, callbacks, pandas, numpy, processing, charts]

# Dependency graph
requires:
  - phase: 15-data-layer-chart-overhaul
    plan: 01
    provides: SUBSYSTEM_POWER, LIFESPAN_DEFAULTS, STAGE_COLORS (3-subsystem keys), EQUIPMENT_COLUMNS (4 fields, no energy_kw/land_area_m2)
provides:
  - processing.py with 3-subsystem energy model using SUBSYSTEM_POWER constants
  - processing.py compute_chart_data returns exactly 3 keys (cost_over_time, energy_breakdown, electrical_total_cost)
  - processing.py LIFESPAN_DEFAULTS fallback in compute_cost_over_time
  - processing.py battery override key updated to "Battery (Tesla Megapack 3.9MWh unit)"
  - processing.py compute_scorecard_metrics returns only "cost" metric
  - charts.py with 2-chart layout (Cost Over Time + Power Breakdown)
  - charts.py chart-pie renamed to chart-power
  - charts.py build_land_chart and build_turbine_chart deleted
  - charts.py update_charts callback reduced from 9 to 7 outputs
  - charts.py build_energy_bar_chart uses 3 subsystem keys with barmode=stack
affects: [15-03-PLAN, src/layout/system_view.py, src/layout/scorecard.py]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "SUBSYSTEM_POWER dict copy per system: dict(SUBSYSTEM_POWER) shallow copy ensures independent offsets per system"
    - "Slider offsets applied after SUBSYSTEM_POWER copy: energy[subsystem] += slider_kw pattern"
    - "7-output callback pattern: 2 figures + 5 labels"

key-files:
  created: []
  modified:
    - src/data/processing.py
    - src/layout/charts.py

key-decisions:
  - "Energy breakdown uses SUBSYSTEM_POWER constants (not Energy sheet) — avoids dependency on optional Energy sheet in data.xlsx"
  - "TDS offset applies to RO Desalination subsystem key; depth offset applies to Groundwater Extraction — matching new 3-subsystem names exactly"
  - "barmode changed from group to stack for power breakdown — stacked bars better convey total load composition than grouped bars"
  - "compute_scorecard_metrics returns only cost — land_area and efficiency columns no longer exist in BOM DataFrames after Plan 01 EQUIPMENT_COLUMNS update"

requirements-completed: [CHART-01, CHART-02, CHART-03, CHART-04, CHART-05, CHART-07]

# Metrics
duration: 4min
completed: 2026-03-28
---

# Phase 15 Plan 02: Data Layer & Chart Overhaul Summary

**3-subsystem power model wired end-to-end: processing.py uses SUBSYSTEM_POWER constants with TDS/depth offsets, charts.py delivers 2-chart layout (cost + power) with 7-output callback and chart-power replacing chart-pie**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-28T22:13:56Z
- **Completed:** 2026-03-28T22:17:57Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Replaced old 7-stage energy model (Energy sheet dependent) with SUBSYSTEM_POWER constants providing 3-subsystem breakdown (Groundwater Extraction, RO Desalination, Brine Reinjection)
- Fixed battery slider to use "Battery (Tesla Megapack 3.9MWh unit)" — matching new xlsx equipment name from Plan 01 update
- Added LIFESPAN_DEFAULTS fallback in compute_cost_over_time so battery and RO membrane replacements are correctly scheduled even when xlsx has no lifespan column
- Removed land/turbine charts (chart-land, chart-turbine, build_land_chart, build_turbine_chart) and reduced callback from 9 to 7 outputs
- Renamed chart-pie to chart-power and updated ALL_STAGES to 3 subsystem keys with stacked bar display

## Task Commits

Each task was committed atomically:

1. **Task 1: Overhaul processing.py energy model, battery name, and lifespan** - `8b96ee2` (feat)
2. **Task 2: Remove land/turbine charts, rename chart-pie to chart-power, reduce callback** - `ffab6d5` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified
- `src/data/processing.py` - New 3-subsystem energy model, LIFESPAN_DEFAULTS fallback, updated battery key, removed dead helpers, scorecard returns cost only
- `src/layout/charts.py` - 2-chart layout, chart-power ID, 7-output callback, stacked bar with 3 subsystem stages

## Decisions Made
- Energy breakdown uses SUBSYSTEM_POWER constants (not Energy sheet) — avoids dependency on optional Energy sheet; identical power demands across all 3 systems
- TDS offset applies to "RO Desalination" and depth offset to "Groundwater Extraction" — matching the new subsystem key names exactly
- barmode changed from group to stack — stacked bars better represent total load composition per system
- compute_scorecard_metrics now returns only cost — BOM DataFrames no longer have energy_kw or land_area_m2 columns after Plan 01

## Deviations from Plan

None - plan executed exactly as written. The grep check for old stage keys triggered on docstrings (not functional code), which were updated as part of the cleanup.

## Issues Encountered
None - all verifications passed on first run.

## Next Phase Readiness
- Plan 03 (scorecard and equipment view updates) can proceed: processing.py returns only cost from compute_scorecard_metrics, which Plan 03 needs to consume correctly
- All chart IDs updated: chart-power is in the DOM, chart-land and chart-turbine are gone
- Battery slider will correctly update the electrical cost-over-time line using new equipment name

---
*Phase: 15-data-layer-chart-overhaul*
*Completed: 2026-03-28*
