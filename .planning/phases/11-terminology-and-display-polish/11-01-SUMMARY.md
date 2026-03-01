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
- **Tasks:** 2 automated complete + 1 human-verify checkpoint pending
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
3. **Task 3: Visual verification** - PENDING (checkpoint:human-verify)

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

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Tasks 1 and 2 complete and committed; human visual verification (Task 3) is the final gate
- After human approval, Phase 11 (and v1.2 milestone) is complete
- POLISH-01 through POLISH-04 requirements satisfied pending visual confirmation

---
*Phase: 11-terminology-and-display-polish*
*Completed: 2026-03-01*
