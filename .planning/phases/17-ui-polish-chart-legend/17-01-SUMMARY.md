---
phase: 17-ui-polish-chart-legend
plan: "01"
subsystem: ui-charts-layout
tags: [chart-legend, plotly, heading-hierarchy, print-css, dash-callback]
dependency_graph:
  requires: []
  provides: [chart-legend-plotly, badge-no-print, section-heading-css]
  affects: [src/layout/charts.py, src/layout/scorecard.py, src/layout/equipment_grid.py, assets/custom.css]
tech_stack:
  added: []
  patterns: [plotly-restyle-data-sync, allow_duplicate-output, section-heading-css-class]
key_files:
  created: []
  modified:
    - src/layout/charts.py
    - assets/custom.css
    - src/layout/scorecard.py
    - src/layout/equipment_grid.py
decisions:
  - "Used allow_duplicate=True on store-legend-visibility Output for sync callback to coexist with toggle_legend callback writing to same store"
  - "Legend positioned horizontally above chart (y=1.02) to avoid overlapping cost data"
  - "Margin top bumped to max(10,50)=50 locally in build_cost_chart only; module-level _MARGIN not mutated"
  - "section-heading CSS class replaces per-element margin classes for uniform visual sizing without changing semantic HTML tags"
metrics:
  duration_minutes: 25
  completed_date: "2026-04-10"
  tasks_completed: 2
  tasks_total: 2
  files_changed: 4
---

# Phase 17 Plan 01: UI Polish — Chart Legend & Heading Hierarchy Summary

**One-liner:** Plotly in-chart legend added to cost chart with store-sync callback, badge pill row hidden in print, and section-heading CSS class normalizes H4/H5/H6 visual size across all system pages.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Enable Plotly in-chart legend, sync callback, badge no-print | f06eb0c | src/layout/charts.py, assets/custom.css |
| 2 | Normalize heading hierarchy with section-heading CSS classes | 2654886 | assets/custom.css, src/layout/charts.py, src/layout/scorecard.py, src/layout/equipment_grid.py |

## What Was Built

### Task 1: Plotly In-Chart Legend + Sync + No-Print

Three coordinated changes:

1. **`build_cost_chart` showlegend=True** — Plotly in-chart legend enabled, positioned horizontally above chart (`orientation="h", y=1.02`) with light background and border so it doesn't overlap data. Margin top bumped to 50px locally to give the legend room.

2. **`sync_chart_legend_to_store` callback** — New callback with `Output("store-legend-visibility", "data", allow_duplicate=True)` and `Input("chart-cost", "restyleData")`. Maps trace indices 0/1/2 → mechanical/electrical/hybrid keys, translates Plotly visible values (`True`/`"legendonly"`/`False`) to store booleans. Existing `toggle_legend` callback (badge clicks) is unmodified. Both write to the same store; `update_charts` reads the store and rebuilds figure with correct `visible` flags, closing the sync loop.

3. **Badge pill row no-print** — `legend_row` className updated to include `legend-badge-row no-print`. New `.legend-badge-row { display: none !important; }` rule added inside `@media print` in custom.css as defense-in-depth alongside the existing `.no-print` rule.

### Task 2: Heading Hierarchy Normalization

Two new CSS classes in `assets/custom.css`:
- `.section-heading` — 1.25rem, weight 600, color #212529 (top-level section labels)
- `.subsection-heading` — 1rem, weight 600, color #495057 (sub-labels within a section)

Applied to four heading sites:
- `charts.py` H4 "System Comparison": `className="section-heading"` (dropped `mt-4 mb-3`)
- `scorecard.py` H5 "System Scorecard": `className="section-heading"` (dropped `mt-3`)
- `equipment_grid.py` per-stage H5: `stage_class = "section-heading"` base (stage accent classes appended, e.g. `section-heading stage-heading-mechanical`)
- `equipment_grid.py` H6 "Cross-System Comparison": `className="subsection-heading text-muted"`

`error_page.py` and `overview.py` untouched.

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `allow_duplicate=True` on sync callback Output | Two callbacks write to same store; Dash requires explicit opt-in |
| Legend `orientation="h", y=1.02` | Horizontal above-chart placement avoids obscuring cost line data |
| Local margin override in build_cost_chart | Bumping t=50 only for this figure; `_MARGIN` module constant stays at t=10 |
| CSS classes instead of tag changes | Preserves semantic HTML hierarchy while achieving visual uniformity |

## Deviations from Plan

None — plan executed exactly as written.

## Success Criteria Verification

- [x] CHART-01: `showlegend=True` in `build_cost_chart`
- [x] CHART-01: `sync_chart_legend_to_store` callback syncs restyleData to store
- [x] POLISH-04 (partial): `legend-badge-row no-print` on legend_row; `.legend-badge-row { display: none !important; }` in @media print
- [x] POLISH-02: `.section-heading` and `.subsection-heading` defined; four heading sites updated; stage accent classes preserved
- [x] All four Python modules import without errors
- [x] `toggle_legend` unmodified; `error_page.py` and `overview.py` untouched

## Known Stubs

None.

## Threat Flags

None — no new network endpoints, auth paths, file access patterns, or schema changes introduced.

## Self-Check: PASSED

- `src/layout/charts.py` modified — confirmed (`f06eb0c`, `2654886`)
- `assets/custom.css` modified — confirmed (`f06eb0c`, `2654886`)
- `src/layout/scorecard.py` modified — confirmed (`2654886`)
- `src/layout/equipment_grid.py` modified — confirmed (`2654886`)
- Commits exist: `git log --oneline` shows `f06eb0c` and `2654886`
