# Phase 14: UX Quality & Content Rewrite - Research

**Researched:** 2026-03-27
**Domain:** Dash 4.0 slider behavior, dcc.Loading spinners, dcc.Store-driven UI, content alignment with data.xlsx
**Confidence:** HIGH

## Summary

Phase 14 makes six categories of changes to a Dash 4.0 / dash-bootstrap-components 2.0.4 application: (1) slider updatemode and direct-input fixes, (2) battery slider mark labels and tooltip, (3) dcc.Loading spinner around chart outputs, (4) a first-visit guidance banner driven by dcc.Store, (5) landing page intro and system card text rewrites, and (6) mechanical PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS alignment with the current data.xlsx BOM.

All changes are confined to four files (`charts.py`, `overview.py`, `config.py`, `shell.py`) plus one callback addition. The Dash 4.0 APIs for `allow_direct_input`, `dcc.Loading`, and `dcc.Store` are confirmed available. The mechanical data.xlsx Part 1 rows (16-30) have been read and the exact column B strings are documented below for PROCESS_STAGES mapping.

**Primary recommendation:** Split into three plans: (1) slider fixes + loading spinner + banner (UX work in charts.py + shell.py), (2) landing page and system card rewrites (overview.py), (3) mechanical content update (config.py + processing.py fallback fix).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: Change slider-tds updatemode from "drag" to "mouseup"
- D-02: Change slider-depth updatemode from "drag" to "mouseup"
- D-03: Add allow_direct_input=False to all four sliders
- D-04: Battery slider marks: {0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}, tooltip: {"always_visible": True, "placement": "bottom"}
- D-05: One dcc.Loading wrapper around the entire chart output area (row1 + row2), not individual per-chart wrappers
- D-06: Spinner type: default circle (type="default")
- D-07: Banner placement: immediately above the control panel card
- D-08: Banner dismiss trigger: first slider interaction (any of four sliders)
- D-09: Session-only persistence via dcc.Store (no localStorage)
- D-10: Banner text (exact): "Use the sliders below to adjust salinity, depth, and storage mix -- charts update on mouse release. Drag any slider to dismiss this tip."
- D-11: dbc.Alert with color="info", dismissable=False, is_open controlled by dcc.Store
- D-12: Full rewrite of intro card body
- D-13: Card title: keep "About This Project" unchanged
- D-14: Content focus: wind-powered desalination explanation, senior design context, three-system technical overview, no data source mentions
- D-15: Hybrid card: remove "build a custom system" / "select one piece of equipment" -- update to fixed preset description
- D-16: Mechanical card: remove "wind-driven pumps" -- update to hydraulic drive architecture
- D-17: Update PROCESS_STAGES["mechanical"] to match data.xlsx Part 1 exactly
- D-18: Write new EQUIPMENT_DESCRIPTIONS for hydraulic components (1-2 sentences, student-accessible)
- D-19: Remove stale mechanical descriptions if no longer referenced by PROCESS_STAGES (verify no other code references first)

### Claude's Discretion
- Exact dcc.Store ID name for the banner dismissed-state flag
- Whether banner store is added to shell.py alongside other stores, or initialized in charts layout
- CSS styling details for the banner within dbc.Alert
- Exact paragraph structure and sentence order in landing page rewrite (within "project purpose + technical context" direction)

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| UX-01 | All chart outputs wrapped in dcc.Loading -- no blank white boxes during callbacks | dcc.Loading API confirmed in Dash 4.0; wrap row1+row2 div per D-05 |
| UX-02 | Battery/tank slider has clear endpoint labels and always-visible tooltip | dcc.Slider marks and tooltip props confirmed; exact values in D-04 |
| UX-03 | TDS and depth sliders use mouseup updatemode | updatemode="mouseup" confirmed available; D-01/D-02 |
| UX-04 | allow_direct_input=False on all four sliders | Confirmed new Dash 4.0 prop, default True; D-03 |
| UX-05 | First-visit dismissable callout above control panel | dbc.Alert + dcc.Store pattern confirmed; D-07 through D-11 |
| CONTENT-01 | Landing page intro rewritten -- wind-powered desalination, three systems, no AI references | overview.py rewrite targets identified; D-12 through D-16 |
| CONTENT-02 | Mechanical process stages and equipment descriptions updated for hydraulic drive | data.xlsx mechanical rows read; exact component names documented below |
</phase_requirements>

## Standard Stack

### Core (already installed, no additions needed)

| Library | Version | Purpose | Verified |
|---------|---------|---------|----------|
| dash | 4.0.0 | Application framework | pip show confirmed |
| dash-bootstrap-components | 2.0.4 | UI component library (dbc.Alert, dbc.Card) | pip show confirmed |
| plotly | (bundled with Dash 4.0) | Chart rendering | Implicit with Dash |

### Key APIs Used

| API | Module | Purpose |
|-----|--------|---------|
| `dcc.Slider(allow_direct_input=False)` | dash.dcc | Suppress Dash 4.0 text input boxes on sliders |
| `dcc.Slider(updatemode="mouseup")` | dash.dcc | Fire callback only on mouse release |
| `dcc.Loading(type="default")` | dash.dcc | Display spinner during chart callback execution |
| `dcc.Store(id=..., data=...)` | dash.dcc | Session-scoped banner dismissed state |
| `dbc.Alert(color="info", is_open=...)` | dash_bootstrap_components | Dismissable info banner |

**Installation:** No new packages required.

## Architecture Patterns

### Files Modified

```
src/
  layout/
    charts.py        # Slider props, dcc.Loading wrapper, banner component + callback
    overview.py      # Landing page intro rewrite, system card descriptions
    shell.py         # New dcc.Store for banner state
  config.py          # PROCESS_STAGES["mechanical"], EQUIPMENT_DESCRIPTIONS
  data/
    processing.py    # Fallback turbine name fix (line 662)
```

### Pattern 1: dcc.Loading Wrapper Around Chart Grid

**What:** Wrap the chart row1 + row2 in a single `dcc.Loading` component so a spinner appears during any chart callback execution.

**Current structure (charts.py make_chart_section return):**
```python
return html.Div([
    html.H4("System Comparison", className="mt-4 mb-3"),
    legend_store,
    control_panel,
    legend_row,
    row1,
    row2,
])
```

**Target structure:**
```python
return html.Div([
    html.H4("System Comparison", className="mt-4 mb-3"),
    legend_store,
    banner,           # NEW: dbc.Alert guidance banner
    control_panel,
    legend_row,
    dcc.Loading(      # NEW: spinner wrapper
        children=[row1, row2],
        type="default",
    ),
])
```

**Why single wrapper:** The update_charts callback outputs to all four chart figures simultaneously. A single wrapper catches any chart update. Multiple wrappers would show four spinners for one logical operation.

### Pattern 2: dcc.Store-Driven Banner Dismiss

**What:** A dcc.Store holds `{"dismissed": False}`. A callback watches all four slider `value` inputs. On first slider interaction, it sets `dismissed: True`. The banner's `is_open` prop reads from this store.

**Implementation pattern:**
```python
@callback(
    Output("store-banner-dismissed", "data"),
    Output("banner-guidance", "is_open"),
    Input("slider-time-horizon", "value"),
    Input("slider-battery", "value"),
    Input("slider-tds", "value"),
    Input("slider-depth", "value"),
    State("store-banner-dismissed", "data"),
    prevent_initial_call=True,
)
def dismiss_banner(th, bat, tds, depth, store):
    return {"dismissed": True}, False
```

**Store location:** shell.py alongside `sidebar-collapsed` and `active-system` stores. This follows the established pattern and ensures the store is initialized before any callback references it (suppress_callback_exceptions=True is set).

### Pattern 3: PROCESS_STAGES Key Matching

**What:** PROCESS_STAGES keys must match column B strings from data.xlsx exactly. The loader reads column B and the equipment_grid.py looks up each name in both PROCESS_STAGES (for stage assignment) and EQUIPMENT_DESCRIPTIONS (for tooltip text).

**Critical:** String matching is exact, including trailing spaces. The data.xlsx mechanical section column B strings (rows 16-30) have been read and are documented in the "Mechanical Data.xlsx Mapping" section below.

### Anti-Patterns to Avoid

- **Per-chart Loading wrappers:** Four spinners appearing for one callback. Use single wrapper.
- **localStorage for banner:** User explicitly chose session-only. dcc.Store with default storage_type is sufficient.
- **Guessing component names:** PROCESS_STAGES keys MUST come from data.xlsx column B, not from memory or approximation.
- **Dismissable=True on Alert:** User explicitly said no X button. Dismiss is slider-driven.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Loading indicator | Custom CSS spinner | `dcc.Loading(type="default")` | Built into Dash, auto-detects callback loading state |
| Banner show/hide | JavaScript visibility toggle | `dbc.Alert(is_open=...)` + `dcc.Store` | Standard Dash pattern, no custom JS needed |
| Session state | Cookie or localStorage | `dcc.Store` (default session) | Built-in Dash component, auto-cleared on page close |

## Mechanical Data.xlsx Mapping (CRITICAL for CONTENT-02)

### Exact Column B Strings from data.xlsx Part 1, Rows 16-30

| Row | Column B (exact string) | Suggested Stage |
|-----|------------------------|-----------------|
| 16 | `1 MW Aeromotor Turbine` | Water Extraction |
| 17 | `Wind turbine rotor lock` | Water Extraction |
| 18 | `Gearbox (Winergy  PEAB series)` | Water Extraction |
| 19 | `Variable-Displacement Hydraulic Power Unit (HPU)` | Water Extraction |
| 20 | `300 Bar Hydraulic Manifold (Custom Ductile Iron Block)` | Water Extraction |
| 21 | `Hydraulic Motor (225 kW rating) (Haaglund CA 50)` | Water Extraction |
| 22 | `Hydraulic Motor (225 kW rating) (Haaglund CA 70)` | Water Extraction |
| 23 | `Vertical Turbine Pump (PSI Prolew Flowserve VTP)` | Water Extraction |
| 24 | `Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)` | Desalination |
| 25 | `High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)` | Desalination |
| 26 | `Gate valve` | Pre-Treatment |
| 27 | `Reverse osmosis train` | Desalination |
| 28 | `Extra storage tank (100,000 gallons)` | Brine Disposal |
| 29 | `Calcite bed contactors` | Post-Treatment |
| 30 | `Pipes (total)` | Pre-Treatment |

**IMPORTANT NOTES:**
1. Row 18 has a DOUBLE SPACE: `"Gearbox (Winergy  PEAB series)"` -- note the two spaces between "Winergy" and "PEAB". Keys must preserve this.
2. Row 24 contains a special character (en-dash or similar) in `"Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)"` -- the character between "13000" and "3G" rendered as `\ufffd` in the Python output, meaning it may be a non-ASCII character. The planner must have the executor read this cell directly to capture the exact bytes.
3. Row 17 `"Wind turbine rotor lock"` is STILL in the mechanical BOM (unchanged from before). This means D-19's "remove stale entries" does NOT apply to this key -- it remains in PROCESS_STAGES.
4. Row 25 string appears to have a missing closing parenthesis: `"High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)"` -- only two opening parens but the string may or may not have a closing paren. Executor must read exact bytes.
5. Several items that were in the OLD mechanical PROCESS_STAGES are gone: `"250kW aeromotor turbine "` (replaced by `"1 MW Aeromotor Turbine"`), `"Submersible pump "` (replaced by VTP), `"2 RO membranes in parallel"` (replaced by `"Reverse osmosis train"`), `"Gear and Booster Pump"` (replaced by multiple hydraulic components).

### Proposed New PROCESS_STAGES["mechanical"]

```python
"mechanical": {
    "Water Extraction": [
        "1 MW Aeromotor Turbine",
        "Wind turbine rotor lock",
        "Gearbox (Winergy  PEAB series)",   # double space!
        "Variable-Displacement Hydraulic Power Unit (HPU)",
        "300 Bar Hydraulic Manifold (Custom Ductile Iron Block)",
        "Hydraulic Motor (225 kW rating) (Haaglund CA 50)",
        "Hydraulic Motor (225 kW rating) (Haaglund CA 70)",
        "Vertical Turbine Pump (PSI Prolew Flowserve VTP)",
    ],
    "Pre-Treatment": [
        "Gate valve",
        "Pipes (total)",
    ],
    "Desalination": [
        "Plunger Pump (Triplex Plunger Pump K 13000 ... 3G)",  # exact char TBD
        "High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)",
        "Reverse osmosis train",
    ],
    "Post-Treatment": [
        "Calcite bed contactors",
    ],
    "Brine Disposal": [
        "Extra storage tank (100,000 gallons)",
    ],
}
```

### New EQUIPMENT_DESCRIPTIONS Needed

Keys that need new description entries (not currently in EQUIPMENT_DESCRIPTIONS):
1. `"1 MW Aeromotor Turbine"` -- (hybrid already has this entry, check if key matches exactly)
2. `"Gearbox (Winergy  PEAB series)"` -- double space variant differs from hybrid's single-space key
3. `"Variable-Displacement Hydraulic Power Unit (HPU)"` -- differs from hybrid's `"Variable-Displacement HPU"`
4. `"Hydraulic Motor (225 kW rating) (Haaglund CA 50)"` -- differs from hybrid's `"Hydraulic Motor (225 kW, Haaglund CA 50)"`
5. `"Hydraulic Motor (225 kW rating) (Haaglund CA 70)"` -- entirely new
6. `"Vertical Turbine Pump (PSI Prolew Flowserve VTP)"` -- hybrid has this exact key, can reuse
7. `"Plunger Pump (Triplex Plunger Pump K 13000 ... 3G)"` -- entirely new
8. `"High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)"` -- differs from hybrid's shorter key
9. `"Reverse osmosis train"` -- lowercase, differs from hybrid's `"Reverse Osmosis Trains"`
10. `"Extra storage tank (100,000 gallons)"` -- lowercase, differs from hybrid's `"Extra Storage Tank (100,000 gallons)"`

### Stale Entries Safe to Remove

| Key | In PROCESS_STAGES? | In processing.py? | Safe to Remove from EQUIPMENT_DESCRIPTIONS? |
|-----|--------------------|--------------------|---------------------------------------------|
| `"250kW aeromotor turbine "` | Will be removed | Yes (line 662 fallback) | Remove AFTER fixing processing.py |
| `"Submersible pump "` | Will be removed | No | YES |
| `"Gear and Booster Pump"` | Will be removed | No | YES |
| `"2 RO membranes in parallel"` | Will be removed | No | YES (not currently in descriptions, so no action) |

### processing.py Fallback Fix (CRITICAL)

**File:** `src/data/processing.py`, line 662
**Current:** `mechanical_df[mechanical_df["name"] == "250kW aeromotor turbine "]["quantity"]`
**Must change to:** `mechanical_df[mechanical_df["name"] == "1 MW Aeromotor Turbine"]["quantity"]`

This is in a fallback code path (only executes when energy sheet data is unavailable), but it must still be correct. The old turbine name no longer exists in data.xlsx.

## Common Pitfalls

### Pitfall 1: String Mismatch in PROCESS_STAGES Keys
**What goes wrong:** Equipment table shows "No description available" or items are missing from stage groupings.
**Why it happens:** Column B strings have trailing spaces, double spaces, non-ASCII characters, or case differences that don't match the keys in config.py.
**How to avoid:** Read the exact cell value from data.xlsx programmatically. Do not type the strings by hand. Compare byte-by-byte if needed.
**Warning signs:** Equipment grid shows ungrouped items or "Other" stage catch-all grows unexpectedly.

### Pitfall 2: Banner Callback Firing on Page Load
**What goes wrong:** Banner disappears immediately because slider default values trigger the dismiss callback.
**Why it happens:** Without `prevent_initial_call=True`, Dash fires all callbacks once on page load with initial values.
**How to avoid:** Set `prevent_initial_call=True` on the banner dismiss callback. This is already noted in the pattern above.
**Warning signs:** Banner never visible on first page load.

### Pitfall 3: dcc.Loading Wrapping Too Much or Too Little
**What goes wrong:** Spinner appears during legend toggle (wrapping too much) or doesn't appear during chart update (wrapping too little).
**Why it happens:** dcc.Loading triggers when any child component's loading_state changes. If legend badges are inside the wrapper, toggling legend shows spinner. If chart graphs are outside, no spinner.
**How to avoid:** Wrap ONLY the div containing row1 and row2 (the four chart cards). Control panel, legend row, and banner must be outside the wrapper.
**Warning signs:** Spinner fires on legend badge click, or no spinner on slider release.

### Pitfall 4: Multiple Outputs to Same Store
**What goes wrong:** Callback registration error because the banner callback and the main chart callback both try to output to conflicting stores.
**Why it happens:** The banner dismiss callback outputs to `"store-banner-dismissed"` which is separate from any chart callback output. But if someone tries to combine it with the existing chart callback, Dash will error on duplicate outputs.
**How to avoid:** Keep the banner dismiss callback completely separate from the update_charts callback. They share slider Inputs but have different Outputs.
**Warning signs:** Dash error about "A component property can only be the Output of one callback."

### Pitfall 5: Hybrid vs Mechanical Key Divergence
**What goes wrong:** Descriptions work for hybrid but not mechanical, or vice versa.
**Why it happens:** data.xlsx uses slightly different component name strings for the same physical equipment in mechanical vs hybrid sections (e.g., "Gearbox (Winergy  PEAB series)" with double space vs "Gearbox (Winergy PEAB series)" with single space).
**How to avoid:** Each system's PROCESS_STAGES keys must match its own section in data.xlsx. Do not assume mechanical and hybrid share the same strings.
**Warning signs:** Mechanical equipment grid shows items without descriptions while hybrid works fine.

## Code Examples

### Slider Fix Pattern (all four sliders)
```python
# Source: Dash 4.0 docs - https://dash.plotly.com/dash-core-components/slider
dcc.Slider(
    id="slider-tds",
    min=0,
    max=35000,
    step=100,
    value=950,
    marks={0: "0", 10000: "10k", 20000: "20k", 35000: "35k"},
    tooltip={"always_visible": True, "placement": "bottom"},
    updatemode="mouseup",           # CHANGED from "drag"
    allow_direct_input=False,       # NEW -- suppresses Dash 4.0 text input
)
```

### dcc.Loading Wrapper
```python
# Source: Dash docs - https://dash.plotly.com/dash-core-components/loading
dcc.Loading(
    children=[row1, row2],
    type="default",
)
```

### Banner Component
```python
# Source: dash-bootstrap-components dbc.Alert
dbc.Alert(
    "Use the sliders below to adjust salinity, depth, and storage mix "
    "-- charts update on mouse release. Drag any slider to dismiss this tip.",
    id="banner-guidance",
    color="info",
    is_open=True,
    dismissable=False,
    className="small no-print",
)
```

### Banner Dismiss Callback
```python
@callback(
    Output("store-banner-dismissed", "data"),
    Output("banner-guidance", "is_open"),
    Input("slider-time-horizon", "value"),
    Input("slider-battery", "value"),
    Input("slider-tds", "value"),
    Input("slider-depth", "value"),
    State("store-banner-dismissed", "data"),
    prevent_initial_call=True,
)
def dismiss_banner(_th, _bat, _tds, _depth, store):
    return {"dismissed": True}, False
```

## Open Questions

1. **Exact byte sequence for Plunger Pump name (row 24)**
   - What we know: Python displayed a replacement character for the character between "13000" and "3G"
   - What's unclear: Whether it is an en-dash, em-dash, or other Unicode character
   - Recommendation: Executor must read the cell value directly with repr() to get exact bytes, then use that exact string as the PROCESS_STAGES key

2. **Row 25 closing parenthesis**
   - What we know: The string appears as `"High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)"`
   - What's unclear: Whether there is a second closing paren that was not visible
   - Recommendation: Executor reads exact cell value

3. **Stage assignment for hydraulic drivetrain components**
   - What we know: HPU, gearbox, manifold, and hydraulic motors are part of the wind-to-pump drivetrain
   - What's unclear: Whether all should be "Water Extraction" or if some should be a different stage
   - Recommendation: Group all drivetrain components (turbine through VTP) under "Water Extraction" since they collectively extract and move water. Plunger pump and high-pressure pump go under "Desalination" since they pressurize for RO.

## Sources

### Primary (HIGH confidence)
- data.xlsx Part 1 rows 15-31 -- read directly via openpyxl, exact column B strings captured
- src/layout/charts.py -- full file read, all slider definitions and chart layout confirmed
- src/layout/overview.py -- full file read, current intro text and system card descriptions confirmed
- src/config.py -- full file read, current PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS confirmed
- src/layout/shell.py -- full file read, existing dcc.Store pattern confirmed
- src/data/processing.py lines 650-680 -- fallback turbine name reference confirmed at line 662

### Secondary (MEDIUM confidence)
- [Dash dcc.Loading docs](https://dash.plotly.com/dash-core-components/loading) -- API properties verified via WebSearch
- [Dash dcc.Slider docs](https://dash.plotly.com/dash-core-components/slider) -- allow_direct_input property confirmed via WebSearch
- pip show dash (4.0.0), pip show dash-bootstrap-components (2.0.4) -- versions confirmed locally

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries already installed and versions confirmed locally
- Architecture: HIGH -- all target files read, patterns clear, no ambiguity in component structure
- Pitfalls: HIGH -- string matching issues identified by reading actual data.xlsx; processing.py fallback fix identified by grep
- Content mapping: MEDIUM -- two column B strings have uncertain characters (rows 24, 25) that need byte-level verification

**Research date:** 2026-03-27
**Valid until:** 2026-04-27 (stable -- Dash 4.0 and data.xlsx unlikely to change)
