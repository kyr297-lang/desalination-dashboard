---
phase: 18-comparison-table-overhaul-slider-explanation
plan: 01
subsystem: layout
tags: [comparison-table, equipment-grid, ui, cleanup]
dependency_graph:
  requires: [phase-17-heading-hierarchy]
  provides: [consolidated-comparison-table, accordion-cleanup]
  affects: [src/layout/equipment_grid.py, src/layout/system_view.py, src/config.py, assets/custom.css]
tech_stack:
  added: []
  patterns: [static-config-dict, inline-style-highlight, hex-to-rgb-helper]
key_files:
  created: []
  modified:
    - src/layout/equipment_grid.py
    - src/layout/system_view.py
    - src/config.py
    - assets/custom.css
decisions:
  - "Keep all_data param in make_equipment_section signature for API compatibility — callers (system_view.py) still pass it"
  - "Use inline styles for active column highlight — avoids dynamic CSS class injection complexity"
  - "Place comparison table after equipment_card in main_content_children — below accordion per D-02"
metrics:
  duration_minutes: 20
  completed: 2026-04-10
  tasks_completed: 2
  files_modified: 4
---

# Phase 18 Plan 01: Comparison Table Overhaul Summary

**One-liner:** Removed per-accordion cross-system comparison blocks and replaced with a single 3-column consolidated table (Mechanical / Electrical / Hybrid) below the equipment accordion, with the active system column dynamically highlighted using its SYSTEM_COLORS entry.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Remove cross-system comparison; define table content | f3cf274 | equipment_grid.py, config.py |
| 2 | Build consolidated comparison table with dynamic highlight | 59da35c | system_view.py, custom.css |

## What Was Built

**Task 1 — Removal and config:**
- Deleted the entire `_make_cross_system_comparison` function (137 lines) from `equipment_grid.py`
- Removed `cross_comparison` variable and the `all_data` parameter from `_make_accordion_item`
- Updated `make_equipment_section` call site to new 3-argument signature
- Updated module docstring
- Added `COMPARISON_TABLE_DATA` dict to `config.py` with 5 rows × 3 systems of static editorial content

**Task 2 — New consolidated table:**
- Added `_hex_to_rgb` helper to `system_view.py` for rgba tint calculation
- Added `_make_comparison_table(active_system)` function building a `dbc.Table` with:
  - Active system column: colored header background (full SYSTEM_COLORS value) + 10% opacity cell tint
  - Other columns: neutral `#f8f9fa` header + default cell background
  - 5 labeled rows: Drive mechanism, Energy storage, Key advantage, Key limitation, Best suited for
- Inserted `comparison_table` into `main_content_children` after `equipment_card`
- Added `.comparison-table` base styles and print color preservation to `custom.css`

## Decisions Made

1. **API compatibility for `make_equipment_section`:** Retained `all_data` parameter in the public function signature since `system_view.py` already passes it. The parameter is accepted but not forwarded — removing it would require updating the caller.

2. **Inline styles for column highlight:** Active column styling (header background, cell tint) applied via inline `style=` dicts in Python rather than dynamic CSS class injection. This matches the existing pattern in `system_view.py` (tab bar active styles use the same approach).

3. **Section heading class:** Used `section-heading mt-0` className on the H5 inside the comparison card — consistent with Phase 17 heading hierarchy normalization.

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None — `COMPARISON_TABLE_DATA` contains complete editorial content for all 3 systems × 5 rows. No placeholders.

## Threat Flags

None — all new surface is static read-only config flowing to HTML. No user input, no new endpoints.

## Self-Check

Verified:
- `src/layout/equipment_grid.py` — does NOT contain `_make_cross_system_comparison` or `cross_comparison`
- `src/config.py` — contains `COMPARISON_TABLE_DATA` with 5 keys, each with 3 system entries
- `src/layout/system_view.py` — contains `_make_comparison_table`, `_hex_to_rgb`, `COMPARISON_TABLE_DATA` import, `comparison_table` in `main_content_children`
- `assets/custom.css` — contains `.comparison-table` and `print-color-adjust: exact` scoped to `.comparison-table`
- All three system layouts render without error (verified via automated test)
- Commits f3cf274 and 59da35c exist

## Self-Check: PASSED
