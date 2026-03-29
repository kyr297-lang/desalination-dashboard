---
phase: 15-data-layer-chart-overhaul
plan: 01
subsystem: database
tags: [openpyxl, pandas, config, data-loader, xlsx-parsing]

# Dependency graph
requires:
  - phase: 14-ux-quality-content-rewrite
    provides: electrical PROCESS_STAGES equipment name context; Phase 14 established exact byte sequences for equipment name keys
provides:
  - SUBSYSTEM_POWER dict (3 shaft power constants in config.py)
  - LIFESPAN_DEFAULTS dict (equipment replacement model in config.py)
  - STAGE_COLORS updated to 3-subsystem keys (config.py)
  - PROCESS_STAGES electrical updated to new xlsx component name strings (config.py)
  - EQUIPMENT_DESCRIPTIONS entries for all new electrical name strings (config.py)
  - loader.py section-aware cost_col parsing (electrical=col E, mech/hybrid=col D)
  - loader.py graceful Energy sheet handling (returns None, not raises)
  - loader.py EQUIPMENT_COLUMNS reduced to 4 fields (name, quantity, cost_usd, lifespan_years)
affects: [15-02-PLAN, 15-03-PLAN, processing.py, charts.py]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "cost_col parameter on _parse_section() enables section-aware column parsing without branching"
    - "SUBSYSTEM_POWER/LIFESPAN_DEFAULTS in config.py as engineering constants rather than xlsx-derived values"
    - "Graceful optional-sheet pattern: return None when Energy sheet absent; callers fall back to constants"

key-files:
  created: []
  modified:
    - src/config.py
    - src/data/loader.py

key-decisions:
  - "SUBSYSTEM_POWER hardcoded in config.py as engineering constants (172.9/311.49/81.865 kW) — identical across all 3 systems, simpler than parsing Energy sheet"
  - "Lifespan reads from column immediately after cost_col (col F for electrical, col E for mech/hybrid) — avoids separate lifespan_col parameter"
  - "STAGE_COLORS reduced from 7 to 4 keys (3 subsystems + Other fallback) — aligns with new power breakdown chart model"
  - "_parse_energy_sheet returns None instead of raising — backward-compatible; downstream processing.py will use SUBSYSTEM_POWER fallback in Plan 15-03"

patterns-established:
  - "cost_col=4 default on _parse_section preserves existing mech/hybrid behavior; electrical passes cost_col=5 explicitly"
  - "LIFESPAN_DEFAULTS: only items with replacement lifespans are listed; all others default to indefinite in processing.py"

requirements-completed: [DATA-01, DATA-02, DATA-03, DATA-04]

# Metrics
duration: 3min
completed: 2026-03-28
---

# Phase 15 Plan 01: Data Foundation Summary

**Config updated with SUBSYSTEM_POWER/LIFESPAN_DEFAULTS/3-subsystem STAGE_COLORS; loader.py parses electrical cost from col E and mech/hybrid from col D with graceful Energy sheet fallback**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-28T21:48:09Z
- **Completed:** 2026-03-28T21:51:00Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added SUBSYSTEM_POWER dict to config.py (172.9 / 311.49 / 81.865 kW shaft power constants)
- Added LIFESPAN_DEFAULTS dict with battery (12yr), RO membrane (7yr) replacement lifespans
- Replaced 7-stage STAGE_COLORS with 3-subsystem model (Groundwater Extraction, RO Desalination, Brine Reinjection) plus Other fallback
- Updated PROCESS_STAGES electrical to use new xlsx component name strings with exact unicode sequences
- Added 10 new EQUIPMENT_DESCRIPTIONS entries for new electrical component names
- Fixed _parse_section to accept cost_col parameter — electrical reads from col E (total cost), mech/hybrid from col D
- Reduced EQUIPMENT_COLUMNS from 6 to 4 fields (removed energy_kw, land_area_m2)
- Made _parse_energy_sheet return None instead of raising when Energy sheet absent

## Task Commits

Each task was committed atomically:

1. **Task 1: Update config.py with new constants and stage mappings** - `3cdb86d` (feat)
2. **Task 2: Fix loader.py for section-aware cost column and Energy sheet resilience** - `570d4bf` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified
- `src/config.py` - Added SUBSYSTEM_POWER, LIFESPAN_DEFAULTS; replaced STAGE_COLORS; updated PROCESS_STAGES electrical; added 10 EQUIPMENT_DESCRIPTIONS entries
- `src/data/loader.py` - Added cost_col to _parse_section(); reduced EQUIPMENT_COLUMNS to 4; graceful Energy sheet None return

## Decisions Made
- SUBSYSTEM_POWER hardcoded in config.py as engineering constants (172.9/311.49/81.865 kW) — identical across all 3 systems regardless of drive type; Energy sheet has these but also contains system-specific drivetrain data. Hardcoding is simpler and more reliable.
- Lifespan reads from column immediately after cost_col — avoids a separate lifespan_col parameter; for electrical (cost_col=5) lifespan is col F (6), for mech/hybrid (cost_col=4) lifespan is col E (5).
- Kept old EQUIPMENT_DESCRIPTIONS keys (e.g., "Turbine", "Battery (1 day of power)") for backward compatibility with any existing mechanical/hybrid references; new electrical keys added alongside them.
- _parse_energy_sheet returns None instead of raising ValueError — allows app to load without Energy sheet while processing.py (Plan 15-03) will add SUBSYSTEM_POWER fallback.

## Deviations from Plan

None — plan executed exactly as written. All 5 changes to config.py and 4 changes to loader.py completed per spec.

## Issues Encountered

**Pre-existing test failure (out of scope):** `tests/test_compute_chart_data_sliders.py` was already failing before Plan 15-01 changes (verified via git stash). The test fixture uses the old 6-column schema (`energy_kw`, `land_area_m2`) and is missing the `hybrid` key in synthetic_data. Also tests `land_area`/`turbine_count` return keys that are removed in Plans 15-02/15-03. Documented in `deferred-items.md` for Plan 15-03 resolution.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- Plan 15-02 (charts.py overhaul) can proceed: STAGE_COLORS has 3-subsystem keys ready
- Plan 15-03 (processing.py overhaul) can proceed: SUBSYSTEM_POWER and LIFESPAN_DEFAULTS available; loader.py energy key returns None when sheet absent (processing.py fallback needed)
- Electrical BOM rows now load cost_usd from col E (total cost) — first row = $1,000,000 for turbine

---
*Phase: 15-data-layer-chart-overhaul*
*Completed: 2026-03-28*
