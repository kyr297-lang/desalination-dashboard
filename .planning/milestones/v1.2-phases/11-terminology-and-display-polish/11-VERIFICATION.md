---
phase: 11-terminology-and-display-polish
verified: 2026-03-01T00:00:00Z
status: human_needed
score: 6/6 must-haves verified
human_verification:
  - test: "Run app and confirm 'Power Breakdown' chart card title renders in browser"
    expected: "Chart card top-left reads 'Power Breakdown', not 'Energy Breakdown'"
    why_human: "Card title string is in make_chart_section() layout factory, not in build_energy_bar_chart(). Static grep confirmed 'Power Breakdown' at charts.py:590, but rendered DOM must be observed."
  - test: "Confirm chart is grouped bars (not stacked) in the running app"
    expected: "Power Breakdown chart shows side-by-side bars per process stage, one cluster per visible system"
    why_human: "barmode='group' is set at charts.py:330, but Plotly renders it client-side. A stacked vs grouped distinction requires a visual check."
  - test: "Confirm scorecard numeric values display at 2 significant figures"
    expected: "Land area and power rows in the scorecard show values like '1,200' or '0.0046', not '1,234.5' or '1234.567'"
    why_human: "fmt_sig2 wiring confirmed in code, but actual data-dependent output requires a live app run with real data loaded."
---

# Phase 11: Terminology and Display Polish — Verification Report

**Phase Goal:** Every power-related label in the dashboard uses "Power" not "Energy", the power breakdown chart is a grouped bar chart, and all numeric values display at consistent 2 significant figures
**Verified:** 2026-03-01
**Status:** human_needed (all automated checks pass; 3 items require visual confirmation in browser)
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Scorecard row header reads "Total Power (kW)" not "Total Energy (kW)" | VERIFIED | scorecard.py lines 219, 260: `html.Th("Total Power (kW)")` in both 2-system and 3-system branches. Zero "Total Energy" matches in file. |
| 2 | Equipment accordion badge label reads "Power" not "Energy" | VERIFIED | equipment_grid.py line 86: `("Power", _fmt_power(...))` in `_make_summary_badges()`. `_fmt_energy` function does not exist; `_fmt_power` at line 44. Zero user-facing "Energy" label strings. |
| 3 | Energy breakdown chart y-axis reads "Power (kW)" and chart card title reads "Power Breakdown" | VERIFIED | charts.py line 331: `yaxis_title="Power (kW)"`. charts.py line 590: `"Power Breakdown"`. charts.py line 591: `"Power use by process stage (kW)"`. No "Energy (kW)" or "Energy Breakdown" strings remain. |
| 4 | Energy breakdown chart uses grouped bar mode (`barmode='group'`) not stacked | VERIFIED | charts.py line 330: `barmode="group"`. All three chart builders (land, turbine, energy) use `barmode="group"`. No `barmode="stack"` anywhere in file. |
| 5 | Numeric values in equipment grid badges and detail table display at 2 significant figures | VERIFIED | equipment_grid.py line 20 imports `fmt_sig2`. `_fmt_power()` at line 49 uses `fmt_sig2`. `_fmt_land()` at line 57 uses `fmt_sig2`. Summary badge "Qty" at line 84 uses `fmt_sig2`. Detail table "Quantity" at line 122 uses `fmt_sig2`. |
| 6 | Numeric values in scorecard (cost, land, power) display at 2 significant figures | VERIFIED | scorecard.py line 33 imports `fmt_sig2`. Land area cells use `fmt_sig2` at lines 206, 210, 214, 251, 255. Power cells use `fmt_sig2` at lines 221, 225, 229, 262, 266. Cost uses `fmt_cost` which internally calls `fmt_sig2` (processing.py lines 102–105). |

**Score:** 6/6 truths verified (automated)

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/data/processing.py` | `fmt_sig2` helper for 2-significant-figure formatting | VERIFIED | Function defined at line 31. Tested: `fmt_sig2(1200)='1,200'`, `fmt_sig2(1234.5)='1,200'`, `fmt_sig2(0.00456)='0.0046'`, `fmt_sig2(85)='85'`, `fmt_sig2(None)='N/A'`, `fmt_sig2(0)='0'`. All pass. |
| `src/layout/scorecard.py` | "Total Power (kW)" row header and `fmt_sig2` formatting | VERIFIED | "Total Power (kW)" at lines 219, 260. `fmt_sig2` imported and applied to all land area and power value cells. |
| `src/layout/equipment_grid.py` | "Power" badge label and `fmt_sig2` display | VERIFIED | `_fmt_power()` at line 44 (renamed from `_fmt_energy`). "Power" label in badges (line 86) and detail table (line 124). "Power" column key in cross-system comparison (lines 181, 197, 211, 228). `fmt_sig2` imported and used throughout. |
| `src/layout/charts.py` | Grouped bar chart with "Power (kW)" y-axis label | VERIFIED | `barmode="group"` at line 330. `yaxis_title="Power (kW)"` at line 331. "Power Breakdown" card title at line 590. |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/layout/scorecard.py` | `src/data/processing.py` | `fmt_sig2` import | WIRED | Line 33: `from src.data.processing import ..., fmt_sig2`. Used at lines 206, 210, 214, 221, 225, 229, 251, 255, 262, 266. Import confirmed, usage confirmed. |
| `src/layout/equipment_grid.py` | `src/data/processing.py` | `fmt_sig2` import | WIRED | Line 20: `from src.data.processing import fmt_cost, fmt_num, fmt, fmt_sig2, get_equipment_stage`. Used in `_fmt_power()`, `_fmt_land()`, `_make_summary_badges()`, `_make_detail_table()`. Import confirmed, usage confirmed. |

---

## Requirements Coverage

| Requirement | Description (from REQUIREMENTS.md) | Status | Evidence |
|-------------|-------------------------------------|--------|----------|
| POLISH-01 | Label "Energy" changed to "Power" in the scorecard row header | SATISFIED | `html.Th("Total Power (kW)")` at scorecard.py lines 219, 260. No "Total Energy" remains. |
| POLISH-02 | Label "Energy" changed to "Power" in the equipment accordion badge | SATISFIED | `("Power", _fmt_power(...))` at equipment_grid.py line 86. `_fmt_energy` function no longer exists. |
| POLISH-03 | Power breakdown chart changed from pie chart to grouped bar chart | SATISFIED | `barmode="group"` at charts.py line 330. Note: the chart was previously stacked bar, not pie — the requirement description in REQUIREMENTS.md says "pie chart" but the actual prior implementation was `barmode="stack"`. Grouped bar is now implemented, satisfying the intent. |
| POLISH-04 | Numeric values in equipment grid and scorecard display at consistent 2 significant figures | SATISFIED | `fmt_sig2` wired in both scorecard.py and equipment_grid.py. All 24 automated tests pass. |

**Requirement note on POLISH-03:** REQUIREMENTS.md text says "changed from pie chart to grouped bar chart" but the PLAN and code show the chart was always a bar chart (previously `barmode="stack"`). The goal — grouped bars — is achieved. This is a documentation description mismatch, not an implementation gap.

---

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/layout/equipment_grid.py` | 81 | Docstring still reads "Five small badge columns: Qty, Cost, **Energy**, Land, Lifespan." | Info | Internal Python docstring only — not user-facing. Does not affect rendered output. No action required. |
| `src/data/processing.py` | 49 | Docstring example claims `fmt_sig2(0.5)` returns `'0.50'` — actual return is `'0.5'` | Info | Python's `.2g` format strips trailing zero from `'0.50'` to `'0.5'`. Docstring is aspirational but inaccurate. Does not affect 2-sig-fig precision for any realistic engineering value in this dataset (kW values are typically > 1). |

No blocker or warning anti-patterns found. No `TODO`, `FIXME`, placeholder, or stub patterns in the modified files.

---

## Human Verification Required

### 1. Power Breakdown Chart Title in Rendered UI

**Test:** Run `python app.py`, open `http://127.0.0.1:8050`, navigate to the System Comparison section.
**Expected:** The bottom-right chart card title reads "Power Breakdown" (not "Energy Breakdown"). The y-axis reads "Power (kW)".
**Why human:** The title string lives in `make_chart_section()` at charts.py:590, which is a layout factory called once at startup. Grep confirmed "Power Breakdown" is the string — but the DOM must be inspected to rule out any caching or ID mismatch.

### 2. Grouped Bar Chart Visual Confirmation

**Test:** With the app running, look at the Power Breakdown chart with Mechanical and Electrical both visible.
**Expected:** Bars appear side-by-side per process stage (Water Extraction, Pre-Treatment, etc.) — one bar per system per stage, not stacked.
**Why human:** `barmode="group"` is set at line 330, but Plotly renders chart mode client-side. Stacked vs grouped is a visual distinction that cannot be confirmed from source code alone.

### 3. Scorecard 2-Sig-Fig Values with Real Data

**Test:** With the app running, view the scorecard on the Overview tab with no hybrid selections.
**Expected:** Land Area and Total Power rows show values like "1,200 m²" or "85 kW", not values with many decimal places.
**Why human:** `fmt_sig2` wiring is confirmed in source. However, actual data-dependent formatted output depends on real Excel data loaded at runtime. A visual check with real data confirms the formatter works end-to-end.

---

## Gaps Summary

No automated gaps found. All 6 must-have truths are VERIFIED in the codebase. All 4 requirements are SATISFIED. All 24 existing tests pass unchanged. All key links (imports and usages) are fully wired.

The `human_needed` status reflects 3 visual checks that cannot be completed programmatically — the chart rendering, the card title in the DOM, and the formatted numeric output with live data. These are standard final-polish verifications, not evidence of missing implementation.

---

*Verified: 2026-03-01*
*Verifier: Claude (gsd-verifier)*
