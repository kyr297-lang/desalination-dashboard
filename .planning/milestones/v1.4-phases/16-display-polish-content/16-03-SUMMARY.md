---
phase: 16-display-polish-content
plan: 03
subsystem: ui
tags: [dash, plotly, scorecard, overview, content]

# Dependency graph
requires:
  - phase: 15-data-layer-chart-overhaul
    provides: compute_scorecard_metrics returns cost-only dict; BOM DataFrames with cost_usd column
provides:
  - Scorecard legend text "Lower total cost is better."
  - Scorecard table with only Total Cost row (land area and power rows removed)
  - generate_comparison_text comparing cost only
  - Overview system card descriptions referencing "equipment and cost data"
  - Intro card without land/energy references
affects: [scorecard, overview, comparison-text]

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - src/layout/scorecard.py
    - src/layout/overview.py
    - src/data/processing.py

key-decisions:
  - "Scorecard renders only Total Cost row — land area and power rows removed to align with Phase 15 cost-only data model"
  - "generate_comparison_text metric_labels reduced to cost only — land_area and efficiency comparisons removed"
  - "Overview card descriptions rewritten to reference equipment and cost data, removing all land/energy mentions"

patterns-established: []

requirements-completed: [DISP-05, DISP-06, DISP-07, DISP-08]

# Metrics
duration: 5min
completed: 2026-03-29
---

# Phase 16 Plan 03: Display Polish Content Summary

**Scorecard legend updated to "Lower total cost is better.", land/power rows removed from scorecard table, and overview card descriptions rewritten to reference only equipment and cost.**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-29T05:31:00Z
- **Completed:** 2026-03-29T05:32:00Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Scorecard legend changed from "Green = best of the compared systems, Red = worst. Lower cost, less land, and less energy are better." to "Lower total cost is better."
- Removed Total Land Area and Total Power (kW) rows from scorecard table in both 2-column and 3-column (hybrid) modes
- Removed land_area and efficiency entries from generate_comparison_text metric_labels — now compares cost only
- All three _SYSTEM_CARDS descriptions updated: "cost, land area, and energy data" -> "equipment and cost data"
- Intro card paragraph updated: "compare costs, land use, and energy requirements" -> "compare equipment and costs"

## Task Commits

Each task was committed atomically:

1. **Task 1: Update scorecard legend and verify cost-only display** - `71800de` (feat)
2. **Task 2: Rewrite overview card descriptions to remove land area and energy references** - `6b2e7b3` (feat)

**Plan metadata:** (committed with final docs commit)

## Files Created/Modified
- `src/layout/scorecard.py` - Legend text updated; land/power rows removed; docstring updated to reflect cost-only
- `src/data/processing.py` - generate_comparison_text metric_labels reduced to cost-only
- `src/layout/overview.py` - System card descriptions and intro card rewritten without land/energy references

## Decisions Made
- Scorecard shows only Total Cost row — this aligns with the Phase 15 data model which removed energy_kw and land_area_m2 from the scorecard path. The columns still exist in BOM DataFrames (for the power chart), but scorecard no longer uses them.
- RAG color computation simplified to use only cost_colors (removed land_colors and energy_colors from green-dot count logic).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed stale land/power rows from scorecard table**
- **Found during:** Task 1 (scorecard.py inspection)
- **Issue:** The plan's DISP-05 verification confirmed land area and power rows were still present in scorecard.py — the STATE.md decision "compute_scorecard_metrics returns only cost" described the intended end state, not the current state. The rows needed to be removed.
- **Fix:** Removed Total Land Area and Total Power (kW) rows from both the hybrid (3-col) and non-hybrid (2-col) table branches. Removed land_colors and energy_colors from RAG computation. Cleaned up related green-dot counting logic.
- **Files modified:** src/layout/scorecard.py
- **Verification:** Automated check confirmed no land_area, energy_kw, or power terms in row definitions
- **Committed in:** 71800de (Task 1 commit)

**2. [Rule 1 - Bug] Updated generate_comparison_text to remove land_area/efficiency comparisons**
- **Found during:** Task 1 (DISP-07 verification)
- **Issue:** metric_labels still contained "land_area" and "efficiency" entries; loop iterated over all three metrics
- **Fix:** Reduced metric_labels to {"cost": "cost"}; loop now only iterates ["cost"]
- **Files modified:** src/data/processing.py
- **Verification:** Confirmed "land_area" and "efficiency" keys absent from metric_labels
- **Committed in:** 71800de (Task 1 commit)

**3. [Rule 1 - Bug] Updated make_scorecard_table docstring**
- **Found during:** Task 2 (post-fix verification grep)
- **Issue:** Docstring still said "Computes aggregate cost, land area, and energy metrics" — grep -i "land area" was catching this stale docstring text
- **Fix:** Updated docstring to "Computes aggregate cost for Mechanical and Electrical systems"
- **Files modified:** src/layout/scorecard.py
- **Verification:** grep -i "land area" returns no matches in scorecard.py
- **Committed in:** 6b2e7b3 (Task 2 commit)

---

**Total deviations:** 3 auto-fixed (all Rule 1 — bugs: stale display code not matching Phase 15 data model intent)
**Impact on plan:** All fixes necessary for correctness — removing obsolete scorecard rows was the core goal of DISP-05. No scope creep.

## Issues Encountered
None — straightforward text and UI-row cleanup.

## Known Stubs
None — all changes are complete. The BOM DataFrames still contain energy_kw and land_area_m2 columns (used by the power breakdown chart), but the scorecard and comparison text no longer reference those columns.

## Next Phase Readiness
- Phase 16 plan 03 complete — scorecard and overview now fully aligned with Phase 15 cost-only data model
- No blockers for remaining Phase 16 plans

## Self-Check: PASSED

- FOUND: src/layout/scorecard.py
- FOUND: src/layout/overview.py
- FOUND: src/data/processing.py
- FOUND: .planning/phases/16-display-polish-content/16-03-SUMMARY.md
- FOUND: commit 71800de (Task 1)
- FOUND: commit 6b2e7b3 (Task 2)

---
*Phase: 16-display-polish-content*
*Completed: 2026-03-29*
