---
phase: 04-hybrid-builder
plan: 01
subsystem: hybrid-builder
tags: [hybrid, config, processing, layout, callbacks, dcc.Store, dropdowns]
dependency_graph:
  requires: [03-02]
  provides: [hybrid-builder-layout, hybrid-processing-helpers, slot-store]
  affects: [src/config.py, src/data/processing.py, src/layout/hybrid_builder.py]
tech_stack:
  added: []
  patterns: [module-level _data / set_data(), dcc.Store slot schema, pipeline layout with flex-wrap]
key_files:
  created:
    - src/layout/hybrid_builder.py
  modified:
    - src/config.py
    - src/data/processing.py
decisions:
  - "Desalination dropdown items sourced from mechanical/electrical DataFrames (not miscellaneous) — hybrid builder uses cross-system equipment selection"
  - "Multi-Media Filtration removed from miscellaneous Pre-Treatment — it exists in electrical sheet only so lookup would always fail"
  - "clear_all_slots callback cascades through update_slot_store — single writer pattern maintained"
  - "_build_dropdown_options verifies each name against all 3 DataFrames at layout time (not in callback)"
  - "hybrid_energy in compute_chart_data uses miscellaneous system key for stage lookup — hybrid items are sourced from that mapping"
metrics:
  duration_minutes: 3
  completed_date: 2026-02-22
  tasks_completed: 2
  files_modified: 3
---

# Phase 4 Plan 1: Hybrid Builder Foundation Summary

**One-liner:** Pipeline builder UI with 5 labeled dropdowns and slot store, plus `compute_hybrid_df` / `generate_comparison_text` data helpers wired to extended `compute_scorecard_metrics` and `compute_chart_data`.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Extend config.py and add hybrid processing helpers | 2e47040 | src/config.py, src/data/processing.py |
| 2 | Create hybrid_builder.py with pipeline layout and callbacks | 586a67c | src/layout/hybrid_builder.py |

## What Was Built

### Task 1: config.py and processing.py

**config.py changes:**
- Added `PROCESS_STAGES["miscellaneous"]["Desalination"]` with 4 items: "2 RO membranes in parallel", "RO membranes in parallel", "Gear and Booster Pump", "Booster Pump" — these exist in the mechanical and electrical DataFrames respectively, making all 4 dropdown options resolvable
- Removed "Multi-Media Filtration" from miscellaneous Pre-Treatment (belongs to electrical only; leaving it would produce a dropdown option that fails lookup)
- Reordered miscellaneous stages to match pipeline flow order (Water Extraction first)

**processing.py additions:**
- `compute_hybrid_df(slots, data)` — searches miscellaneous, mechanical, electrical DataFrames in priority order for each slot selection; returns a 5-row DataFrame or None if any slot is empty or lookup fails
- `generate_comparison_text(hybrid_metrics, mech_metrics, elec_metrics)` — produces factual percentage-difference sentences for cost, land_area, efficiency; handles division-by-zero and None values; returns "similar" for < 0.1% difference
- Extended `compute_scorecard_metrics` to accept optional `hybrid_df` — adds "hybrid" key to result when provided
- Extended `compute_chart_data` to accept optional `hybrid_df` — replaces all TODO Phase 4 placeholder zeros with real computed values (cumulative cost, land area, energy breakdown); hybrid turbines remain 0 (miscellaneous items include no turbines)

### Task 2: hybrid_builder.py

New self-contained module at `src/layout/hybrid_builder.py`:

- `SLOT_STAGES` — ordered list of 5 stage names
- `make_hybrid_builder(data)` — builds horizontal pipeline layout with:
  - `dcc.Store(id="store-hybrid-slots")` initialized to `{stage: None for stage in SLOT_STAGES}`
  - Top bar: `html.Span(id="slot-counter")` + `dbc.Button(id="btn-clear-all")`
  - Pipeline: 5 labeled dropdowns (IDs: slot-dd-water-extraction, slot-dd-pre-treatment, slot-dd-desalination, slot-dd-post-treatment, slot-dd-brine-disposal) separated by `→` arrows
  - Dropdowns use `d-flex flex-wrap` for responsive wrapping on small screens
  - Options built by `_build_dropdown_options()` at layout time (never in a callback)
- Three callbacks:
  - `update_slot_store` — sole writer to store-hybrid-slots; consolidates all 5 dropdown values
  - `clear_all_slots` — resets all 5 dropdowns to None on button click; cascades to store through update_slot_store
  - `update_slot_counter` — reads store and displays "X/5 slots filled"

## Verifications Passed

1. `PROCESS_STAGES['miscellaneous']['Desalination']` has exactly 4 items
2. `compute_hybrid_df` and `generate_comparison_text` import cleanly
3. `SLOT_STAGES` has exactly 5 items
4. `app.py` imports without errors; no duplicate IDs

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing config] Reordered miscellaneous PROCESS_STAGES keys**
- **Found during:** Task 1
- **Issue:** The plan specified ordering by pipeline flow (Water Extraction first) but the original miscellaneous dict had Pre-Treatment first, Water Extraction last — inconsistency with the SLOT_STAGES pipeline order
- **Fix:** Reordered miscellaneous keys to match SLOT_STAGES pipeline flow order
- **Files modified:** src/config.py
- **Commit:** 2e47040

None of the auto-fixes represent architectural changes or blocked tasks.

## Self-Check

Checking created/modified files exist:
- src/config.py — modified (PROCESS_STAGES["miscellaneous"]["Desalination"] added)
- src/data/processing.py — modified (compute_hybrid_df, generate_comparison_text added)
- src/layout/hybrid_builder.py — created (327 lines)

Checking commits exist:
- 2e47040 — feat(04-01): extend config and add hybrid processing helpers
- 586a67c — feat(04-01): create hybrid_builder.py with pipeline layout and callbacks

## Self-Check: PASSED
