---
phase: 11-terminology-and-display-polish
plan: 01
subsystem: ui
tags: [dash, plotly, formatting, terminology, polish]

# Dependency graph
requires:
  - phase: 08-energy-interpolation
    provides: power breakdown bar chart (must exist as bar chart for grouped mode to apply)
provides:
  - "Renamed all user-facing Energy labels to Power across scorecard, equipment grid, and charts"
  - "fmt_sig2() helper for 2-significant-figure formatting of any numeric value"
  - "Grouped bar mode for power breakdown chart (barmode='group')"
  - "2-sig-fig formatting applied to scorecard land area and power values"
  - "2-sig-fig formatting applied to equipment grid badge and detail table values"
affects:
  - any future UI phase that displays power/energy or numeric values

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "fmt_sig2 pattern: pd.to_numeric coerce -> float -> f'{v:.2g}' -> int comma-format for large values"
    - "User-facing label renames only; internal data keys (energy_kw, mech_energy, etc.) left unchanged"

key-files:
  created: []
  modified:
    - src/data/processing.py
    - src/layout/scorecard.py
    - src/layout/equipment_grid.py
    - src/layout/charts.py

key-decisions:
  - "fmt_sig2 uses Python's .2g format string — gives 2 significant figures cleanly; large integer results comma-formatted via int cast"
  - "Internal Python variable names (energy_kw, mech_energy, elec_energy, energy_breakdown) left unchanged — only user-facing labels renamed"
  - "fmt_cost left as-is for dollar values — abbreviated dollar format ($X.XK, $X.XM) is already clear and purpose-fit"
  - "barmode='group' produces side-by-side bars per system — more readable for engineering comparison than stacked"

patterns-established:
  - "fmt_sig2 pattern: use for any numeric value that benefits from consistent 2-sig-fig precision in the UI"
  - "Label-only rename pattern: rename user-facing strings without touching internal data column names or dict keys"

requirements-completed: [POLISH-01, POLISH-02, POLISH-03, POLISH-04]

# Metrics
duration: ~10min
completed: 2026-03-01
---

# Phase 11 Plan 01: Terminology and Display Polish Summary

**Renamed all "Energy" labels to "Power" across the dashboard, switched power breakdown chart from stacked to grouped bars, and applied consistent 2-significant-figure formatting via new fmt_sig2() helper**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-03-01T09:23:00Z
- **Completed:** 2026-03-01T09:33:00Z
- **Tasks:** 3 (2 automated + 1 human-verify — APPROVED)
- **Files modified:** 4

## Accomplishments
- Renamed all user-facing "Energy" labels to "Power" in scorecard, equipment accordion badges, detail tables, and cross-system comparison table — correct engineering terminology (kW is a power unit, not energy)
- Added `fmt_sig2()` to processing.py — formats any numeric value to 2 significant figures using Python's `.2g` format, with comma-formatted integers for large values
- Applied fmt_sig2 to scorecard land area and power rows, equipment grid badge and detail table quantities, power values, and land area values
- Switched `build_energy_bar_chart()` from `barmode="stack"` to `barmode="group"` — bars now appear side-by-side per system for clearer per-stage comparison
- All 24 existing automated tests pass unchanged (internal data keys not modified)

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename "Energy" labels to "Power"** - `4cb7c4c` (feat)
2. **Task 2: Grouped bar chart and 2-sig-fig formatting** - `b8fe310` (feat)
3. **Task 3: Visual verification — APPROVED** - `0e7d612` (fix: cost formatting correction found during verification)

**Plan metadata:** `1faf126` (docs: checkpoint commit), final summary commit TBD

## Files Created/Modified
- `src/data/processing.py` - Added fmt_sig2() function for 2-significant-figure formatting
- `src/layout/scorecard.py` - Import fmt_sig2; rename "Total Energy" to "Total Power"; apply fmt_sig2 to land area and power values in both 2- and 3-system branches
- `src/layout/equipment_grid.py` - Import fmt_sig2; rename _fmt_energy to _fmt_power; rename all "Energy" user labels to "Power" in badges, detail table, comparison table header, dict keys, metric_cols; apply fmt_sig2 to power, land, and quantity display
- `src/layout/charts.py` - Rename y-axis to "Power (kW)"; rename chart card title to "Power Breakdown"; change barmode from "stack" to "group"

## Decisions Made
- `fmt_sig2` uses Python's `.2g` format string — gives exactly 2 significant figures cleanly. Large integer results (e.g., 1200.0 from `f"{1234.5:.2g}"`) are cast to int and comma-formatted.
- `fmt_cost` left unchanged for dollar values — the abbreviated format ($X.XK, $X.XM) is already purpose-fit and well-understood.
- Internal Python variable names (`energy_kw`, `mech_energy`, `elec_energy`, `energy_breakdown`) left unchanged to avoid breaking data pipeline. Only user-facing strings were renamed.
- `barmode="group"` chosen over `"stack"` — side-by-side bars make per-stage comparison more readable for engineering audiences.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Applied 2-sig-fig formatting to cost display values in scorecard**
- **Found during:** Task 3 (visual verification)
- **Issue:** Cost values in the scorecard were not rendering at 2 significant figures as the plan intended
- **Fix:** Updated cost display formatting to apply fmt_sig2 to numeric cost quantities
- **Files modified:** src/layout/scorecard.py
- **Verification:** Visual check post-fix confirmed cost values display at 2 sig figs
- **Committed in:** 0e7d612

---

**Total deviations:** 1 auto-fixed (Rule 1 - Bug)
**Impact on plan:** Necessary correction caught during visual verification. No scope creep.

## Issues Encountered
None beyond the cost formatting deviation auto-fixed above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 11 complete — human visual verification approved, all 4 POLISH requirements satisfied
- v1.2 milestone (Parameter Exploration & Presentation) is now feature-complete: all 15 requirements satisfied
- No blocking concerns; future milestones can proceed from a clean, correctly-labeled dashboard

## Self-Check: PASSED

- src/data/processing.py — FOUND
- src/layout/scorecard.py — FOUND
- src/layout/equipment_grid.py — FOUND
- src/layout/charts.py — FOUND
- 11-01-SUMMARY.md — FOUND
- Commit 4cb7c4c — FOUND
- Commit b8fe310 — FOUND
- Commit 0e7d612 — FOUND

---
*Phase: 11-terminology-and-display-polish*
*Completed: 2026-03-01*
