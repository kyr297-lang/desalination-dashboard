---
phase: 12-data-layer-hybrid-builder-removal
plan: 02
subsystem: ui
tags: [dash, plotly, hybrid-builder, scorecard, equipment-grid, refactor]

requires:
  - phase: 12-data-layer-hybrid-builder-removal/12-01
    provides: load_data() returning 7 keys including data["hybrid"] and PROCESS_STAGES["hybrid"]

provides:
  - hybrid_builder.py deleted from codebase — no slot dropdowns, gate overlay, or slot counter
  - system_view.py renders hybrid equipment as static table via make_equipment_section (identical to mechanical/electrical)
  - scorecard always renders 3 columns from BOM data on initial page load — no gating
  - comparison text generated at render time from BOM metrics
  - processing.py compute_chart_data reads data["hybrid"] directly (no hybrid_df parameter)
  - equipment_grid.py make_equipment_section: all systems use same stage-grouped rendering path

affects:
  - 12-03-charts-energy-update
  - app.py (entry point clean of hybrid_builder)
  - src/layout/charts.py (store-hybrid-slots Input removed; also cleaned in this plan)

tech-stack:
  added: []
  patterns:
    - "Static BOM rendering: hybrid system rendered via make_equipment_section(data['hybrid'], 'hybrid', data) — same call as mechanical/electrical"
    - "Scorecard and comparison text generated at layout render time in system_view.py — no callback updates needed"
    - "compute_chart_data reads all three system DataFrames from data dict directly — no external df parameters"

key-files:
  created: []
  modified:
    - src/layout/system_view.py
    - src/layout/shell.py
    - src/layout/scorecard.py
    - src/layout/equipment_grid.py
    - src/layout/charts.py
    - src/data/processing.py
    - app.py

key-decisions:
  - "Hybrid system rendered as static equipment table — identical code path to mechanical/electrical via make_equipment_section"
  - "Scorecard always 3-column: initial render passes data['hybrid'] as third arg to make_scorecard_table, no callback needed"
  - "Rule 3 fix applied to charts.py: store-hybrid-slots removed as Input and compute_hybrid_df removed — store no longer exists in DOM"
  - "compute_chart_data signature simplified: hybrid_df parameter removed; reads data['hybrid'] directly"
  - "equipment_grid _make_cross_system_comparison now includes hybrid as a comparison system"

patterns-established:
  - "All systems equal: make_equipment_section(system_df, system_key, data) works for mechanical, electrical, and hybrid with identical code"
  - "Layout-time rendering: scorecard and comparison text built in create_system_view_layout, not in callbacks"

requirements-completed: [DATA-02, DATA-03, CONTENT-03]

duration: 5min
completed: 2026-03-27
---

# Phase 12 Plan 02: Hybrid Builder Removal Summary

**Deleted hybrid_builder.py and replaced slot-driven hybrid UI with static BOM rendering — hybrid tab now identical to mechanical/electrical with immediate 3-column scorecard and stage-grouped equipment table.**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-27T00:31:40Z
- **Completed:** 2026-03-27T00:36:31Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments

- `hybrid_builder.py` deleted — zero slot dropdowns, gate overlays, or slot counter remaining in the codebase
- Hybrid tab renders static equipment table using the same `make_equipment_section` call as mechanical/electrical
- Scorecard renders 3 columns immediately on page load using `data["hybrid"]` from BOM — no slot-fill gate
- `compute_chart_data` simplified: no `hybrid_df` parameter, reads `data["hybrid"]` directly
- Cross-system comparison in equipment grid now includes hybrid as a comparison target

## Task Commits

1. **Task 1: Delete hybrid_builder.py and remove all imports/references** - `442d970` (feat)
2. **Task 2: Rewrite scorecard and processing to use hybrid BOM directly** - `c37fbcb` (feat)

**Plan metadata:** (docs commit — created after this summary)

## Files Created/Modified

- `src/layout/hybrid_builder.py` — DELETED
- `src/layout/system_view.py` — Removed hybrid builder import, gate overlay, slot UI; unified equipment rendering; 3-column scorecard at render time
- `src/layout/shell.py` — Removed SLOT_STAGES import and store-hybrid-slots dcc.Store
- `src/layout/scorecard.py` — Removed update_scorecard, update_gate_overlay, update_hybrid_equipment callbacks; removed compute_hybrid_df and make_equipment_section imports
- `src/layout/equipment_grid.py` — Removed hybrid_selected gate branch; all systems use same stage-grouped path; cross-system comparison includes hybrid
- `src/data/processing.py` — Deleted compute_hybrid_df function; updated compute_chart_data to read data["hybrid"] directly
- `app.py` — Removed set_hybrid_builder_data import and call
- `src/layout/charts.py` — Removed store-hybrid-slots Input and compute_hybrid_df call (Rule 3 fix)

## Decisions Made

- Scorecard and comparison text are now built at layout render time in `create_system_view_layout` — no callback needed since the data is static (loaded from data.xlsx).
- `compute_chart_data` now always has full hybrid data — uses real values for all charts rather than placeholder zeros.
- Hybrid turbine count in charts uses name substring search for "turbine" (case-insensitive) from the hybrid BOM.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed charts.py store-hybrid-slots Input removed from DOM**
- **Found during:** Task 1 (removing store-hybrid-slots from shell.py)
- **Issue:** `charts.py` callback had `Input("store-hybrid-slots", "data")` as one of 6 inputs. After removing the dcc.Store from shell.py, the store no longer exists in the DOM. With `suppress_callback_exceptions=True`, the callback would never fire, breaking all four charts.
- **Fix:** Removed `Input("store-hybrid-slots", "data")` and the `slots` parameter from `update_charts` in charts.py; removed `compute_hybrid_df` call and import from charts.py; updated `compute_chart_data` call to not pass `hybrid_df` keyword argument.
- **Files modified:** src/layout/charts.py
- **Verification:** App imports cleanly; all cleanup checks pass (`store-hybrid-slots` absent from all files).
- **Committed in:** `442d970` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 3 - Blocking)
**Impact on plan:** Essential fix — removing the store without removing the Input reference would have silently broken all chart rendering. Plan 12-03 (charts energy update) will not need to re-address this since it was handled here.

## Issues Encountered

None beyond the Rule 3 deviation above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `hybrid_builder.py` is gone — zero references remain in the codebase
- `data["hybrid"]` is live in all chart and scorecard computations
- Plan 12-03 (charts energy update) can proceed — `compute_chart_data` now accepts data dict with all three systems
- `PROCESS_STAGES["hybrid"]` stage mapping drives energy breakdown chart for hybrid system

## Self-Check

- FOUND: src/layout/system_view.py
- FOUND: src/layout/shell.py
- FOUND: src/layout/scorecard.py
- FOUND: src/layout/equipment_grid.py
- FOUND: src/data/processing.py
- FOUND: app.py
- FOUND: src/layout/charts.py
- NOT FOUND: src/layout/hybrid_builder.py (expected — deleted)
- FOUND: commit 442d970 (Task 1)
- FOUND: commit c37fbcb (Task 2)

## Self-Check: PASSED

---
*Phase: 12-data-layer-hybrid-builder-removal*
*Completed: 2026-03-27*
