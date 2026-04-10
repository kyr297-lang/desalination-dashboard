---
phase: 260410-oqc
plan: 01
subsystem: ui
tags: [dash, layout, scorecard, overview, charts, callback]

# Dependency graph
requires:
  - phase: 18-comparison-table-overhaul-slider-explanation
    provides: comparison table, chart callbacks, scorecard layout
provides:
  - Merged single card containing RAG scorecard + qualitative comparison table
  - Scorecard without Best Overall summary row or green-dot counting logic
  - Landing page system card descriptions without Click Explore opener
  - Chart section without label-elec-cost span or callback output (6-output callback)
affects: [system_view, scorecard, overview, charts]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "_make_comparison_table() returns html.Div for embedding, not standalone dbc.Card"

key-files:
  created: []
  modified:
    - src/layout/scorecard.py
    - src/layout/system_view.py
    - src/layout/overview.py
    - src/layout/charts.py

key-decisions:
  - "Comparison table returned as html.Div (with Hr divider + Qualitative Comparison heading) rather than dbc.Card, so it embeds cohesively inside the merged scorecard card"
  - "intro_card Click Explore text also updated to Select any system card below — keeps verify clean and removes all imperative Explore prompts"
  - "fmt_cost removed from charts.py import entirely since it was only used for label_cost"

requirements-completed: [OQC-01, OQC-02, OQC-03, OQC-04]

# Metrics
duration: 15min
completed: 2026-04-10
---

# Quick Task 260410-oqc: UI Cleanup Summary

**Merged scorecard and qualitative comparison into one cohesive card, stripped Best Overall row and green-dot counting, removed Click Explore text from all landing descriptions, and dropped label-elec-cost from chart layout and 6-output callback.**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-04-10
- **Completed:** 2026-04-10
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Scorecard and qualitative comparison now appear inside one `dbc.Card` with a thin `<hr>` divider and "Qualitative Comparison" sub-heading — cohesive single-card flow
- Removed "Best Overall: X" summary row, `col_span` variables, green-dot counting block (18 lines), and `RAG_COLORS` import from scorecard.py
- Stripped "Click Explore to view equipment and cost data for the [X] system." opener from all three system card descriptions in overview.py; also updated intro card wording
- Removed `label-elec-cost` span from chart layout, removed its `Output` from callback decorator (7 → 6 outputs), removed `label_cost` variable and `fmt_cost` import from charts.py

## Task Commits

1. **Task 1: Merge scorecard+comparison into one card, remove Best Overall row** - `6f83b26` (feat)
2. **Task 2: Remove Click Explore text and label-elec-cost span/callback** - `f8057fa` (feat)

## Files Created/Modified

- `src/layout/scorecard.py` - Removed green-dot counting, col_span, summary_row, RAG_COLORS import; Tbody now uses rows only
- `src/layout/system_view.py` - _make_comparison_table() returns html.Div; merged comparison_content into scorecard_card CardBody; removed standalone comparison_table
- `src/layout/overview.py` - Stripped Click Explore opener from all three _SYSTEM_CARDS descriptions and updated intro card text
- `src/layout/charts.py` - Removed label-elec-cost span, Output, label_cost variable, fmt_cost import; 6-value returns in both guard and main path

## Decisions Made

- `_make_comparison_table()` now returns `html.Div([html.Hr(...), html.H5("Qualitative Comparison", ...), table])` rather than a standalone `dbc.Card` so it slots cleanly into the merged card's CardBody
- Intro card "Click Explore on any system card below" changed to "Select any system card below" — keeps all "Click Explore" strings out of the file, satisfying the AST verify check and aligning with the broader noise-reduction intent
- `fmt_cost` removed from import since it was the sole user of that function in charts.py

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Intro card "Click Explore" text caught by AST verify check**
- **Found during:** Task 2 verification
- **Issue:** The automated verify scanned all string literals in overview.py for "Click Explore". The `_SYSTEM_CARDS` descriptions were clean, but the intro card body still contained "Click Explore on any system card below" — causing `sys.exit(1)`.
- **Fix:** Changed "Click Explore on any system card below" to "Select any system card below" in the intro card paragraph. Consistent with the noise-reduction goal.
- **Files modified:** src/layout/overview.py
- **Verification:** AST check passes — no "Click Explore" strings found in file
- **Committed in:** f8057fa (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — verify-driven fix)
**Impact on plan:** Fix is consistent with the stated goal of removing Click Explore prompts. No scope creep.

## Issues Encountered

None beyond the intro card deviation above.

## Threat Surface Scan

No new network endpoints, auth paths, file access patterns, or schema changes introduced. All changes are cosmetic layout modifications.

## Self-Check

- `src/layout/scorecard.py` exists and imports cleanly: PASS
- `src/layout/system_view.py` exists and imports cleanly: PASS
- `src/layout/overview.py` exists, no "Click Explore" strings: PASS
- `src/layout/charts.py` exists, no "label-elec-cost" strings, 6-output callback: PASS
- Commits 6f83b26 and f8057fa exist in git log: PASS

## Self-Check: PASSED

## Next Steps

None — this was a self-contained quick task. App is ready for manual smoke-test (run `python app.py`, verify merged card, no Best Overall row, no Click Explore text, no Electrical total label near slider).

---
*Quick Task: 260410-oqc*
*Completed: 2026-04-10*
