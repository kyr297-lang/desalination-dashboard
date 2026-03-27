# Architecture Patterns for v1.3 Systems Overhaul

**Domain:** Dash 4.0 app restructuring -- data loader, hybrid removal, image serving, per-system layouts
**Researched:** 2026-03-26
**Overall confidence:** HIGH (based on direct codebase analysis; all recommendations derive from reading every relevant module)

---

## 1. Data Loader Restructuring

### What Changed in data.xlsx

The "Part 1" sheet has changed structurally:

| Aspect | v1.2 (Old) | v1.3 (New) |
|--------|-----------|-----------|
| Electrical BOM | Rows 1-12 | Rows 1-12 (unchanged) |
| Mechanical BOM | Rows 15-24 (9 components) | Rows 15-31 (hydraulic redesign, more components) |
| Miscellaneous section | Rows 27+ (existed) | **REMOVED entirely** |
| Hybrid BOM | Did not exist | Rows 33-50 (new, total-cost-per-row format) |
| New "Energy" sheet | Did not exist | Added (shaft powers, drivetrain efficiencies, turbine sizes) |

### Recommended Loader Changes

**File:** `src/data/loader.py`

#### A. Update SECTION_HEADERS to remove miscellaneous, add hybrid

```python
# OLD
SECTION_HEADERS: dict[str, str] = {
    "Electrical Components": "electrical",
    "Mechanical Components": "mechanical",
    "Miscalleneous": "miscellaneous",       # DELETE this line
}

# NEW
SECTION_HEADERS: dict[str, str] = {
    "Electrical Components": "electrical",
    "Mechanical Components": "mechanical",
    "Hybrid Components": "hybrid",           # ADD -- verify exact header text in column B
}
```

**IMPORTANT:** The exact header string for the hybrid section in column B of the updated data.xlsx must be confirmed. The old code matched the deliberate typo "Miscalleneous" exactly. Open the file and check what text appears at row 33, column B.

#### B. Update the required sections validation

```python
# OLD
required = {"electrical", "mechanical", "miscellaneous"}

# NEW
required = {"electrical", "mechanical", "hybrid"}
```

#### C. Update _parse_section calls with new row boundaries

The old code used miscellaneous start row as the stop boundary for mechanical. Now hybrid start row serves that role:

```python
# OLD
elec_start = section_row_map["electrical"]
mech_start = section_row_map["mechanical"]
misc_start = section_row_map["miscellaneous"]
electrical_rows   = _parse_section(ws, elec_start,  stop_rows={mech_start})
mechanical_rows   = _parse_section(ws, mech_start,  stop_rows={misc_start})
miscellaneous_rows = _parse_section(ws, misc_start, stop_rows=set())

# NEW
elec_start = section_row_map["electrical"]
mech_start = section_row_map["mechanical"]
hybrid_start = section_row_map["hybrid"]
electrical_rows  = _parse_section(ws, elec_start,  stop_rows={mech_start})
mechanical_rows  = _parse_section(ws, mech_start,  stop_rows={hybrid_start})
hybrid_rows      = _parse_section(ws, hybrid_start, stop_rows=set())
```

The dynamic header scanning (iterating column B for known strings) is already robust. It does not hardcode row numbers. As long as the header strings match, it will find the correct boundaries. This is one of the cleanest parts of the existing design.

#### D. Update the return dict

```python
# OLD return keys
return {
    "electrical":     pd.DataFrame(electrical_rows, columns=EQUIPMENT_COLUMNS),
    "mechanical":     pd.DataFrame(mechanical_rows, columns=EQUIPMENT_COLUMNS),
    "miscellaneous":  pd.DataFrame(miscellaneous_rows, columns=EQUIPMENT_COLUMNS),
    "battery_lookup": battery_df,
    "tds_lookup":     tds_df,
    "depth_lookup":   depth_df,
}

# NEW return keys
return {
    "electrical":     pd.DataFrame(electrical_rows, columns=EQUIPMENT_COLUMNS),
    "mechanical":     pd.DataFrame(mechanical_rows, columns=EQUIPMENT_COLUMNS),
    "hybrid":         pd.DataFrame(hybrid_rows, columns=EQUIPMENT_COLUMNS),
    "battery_lookup": battery_df,
    "tds_lookup":     tds_df,
    "depth_lookup":   depth_df,
    "energy":         energy_df,     # new Energy sheet
}
```

#### E. Parse the new Energy sheet

Add a `_parse_energy_sheet(wb)` function. The Energy sheet contains per-system shaft powers, drivetrain efficiencies, and selected turbine sizes. The exact cell layout needs to be confirmed from the actual sheet, but the pattern mirrors `_parse_part2_lookups`:

```python
def _parse_energy_sheet(wb) -> pd.DataFrame:
    """Parse the Energy sheet into a DataFrame."""
    if "Energy" not in wb.sheetnames:
        raise ValueError(
            f"Expected sheet 'Energy' not found. "
            f"Available sheets: {wb.sheetnames}"
        )
    ws = wb["Energy"]
    # Parse structure TBD -- confirm row/column layout from actual file
    # Expected: system names in rows, columns for shaft loads, efficiencies, turbine sizes
    ...
```

#### F. Battery lookup table -- verify it still exists

The battery lookup (J3:P14 in Part 1) is still needed for the electrical system's battery/tank slider. Confirm these cells are still present and correctly positioned in the updated data.xlsx. The `_parse_battery_lookup` function uses hardcoded cell positions (J3:P14, rows 4-14), so if the sheet layout shifted, these ranges need updating.

### Downstream Impact of Removing "miscellaneous" Key

Every module that references `data["miscellaneous"]` must be updated. The key `"miscellaneous"` appears in:

| File | Usage | Action |
|------|-------|--------|
| `src/data/loader.py` | Returns it | Change to `"hybrid"` |
| `src/data/processing.py` `compute_hybrid_df()` | Searches `data["miscellaneous"]` first | Remove `"miscellaneous"` from search_order; hybrid is now a static BOM, not user-built |
| `src/data/processing.py` `compute_chart_data()` | References `data["miscellaneous"]` indirectly via hybrid_df | No longer needed (hybrid_df comes from `data["hybrid"]` directly) |
| `src/config.py` PROCESS_STAGES | Has `"miscellaneous"` key | Replace with `"hybrid"` key and update component names to match new hybrid BOM |
| `src/layout/hybrid_builder.py` | Looks up `PROCESS_STAGES["miscellaneous"]` for dropdown options | Being deleted entirely |
| `src/layout/equipment_grid.py` | Passes `"miscellaneous"` as system key for hybrid accordion items | Change to `"hybrid"` |

---

## 2. Serving and Displaying Static Images

### Current State

Three PNG files are in the project root (not in `assets/`):
- `Electrical System Layout.png` (63 KB)
- `Hybrid System Layout.png` (100 KB)
- `Mechanical System Layout.png` (333 KB)

The `assets/` folder exists with only `custom.css`.

### Recommended Pattern: assets/ folder + html.Img with get_asset_url

**Step 1:** Move PNGs into `assets/` with URL-safe filenames (no spaces):

```
assets/
  custom.css
  mechanical-system-layout.png
  electrical-system-layout.png
  hybrid-system-layout.png
```

Dash automatically serves everything in `assets/` at `/_dash-app/assets/`. No configuration needed.

**Step 2:** Reference in layout code using `dash.get_asset_url()`:

```python
from dash import html, get_asset_url

html.Img(
    src=get_asset_url("mechanical-system-layout.png"),
    alt="Mechanical System Layout",
    style={"maxWidth": "100%", "height": "auto"},
    className="img-fluid shadow-sm rounded",
)
```

**Why `get_asset_url` over hardcoded paths:**
- Works regardless of `requests_pathname_prefix` (important for Render deployment)
- Works with Dash's built-in asset serving (no Flask route needed)
- Cache-busted automatically when Dash detects file changes

**Why NOT `app.get_asset_url`:** In Dash 4.0, `dash.get_asset_url()` is the module-level function. Using `app.get_asset_url()` would require importing the app object, creating circular import risk in layout modules. The module-level function avoids this entirely.

**Step 3:** Add a mapping constant in `src/config.py`:

```python
SYSTEM_LAYOUT_IMAGES = {
    "mechanical": "mechanical-system-layout.png",
    "electrical": "electrical-system-layout.png",
    "hybrid":     "hybrid-system-layout.png",
}
```

This keeps filenames centralized and makes the system_view.py code cleaner.

---

## 3. Removing Hybrid Builder and Cleaning Up Callbacks

### What hybrid_builder.py Currently Provides

| Component | ID | Purpose |
|-----------|----|---------|
| `make_hybrid_builder(data)` | Layout factory | 5-dropdown pipeline UI |
| `dcc.Store("store-hybrid-slots")` | Lives in `shell.py` | Holds {stage: equipment_name} state |
| `update_slot_store` callback | Writes `store-hybrid-slots` | Reads 5 dropdown values, writes to store |
| `clear_all_slots` callback | Clears 5 dropdowns | "Clear All" button handler |
| `update_slot_counter` callback | Writes `slot-counter.children` | "3/5 slots filled" label |
| `set_data(data)` | Module-level data setter | Called from app.py |

### Callbacks That READ store-hybrid-slots (Downstream Consumers)

These callbacks take `Input("store-hybrid-slots", "data")` and must be modified:

| File | Callback | What It Does | Action |
|------|----------|--------------|--------|
| `charts.py` `update_charts` | Reads slots to compute hybrid chart data | **Modify** -- use `data["hybrid"]` directly instead of `compute_hybrid_df(slots, data)` |
| `scorecard.py` `update_scorecard` | Reads slots to compute hybrid scorecard | **Modify** -- use `data["hybrid"]` directly, always show 3-column scorecard |
| `scorecard.py` `update_gate_overlay` | Shows/hides hybrid gate overlay | **DELETE** -- no gate needed, hybrid data is always available |
| `scorecard.py` `update_hybrid_equipment` | Renders hybrid equipment accordion | **Modify** -- hybrid equipment is now static, render from `data["hybrid"]` |

### Cleanup Sequence (Order Matters)

**Phase A: Delete hybrid_builder.py entirely**

1. Delete `src/layout/hybrid_builder.py`
2. Remove from `app.py`:
   ```python
   # DELETE these lines
   from src.layout.hybrid_builder import set_data as set_hybrid_builder_data
   set_hybrid_builder_data(DATA)
   ```

**Phase B: Remove store-hybrid-slots from shell.py**

In `shell.py` `create_layout()`, remove the `dcc.Store(id="store-hybrid-slots", ...)` component. Also remove the import of `SLOT_STAGES` from hybrid_builder:

```python
# DELETE from shell.py
from src.layout.hybrid_builder import SLOT_STAGES

# DELETE from create_layout()
dcc.Store(
    id="store-hybrid-slots",
    data={stage: None for stage in SLOT_STAGES},
),
```

**Phase C: Update system_view.py**

Remove the hybrid_builder import and all conditional hybrid logic:

```python
# DELETE
from src.layout.hybrid_builder import make_hybrid_builder

# In create_system_view_layout():
# DELETE the hybrid_builder_section conditional block (lines 107-109)
# DELETE the "if hybrid_builder_section is not None" append (lines 235-237)

# MODIFY the equipment section for hybrid:
# OLD: if active_system == "hybrid": show callback-driven container
# NEW: if active_system == "hybrid": render static equipment from data["hybrid"]
if active_system == "hybrid":
    system_df = data["hybrid"]
    equipment = make_equipment_section(system_df, "hybrid", data)
```

Also remove the gate overlay wrapping for the hybrid chart section -- hybrid charts should display immediately since data is always available.

**Phase D: Update charts.py -- remove slots Input**

The `update_charts` callback currently takes `Input("store-hybrid-slots", "data")`. This must be removed. Instead, the hybrid chart data comes from `_data["hybrid"]` directly:

```python
# OLD signature
@callback(
    ...
    Input("store-hybrid-slots", "data"),  # DELETE this Input
    ...
)
def update_charts(years, battery_fraction, visibility, slots, tds_ppm, depth_m):
    ...
    hybrid_df = compute_hybrid_df(slots, _data)  # DELETE
    ...

# NEW: hybrid_df is always available
def update_charts(years, battery_fraction, visibility, tds_ppm, depth_m):
    ...
    hybrid_df = _data["hybrid"]  # Always present, no gate check needed
    ...
```

**Phase E: Update scorecard.py -- remove slots-driven callbacks**

1. `update_scorecard`: Remove `Input("store-hybrid-slots", "data")`. Always render 3-column scorecard using `_data["hybrid"]`. The comparison text is always generated (no gate check).

2. `update_gate_overlay`: DELETE entirely. The overlay div no longer exists.

3. `update_hybrid_equipment`: DELETE entirely. Equipment is rendered statically in system_view.py.

**Phase F: Update processing.py -- simplify compute_hybrid_df**

`compute_hybrid_df(slots, data)` is no longer needed. It searched miscellaneous/mechanical/electrical DataFrames to build a 5-row hybrid DataFrame from user dropdown selections. With a static hybrid BOM in data.xlsx, hybrid data is just `data["hybrid"]`.

This function can either be deleted or repurposed. If no other code path calls it after the refactor, delete it. Also delete `generate_comparison_text` if the comparison text feature is being removed (or keep it if the static hybrid still shows comparison text).

### IDs to Remove From the DOM

After cleanup, these IDs should no longer exist anywhere:

| ID | Was In | Status |
|----|--------|--------|
| `store-hybrid-slots` | shell.py | DELETE |
| `slot-dd-water-extraction` | hybrid_builder.py | DELETE (file deleted) |
| `slot-dd-pre-treatment` | hybrid_builder.py | DELETE |
| `slot-dd-desalination` | hybrid_builder.py | DELETE |
| `slot-dd-post-treatment` | hybrid_builder.py | DELETE |
| `slot-dd-brine-disposal` | hybrid_builder.py | DELETE |
| `slot-counter` | hybrid_builder.py | DELETE |
| `btn-clear-all` | hybrid_builder.py | DELETE |
| `hybrid-gate-overlay` | system_view.py | DELETE |
| `hybrid-equipment-container` | system_view.py | DELETE (replaced with static render) |

IDs that REMAIN unchanged:
- `scorecard-container` -- still updated, but now always shows 3-column
- `comparison-text` -- kept if comparison text feature is retained
- All chart IDs, slider IDs, legend IDs -- unchanged
- `system-tabs`, `active-system`, `page-content` -- unchanged

---

## 4. Per-System Layout Differences Within the Tab Structure

### The Question

For v1.3, mechanical, electrical, and hybrid system pages need layout differences (different content sections, image placement, possibly different equipment groupings). Should this be done with:

(A) Conditional rendering inside callbacks, or
(B) Separate layout functions per system?

### Recommendation: Separate Layout Functions Per System

**Use pattern B.** Create per-system layout helper functions that `system_view.py` dispatches to.

**Rationale:**
- The existing `create_system_view_layout` already has growing `if active_system == "hybrid"` branches (lines 107-109, 137-139, 147-191). Adding more per-system conditionals will make it unreadable.
- Each system page will have a layout image, different equipment descriptions (hydraulic components for mechanical), and potentially different slider configurations. These differences are structural, not cosmetic.
- Separate functions keep each system's layout self-contained and independently testable.

### Recommended Pattern

**File:** `src/layout/system_view.py`

```python
def create_system_view_layout(active_system: str, data: dict) -> html.Div:
    """Dispatch to per-system layout builder."""
    # Shared: breadcrumb, tab bar, system badge
    breadcrumb = _make_breadcrumb()
    tab_bar = _make_tab_bar(active_system)
    system_badge = _make_system_badge(active_system)

    # Per-system content
    if active_system == "mechanical":
        content = _build_mechanical_content(data)
    elif active_system == "electrical":
        content = _build_electrical_content(data)
    elif active_system == "hybrid":
        content = _build_hybrid_content(data)
    else:
        content = html.P("Unknown system", className="text-danger")

    return html.Div([breadcrumb, tab_bar, system_badge, content])
```

Each `_build_*_content` function returns the full content below the tab bar. They share sub-components via imports (scorecard, charts, equipment_grid) but can compose them differently:

```python
def _build_mechanical_content(data: dict) -> html.Div:
    """Mechanical system page: hydraulic components, layout image, equipment, charts."""
    layout_image = _make_layout_image("mechanical")
    scorecard = ...  # scorecard card (shared)
    equipment = make_equipment_section(data["mechanical"], "mechanical", data)
    charts = make_chart_section()
    return html.Div([layout_image, scorecard_card, equipment_card, charts])
```

### Where to Place the Layout Image

The layout image should appear between the system badge and the scorecard -- it provides visual context for the equipment list below it. Wrap it in a `dbc.Card` for consistency:

```python
def _make_layout_image(system: str) -> dbc.Card:
    from dash import get_asset_url
    from src.config import SYSTEM_LAYOUT_IMAGES

    filename = SYSTEM_LAYOUT_IMAGES.get(system)
    if not filename:
        return html.Div()

    return dbc.Card(
        dbc.CardBody([
            html.H5(f"{system.capitalize()} System Layout", className="mb-2"),
            html.Img(
                src=get_asset_url(filename),
                alt=f"{system.capitalize()} System Layout Diagram",
                style={"maxWidth": "100%", "height": "auto"},
                className="img-fluid",
            ),
        ]),
        className="shadow-sm mb-3",
    )
```

### Shared vs Per-System Components

| Component | Shared or Per-System | Notes |
|-----------|---------------------|-------|
| Breadcrumb | Shared | Same "Back to Overview" link |
| Tab bar | Shared | Same 3 tabs |
| System badge | Shared | Same colored pill |
| Layout image | Per-system | Different PNG per system |
| Scorecard card | Shared | Always 3-column now (static hybrid) |
| Equipment section | Per-system | Different DataFrame, different PROCESS_STAGES mapping |
| Chart section | Shared | Same 4 charts, same sliders |
| Chart gate overlay | Removed | No longer needed |

---

## 5. PROCESS_STAGES Config Update

The `PROCESS_STAGES` dict in `config.py` must be updated for v1.3:

1. **Replace `"miscellaneous"` key with `"hybrid"`** and update component names to match the new hybrid BOM in data.xlsx (rows 33-50).

2. **Update `"mechanical"` key** with the new hydraulic component names (HPU, manifold, hydraulic motors, VTP, plunger pump). The exact names must match column B of the updated data.xlsx.

3. **`"electrical"` key** likely unchanged unless component names changed.

4. **Add `EQUIPMENT_DESCRIPTIONS` entries** for all new components (hydraulic motor, HPU, manifold, VTP, Danfoss APP pump, Tesla Megapack, etc.).

---

## 6. Scorecard Simplification

With hybrid data always available (static BOM in data.xlsx), the scorecard callback chain simplifies dramatically:

**Before (v1.2):**
- `update_scorecard` fires on `store-hybrid-slots` change, checks gate, conditionally shows 2 or 3 columns
- `update_gate_overlay` fires on `store-hybrid-slots` change, shows/hides overlay
- `update_hybrid_equipment` fires on `store-hybrid-slots` change, conditionally renders equipment

**After (v1.3):**
- `update_scorecard` is triggered on initial render only (or can be removed entirely and scorecard rendered statically in the layout factory)
- No gate overlay
- No hybrid equipment callback

**Decision point:** The scorecard is currently re-rendered via callback because hybrid data was dynamic. Now that all three systems have static data, the scorecard can be rendered at layout time in `create_system_view_layout` (or its per-system helpers). This eliminates one more callback. The scorecard callback only needs to survive if there is still a dynamic input that affects it (there is not -- the sliders only affect charts, not the scorecard).

**Recommendation:** Render the scorecard statically in the layout factory. Delete the `update_scorecard` callback. The `scorecard-container` div can still exist for the export/print button sibling structure, but its children are set at layout time.

---

## 7. Complete File Change Map

| File | Change Type | Summary |
|------|------------|---------|
| `src/data/loader.py` | **Modify** | Remove miscellaneous, add hybrid section + Energy sheet parser |
| `src/config.py` | **Modify** | Update PROCESS_STAGES (mechanical components, hybrid replaces miscellaneous), add SYSTEM_LAYOUT_IMAGES, add new EQUIPMENT_DESCRIPTIONS |
| `src/data/processing.py` | **Modify** | Delete `compute_hybrid_df`, simplify `compute_chart_data` (hybrid_df always from data["hybrid"]), remove miscellaneous references |
| `src/layout/hybrid_builder.py` | **DELETE** | Entire file removed |
| `src/layout/system_view.py` | **Modify** | Remove hybrid_builder import, refactor to per-system layout functions, add layout image, remove gate overlay |
| `src/layout/shell.py` | **Modify** | Remove store-hybrid-slots and SLOT_STAGES import |
| `src/layout/charts.py` | **Modify** | Remove store-hybrid-slots Input from update_charts, use data["hybrid"] directly |
| `src/layout/scorecard.py` | **Modify** | Remove update_gate_overlay callback, remove update_hybrid_equipment callback, simplify update_scorecard to always use 3-column (or render statically) |
| `src/layout/equipment_grid.py` | **Modify** | Change "miscellaneous" system key references to "hybrid" |
| `app.py` | **Modify** | Remove hybrid_builder set_data call |
| `assets/` | **Add files** | Move 3 PNGs with URL-safe names |

---

## 8. Callback Dependency Map (After v1.3)

```
User clicks system card/tab
  |
  v
shell.py: select_system_from_card / select_system_from_tab
  |
  v
shell.py: render_content (reads active-system store)
  |
  v
system_view.py: create_system_view_layout(active_system, data)
  |-- _make_breadcrumb()
  |-- _make_tab_bar(active_system)
  |-- _make_system_badge(active_system)
  |-- _make_layout_image(active_system)     [NEW]
  |-- scorecard (always 3-column, static)   [SIMPLIFIED]
  |-- make_equipment_section(data[system])   [STATIC for all 3 systems now]
  |-- make_chart_section()
       |
       v
  charts.py: update_charts
    Inputs: slider-time-horizon, slider-battery, store-legend-visibility,
            slider-tds, slider-depth
    [REMOVED: store-hybrid-slots]
    Uses _data["hybrid"] directly for hybrid chart data
```

Callback count reduction:
- **Deleted:** update_slot_store, clear_all_slots, update_slot_counter, update_gate_overlay, update_hybrid_equipment (5 callbacks removed)
- **Potentially deleted:** update_scorecard (if scorecard rendered statically -- 1 more callback removed)
- **Simplified:** update_charts (1 fewer Input), update_scorecard (1 fewer Input, no gate logic)
- **Unchanged:** toggle_sidebar, select_system_from_card, select_system_from_tab, back_to_overview, render_content, toggle_legend, update_badge_styles, export/print clientside callback

---

## 9. Migration Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Hybrid BOM header text mismatch | HIGH | Manually verify the exact string in column B row 33 of data.xlsx before coding |
| Battery lookup table position shifted | MEDIUM | Verify J3:P14 range is still correct; if mechanical BOM expanded to row 31, check no overlap |
| `suppress_callback_exceptions=True` masking real errors during refactor | MEDIUM | Temporarily set to False during development, test all 3 system pages end-to-end, then re-enable |
| Orphaned IDs in DOM after removing hybrid builder | LOW | Search all .py files for each deleted ID string to confirm no dangling references |
| PROCESS_STAGES component name mismatches | HIGH | Cross-reference every equipment name in the new data.xlsx Part 1 against PROCESS_STAGES entries exactly (trailing spaces, capitalization) |
| Render deployment breaks | LOW | Test locally, then push; Render auto-deploys from main |

---

## Sources

- Direct codebase analysis of all 11 modules (8,218 LOC)
- Memory files: project_context.md, project_energy_numbers.md, project_hybrid_bom.md
- Dash 4.0 asset serving: `assets/` folder auto-served, `dash.get_asset_url()` for path resolution (confirmed from project's existing use of `assets/custom.css`)
- Confidence: HIGH -- all recommendations derived from reading the actual code, not assumptions
