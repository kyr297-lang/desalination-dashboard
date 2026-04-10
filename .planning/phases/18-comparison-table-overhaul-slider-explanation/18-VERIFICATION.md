---
phase: 18-comparison-table-overhaul-slider-explanation
verified: 2026-04-10T00:00:00Z
status: human_needed
score: 5/5 must-haves verified
re_verification: false
human_verification:
  - test: "Open the Mechanical tab. Expand several accordion items. Confirm no cross-system comparison block appears inside any accordion item — only description text, summary badges, and the detail table."
    expected: "No per-stage comparison table or block inside any accordion item on any system tab."
    why_human: "The function _make_cross_system_comparison has been deleted from code, but visual confirmation that no residual HTML is generated at runtime is a UI behavior check."
  - test: "Open each system tab (Mechanical, Electrical, Hybrid) and scroll below the equipment accordion. Confirm the 3-column comparison table is present with exactly 5 labeled rows."
    expected: "A card labeled 'System Comparison' with columns: Mechanical, Electrical, Hybrid and rows: Drive mechanism, Energy storage, Key advantage, Key limitation, Best suited for."
    why_human: "Table render position and visual presence requires a running app."
  - test: "On the Mechanical tab, verify the Mechanical column header has a blue/steel background. Switch to the Electrical tab and verify the Electrical column has orange background. Switch to Hybrid and verify green background."
    expected: "Active system column header has its SYSTEM_COLORS background (#5B8DB8 / #D4854A / #6BAA75); cells have a light tint of the same color; inactive columns have neutral grey headers."
    why_human: "Dynamic column highlighting requires visual inspection — inline styles are applied from Python at render time."
  - test: "Scroll to the chart section. Confirm the explanatory paragraph appears above the slider control panel (not inside it) and reads about both 'Source Water Salinity (TDS)' and 'Groundwater Well Depth'."
    expected: "Paragraph is visible above the sliders in normal view. It covers both slider purposes in an academic tone."
    why_human: "Placement above vs. inside the control panel and paragraph readability requires visual check."
  - test: "Trigger browser Print Preview (Ctrl+P). Confirm the slider explanation paragraph is NOT visible in the print preview."
    expected: "Paragraph hidden in print via no-print class."
    why_human: "Print output requires browser-level rendering check."
---

# Phase 18: Comparison Table Overhaul & Slider Explanation — Verification Report

**Phase Goal:** Users see a consolidated 3-system comparison (including hybrid) on each system tab with their current system highlighted, and understand what the TDS and depth sliders control before interacting with them.

**Verified:** 2026-04-10
**Status:** HUMAN_NEEDED — all automated checks pass; 5 visual/behavioral items require a running app to confirm.
**Re-verification:** No — initial verification.

---

## Goal Achievement

### Observable Truths (Roadmap Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User no longer sees per-stage cross-system comparison slots inside the equipment accordion | VERIFIED | `_make_cross_system_comparison` function deleted from `equipment_grid.py`; `cross_comparison` variable removed; `_make_accordion_item` content builds only `[description, _make_summary_badges(row), detail_table]` (lines 166-170). Grep for both strings returns no matches. |
| 2 | User sees a single consolidated 3-system comparison table below the accordion on every system tab | VERIFIED | `_make_comparison_table(active_system)` defined in `system_view.py` (lines 60-111). Called at line 262 and inserted into `main_content_children` after `equipment_card` (lines 264-269). This applies to all three systems since the same layout function handles all tabs. |
| 3 | User sees comparison rows for drive mechanism, energy storage, key advantage, key limitation, and best suited for | VERIFIED | `COMPARISON_TABLE_DATA` in `config.py` (lines 468-494) has exactly 5 keys: "Drive mechanism", "Energy storage", "Key advantage", "Key limitation", "Best suited for". Each key has 3 system entries (Mechanical, Electrical, Hybrid) with non-placeholder text. |
| 4 | User sees the current system's column visually highlighted using that system's existing CSS identity | VERIFIED | `_make_comparison_table` uses `SYSTEM_COLORS.get(active_label)` for the active column header background and computes a 10% rgba tint for body cells (lines 76-85, 93-94). Helper `_hex_to_rgb` present at lines 54-57. Inactive columns use `#f8f9fa` header. |
| 5 | User reads a brief explanatory paragraph above the TDS and depth sliders describing what each slider controls | VERIFIED | `slider_explanation` html.P with `id="slider-explanation"` and `className="text-muted small no-print"` added in `charts.py` (lines 305-316). Paragraph text contains both "Source Water Salinity (TDS)" and "Groundwater Well Depth". In the return block `slider_explanation` appears at index 3 (after `banner`, before `control_panel`) — line 527. |

**Score: 5/5 truths verified**

---

### Deferred Items

None.

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/layout/equipment_grid.py` | Equipment accordion without cross-system comparison; contains `_make_accordion_item` | VERIFIED | File exists, 262 lines. No `_make_cross_system_comparison`. `_make_accordion_item` signature is `(row, system, idx)` — no `all_data` parameter. `make_equipment_section` retains `all_data` param for API compatibility but does not forward it. |
| `src/layout/system_view.py` | Contains `make_comparison_table`, `_hex_to_rgb`, `COMPARISON_TABLE_DATA` import, comparison table in layout | VERIFIED | All four items present. Import at line 20: `from src.config import SYSTEM_COLORS, COMPARISON_TABLE_DATA`. `_hex_to_rgb` at line 54. `_make_comparison_table` at line 60. `comparison_table` in `main_content_children` at lines 262-268. |
| `src/config.py` | Contains `COMPARISON_TABLE_DATA` with 5 rows x 3 systems | VERIFIED | `COMPARISON_TABLE_DATA` present at lines 468-494. 5 keys, each with Mechanical / Electrical / Hybrid sub-keys containing full editorial text (no placeholders). |
| `assets/custom.css` | Contains `.comparison-table` styles and print color preservation | VERIFIED | `.comparison-table` rule at line 152. `.comparison-table th, td` vertical-align rule at lines 156-159. Print preservation rule for `.comparison-table th, td` with `print-color-adjust: exact` inside the existing `@media print` block at lines 214-219. |
| `src/layout/charts.py` | Slider explanation paragraph above control panel | VERIFIED | `slider_explanation` html.P at lines 305-316 with correct id, className, and text. Placed before `control_panel` in return children at lines 523-534. |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/layout/system_view.py` | `src/config.py` | `import COMPARISON_TABLE_DATA` | WIRED | Line 20: `from src.config import SYSTEM_COLORS, COMPARISON_TABLE_DATA`. Used in `_make_comparison_table` body at line 89. |
| `src/layout/system_view.py` | `src/config.py` | `import SYSTEM_COLORS` | WIRED | Same import line 20. Used in tab bar (line 165) and in `_make_comparison_table` (lines 68, 76). |
| `src/layout/charts.py` | HTML output | `html.P` with `no-print` className | WIRED | `slider_explanation` html.P has `className="text-muted small no-print"`. The `no-print` class is defined in `custom.css` inside `@media print { .no-print { display: none !important; } }` at line 178. |
| `_make_comparison_table` | `main_content_children` | `comparison_table` variable inserted after `equipment_card` | WIRED | `comparison_table = _make_comparison_table(active_system)` at line 262; included at position 3 in `main_content_children` list (lines 264-269). |

---

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `_make_comparison_table` | `COMPARISON_TABLE_DATA` | Static config dict in `config.py` | Yes — 5 rows x 3 systems, all non-empty strings | FLOWING |
| `_make_comparison_table` | `active_system` (for column highlight) | Passed as argument from `create_system_view_layout`, which receives it from the tab/routing callback | Yes — string from live app state | FLOWING |
| `slider_explanation` | Static paragraph text | Hardcoded in `charts.py` — intentional, no data source needed | N/A (static) | FLOWING |

---

### Behavioral Spot-Checks

Step 7b skipped for comparison table and slider text — these are pure layout/HTML additions with no runnable CLI entry points that can be tested without a running Dash server.

Import-level checks (what can be verified statically):

| Behavior | Check | Result | Status |
|----------|-------|--------|--------|
| `equipment_grid.py` importable with no cross-system function | Grep for `_make_cross_system_comparison` | No matches | PASS |
| `config.py` has 5-row COMPARISON_TABLE_DATA | Read file, counted keys | 5 keys, each 3 systems | PASS |
| `system_view.py` imports COMPARISON_TABLE_DATA | Grep import line | Line 20 confirmed | PASS |
| `system_view.py` inserts comparison_table in layout | Read lines 262-269 | Present after equipment_card | PASS |
| `charts.py` slider_explanation before control_panel | Read lines 523-534 | Index 3 before index 4 (control_panel) | PASS |
| `custom.css` comparison-table print rule present | Read lines 214-219 | `print-color-adjust: exact` confirmed | PASS |

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| COMP-01 | 18-01-PLAN.md | Remove per-stage cross-system comparison from accordion items | SATISFIED | `_make_cross_system_comparison` deleted; `_make_accordion_item` no longer calls it or accepts `all_data` |
| COMP-02 | 18-01-PLAN.md | Consolidated comparison table added below equipment accordion | SATISFIED | `_make_comparison_table` called and inserted in `main_content_children` |
| COMP-03 | 18-01-PLAN.md | Table has 5 rows: drive mechanism, energy storage, key advantage, key limitation, best suited for | SATISFIED | `COMPARISON_TABLE_DATA` has exactly these 5 keys |
| COMP-04 | 18-01-PLAN.md | Current system column header highlighted with system color; cells have light tint | SATISFIED (code path) | Inline styles applied from `SYSTEM_COLORS` in `_make_comparison_table`; visual confirmation is human-only |
| COMP-05 | 18-01-PLAN.md | Hybrid column has real values, not placeholders | SATISFIED | Hybrid values in `COMPARISON_TABLE_DATA` are complete editorial text (e.g., "Hydraulic drivetrain for RO; electric motors for extraction and brine") |
| SLDR-01 | 18-02-PLAN.md | Explanatory paragraph above slider control panel covering TDS and depth | SATISFIED (code path) | `slider_explanation` html.P with correct id, className, text content, and position before `control_panel` |

---

### Anti-Patterns Found

Scanned modified files (`equipment_grid.py`, `system_view.py`, `config.py`, `custom.css`, `charts.py`) for stubs, placeholders, and disconnected data.

| File | Pattern | Severity | Impact |
|------|---------|----------|--------|
| `src/layout/equipment_grid.py` | `all_data` parameter retained in `make_equipment_section` but unused internally | INFO | Intentional per SUMMARY decision: kept for API compatibility since callers already pass it. Does not affect user-visible output. |
| `src/layout/charts.py` | `slider_explanation` missing `style={"fontStyle": "italic", "marginBottom": "0.5rem"}` that was in the plan | INFO | Minor deviation from plan spec. Acceptance criteria for SLDR-01 do not require the style attribute — only id, className, and text content were required. No functional impact. |

No blockers. No stubs in user-visible data paths.

---

### Human Verification Required

All 5 automated truth checks pass in static analysis. The following items require a running app for final confirmation:

#### 1. No Per-Stage Comparison Inside Accordion Items (COMP-01)

**Test:** Open the Mechanical tab. Expand 2-3 accordion items (e.g., "Gearbox", "Hydraulic Motor"). Check that no cross-system comparison block, table, or "Other Systems" section appears inside any expanded accordion item.
**Expected:** Only the equipment description (italic text), summary badges (Qty / Cost / Lifespan), and a small detail table. No per-stage comparison.
**Why human:** The function was deleted from code, but visual confirmation that the rendered DOM contains no residual comparison elements requires a running app.

#### 2. Consolidated Table Present Below Accordion on All Three Tabs (COMP-02)

**Test:** Visit the Mechanical tab, scroll below the equipment accordion. Then repeat for Electrical and Hybrid tabs.
**Expected:** A "System Comparison" card with a 3-column table (Mechanical | Electrical | Hybrid) is present below the accordion on every tab.
**Why human:** Layout assembly and scroll position require visual verification.

#### 3. Table Has Exactly 5 Rows with Correct Labels (COMP-03)

**Test:** Count the rows in the comparison table on any system tab.
**Expected:** Drive mechanism, Energy storage, Key advantage, Key limitation, Best suited for — exactly 5 labeled rows.
**Why human:** Row count in rendered HTML confirmed via visual inspection; static data verified programmatically.

#### 4. Active Column Dynamic Highlight (COMP-04)

**Test:** On Mechanical tab, confirm Mechanical column header has blue background (#5B8DB8). Switch to Electrical — Electrical column should have orange (#D4854A). Switch to Hybrid — Hybrid column should have green (#6BAA75). Body cells in the active column should have a faint tint.
**Expected:** Column header background matches SYSTEM_COLORS for the current tab's system. Other headers are neutral grey. Active column cells have light color tint.
**Why human:** Dynamic inline styles are applied at render time; requires visual check or DOM inspection.

#### 5. Slider Explanation Visible Above Sliders, Hidden in Print (SLDR-01)

**Test:** Scroll to the chart section on any system tab. Confirm the explanation paragraph appears above the slider controls. Then open Print Preview (Ctrl+P) and confirm the paragraph is not visible.
**Expected:** Paragraph visible in browser above sliders. Paragraph hidden in print preview via `no-print` class.
**Why human:** Relative positioning (above vs. inside control panel) and print suppression require browser-level rendering.

---

### Gaps Summary

No gaps. All 5 roadmap success criteria are satisfied in the codebase. The `status: human_needed` is set because 5 items require a running browser to confirm visual rendering, dynamic highlighting, and print suppression — not because any automated check failed.

---

_Verified: 2026-04-10_
_Verifier: Claude (gsd-verifier)_
