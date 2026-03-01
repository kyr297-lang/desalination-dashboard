---
phase: 07-data-layer
plan: 01
subsystem: database
tags: [openpyxl, pandas, excel, data-loading]

# Dependency graph
requires: []
provides:
  - load_data() updated to read 'Part 1' sheet (renamed from 'Sheet1')
  - 'tds_lookup' DataFrame: 20 rows, columns [tds_ppm, ro_energy_kw], TDS range 0-1900 PPM
  - 'depth_lookup' DataFrame: 20 rows, columns [depth_m, pump_energy_kw], depth range 0-1900 m
  - _parse_part2_lookups(wb) helper function reading 'Part 2' sheet
affects:
  - 08-sliders (needs tds_lookup and depth_lookup for slider interpolation)
  - any module that calls load_data()

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Named-key dict return from load_data() extended (not replaced) — backward-compatible additions"
    - "Private helper _parse_part2_lookups() follows same pattern as _parse_battery_lookup()"

key-files:
  created: []
  modified:
    - src/data/loader.py

key-decisions:
  - "Part 2 lookup tables parsed in load_data() call order before Part 1 parsing — workbook already open, no extra file I/O"
  - "Row range 2-21 confirmed for Part 2 data (20 rows each table, 100-unit steps from 0 to 1900)"
  - "All 'Sheet1' references updated to 'Part 1' including docstrings, comments, error messages, and code"

patterns-established:
  - "Lookup table columns defined as module-level constants (TDS_LOOKUP_COLUMNS, DEPTH_LOOKUP_COLUMNS)"
  - "Private parser functions validate sheet presence before reading, raising ValueError with available sheet names"

requirements-completed: [DATA-01, DATA-02, DATA-03]

# Metrics
duration: 6min
completed: 2026-02-28
---

# Phase 7 Plan 01: Data Layer — loader.py Sheet Rename and Part 2 Lookup Tables Summary

**loader.py updated to read 'Part 1' sheet and return two new DataFrames — tds_lookup (TDS vs RO-energy, 20 rows) and depth_lookup (depth vs pump-energy, 20 rows) — from the 'Part 2' sheet of data.xlsx**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-01T04:24:41Z
- **Completed:** 2026-03-01T04:30:41Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Fixed app startup crash: loader.py now opens "Part 1" sheet (was "Sheet1") — DATA-01
- Added _parse_part2_lookups() that reads TDS and depth lookup tables from "Part 2" sheet — DATA-02, DATA-03
- load_data() return dict extended from 4 keys to 6 keys; existing keys unchanged (backward-compatible)

## New load_data() Return Shape

```python
{
    "electrical":    pd.DataFrame  # equipment rows, columns: name/quantity/cost_usd/energy_kw/land_area_m2/lifespan_years
    "mechanical":    pd.DataFrame  # equipment rows, same columns
    "miscellaneous": pd.DataFrame  # equipment rows, same columns
    "battery_lookup":pd.DataFrame  # 11 rows, columns: battery_fraction/tank_fraction/battery_kwh/tank_gal/battery_cost/tank_cost/total_cost
    "tds_lookup":    pd.DataFrame  # 20 rows, columns: [tds_ppm, ro_energy_kw]
    "depth_lookup":  pd.DataFrame  # 20 rows, columns: [depth_m, pump_energy_kw]
}
```

## Part 2 Sheet Layout (Confirmed)

```
Row 1 (headers):  col A="TDS",   col B="kW required (RO Desalination)",
                  col D="Depth", col E="kW required (pump energy)"
Rows 2-21 (data): 20 data rows per table
  - TDS:   col A values  0, 100, 200, ..., 1900 PPM   | col B = RO energy kW
  - Depth: col D values  0, 100, 200, ..., 1900 m      | col E = pump energy kW
```

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix Part 1 sheet reference** - `74d7bb2` (fix)
2. **Task 2: Add Part 2 lookup table parsers** - `5b869d9` (feat)

**Plan metadata:** TBD (docs: complete plan)

## Files Created/Modified

- `src/data/loader.py` - Updated sheet name references (Sheet1 -> Part 1), added TDS_LOOKUP_COLUMNS and DEPTH_LOOKUP_COLUMNS constants, added _parse_part2_lookups() helper, extended load_data() return dict with tds_lookup and depth_lookup keys

## Decisions Made

- Parse Part 2 before Part 1 in load_data() since workbook is already open — no additional file I/O cost
- Row range 2-21 (20 data rows) confirmed by inspecting data.xlsx Part 2 sheet structure
- Column positions confirmed: TDS in col A (pos 1), RO energy in col B (pos 2), Depth in col D (pos 4), pump energy in col E (pos 5)

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None — both tasks executed cleanly on first attempt.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 8 (sliders) is unblocked: load_data() now provides 'tds_lookup' and 'depth_lookup' DataFrames with the correct columns and 20-row structure needed for slider interpolation
- All existing keys (electrical, mechanical, miscellaneous, battery_lookup) remain present and non-empty — no regressions

---
*Phase: 07-data-layer*
*Completed: 2026-02-28*
