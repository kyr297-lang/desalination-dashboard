---
phase: 14-ux-quality-content-rewrite
plan: 03
subsystem: ui
tags: [config, process-stages, equipment-descriptions, data-mapping, openpyxl]

# Dependency graph
requires:
  - phase: 12-data-layer-hybrid-builder-removal
    provides: Updated data.xlsx BOM with hydraulic mechanical components (HPU, manifold, motors, VTP, plunger pump)
provides:
  - PROCESS_STAGES["mechanical"] updated with 15 current hydraulic BOM components across 5 process stages
  - EQUIPMENT_DESCRIPTIONS entries for all 10 new hydraulic components (1-2 sentences, student-accessible)
  - Stale mechanical descriptions removed (250kW turbine, submersible pump, gear pump, Pipes, extra storage tank)
  - processing.py fallback turbine name fixed from "250kW aeromotor turbine " to "1 MW Aeromotor Turbine"
affects: [mechanical equipment table rendering, equipment stage groupings, tooltips, turbine count fallback]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "PROCESS_STAGES keys must match column B data.xlsx strings byte-for-byte (including en-dash U+2013, double spaces)"
    - "Read exact cell values via openpyxl repr() before writing any key string -- never type by hand"

key-files:
  created: []
  modified:
    - src/config.py
    - src/data/processing.py

key-decisions:
  - "Plunger Pump key uses en-dash (U+2013) as the separator in 'K 13000 - 3G' matching exact data.xlsx byte sequence"
  - "High Pressure Pump key has no closing paren (matches data.xlsx row 25 exactly)"
  - "Gearbox key preserves double space: 'Gearbox (Winergy  PEAB series)' -- differs from hybrid single-space variant"
  - "Stale entries removed: 250kW aeromotor turbine, Submersible pump, Gear and Booster Pump, Pipes, Extra storage tank (no gallons)"

patterns-established:
  - "Pattern: Always read data.xlsx column B with openpyxl repr() before updating PROCESS_STAGES keys"

requirements-completed: [CONTENT-02]

# Metrics
duration: 10min
completed: 2026-03-27
---

# Phase 14 Plan 03: Mechanical Content Update Summary

**Mechanical PROCESS_STAGES replaced with 15 hydraulic BOM components mapped to correct process stages, new EQUIPMENT_DESCRIPTIONS added for all hydraulic drive components, and processing.py fallback turbine name fixed to match current data.xlsx**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-03-27T01:18:00Z
- **Completed:** 2026-03-27T01:28:00Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Replaced stale mechanical PROCESS_STAGES (5 old components) with 15 current hydraulic drive components grouped into correct process stages (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal)
- Added EQUIPMENT_DESCRIPTIONS for 10 new hydraulic components: Gearbox (Winergy PEAB), HPU, Hydraulic Motor CA 50, Hydraulic Motor CA 70, Plunger Pump, High Pressure Pump (Danfoss), Reverse osmosis train, Extra storage tank (100k gal), plus retained Wind turbine rotor lock, Gate valve, Calcite bed contactors
- Removed 5 stale EQUIPMENT_DESCRIPTIONS (250kW aeromotor turbine, Submersible pump, Gear and Booster Pump, Pipes, Extra storage tank without gallons suffix)
- Fixed processing.py line 662 fallback from "250kW aeromotor turbine " to "1 MW Aeromotor Turbine"

## Task Commits

Each task was committed atomically:

1. **Task 1: Read exact component names from data.xlsx and update PROCESS_STAGES + EQUIPMENT_DESCRIPTIONS + processing.py fallback** - `62208db` (feat)

**Plan metadata:** (pending docs commit)

## Files Created/Modified
- `src/config.py` - PROCESS_STAGES["mechanical"] replaced; stale EQUIPMENT_DESCRIPTIONS removed; new hydraulic component descriptions added
- `src/data/processing.py` - Line 662 fallback turbine name fixed from "250kW aeromotor turbine " to "1 MW Aeromotor Turbine"

## Decisions Made
- Used exact bytes from openpyxl repr() for all PROCESS_STAGES keys, capturing en-dash (U+2013) in Plunger Pump key and double space in Gearbox key
- Row 25 (High Pressure Pump) has no closing paren in data.xlsx -- key matches data exactly without adding one
- Hybrid PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS left completely untouched (separate keys, separate section)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Mechanical equipment table will now correctly display hydraulic components grouped by process stage with descriptions
- All three systems (mechanical, electrical, hybrid) have matching PROCESS_STAGES keys and EQUIPMENT_DESCRIPTIONS
- App starts without errors; ready for deployment

## Self-Check: PASSED

- FOUND: src/config.py
- FOUND: src/data/processing.py
- FOUND: .planning/phases/14-ux-quality-content-rewrite/14-03-SUMMARY.md
- FOUND: commit 62208db (feat task commit)
- FOUND: commit ff55354 (docs metadata commit)

---
*Phase: 14-ux-quality-content-rewrite*
*Completed: 2026-03-27*
