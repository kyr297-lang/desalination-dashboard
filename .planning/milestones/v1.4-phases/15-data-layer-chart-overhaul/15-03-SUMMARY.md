---
plan: 15-03
phase: 15-data-layer-chart-overhaul
status: complete
completed: 2026-03-28
---

## Summary

Updated test suite for new 4-column BOM schema and 3-subsystem energy model. Fixed scorecard crash caused by `land_area`/`efficiency` removal from `compute_scorecard_metrics`. Verified all app interactions via Playwright (13/13 checks passed).

## Tasks Completed

1. **test_compute_chart_data_sliders.py updated** — 4-column fixtures, `hybrid` key, `RO Desalination`/`Groundwater Extraction` stage names, updated energy values from SUBSYSTEM_POWER constants
2. **Scorecard crash fixed** — `scorecard.py` removed `land_area` and `efficiency` references that were broken after phase 15-02's processing.py overhaul; now shows cost-only table
3. **Human checkpoint verified via Playwright** — all 13 checks passed on clean server (port 8055)

## Verification Results (Playwright)

| Check | Result |
|-------|--------|
| chart-cost present | PASS |
| chart-power present (no chart-pie) | PASS |
| No old chart-land/turbine/pie in DOM | PASS |
| Power chart: Groundwater Extraction bar | PASS |
| Power chart: RO Desalination bar | PASS |
| Power chart: Brine Reinjection bar | PASS |
| Time Horizon slider updates label | PASS |
| Battery/Tank slider updates label | PASS |
| TDS slider updates label | PASS |
| Depth slider updates label | PASS |
| Mechanical badge clickable | PASS |
| Electrical badge clickable | PASS |
| Hybrid badge clickable | PASS |

## Key Files

- `tests/test_compute_chart_data_sliders.py` — updated for new schema
- `src/layout/scorecard.py` — removed land_area/efficiency (gap fix, not in original plan)

## Self-Check: PASSED
