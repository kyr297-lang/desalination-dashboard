# Phase 15: data-layer-chart-overhaul - Research

**Researched:** 2026-03-28
**Domain:** Dash/Plotly data pipeline, openpyxl Excel parsing, chart callback refactoring
**Confidence:** HIGH

## Summary

Phase 15 restructures the data loader (`loader.py`) for a changed xlsx column layout, removes two obsolete charts (land area, wind turbine count), replaces the 7-stage energy breakdown with a 3-subsystem power model, renames the chart-pie ID to chart-power, and fixes the battery slider to use the new battery component name. All changes are confined to four files: `loader.py`, `processing.py`, `charts.py`, and `config.py`.

The current data.xlsx already has the "new" structure for Part 1 BOM: electrical uses cols B-E (name, qty, unit cost, total cost) while mechanical/hybrid use cols B-D (name, qty, cost). No lifespan data exists in the current xlsx -- every BOM row has None for cols F-G. The Energy sheet still exists in the current xlsx but requirements say to stop depending on it. The three subsystem shaft power values (172.9, 311.49, 81.865 kW) are currently only in the Energy sheet, so either (a) the Energy sheet is kept but made optional, or (b) these values are hardcoded in config.py, or (c) the xlsx will be updated to embed them in Part 1. Given DATA-04 says "parsed from Part 1", the plan should either hardcode them or add them to the xlsx as a small table.

**Primary recommendation:** Split into 3 plans -- (1) loader fixes: column-aware parsing per section + lifespan + graceful Energy sheet handling, (2) chart removals + ID rename + callback output reduction, (3) 3-subsystem power model + slider fixes (battery name, stage key updates for TDS/depth offsets).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DATA-01 | App loads without crash on new data.xlsx (no Energy sheet, new column layout) | Loader `_parse_section()` must branch on section type: electrical reads cost from col E (pos 5), mech/hybrid from col D (pos 4). `_parse_energy_sheet()` must not crash when Energy sheet absent -- guard with `if "Energy" not in wb.sheetnames: return None`. |
| DATA-02 | Electrical BOM uses total_cost column (col E); mechanical/hybrid use cost column (col D) | Current `_parse_section()` always reads `cost_usd` from `ws.cell(r, 4)`. Electrical needs `ws.cell(r, 5)`. Pass a `cost_col` parameter or branch inside the function. |
| DATA-03 | Lifespan column parsed correctly per section; cost-over-time graph is non-flat | Current xlsx has NO lifespan data in any column. Either (a) add a lifespan column to the xlsx, or (b) define a LIFESPAN_MAP dict in config.py keyed by equipment name. Since the user controls xlsx, recommend approach (b) as a code-only fallback that also works if xlsx is updated later. Key lifespans: Battery=12yr, RO membranes=7yr, turbine=indefinite, pumps=15yr, etc. `compute_cost_over_time()` already handles lifespan correctly -- it just needs non-None values. |
| DATA-04 | Three subsystem energy values parsed from Part 1 (172.9 / 311.5 / 81.9 kW) | Current xlsx has these only in Energy sheet. Since DATA-01 says "no Energy sheet" and DATA-04 says "parsed from Part 1": recommend hardcoding in config.py as `SUBSYSTEM_POWER = {"Groundwater Extraction": 172.9, "RO Desalination": 311.49, "Brine Reinjection": 81.865}` since these are engineering constants, not user-variable data. This also simplifies the code enormously. |
| CHART-01 | Land Area chart removed entirely | Delete `build_land_chart()` from charts.py, remove `chart-land` dcc.Graph from `make_chart_section()`, remove `Output("chart-land", "figure")` from callback. |
| CHART-02 | Wind Turbine Count chart removed entirely | Delete `build_turbine_chart()` from charts.py, remove `chart-turbine` dcc.Graph from `make_chart_section()`, remove `Output("chart-turbine", "figure")` from callback. |
| CHART-03 | Power breakdown chart shows 3 subsystems as stacked bars | Replace 7-stage `ALL_STAGES` list and `STAGE_COLORS` with 3 subsystem keys: "Groundwater Extraction", "RO Desalination", "Brine Reinjection". Update `build_energy_bar_chart()` accordingly. |
| CHART-04 | TDS slider offsets RO Desalination bar; Depth slider offsets Groundwater Extraction bar | In `compute_chart_data()`, change energy offset keys from `"Desalination"` to `"RO Desalination"` and `"Water Extraction"` to `"Groundwater Extraction"`. |
| CHART-05 | Battery/tank slider correctly updates electrical cost-over-time (new battery name) | Change `override_costs` key from `"Battery (1 day of power)"` to `"Battery (Tesla Megapack 3.9MWh unit)"` (exact string from row 5 of current xlsx). Also update the `elec_base_cost` filter that excludes the battery row. |
| CHART-06 | All slider labels update on interaction | Labels already work -- just verify they survive the callback output count change (9 outputs -> 7 outputs after removing land and turbine). |
| CHART-07 | chart-pie ID renamed to chart-power throughout | Rename in `make_chart_section()` layout, in callback `Output("chart-pie", ...)` -> `Output("chart-power", ...)`. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| openpyxl | (already installed) | Excel xlsx parsing | Already used in loader.py; data_only=True for formula values |
| pandas | (already installed) | DataFrame operations | Already used for BOM DataFrames throughout |
| plotly | (already installed) | Chart figures | Already used for all go.Figure builders |
| dash | (already installed) | Callbacks, layout | Already used for all UI components |

No new dependencies required. This phase modifies existing code only.

## Architecture Patterns

### Current Data Flow
```
data.xlsx --> loader.py (load_data) --> dict with 7 keys
  --> processing.py (compute_chart_data) --> dict with 5 chart datasets
  --> charts.py (build_*_chart functions) --> go.Figure objects
  --> callback returns (4 figures + 5 labels = 9 outputs)
```

### Target Data Flow (after Phase 15)
```
data.xlsx --> loader.py (load_data) --> dict with 6 keys (energy key removed or made optional)
  --> processing.py (compute_chart_data) --> dict with 3 chart datasets (land/turbine removed)
  --> charts.py (build_cost_chart, build_energy_bar_chart) --> 2 go.Figure objects
  --> callback returns (2 figures + 5 labels = 7 outputs)
```

### Pattern: Section-Aware Column Parsing
```python
# Current: all sections use same column positions (WRONG for electrical)
"cost_usd": ws.cell(r, 4).value

# Target: electrical uses col E (5), mech/hybrid use col D (4)
def _parse_section(ws, header_row, stop_rows, cost_col=4):
    ...
    "cost_usd": ws.cell(r, cost_col).value
```

### Pattern: Hardcoded Subsystem Power Constants
```python
# In config.py -- engineering constants from Energy sheet analysis
SUBSYSTEM_POWER = {
    "Groundwater Extraction": 172.9,    # kW shaft power
    "RO Desalination": 311.49,          # kW shaft power
    "Brine Reinjection": 81.865,        # kW shaft power
}
```

### Pattern: Lifespan Fallback Map
```python
# In config.py -- used when xlsx has no lifespan column
LIFESPAN_DEFAULTS = {
    "Battery (Tesla Megapack 3.9MWh unit)": 12,
    "Battery (Tesla Megapack 3.9 MWh)": 12,
    "RO Membrane Trains": 7,
    "Reverse Osmosis Trains": 7,
    "Reverse osmosis train": 7,
    "RO membranes in parallel": 7,
    # ... all other items default to "indefinite"
}
```

### Anti-Patterns to Avoid
- **Parsing Energy sheet subsystem names to extract power values**: The Energy sheet has drive-type-specific data (hydraulic efficiency, turbine input) that varies by system. The shaft power values are the same across all 3 systems (172.9, 311.49, 81.865). Hardcoding these as constants is simpler and more reliable than parsing.
- **Changing callback output count without updating ALL return paths**: The `update_charts` callback has a guard clause (`if _data is None`) that returns 9 empty values. After removing 2 chart outputs, this must return 7 values. Missing this causes a Dash error.
- **Renaming chart IDs without checking all Input/Output/State references**: The chart-pie -> chart-power rename must hit both the `dcc.Graph(id=...)` in layout AND the `Output("chart-pie", "figure")` in the callback decorator.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Battery name matching | Fuzzy string matching for battery name | Exact string key from xlsx row 5: `"Battery (Tesla Megapack 3.9MWh unit)"` | The name must match exactly; fuzzy matching adds complexity for no gain |
| Lifespan data source | Complex xlsx column detection logic | Simple dict lookup in config.py (`LIFESPAN_DEFAULTS`) | xlsx may or may not have lifespan column; a code-level default is reliable |
| Subsystem power values | Re-parsing Energy sheet or embedding in Part 1 | Config constants `SUBSYSTEM_POWER` | These are engineering constants derived once from analysis; they don't change with slider inputs |

## Common Pitfalls

### Pitfall 1: Callback Output Count Mismatch
**What goes wrong:** Removing 2 chart Outputs from the callback decorator but forgetting to update the return tuple (or the guard-clause early return) causes Dash to throw "An Output was not found" or "callback returned N values but expected M".
**Why it happens:** The callback returns a tuple. Every return path must match the Output count exactly.
**How to avoid:** After modifying the decorator, grep for every `return` statement in `update_charts` and verify tuple length. Current: 9 outputs. Target: 7 outputs (cost_fig, power_fig, label_years, label_ratio, label_cost, label_tds, label_depth).
**Warning signs:** App crashes on page load with "Invalid number of output values" error.

### Pitfall 2: Battery Name Mismatch Breaks Slider
**What goes wrong:** The `override_costs` dict key doesn't match the exact string in the electrical DataFrame's `name` column, so the battery cost override is silently ignored.
**Why it happens:** The old name was `"Battery (1 day of power)"`. The new xlsx has `"Battery (Tesla Megapack 3.9MWh unit)"` (note: no space before "3.9MWh" and exact parenthesis placement). The hybrid battery is a DIFFERENT string: `"Battery (Tesla Megapack 3.9 MWh)"` (with space before "MWh").
**How to avoid:** Copy the exact string from xlsx row 5 col B. Also update the `elec_base_cost` filter in `compute_chart_data()` which currently excludes `"Battery (1 day of power)"` from the base cost sum.
**Warning signs:** Electrical cost-over-time line doesn't change when battery slider moves.

### Pitfall 3: Stage Key Mismatch After Rename
**What goes wrong:** TDS/depth energy offsets are added to old stage keys ("Desalination", "Water Extraction") but the energy breakdown dict now uses new keys ("RO Desalination", "Groundwater Extraction"), so offsets are stored in orphan keys that never appear in the chart.
**Why it happens:** The energy offset code in `compute_chart_data()` uses hardcoded stage key strings that must match the new subsystem names.
**How to avoid:** Update all three pairs of offset lines (mech/elec/hybrid) to use the new subsystem key names.
**Warning signs:** TDS and depth sliders have no visible effect on the power breakdown chart.

### Pitfall 4: PROCESS_STAGES Still References Old Names
**What goes wrong:** `get_equipment_stage()` returns "Water Extraction" or "Desalination" (old 7-stage names) but the chart now expects 3-subsystem names.
**Why it happens:** PROCESS_STAGES in config.py still maps equipment to old stage names.
**How to avoid:** Either (a) update PROCESS_STAGES to use new subsystem names, or (b) since the power breakdown no longer uses per-equipment energy from BOM (it uses fixed subsystem constants + slider offsets), PROCESS_STAGES may not need updating for Phase 15. It's used by `get_equipment_stage()` which is called by the BOM-based fallback path. If the Energy sheet fallback is removed entirely, this code path is dead for power breakdown. PROCESS_STAGES IS still used by `equipment_grid.py` for stage grouping -- but that's Phase 16 (DISP-03).
**Warning signs:** None for Phase 15 specifically -- but verify PROCESS_STAGES consumers.

### Pitfall 5: Lifespan None Treated as Indefinite Makes Cost Chart Flat
**What goes wrong:** `compute_cost_over_time()` treats `None` lifespan as unparseable, falling into the `except` block which adds cost at year 0 only. Result: a flat horizontal line.
**Why it happens:** Current xlsx has no lifespan data. Every row has `lifespan_years=None`.
**How to avoid:** Implement `LIFESPAN_DEFAULTS` lookup in config.py. In `compute_cost_over_time()`, if `lifespan` is None, check `LIFESPAN_DEFAULTS.get(row["name"], "indefinite")` before the existing logic.
**Warning signs:** Cost-over-time chart shows flat lines (no step-ups from equipment replacement).

## Code Examples

### Example 1: Section-Aware Cost Column
```python
# In loader.py _parse_section(), add cost_col parameter:
def _parse_section(ws, header_row, stop_rows, cost_col=4):
    rows = []
    for r in range(header_row + 1, ws.max_row + 1):
        if r in stop_rows:
            break
        name = ws.cell(r, 2).value
        if name is None:
            break
        if name == "Total":
            continue
        rows.append({
            "name":           name,
            "quantity":       ws.cell(r, 3).value,
            "cost_usd":       ws.cell(r, cost_col).value,
            "lifespan_years": ws.cell(r, cost_col + 1).value,  # col after cost
        })
    return rows

# Called with:
electrical_rows = _parse_section(ws, elec_start, stop_rows={mech_start}, cost_col=5)
mechanical_rows = _parse_section(ws, mech_start, stop_rows={hybrid_start}, cost_col=4)
hybrid_rows     = _parse_section(ws, hybrid_start, stop_rows=set(), cost_col=4)
```

### Example 2: Reduced Callback Outputs
```python
@callback(
    Output("chart-cost", "figure"),
    Output("chart-power", "figure"),      # renamed from chart-pie
    Output("label-years", "children"),
    Output("label-battery-ratio", "children"),
    Output("label-elec-cost", "children"),
    Output("label-tds", "children"),
    Output("label-depth", "children"),
    Input("slider-time-horizon", "value"),
    Input("slider-battery", "value"),
    Input("store-legend-visibility", "data"),
    Input("slider-tds", "value"),
    Input("slider-depth", "value"),
)
def update_charts(years, battery_fraction, visibility, tds_ppm, depth_m):
    if _data is None:
        empty = go.Figure()
        return empty, empty, "", "", "", "", ""  # 7 values, not 9
    # ...
    return cost_fig, power_fig, label_years, label_ratio, label_cost, label_tds, label_depth
```

### Example 3: Updated STAGE_COLORS for 3 Subsystems
```python
# In config.py -- replaces the 7-stage STAGE_COLORS
STAGE_COLORS = {
    "Groundwater Extraction": "#4AACB0",  # muted teal
    "RO Desalination":        "#D4A739",  # muted amber
    "Brine Reinjection":      "#C46E5A",  # muted brick red
}
```

### Example 4: Fixed Energy Breakdown (No Energy Sheet Dependency)
```python
# In processing.py compute_chart_data() -- replaces energy_data branch
from src.config import SUBSYSTEM_POWER

# Base subsystem power is constant across all 3 systems (same shaft loads)
base_energy = dict(SUBSYSTEM_POWER)  # shallow copy

# TDS offset adds to RO Desalination
ro_kw = interpolate_energy(tds_ppm, data["tds_lookup"], "tds_ppm", "ro_energy_kw")
# Depth offset adds to Groundwater Extraction
pump_kw = interpolate_energy(depth_m, data["depth_lookup"], "depth_m", "pump_energy_kw")

# Each system gets the same base + offsets (shaft power is identical)
for sys_key in ["mechanical", "electrical", "hybrid"]:
    energy = dict(base_energy)
    energy["RO Desalination"] += ro_kw
    energy["Groundwater Extraction"] += pump_kw
    # Store per-system energy breakdown
```

## Detailed Change Inventory

### loader.py
| Change | Lines | Impact |
|--------|-------|--------|
| Remove `energy_kw` and `land_area_m2` from EQUIPMENT_COLUMNS | L44-50 | Simplifies BOM schema to 4 cols: name, quantity, cost_usd, lifespan_years |
| Add `cost_col` param to `_parse_section()` | L73-116 | Electrical: cost_col=5 (col E), mech/hybrid: cost_col=4 (col D) |
| Make `_parse_energy_sheet()` return None when sheet missing | L187-218 | Prevents crash on DATA-01 scenario |
| Update `load_data()` to pass cost_col per section | L390-396 | Wire up the section-aware parsing |
| Optionally remove `"energy"` key from return dict | L409-417 | If energy data is moved to config.py constants |

### processing.py
| Change | Lines | Impact |
|--------|-------|--------|
| Replace energy_data branch with SUBSYSTEM_POWER constants | L587-690 | Removes Energy sheet dependency entirely |
| Remove `land_area` and `turbine_count` from return dict | L700-723 | These chart datasets are no longer needed |
| Update battery override key to new name | L570-576 | `"Battery (Tesla Megapack 3.9MWh unit)"` |
| Update elec_base_cost filter to new battery name | L692-699 | Same name update for exclusion filter |
| Update energy offset keys to new subsystem names | L684-689 | `"RO Desalination"` and `"Groundwater Extraction"` |
| Add LIFESPAN_DEFAULTS fallback in compute_cost_over_time | L473-499 | Non-flat cost curves when xlsx has no lifespan col |
| Remove `_subsystem_name_to_stage()` and `_energy_by_stage()` helper functions | L591-629 | Dead code after removing Energy sheet dependency |

### charts.py
| Change | Lines | Impact |
|--------|-------|--------|
| Delete `build_land_chart()` | L140-193 | CHART-01 |
| Delete `build_turbine_chart()` | L196-250 | CHART-02 |
| Update `build_energy_bar_chart()` ALL_STAGES to 3 subsystems | L281-289 | CHART-03 |
| Rename `"chart-pie"` to `"chart-power"` in layout | L607 | CHART-07 |
| Remove chart-land and chart-turbine from make_chart_section() | L581-611 | Layout simplification: 2x2 grid becomes 1x2 or single row |
| Update callback Output list (9 -> 7) | L630-639 | Remove land_fig and turbine_fig outputs |
| Update callback return tuple | L711 | 7 values instead of 9 |
| Update guard-clause return | L674-675 | 7 empty values instead of 9 |
| Remove build_land_chart and build_turbine_chart calls from callback body | L686-697 | Dead code removal |

### config.py
| Change | Lines | Impact |
|--------|-------|--------|
| Replace STAGE_COLORS (7 stages -> 3 subsystems) | L23-31 | New keys: Groundwater Extraction, RO Desalination, Brine Reinjection |
| Add SUBSYSTEM_POWER dict | new | 3 shaft power constants |
| Add LIFESPAN_DEFAULTS dict | new | Equipment name -> lifespan years mapping |
| Update PROCESS_STAGES electrical battery name | L77 | `"Battery (Tesla Megapack 3.9MWh unit)"` to match new xlsx |
| Update PROCESS_STAGES electrical entries to match new xlsx names | L73-96 | New component names from xlsx rows 2-11 |
| Update EQUIPMENT_DESCRIPTIONS for new electrical component names | L188-238 | Match the new xlsx names |

## Exact String Mapping (Critical for Correctness)

### New Electrical BOM Names (from xlsx Part 1 rows 2-11)
| Row | Old Name (in PROCESS_STAGES) | New Name (in xlsx) |
|-----|-----|-----|
| 2 | `"Turbine"` | `"1.5\u202fMW Turbine (GE Vernova 1.5sle)"` |
| 3 | `"PLC"` | `"PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)"` |
| 4 | `"Submersible pump"` | `"Submersible Pumps (WDM (Nidec) NHE Series high-he..."` |
| 5 | `"Battery (1 day of power)"` | `"Battery (Tesla Megapack 3.9MWh unit)"` |
| 6 | `"Booster Pump"` | `"Booster Pumps (Grundfos CR 10-10 K)"` |
| 7 | `"RO membranes in parallel"` | `"RO Membrane Trains"` |
| 8 | `"Calcite bed contactors"` | `"Calcite Bed Contactor (DrinTec FRP Calcite Contac..."` |
| 9 | `"Multi-Media Filtration"` | `"Multi-Media Filtration System (Pure Aqua MF-500 S..."` |
| 10 | `"Brine Well"` | `"Brine Disposal Well"` |
| 11 | `"Pipes (total)"` | `"Piping (total)"` |

**Note:** Row 4 full name needs verification (truncated at 50 chars in repr output). Row 3 has `\xa0` (non-breaking space). Row 2 has `\u202f` (narrow no-break space).

### Battery Name for override_costs
- **Electrical system:** `"Battery (Tesla Megapack 3.9MWh unit)"` (no space before "3.9MWh")
- **Hybrid system:** `"Battery (Tesla Megapack 3.9 MWh)"` (space before "MWh") -- different string, does NOT use battery slider

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | none (default discovery) |
| Quick run command | `python -m pytest tests/ -x -q` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DATA-01 | App loads without crash (no Energy sheet) | smoke | `python -c "from src.data.loader import load_data; load_data()"` | No -- Wave 0 |
| DATA-02 | Electrical cost from col E, mech/hybrid from col D | unit | `pytest tests/test_loader_columns.py -x` | No -- Wave 0 |
| DATA-03 | Lifespan parsed; cost-over-time non-flat | unit | `pytest tests/test_cost_over_time.py -x` | No -- Wave 0 |
| DATA-04 | 3 subsystem energy values available | unit | `pytest tests/test_subsystem_power.py -x` | No -- Wave 0 |
| CHART-01 | Land chart removed | smoke | `python -c "from src.layout.charts import make_chart_section; s=make_chart_section(); assert 'chart-land' not in str(s)"` | No |
| CHART-02 | Turbine chart removed | smoke | same as CHART-01 pattern | No |
| CHART-03 | Power breakdown shows 3 subsystems | unit | `pytest tests/test_energy_bar_chart.py -x` | No -- Wave 0 |
| CHART-04 | TDS/depth offsets correct subsystem keys | unit | existing `test_compute_chart_data_sliders.py` (needs update) | Yes -- needs update |
| CHART-05 | Battery slider updates electrical cost | unit | existing `test_compute_chart_data_sliders.py` (needs update) | Yes -- needs update |
| CHART-06 | All slider labels update | manual | Run app, drag each slider, verify labels | manual-only |
| CHART-07 | chart-pie renamed to chart-power | smoke | grep for "chart-pie" in src/ returns 0 results | No |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/ -x -q`
- **Per wave merge:** `python -m pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] Update `tests/test_compute_chart_data_sliders.py` -- fixture uses old battery name and old stage keys
- [ ] Update `tests/test_interpolate_energy.py` -- verify still passes after processing.py changes

## Open Questions

1. **Where should subsystem power values live?**
   - What we know: Energy sheet has 172.9, 311.49, 81.865 kW for all 3 systems. DATA-04 says "parsed from Part 1" but Part 1 has no such data currently.
   - What's unclear: Will the user update the xlsx to add these values to Part 1, or should we hardcode?
   - Recommendation: Hardcode in `config.py` as `SUBSYSTEM_POWER` dict. These are engineering analysis results, not BOM line items. If xlsx is updated later, the loader can be adapted. This unblocks the plan without xlsx changes.

2. **What lifespan values to use?**
   - What we know: DATA-03 requires "non-flat" cost-over-time. Current xlsx has no lifespan data.
   - What's unclear: The exact lifespan for each component.
   - Recommendation: Use standard engineering estimates: batteries 12yr, RO membranes 7yr, pumps 15yr, turbines/structures indefinite. Define in `LIFESPAN_DEFAULTS` in config.py. User can override by adding a lifespan column to xlsx later.

3. **Should PROCESS_STAGES electrical entries be updated in Phase 15 or 16?**
   - What we know: PROCESS_STAGES maps equipment names to stage groups. The electrical names have all changed. PROCESS_STAGES is used by `get_equipment_stage()` in processing.py and by equipment_grid.py for accordion grouping.
   - Recommendation: Update electrical PROCESS_STAGES entries in Phase 15 since `compute_chart_data()` uses `get_equipment_stage()` in the BOM fallback path, and the battery name update (CHART-05) requires it. The full accordion regrouping (DISP-03) is Phase 16.

## Sources

### Primary (HIGH confidence)
- Direct reading of `data.xlsx` via openpyxl -- verified exact cell values, column positions, sheet names
- Direct reading of `src/data/loader.py`, `src/data/processing.py`, `src/layout/charts.py`, `src/config.py` -- verified all function signatures, callback decorators, return values
- `.planning/REQUIREMENTS.md` -- exact requirement text for DATA-01 through CHART-07

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` decisions from Phase 12 -- battery lookup table position confirmed at L3:R14
- `.planning/PROJECT.md` -- v1.4 milestone goal description

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new libraries needed, all existing
- Architecture: HIGH - direct code reading, exact line numbers identified
- Pitfalls: HIGH - verified by reading actual xlsx data vs code expectations

**Research date:** 2026-03-28
**Valid until:** 2026-04-28 (stable -- xlsx format and Dash/Plotly APIs don't change fast)
