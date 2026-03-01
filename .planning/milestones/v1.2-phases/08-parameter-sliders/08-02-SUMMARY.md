---
phase: 08-parameter-sliders
plan: 02
subsystem: ui
tags: [dash, plotly, dcc.Slider, numpy.interp, TDS, desalination, callbacks, stacked-bar, STAGE_COLORS]

# Dependency graph
requires:
  - phase: 08-01
    provides: interpolate_energy() function in processing.py; tds_lookup and depth_lookup DataFrames in data dict
  - phase: 07-02
    provides: Verified data layer with tds_lookup and depth_lookup available at app startup

provides:
  - TDS slider (slider-tds, range 0-35000 PPM) and depth slider (slider-depth, range 0-1900 m) in chart-controls card
  - compute_chart_data() extended with tds_ppm and depth_m kwargs (default 950)
  - Energy breakdown stacked bar chart with fixed STAGE_COLORS for stable color assignment
  - Energy breakdown chart updates live from slider drag events
  - label-tds and label-depth span IDs for dynamic labels below each slider
  - STAGE_COLORS dict in src/config.py for deterministic stage color mapping

affects:
  - 08-03 (if any)
  - Phase 09 (turbine count chart uses energy_breakdown totals which now include TDS/depth offsets)
  - Phase 11 (power breakdown chart relies on energy_breakdown from compute_chart_data)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - TDD RED→GREEN: test file committed before implementation code
    - Slider pattern: dcc.Slider with updatemode="drag", always_visible tooltip, html.Span label below
    - Energy offset pattern: interpolate_energy() result added to stage dict via .get() + 0.0 default
    - Callback expansion: added 2 Inputs and 2 Outputs to existing callback without breaking existing returns

key-files:
  created:
    - tests/test_compute_chart_data_sliders.py
  modified:
    - src/data/processing.py
    - src/layout/charts.py
    - src/config.py

key-decisions:
  - "tds_ppm and depth_m default to 950 (midpoint) — consistent with user decision from 08-01 context"
  - "TDS and depth offsets applied to BOTH mechanical and electrical energy breakdowns — both drive types have RO and pumping stages"
  - "Offsets use .get(stage, 0.0) + offset pattern — creates stage key if absent, adds to existing if present"
  - "Guard clause extended to 9-tuple return to match the expanded 9-output callback decorator"
  - "TDS slider max changed from 1900 to 35000 PPM — seawater salinity is ~35000 mg/L; 1900 was too small for realistic ocean desalination scenarios"
  - "Pie chart replaced with stacked bar chart using fixed STAGE_COLORS dict — pie chart colors shifted on slider interaction due to Plotly index-based color assignment"

patterns-established:
  - "Callback expansion: add Inputs/Outputs in matching order; update guard clause return tuple to match"
  - "Energy stage offset: mech_energy['Stage'] = mech_energy.get('Stage', 0.0) + interpolated_kw"

requirements-completed: [SLDR-01, SLDR-02, SLDR-03]

# Metrics
duration: ~90min (including checkpoint verification and two post-checkpoint fixes)
completed: 2026-02-28
---

# Phase 8 Plan 02: Slider Wiring Summary

**TDS (0-35000 PPM) and depth (0-1900 m) sliders wired end-to-end: UI controls in chart-controls card drive live stacked bar energy breakdown updates via interpolated Part 2 lookup table values, with fixed STAGE_COLORS preventing color-shift artifacts**

## Performance

- **Duration:** ~90 min (including checkpoint verification and two post-checkpoint fixes)
- **Started:** 2026-03-01T04:59:37Z
- **Completed:** 2026-03-01T05:30:00Z
- **Tasks:** 2 auto tasks complete; 1 checkpoint approved with 2 post-approval fixes
- **Files modified:** 4 (processing.py, charts.py, config.py, new test file)

## Accomplishments

- Extended `compute_chart_data()` with `tds_ppm` (default 950) and `depth_m` (default 950) kwargs that apply interpolated RO and pump energy offsets to both mechanical and electrical energy breakdowns
- Added two new `dcc.Slider` components (`slider-tds` 0-35000 PPM, `slider-depth` 0-1900 m) in a second row of the chart-controls card, each with `updatemode="drag"`, always-visible tooltip, and a dynamic label span
- Expanded the `update_charts()` callback from 4 inputs/7 outputs to 6 inputs/9 outputs — wired TDS and depth sliders through to `compute_chart_data()` and returns formatted label strings
- Replaced pie chart with stacked bar chart (`build_energy_bar_chart()`) using `STAGE_COLORS` dict from `src/config.py` to eliminate color-shift artifacts during slider interaction

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Failing TDD tests for compute_chart_data() sliders** - `8634dbf` (test)
2. **Task 1 GREEN: Extend compute_chart_data() with tds_ppm and depth_m** - `d6368b4` (feat)
3. **Task 2: Add TDS/depth sliders to chart controls and wire update_charts() callback** - `72a000a` (feat)
4. **Checkpoint fix: pie-to-stacked-bar chart + TDS slider max 35k** - `ec1e6bf` (fix)

_Note: TDD task has two commits (test RED → feat GREEN); no refactor needed. Post-checkpoint fix committed by orchestrator._

## Files Created/Modified

- `tests/test_compute_chart_data_sliders.py` - 12 TDD tests across 4 test classes (zero offset, midpoint offset, defaults, backward compat); synthetic data fixtures only, no data.xlsx dependency
- `src/data/processing.py` - Extended `compute_chart_data()` with `tds_ppm`/`depth_m` params, TDS/depth interpolation block, updated module and function docstrings
- `src/layout/charts.py` - Added second slider row in `make_chart_section()`, expanded `update_charts()` decorator (2 new Inputs, 2 new Outputs), updated guard clause and return tuple, updated module docstring; replaced pie chart with stacked bar
- `src/config.py` - Added `STAGE_COLORS` dict for deterministic color mapping in stacked bar chart

## Decisions Made

- **Applied offsets to both systems:** TDS and depth affect desalination and pumping energy demand regardless of drive type (mechanical vs. electrical) — both systems get RO and pump energy added to their respective stages.
- **Default 950 for both sliders:** Consistent with the midpoint decision recorded in 08-01 context; students start at a representative mid-range scenario.
- **`.get(stage, 0.0) + offset` pattern:** Creates the "Desalination" and "Water Extraction" stage keys if they don't exist in the energy dict, adds to existing values if they do — clean, no KeyError risk.

## Deviations from Plan

### Post-Checkpoint Fixes (committed as ec1e6bf by orchestrator)

These were identified by the human reviewer during visual verification and fixed before final approval.

**1. [Rule 1 - Bug] TDS slider max too small for realistic ocean desalination**
- **Found during:** Task 3 (human-verify checkpoint)
- **Issue:** Plan specified slider max 1900 (matching lookup table row index max), but seawater TDS is ~35000 mg/L — students couldn't model realistic ocean desalination scenarios
- **Fix:** Changed `slider-tds` max from 1900 to 35000; updated marks to {0: "0", 17500: "17,500", 35000: "35,000"}. `interpolate_energy()` uses `np.interp` which clamps at boundary so values beyond 1900 return the max lookup value
- **Files modified:** src/layout/charts.py
- **Verification:** Slider renders at full 0-35000 range; 24 tests still pass
- **Committed in:** ec1e6bf

**2. [Rule 1 - Bug] Pie chart colors shifted on slider interaction**
- **Found during:** Task 3 (human-verify checkpoint)
- **Issue:** Plotly pie chart assigns colors by data index; when slider moved and stage values changed, colors shifted making the Energy Breakdown chart confusing and misleading
- **Fix:** Replaced pie chart with stacked bar chart (`build_energy_bar_chart()`); added `STAGE_COLORS` dict to `src/config.py` mapping each stage name to a fixed hex color — color is now determined by stage name, not data position
- **Files modified:** src/layout/charts.py, src/config.py
- **Verification:** Dragging sliders shows smooth bar updates with consistent stage colors; no color shifts; 24 tests pass
- **Committed in:** ec1e6bf

---

**Total deviations:** 2 post-checkpoint fixes (both Rule 1 - Bug)
**Impact on plan:** Both fixes essential for correct and usable student experience. Stacked bar chart is strictly better than pie for parameterized slider interaction. No scope creep.

## Issues Encountered

None beyond the two post-checkpoint fixes documented above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 8 is complete: `interpolate_energy()` (08-01) + slider wiring (08-02) both approved and done
- Phases 9 and 10 can begin in parallel — no cross-dependency between them
- Phase 11 depends on Phase 8 complete (power breakdown chart must exist as stacked bar chart, not pie) — this is now satisfied by the ec1e6bf fix

## Self-Check: PASSED

- FOUND: tests/test_compute_chart_data_sliders.py
- FOUND: src/data/processing.py
- FOUND: src/layout/charts.py
- FOUND: src/config.py
- FOUND: .planning/phases/08-parameter-sliders/08-02-SUMMARY.md
- FOUND: commit 8634dbf (test RED phase)
- FOUND: commit d6368b4 (feat GREEN phase)
- FOUND: commit 72a000a (feat Task 2)
- FOUND: commit ec1e6bf (fix checkpoint post-approval fixes)
- 24/24 tests pass: pytest tests/test_interpolate_energy.py tests/test_compute_chart_data_sliders.py

---
*Phase: 08-parameter-sliders*
*Completed: 2026-02-28*
