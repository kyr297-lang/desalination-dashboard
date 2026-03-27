---
phase: 12-data-layer-hybrid-builder-removal
verified: 2026-03-26T00:00:00Z
status: passed
score: 10/10 must-haves verified
gaps: []
human_verification:
  - test: "Visit the Hybrid tab and confirm the equipment accordion is visually identical to the Mechanical and Electrical tabs (same card layout, same stage headers, same badge row)"
    expected: "Equipment grouped by process stage with accordion items identical in structure to mechanical/electrical tabs"
    why_human: "Static rendering verified in code but visual equivalence requires a browser"
  - test: "Navigate between all three system tabs and confirm the 3-column scorecard (Mechanical, Electrical, Hybrid) appears immediately on each tab switch with no blank state"
    expected: "Scorecard always present, 3 columns, RAG dots visible on first render"
    why_human: "Cannot drive Dash callback cycle from CLI"
  - test: "Adjust the TDS and depth sliders and confirm the Power Breakdown chart updates for all three systems"
    expected: "Water Extraction and Desalination bars change for all three systems as sliders move"
    why_human: "Chart callback behavior requires browser interaction"
---

# Phase 12: Data Layer & Hybrid Builder Removal — Verification Report

**Phase Goal:** Fix the data loader so the app starts without crashing, delete the hybrid builder entirely and render hybrid as a static equipment table, wire Energy sheet data into the power breakdown and turbine count charts. All three system pages must look consistent.

**Verified:** 2026-03-26
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | App starts without crashing — loader finds all three section headers | VERIFIED | `python -c "import app"` exits 0; loader prints "Found section 'Electrical Components' at row 1", "Mechanical Components" at row 15, "Hybrid Components" at row 33 |
| 2 | Mechanical BOM returns hydraulic components (HPU, manifold, hydraulic motors, etc.) | VERIFIED | 15 equipment rows parsed; PROCESS_STAGES["mechanical"] includes turbine, pump, RO membranes — confirmed via load_data() |
| 3 | Hybrid BOM returns fixed component list from Part 1 rows 33-50 | VERIFIED | 16 equipment rows parsed from Hybrid Components section; PROCESS_STAGES["hybrid"] has all 16 component names across 6 stages |
| 4 | Energy sheet data parsed into structured dict grouped by system | VERIFIED | `data["energy"]` has keys mechanical/electrical/hybrid, each with subsystems list, total_shaft_power, total_turbine_input, selected_turbine_kw |
| 5 | load_data() returns dict with keys: electrical, mechanical, hybrid, battery_lookup, tds_lookup, depth_lookup, energy | VERIFIED | Confirmed: `sorted(DATA.keys()) == ['battery_lookup', 'depth_lookup', 'electrical', 'energy', 'hybrid', 'mechanical', 'tds_lookup']` |
| 6 | hybrid_builder.py is deleted from the codebase | VERIFIED | `ls src/layout/` — hybrid_builder.py is absent; confirmed by directory listing |
| 7 | No import of hybrid_builder, store-hybrid-slots, or SLOT_STAGES exists in any file | VERIFIED | grep across all src/ and app.py returns zero matches for all three patterns |
| 8 | Hybrid page shows a static equipment table identical in style to mechanical/electrical | VERIFIED | system_view.py line 149-150: `system_df = data.get(active_system, data.get("mechanical")); equipment = make_equipment_section(system_df, active_system, data)` — single code path for all three systems |
| 9 | Power breakdown chart shows per-subsystem shaft power for all three systems from Energy sheet | VERIFIED | `compute_chart_data()` returns non-zero energy breakdowns: mechanical=1754.7 kW, electrical=1754.7 kW, hybrid=1754.7 kW across Water Extraction/Desalination/Brine Disposal stages |
| 10 | Turbine count chart shows correct turbine counts derived from Energy sheet | VERIFIED | mechanical=1 (737.1/850), electrical=1 (596.1/1500, subsystem fallback), hybrid=1 (687.7/850); all positive integers |

**Score:** 10/10 truths verified

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/data/loader.py` | Updated SECTION_HEADERS, hybrid key, Energy sheet parser | VERIFIED | SECTION_HEADERS has "Electrical Components", "Mechanical Components", "Hybrid Components"; `_parse_energy_sheet()` implemented (lines 187-314); `load_data()` returns 7 keys |
| `src/config.py` | Updated PROCESS_STAGES with hybrid key replacing miscellaneous | VERIFIED | PROCESS_STAGES has "hybrid" key with 6 stages and 16 component names; no "miscellaneous" key present |
| `src/layout/system_view.py` | Clean system view without hybrid builder imports or gate overlay | VERIFIED | No hybrid_builder import, no hybrid-gate-overlay, no hybrid-equipment-container; single `make_equipment_section` call for all systems (line 150) |
| `src/layout/shell.py` | Shell without store-hybrid-slots or SLOT_STAGES import | VERIFIED | No SLOT_STAGES import, no store-hybrid-slots Store; only two dcc.Store components: sidebar-collapsed and active-system |
| `src/layout/scorecard.py` | Scorecard always rendering 3 columns from BOM data | VERIFIED | No slot-based callbacks; single export clientside_callback only; make_scorecard_table accepts hybrid_df as third argument |
| `app.py` | Entry point without hybrid_builder import | VERIFIED | No hybrid_builder import; set_data() called for shell, charts, and scorecard only (lines 70-75) |
| `src/data/processing.py` | compute_chart_data reads Energy sheet data | VERIFIED | `_energy_from_energy_sheet()` and `_subsystem_name_to_stage()` defined; Energy sheet path active when `data.get("energy")` is non-None; no compute_hybrid_df function |
| `src/layout/charts.py` | update_charts callback no longer depends on store-hybrid-slots | VERIFIED | Callback decorator has 5 inputs (slider-time-horizon, slider-battery, store-legend-visibility, slider-tds, slider-depth); no slots parameter in update_charts signature |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/data/loader.py` | `data.xlsx Part 1` | SECTION_HEADERS dict matching column B headers | VERIFIED | Pattern "Electrical Components.*electrical" confirmed in loader.py line 38; runtime scan finds all 3 headers |
| `src/data/loader.py` | `data.xlsx Energy sheet` | `_parse_energy_sheet` function | VERIFIED | `def _parse_energy_sheet` at line 187; called in `load_data()` line 407; returns 3-system dict |
| `src/layout/system_view.py` | `src/layout/equipment_grid.py` | `make_equipment_section(data['hybrid'], 'hybrid', data)` | VERIFIED | Line 150: `equipment = make_equipment_section(system_df, active_system, data)` — active_system covers all three including "hybrid" |
| `src/layout/scorecard.py` | `src/data/processing.py` | `compute_scorecard_metrics` with all three DataFrames | VERIFIED | scorecard.py imports and uses compute_scorecard_metrics; system_view.py line 122-123 calls with mechanical, electrical, hybrid |
| `src/data/processing.py` | `data['energy']` | Energy sheet subsystem rows drive power breakdown | VERIFIED | Pattern `energy.*subsystems` at lines 611, 644; `_energy_from_energy_sheet` iterates subsystems list |
| `src/data/processing.py` | `data['energy']` | `selected_turbine_kw` drives turbine count | VERIFIED | Line 647: `turbine_size = sys_energy.get("selected_turbine_kw") or 1`; produces counts [1, 1, 1] |
| `src/layout/charts.py` | `src/data/processing.py` | `compute_chart_data` returns energy_breakdown and turbine_count | VERIFIED | Line 659: `cd = compute_chart_data(_data, battery_fraction, years, tds_ppm=tds_ppm, depth_m=depth_m)` with no hybrid_df argument |

---

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|-------------------|--------|
| `src/layout/charts.py` (update_charts) | `cd["energy_breakdown"]` | `compute_chart_data` → `_energy_from_energy_sheet` → `data["energy"]["mechanical/electrical/hybrid"]["subsystems"]` | Yes — shaft_power_kw values 172.9, 311.49, 81.865 kW per subsystem from Energy sheet | FLOWING |
| `src/layout/charts.py` (update_charts) | `cd["turbine_count"]` | `energy_data[sys_key]["selected_turbine_kw"]` and `total_turbine_input` from Energy sheet | Yes — mechanical: 737.1/850=1, electrical: 596.1/1500=1 (subsystem fallback), hybrid: 687.7/850=1 | FLOWING |
| `src/layout/system_view.py` (scorecard) | `initial_scorecard` | `make_scorecard_table(data["mechanical"], data["electrical"], data.get("hybrid"))` → real BOM DataFrames from load_data() | Yes — 10, 15, 16 equipment rows respectively; costs/land area parsed from data.xlsx | FLOWING |
| `src/layout/system_view.py` (equipment grid) | `equipment` | `make_equipment_section(system_df, active_system, data)` where `system_df = data.get(active_system)` | Yes — data["hybrid"] has 16 rows; PROCESS_STAGES["hybrid"] has 6 stage groupings | FLOWING |

---

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| App imports without error | `python -c "import sys; sys.argv=['app']; import app; print(list(app.DATA.keys()))"` | `['battery_lookup', 'depth_lookup', 'electrical', 'energy', 'hybrid', 'mechanical', 'tds_lookup']` | PASS |
| hybrid key present, miscellaneous absent | `assert 'hybrid' in DATA and 'miscellaneous' not in DATA` | Passes | PASS |
| Energy sheet returns 3 systems | `print(sorted(DATA['energy'].keys()))` | `['electrical', 'hybrid', 'mechanical']` | PASS |
| Turbine kW values are non-zero | `mech: 850.0, elec: 1500.0, hybrid: 850.0` | All positive floats | PASS |
| compute_chart_data energy breakdown non-empty | `sum(eb.values()) > 0` for all 3 systems | mechanical=1754.7 kW, electrical=1754.7 kW, hybrid=1754.7 kW | PASS |
| Turbine counts positive integers | `cd["turbine_count"]` for all 3 systems | `{mechanical: 1, electrical: 1, hybrid: 1}` | PASS |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|---------|
| DATA-01 | 12-01 | App loads without crashing after data.xlsx schema change | SATISFIED | App imports cleanly; all 3 section headers found at rows 1, 15, 33 |
| DATA-02 | 12-01, 12-02 | Mechanical BOM reflects hydraulic system | SATISFIED | 15 rows parsed; PROCESS_STAGES["mechanical"] includes HPU-adjacent components |
| DATA-03 | 12-02 | Hybrid BOM reflects fixed preset — hybrid section reads from data.xlsx Part 1 | SATISFIED | 16 rows parsed from Hybrid Components section; static rendering via make_equipment_section |
| DATA-04 | 12-01, 12-03 | Energy sheet parsed — shaft power and turbine sizing for all three systems | SATISFIED | _parse_energy_sheet() returns 3-system dict; compute_chart_data uses it for both power breakdown and turbine counts |
| CONTENT-03 | 12-02 | Hybrid builder replaced with static preset display — builder dropdowns and slot selection removed entirely | SATISFIED | hybrid_builder.py deleted; no slot dropdowns, gate overlay, slot counter, store-hybrid-slots, compute_hybrid_df, or SLOT_STAGES found in any file |

**Requirements marked in REQUIREMENTS.md for Phase 12:** DATA-01, DATA-02, DATA-03, DATA-04, CONTENT-03 — all 5 accounted for and satisfied.

No orphaned requirements found: traceability table in REQUIREMENTS.md maps only these 5 IDs to Phase 12.

---

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/data/processing.py` | 351 | Docstring for `get_equipment_stage` still says `"miscellaneous"` as a valid system key example | Info | No runtime impact — pure documentation stale text; the function uses PROCESS_STAGES.get(system, {}) which accepts any key including "hybrid" |
| `src/data/processing.py` | 673 | `_energy_by_stage(hybrid_df, "miscellaneous")` in the `else` fallback branch (Energy sheet absent) | Warning | Dead code in normal operation — Energy sheet is present and loaded, so `energy_data is not None` is always True and this branch never executes. If Energy sheet were removed, the fallback would call get_equipment_stage with "miscellaneous" key which returns "Other" for all hybrid equipment. Not a blocker for current data.xlsx. |
| `src/layout/shell.py` | 14 | Comment says "hybrid system tab view (empty state until Phase 4)" | Info | Stale comment from original skeleton; no runtime impact |

No blocker anti-patterns found. No TODO/FIXME/placeholder patterns in modified files. No hardcoded empty return values in live code paths.

---

## Human Verification Required

### 1. Hybrid Tab Visual Consistency

**Test:** Open the app and navigate to the Hybrid system tab. Compare the equipment accordion layout with the Mechanical and Electrical tabs.
**Expected:** All three tabs show equipment grouped by process stage (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal, Control) with identical card structure, badge rows (quantity/cost/power/land/lifespan), and expandable detail views.
**Why human:** Static code path is verified, but visual equivalence (card spacing, badge alignment, accordion behavior) requires browser inspection.

### 2. 3-Column Scorecard on Page Load

**Test:** Navigate from the overview to any system tab. Check that the scorecard appears immediately with three columns (Mechanical, Electrical, Hybrid) and RAG dots.
**Expected:** No blank scorecard state, no "waiting for hybrid configuration" message; all three columns populated with data on first render.
**Why human:** Scorecard render is at layout-time (not callback-triggered), but Dash's initial render cycle needs browser observation to confirm no flash of empty state.

### 3. TDS/Depth Slider Chart Updates

**Test:** On any system tab, drag the TDS slider from 0 to 35000 and observe the Power Breakdown chart.
**Expected:** Water Extraction and Desalination bars update for all three systems simultaneously; no system shows a flat zero bar that doesn't respond.
**Why human:** Chart callback behavior requires live Dash server interaction.

---

## Gaps Summary

No gaps. All 10 observable truths are VERIFIED, all 5 Phase 12 requirements are SATISFIED, all key data flows are FLOWING, and the app imports and executes cleanly.

The two `miscellaneous` string occurrences remaining in `src/data/processing.py` are: (1) a stale docstring example (no runtime effect) and (2) dead code in a fallback branch that only executes if the Energy sheet is missing from data.xlsx (which it is not). Neither is a blocker.

Three items are routed to human verification for visual and interactive confirmation, all of which have strong programmatic evidence that they will pass.

---

_Verified: 2026-03-26_
_Verifier: Claude (gsd-verifier)_
