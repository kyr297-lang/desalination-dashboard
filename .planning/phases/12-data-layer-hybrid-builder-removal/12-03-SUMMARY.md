---
phase: 12-data-layer-hybrid-builder-removal
plan: 03
subsystem: ui
tags: [plotly, dash, callback, energy-sheet, pandas, processing]

requires:
  - phase: 12-data-layer-hybrid-builder-removal
    plan: 01
    provides: load_data() returning data["energy"] dict with subsystems, total_shaft_power, total_turbine_input, selected_turbine_kw per system

provides:
  - compute_chart_data reads Energy sheet subsystem shaft_power_kw for power breakdown instead of BOM energy_kw columns
  - compute_chart_data computes turbine counts via math.ceil(total_turbine_input / selected_turbine_kw) from Energy sheet
  - TDS and depth slider offsets applied to all three systems including hybrid
  - update_charts callback has no dependency on store-hybrid-slots (5 inputs only)
  - Fallback to BOM-based calculation when data["energy"] is None

affects:
  - 12-04 and beyond (charts now use authoritative Energy sheet data)

tech-stack:
  added: []
  patterns:
    - "_subsystem_name_to_stage() keyword mapper: maps Energy sheet descriptive subsystem names to STAGE_COLORS canonical keys using lowercase keyword matching"
    - "turbine_input_kw subsystem fallback: when total_turbine_input=0 (electrical system uses variant header), sum subsystem turbine_input_kw values instead"

key-files:
  created: []
  modified:
    - src/data/processing.py
    - src/layout/charts.py

key-decisions:
  - "Energy sheet subsystem names mapped to STAGE_COLORS keys via keyword matching (gw extraction -> Water Extraction, ro feed -> Desalination, brine -> Brine Disposal) rather than exact name lookup — more robust to minor naming variations"
  - "Electrical turbine count uses fallback sum of subsystem turbine_input_kw because Energy sheet uses 'Total Electrical Demand' header (not 'Total at Turbine') which the loader does not capture as total_turbine_input"
  - "TDS and depth offsets extended to hybrid system in addition to mechanical and electrical — consistent energy representation"
  - "compute_hybrid_df import removed from charts.py — charts no longer builds hybrid_df; hybrid data comes directly from data['hybrid'] BOM via compute_chart_data"

patterns-established:
  - "Energy data access pattern: data.get('energy') with graceful fallback to BOM calculation when sheet missing — app never crashes on missing sheet"

requirements-completed: [DATA-04]

duration: 25min
completed: 2026-03-26
---

# Phase 12 Plan 03: Charts Energy Update Summary

**Power breakdown and turbine count charts now driven by Energy sheet shaft power and selected turbine size; update_charts callback reduced to 5 inputs with store-hybrid-slots dependency removed.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-03-26
- **Completed:** 2026-03-26
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Power breakdown chart now reads per-subsystem shaft_power_kw from Energy sheet for all three systems (mechanical, electrical, hybrid)
- Turbine count chart now computes counts via ceil(total_turbine_input / selected_turbine_kw) from Energy sheet instead of hardcoded BOM row-name lookups
- update_charts callback cleaned: removed store-hybrid-slots Input and slots parameter; compute_chart_data called without hybrid_df
- TDS and depth slider offsets now applied to hybrid system in addition to mechanical and electrical

## Task Commits

1. **Task 1: Update compute_chart_data to use Energy sheet** - `2c39d80` (feat)
2. **Task 2: Remove store-hybrid-slots dependency from charts.py** - `1876e30` (feat)
3. **chore: update data.xlsx with Energy sheet** - `e530794` (chore)

## Files Created/Modified

- `src/data/processing.py` — Added _subsystem_name_to_stage() mapper, _energy_from_energy_sheet(), replaced turbine count with Energy sheet math, added electrical turbine fallback, extended TDS/depth offsets to hybrid
- `src/layout/charts.py` — Removed compute_hybrid_df import, removed store-hybrid-slots Input, removed slots parameter, updated docstrings

## Decisions Made

- Used keyword matching (lowercase contains checks) for Energy sheet subsystem names to STAGE_COLORS keys rather than an exact string map. This handles naming variations gracefully and maps all three actual subsystem names (GW Extraction, RO Feed Pressurization, Brine Disposal/Reinjection) correctly.
- Electrical total_turbine_input in the Energy sheet is 0.0 because the loader only recognizes "Total at Turbine" prefix but the electrical row is "Total Electrical Demand". Fixed with a fallback: sum subsystem turbine_input_kw values when total_turbine_input is 0. This avoids modifying loader.py (Plan 01's file) and correctly produces electrical turbine count = 1 (596.1 kW / 1500 kW = ceil(0.397) = 1).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Electrical turbine count was 0 due to Energy sheet summary row label mismatch**
- **Found during:** Task 1 verification
- **Issue:** Energy sheet electrical system uses "Total Electrical Demand" as the turbine total row label, but loader.py only captures rows starting with "Total at Turbine". So total_turbine_input=0.0 for electrical, causing turbine count to be 0.
- **Fix:** Added fallback in turbine count calculation: when total_turbine_input is 0, sum subsystem turbine_input_kw values (GW Extraction: 182 + RO Feed: 327.9 + Brine Disposal: 86.2 = 596.1 kW). ceil(596.1/1500) = 1.
- **Files modified:** src/data/processing.py
- **Verification:** Turbine count test passes — electrical turbine count = 1
- **Committed in:** 2c39d80 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - Bug)
**Impact on plan:** Fix essential for correct turbine count display. No scope creep — fix is contained to processing.py turbine count calculation.

## Issues Encountered

- data.xlsx in the worktree was the old version (only Part 1 and Part 2 sheets, no Energy sheet). Copied updated data.xlsx from main project directory before proceeding.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Power breakdown and turbine count charts are now fully driven by Energy sheet data
- The electrical "Total Electrical Demand" label mismatch in the loader is a known issue logged here; the processing.py fallback handles it gracefully
- store-hybrid-slots is still present in shell.py, scorecard.py, and hybrid_builder.py — those are out of scope for Plan 03 and will be handled by Plan 02 (hybrid builder removal)

## Known Stubs

None - all three systems have live Energy sheet data wired to charts.

## Self-Check: PASSED

- FOUND: src/data/processing.py
- FOUND: src/layout/charts.py
- FOUND: commit 2c39d80 (Task 1)
- FOUND: commit 1876e30 (Task 2)
- FOUND: commit e530794 (data.xlsx)

---
*Phase: 12-data-layer-hybrid-builder-removal*
*Completed: 2026-03-26*
