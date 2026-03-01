---
phase: 08-parameter-sliders
plan: 01
subsystem: data-processing
tags: [tdd, interpolation, numpy, processing, energy]
dependency_graph:
  requires: []
  provides: [interpolate_energy]
  affects: [src/data/processing.py, slider callbacks in Phase 9]
tech_stack:
  added: []
  patterns: [numpy.interp linear interpolation, pd.to_numeric coerce pattern, TDD red-green]
key_files:
  created:
    - tests/test_interpolate_energy.py
  modified:
    - src/data/processing.py
decisions:
  - "Mirror interpolate_battery_cost pattern: pd.to_numeric + np.interp + float() cast"
  - "12 test cases: 7 TDS + 5 depth covering boundary, midpoint, on-row, clamp behaviors"
  - "No separate refactor phase needed — implementation was clean on first pass"
metrics:
  duration_seconds: 103
  completed_date: "2026-03-01"
  tasks_completed: 2
  files_modified: 2
---

# Phase 8 Plan 01: interpolate_energy TDD Implementation Summary

**One-liner:** TDD implementation of `interpolate_energy(value, lookup_df, col_x, col_y) -> float` using `numpy.interp` against Part 2 slider lookup tables.

## What Was Built

`interpolate_energy()` added to `src/data/processing.py`. The function accepts a slider value (TDS PPM or depth m) and a 20-row lookup DataFrame, returning a linearly interpolated energy value (kW) via `numpy.interp`. Values outside the lookup range are automatically clamped to boundary values by numpy.

## TDD Phases

### RED — Failing Tests (commit: caaa6a0)

- Created `tests/test_interpolate_energy.py` with 12 test cases
- Two test classes: `TestInterpolateEnergyTDS` (7 cases) and `TestInterpolateEnergyDepth` (5 cases)
- Synthetic DataFrames used (no data.xlsx dependency)
- TDS fixture: `tds_ppm=[0,100,...,1900]`, `ro_energy_kw=[0,10,...,190]` (linear scale for exact math)
- Depth fixture: same pattern with `depth_m` / `pump_energy_kw` columns
- Tests covered: boundary min/max, clamp below/above, midpoint interpolation (950 -> 95.0), on-row exact lookup (100 -> 10.0), return type float
- Import error confirmed: `cannot import name 'interpolate_energy'`

### GREEN — Implementation (commit: 126839a)

- Added `interpolate_energy()` to `src/data/processing.py` after `interpolate_battery_cost()`
- Signature: `(value: float, lookup_df: pd.DataFrame, col_x: str, col_y: str) -> float`
- Implementation:
  ```python
  x_vals = pd.to_numeric(lookup_df[col_x], errors="coerce").values
  y_vals = pd.to_numeric(lookup_df[col_y], errors="coerce").values
  return float(np.interp(value, x_vals, y_vals))
  ```
- Updated module docstring Exports list to include `interpolate_energy`
- All 12 tests passed on first run

### REFACTOR

No refactor needed — implementation was minimal and clean.

## Commits

| Hash | Type | Description |
|------|------|-------------|
| caaa6a0 | test | Add 12 failing tests for interpolate_energy (RED) |
| 126839a | feat | Implement interpolate_energy in processing.py (GREEN) |

## Verification

```
python -m pytest tests/test_interpolate_energy.py -v
12 passed in 0.34s

python -c "from src.data.processing import interpolate_energy; print('OK')"
OK
```

## Deviations from Plan

None — plan executed exactly as written. pytest was already installed (no infrastructure setup needed). Implementation was clean on first pass with no refactor required.

## Success Criteria Check

- [x] tests/test_interpolate_energy.py exists with at least 6 test cases — 12 tests created
- [x] All tests pass: exits 0 — 12/12 passed
- [x] interpolate_energy importable from src.data.processing — confirmed
- [x] Function signature matches: (value: float, lookup_df: pd.DataFrame, col_x: str, col_y: str) -> float — confirmed

## Self-Check: PASSED

- FOUND: tests/test_interpolate_energy.py
- FOUND: src/data/processing.py
- FOUND: .planning/phases/08-parameter-sliders/08-01-SUMMARY.md
- FOUND commit: caaa6a0 (RED — failing tests)
- FOUND commit: 126839a (GREEN — implementation)
