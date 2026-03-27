---
phase: 12-data-layer-hybrid-builder-removal
plan: 01
subsystem: database
tags: [openpyxl, pandas, excel, data-loader, energy-sheet]

requires:
  - phase: 11-parameter-exploration
    provides: Stable loader.py with SECTION_HEADERS, _parse_section, and Part 2 lookup parsing

provides:
  - Updated SECTION_HEADERS matching updated data.xlsx Part 1 headers (Hybrid Components)
  - _parse_energy_sheet() function returning grouped energy data dict
  - load_data() returning 7 keys including "hybrid" and "energy"
  - Fixed battery lookup column offsets (L-R instead of J-P)
  - PROCESS_STAGES["hybrid"] with all 16 actual hybrid BOM component names
  - EQUIPMENT_DESCRIPTIONS for all 16 new hybrid components

affects:
  - 12-02-hybrid-builder-removal
  - 12-03-charts-energy-update
  - src/data/processing.py (must replace data["miscellaneous"] with data["hybrid"])
  - src/layout/equipment_grid.py (must replace "miscellaneous" key reference)
  - src/layout/hybrid_builder.py (planned for deletion in 12-02)

tech-stack:
  added: []
  patterns:
    - "_parse_energy_sheet(wb) private function pattern — mirrors _parse_battery_lookup and _parse_part2_lookups for Energy sheet parsing"
    - "load_data() now returns 7 keys: electrical, mechanical, hybrid, battery_lookup, tds_lookup, depth_lookup, energy"

key-files:
  created: []
  modified:
    - src/data/loader.py
    - src/config.py

key-decisions:
  - "Battery lookup table column positions shifted from J-P (10-16) to L-R (12-18) in updated data.xlsx — fixed as auto Rule 1 bug"
  - "Energy sheet parser uses system header row detection (Mechanical System / Electrical System / Hybrid System) to group subsystem rows"
  - "Summary rows distinguished from subsystem rows via startswith() matching on known summary labels"
  - "All 16 hybrid BOM components mapped to PROCESS_STAGES['hybrid'] — no old miscellaneous placeholder entries retained"

patterns-established:
  - "Energy sheet parser: header rows in col A trigger system group flush; summary rows captured by startswith(); remaining rows are subsystem data"
  - "load_data() return contract: 7 keys — BOM DataFrames (electrical/mechanical/hybrid), lookup DataFrames (battery/tds/depth), energy dict"

requirements-completed: [DATA-01, DATA-02, DATA-04]

duration: 18min
completed: 2026-03-26
---

# Phase 12 Plan 01: Data Layer Fix Summary

**Fixed loader crash by updating SECTION_HEADERS for Hybrid Components, adding Energy sheet parser with three-system grouped dict, fixing battery lookup column offsets, and renaming all miscellaneous references to hybrid throughout data layer.**

## Performance

- **Duration:** ~18 min
- **Started:** 2026-03-26
- **Completed:** 2026-03-26
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `load_data()` no longer crashes on startup — SECTION_HEADERS now matches actual Part 1 headers in updated data.xlsx
- Energy sheet parsed into structured dict grouped by system with subsystems, total_shaft_power, total_turbine_input, and selected_turbine_kw
- All 16 hybrid BOM components mapped to PROCESS_STAGES["hybrid"] with full EQUIPMENT_DESCRIPTIONS

## Task Commits

1. **Task 1: Update loader SECTION_HEADERS, rename miscellaneous to hybrid, parse Energy sheet** - `2db69b0` (feat)
2. **Task 2: Update config.py PROCESS_STAGES — rename miscellaneous to hybrid** - `6c5c843` (feat)

## Files Created/Modified

- `src/data/loader.py` — Updated SECTION_HEADERS, added _parse_energy_sheet(), renamed all miscellaneous->hybrid, fixed battery column offsets, updated docstrings
- `src/config.py` — Renamed PROCESS_STAGES key miscellaneous->hybrid, added 16 hybrid component mappings, added 16 EQUIPMENT_DESCRIPTIONS entries

## Decisions Made

- Battery lookup table column positions had shifted from J-P (cols 10-16) to L-R (cols 12-18) in the updated data.xlsx — fixed as deviation Rule 1 bug within Task 1 commit.
- Energy sheet parser reads row-by-row, uses system header strings to demarcate groups, and startswith() matching to capture Total Shaft Power / Total at Turbine / Selected Turbine summary rows.
- All 16 hybrid BOM component names mapped to PROCESS_STAGES["hybrid"] stages based on equipment function — turbine and drivetrain to Water Extraction, filtration to Pre-Treatment, RO trains and pumps to Desalination, calcite contactor to Post-Treatment, brine well and storage tank to Brine Disposal, PLC to Control.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed battery lookup column offset shift**
- **Found during:** Task 1 (updating loader)
- **Issue:** Battery lookup table in updated data.xlsx starts at column L (12), not column J (10). The old _parse_battery_lookup() used hardcoded column indices 10-16, which now read empty cells, returning all-None rows.
- **Fix:** Updated column indices in _parse_battery_lookup() from 10-16 to 12-18 to match actual table position.
- **Files modified:** src/data/loader.py
- **Verification:** Battery lookup returns 11 rows with correct battery_fraction 0.0-1.0 values.
- **Committed in:** 2db69b0 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - Bug)
**Impact on plan:** Battery fix essential for correct electrical system slider behavior. No scope creep.

## Issues Encountered

- `processing.py`, `equipment_grid.py`, and `hybrid_builder.py` still reference `data["miscellaneous"]` and `PROCESS_STAGES["miscellaneous"]`. These are out-of-scope for plan 12-01 and are logged in `deferred-items.md`. Plans 12-02 and 12-03 will resolve them.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `load_data()` returns 7 keys including "hybrid" and "energy" — ready for 12-02 and 12-03
- `PROCESS_STAGES["hybrid"]` has all 16 actual component names — ready for equipment grid
- `deferred-items.md` lists remaining "miscellaneous" references in processing.py, equipment_grid.py, and hybrid_builder.py for plans 12-02 and 12-03 to resolve

---
*Phase: 12-data-layer-hybrid-builder-removal*
*Completed: 2026-03-26*
