# Phase 4: Hybrid Builder - Research

**Researched:** 2026-02-22
**Domain:** Dash dcc.Dropdown, dcc.Store slot schema, completion gate pattern, dynamic scorecard, chart integration
**Confidence:** HIGH (all findings verified against live codebase and installed packages)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Builder layout & slots**
- Horizontal pipeline layout: slots flow left-to-right representing the process flow
- Visual arrows (→) connect each stage to reinforce the pipeline concept
- Each slot is a labeled dropdown only — minimal, clean, no per-slot stats before gate opens
- Dropdown options show equipment names only (no inline stats)
- Builder sits at the top of the Hybrid tab, above charts/scorecard
- Include a "Clear All" / reset button to start over
- On small screens, pipeline wraps to multiple rows (not horizontal scroll)

**Completion gate UX**
- Before all 5 slots are filled: charts area shows a centered message overlay (e.g., "Fill all 5 slots to see hybrid results") with empty/placeholder chart outlines behind it
- Simple counter displayed: "3/5 slots filled"
- When 5th slot is filled: charts and scorecard appear instantly (no animation)
- If a user clears a slot after gate was met: charts disappear immediately and message overlay returns (gate re-engages)

**Hybrid results integration**
- Hybrid color: Claude's discretion — pick a color that complements existing Mechanical and Electrical colors
- Charts recalculate only when all 5 slots are filled — changing one slot hides results until all 5 are set again
- Hybrid row in scorecard uses same styling as preset systems (no special distinction)
- Clicking hybrid equipment opens the same detail view as preset equipment items
- Hybrid system appears as an equal third system in all comparison charts

**Comparison description text**
- Neutral/factual tone: straightforward percentage comparisons (e.g., "Hybrid costs 15% less than Mechanical")
- Covers all scorecard metrics: cost, land area, and efficiency
- Appears below the scorecard table
- Updates dynamically whenever the hybrid configuration changes (and gate is met)

### Claude's Discretion
- Hybrid system color choice
- Exact arrow styling between pipeline slots
- Loading/placeholder chart outline design behind the gate message
- Responsive breakpoints for pipeline wrapping

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| HYB-01 | User sees 5 functional slots: Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal | `dcc.Dropdown` per stage; stage names are keys in `store-hybrid-slots`; rendered in pipeline row in `hybrid_builder.py` |
| HYB-02 | Each slot presents a dropdown of valid equipment from the Miscellaneous sheet | Equipment pool built from `data["miscellaneous"]` filtered by `PROCESS_STAGES["miscellaneous"][stage]`; Desalination gap requires adding mech/elec RO items to `PROCESS_STAGES["miscellaneous"]["Desalination"]` in `config.py` |
| HYB-03 | User cannot see comparison results or detailed output until all 5 slots are filled (completion gate) | `store-hybrid-slots` dict; `gate_open = all(v is not None for v in slots.values())`; overlay `html.Div` positioned absolutely over charts; charts callback guards on `gate_open` |
| HYB-04 | After completion, user can select hybrid equipment for detailed data view | Reuse existing `_make_accordion_item` / `make_equipment_section` pattern from `equipment_grid.py`; populate hybrid equipment section when gate is open |
| SCORE-03 | Hybrid system shows comparison description text against the two preset systems | Text generated from scorecard metrics (cost/land/efficiency % comparisons); placed below scorecard table; updates via callback when `store-hybrid-slots` changes and gate is met |
</phase_requirements>

---

## Summary

Phase 4 adds the hybrid builder to the existing Hybrid tab, which currently shows a placeholder empty-state message. All packages needed are already installed (Dash 4.0, DBC 2.0.4, plotly 6.5.2, pandas 2.3.3). No new dependencies required.

The most critical finding is a **data gap**: the `Desalination` stage has zero items in the miscellaneous sheet and `PROCESS_STAGES["miscellaneous"]`. The requirement says "dropdown of valid equipment from the Miscellaneous sheet" — but Desalination only has equipment in the mechanical and electrical sheets (`2 RO membranes in parallel`, `Gear and Booster Pump`, `RO membranes in parallel`, `Booster Pump`). The fix is to extend `PROCESS_STAGES["miscellaneous"]["Desalination"]` in `config.py` to include those items (they are the RO membranes and pumps that are the only physically valid desalination choices in the dataset). A second finding: `Multi-Media Filtration` appears in `PROCESS_STAGES["miscellaneous"]["Pre-Treatment"]` in config.py but is not in the actual miscellaneous data — it is in the electrical sheet. This means Pre-Treatment currently provides only `Antiscalant` from the miscellaneous pool.

The completion gate is implemented as a `dcc.Store("store-hybrid-slots")` holding a dict of `{stage_name: selected_equipment_name | None}`. When all 5 values are non-None, the gate opens. Charts and scorecard update by reading this store as an additional Input on the existing `update_charts` callback and a new `update_scorecard` callback. The overlay uses an absolutely-positioned `html.Div` that is shown/hidden via a callback controlling its `style` property (`display: block` vs `display: none`).

The hybrid color `#6BAA75` (muted sage green) is already defined in `config.py` `SYSTEM_COLORS["Hybrid"]` and is already used in Phase 3 as a placeholder. No change needed.

**Primary recommendation:** Create `src/layout/hybrid_builder.py` containing the pipeline UI and its callbacks. Modify `system_view.py` to render the hybrid builder when the active system is "hybrid". Modify `charts.py` to accept a 4th Input (`store-hybrid-slots`) and compute real hybrid data when gate is open. Modify `scorecard.py` and `processing.py` to support a third system (hybrid). Add a `scorecard-container` id to enable dynamic scorecard updates.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash (dcc.Dropdown) | 4.0.0 (installed) | 5 dropdown selectors for equipment slots | Built-in; `options`, `value`, `clearable`, `placeholder` exactly fit the slot pattern |
| dash (dcc.Store) | 4.0.0 (installed) | `store-hybrid-slots` dict holding 5 slot selections | Established project pattern for cross-callback state (see shell.py, charts.py) |
| dash_bootstrap_components | 2.0.4 (installed) | dbc.Row/Col pipeline layout, dbc.Button for Clear All | Consistent with existing UI; `dbc.Col` with `xs=12 md=auto` for responsive wrapping |
| plotly | 6.5.2 (installed) | Chart updates with real hybrid data (replacing zeros) | Already integrated; hybrid trace already built in all 4 figure builders |
| pandas | 2.3.3 (installed) | Filter miscellaneous DataFrame for dropdown options; compute hybrid metrics | Already the data layer |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| dash.ctx | bundled with Dash 4.0 | Identify which dropdown fired (pattern-matching or 5 explicit Inputs) | Use 5 explicit Inputs for simplicity; ctx not needed for basic slot updates |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 5 explicit dcc.Dropdown Inputs | Pattern-matching `Input({"type": "slot-dropdown", "index": ALL}, "value")` | Pattern-matching adds `ctx` complexity with no benefit; 5 explicit Inputs are readable and fixed |
| Absolute-positioned overlay for gate | dbc.Modal or dbc.Collapse | Modal is disruptive; Collapse doesn't show chart outlines "behind" message; absolute overlay is cleanest |
| Separate `store-hybrid-metrics` derived store | Direct slot store Input to all callbacks | Extra indirection; simpler to let update_charts and update_scorecard read `store-hybrid-slots` directly |

**Installation:** No new packages. All dependencies already installed.

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── data/
│   └── processing.py       # MODIFY: compute_scorecard_metrics() add hybrid_df param;
│                           #         compute_chart_data() accept hybrid_slots param;
│                           #         add compute_hybrid_df() helper;
│                           #         add generate_comparison_text() for SCORE-03
├── layout/
│   ├── hybrid_builder.py   # NEW: make_hybrid_builder(), slot store, callbacks
│   ├── scorecard.py        # MODIFY: make_scorecard_table() add hybrid_df param;
│   │                       #         add scorecard-container id; make callback-driven
│   ├── charts.py           # MODIFY: update_charts() add Input("store-hybrid-slots", "data")
│   ├── system_view.py      # MODIFY: render hybrid tab with hybrid_builder instead of empty state
│   └── equipment_grid.py   # MODIFY: hybrid case builds from slot selections (HYB-04)
└── config.py               # MODIFY: add Desalination items to PROCESS_STAGES["miscellaneous"]
```

### Pattern 1: dcc.Store Slot Schema
**What:** A single `dcc.Store("store-hybrid-slots")` holds a dict with one key per stage. None = unselected, string = equipment name chosen.
**When to use:** Any time multi-step form state must be accessible across multiple callbacks without re-querying inputs.
**Example:**
```python
# Source: Established project pattern — mirrors store-legend-visibility in charts.py

# Initial store value
slot_schema = {
    "Water Extraction": None,
    "Pre-Treatment":    None,
    "Desalination":     None,
    "Post-Treatment":   None,
    "Brine Disposal":   None,
}

dcc.Store(id="store-hybrid-slots", data=slot_schema)

# Gate check (used in every callback that depends on gate state)
def _gate_open(slots: dict) -> bool:
    return all(v is not None for v in slots.values())

# Filled count for counter display
def _slots_filled(slots: dict) -> int:
    return sum(1 for v in slots.values() if v is not None)
```

### Pattern 2: Slot Update Callback (5 Explicit Inputs)
**What:** One callback listens to all 5 dropdown `value` properties and writes the full updated dict to the slot store.
**When to use:** Fixed number of slots (5) — explicit Inputs are clear and debuggable.
**Example:**
```python
# Source: Dash 4.0 docs - multiple Input callback pattern
from dash import callback, Input, Output

@callback(
    Output("store-hybrid-slots", "data"),
    Input("slot-dd-water-extraction", "value"),
    Input("slot-dd-pre-treatment",    "value"),
    Input("slot-dd-desalination",     "value"),
    Input("slot-dd-post-treatment",   "value"),
    Input("slot-dd-brine-disposal",   "value"),
)
def update_slot_store(water, pre, desal, post, brine):
    return {
        "Water Extraction": water,
        "Pre-Treatment":    pre,
        "Desalination":     desal,
        "Post-Treatment":   post,
        "Brine Disposal":   brine,
    }
```

### Pattern 3: Clear All Button Resets Dropdowns
**What:** A "Clear All" button sets all 5 dropdown values to None, which triggers the slot update callback, which zeroes the store.
**When to use:** Reset pattern where the button drives state through the existing callback chain rather than directly writing the store.
**Example:**
```python
# Source: Dash 4.0 docs - State + Output pattern for reset
from dash import callback, Input, Output, State

@callback(
    Output("slot-dd-water-extraction", "value"),
    Output("slot-dd-pre-treatment",    "value"),
    Output("slot-dd-desalination",     "value"),
    Output("slot-dd-post-treatment",   "value"),
    Output("slot-dd-brine-disposal",   "value"),
    Input("btn-clear-all", "n_clicks"),
    prevent_initial_call=True,
)
def clear_all_slots(n_clicks):
    return None, None, None, None, None

# NOTE: Returning None to each dropdown sets value=None, which fires the
# update_slot_store callback above, cascading the gate back to closed.
```

### Pattern 4: Gate Overlay (Absolute Positioning)
**What:** A `html.Div` positioned absolutely over the charts container shows "Fill all 5 slots" message when gate is closed, and is hidden when gate opens.
**When to use:** When the gated content (charts with outlines) must be visually present but obscured until condition is met.
**Example:**
```python
# Wrapper with relative positioning
html.Div(
    [
        # Overlay (shown when gate closed)
        html.Div(
            html.P(
                "Fill all 5 slots to see hybrid results",
                className="text-center text-muted fst-italic mt-5",
            ),
            id="hybrid-gate-overlay",
            style={
                "position": "absolute",
                "top": "0", "left": "0",
                "width": "100%", "height": "100%",
                "backgroundColor": "rgba(255,255,255,0.85)",
                "zIndex": "10",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            },
        ),
        # Actual chart section (always rendered, shown behind overlay)
        make_chart_section(),
    ],
    style={"position": "relative"},
)

# Callback to show/hide overlay based on gate state
@callback(
    Output("hybrid-gate-overlay", "style"),
    Input("store-hybrid-slots", "data"),
)
def toggle_gate_overlay(slots):
    base_style = {
        "position": "absolute", "top": "0", "left": "0",
        "width": "100%", "height": "100%",
        "backgroundColor": "rgba(255,255,255,0.85)",
        "zIndex": "10",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
    }
    gate_open = all(v is not None for v in (slots or {}).values()) and len(slots or {}) == 5
    base_style["display"] = "none" if gate_open else "flex"
    return base_style
```

### Pattern 5: Hybrid DataFrame Construction from Slot Selections
**What:** Given the 5 slot selections (equipment names), look up each item's row from the combined data pool (miscellaneous + mechanical + electrical) and build a hybrid DataFrame with the same columns as other system DataFrames.
**When to use:** Whenever the slot store changes and gate is open — feed this DataFrame to all scorecard and chart computations.
**Example:**
```python
# In processing.py
def compute_hybrid_df(slots: dict, data: dict) -> pd.DataFrame | None:
    """Build a hybrid DataFrame from 5 slot selections.

    Parameters
    ----------
    slots : dict
        {"Water Extraction": "Piston pump", ..., "Desalination": "2 RO membranes in parallel"}
    data : dict
        Full data dict from load_data().

    Returns
    -------
    pd.DataFrame or None
        5-row DataFrame (one per stage) with EQUIPMENT_COLUMNS, or None if gate not met.
    """
    if not all(v for v in slots.values()):
        return None

    # Pool: miscellaneous first (natural home), then mechanical, then electrical
    search_order = ["miscellaneous", "mechanical", "electrical"]
    rows = []
    for stage, equipment_name in slots.items():
        for source_key in search_order:
            df = data.get(source_key, pd.DataFrame())
            match = df[df["name"] == equipment_name]
            if not match.empty:
                rows.append(match.iloc[0].to_dict())
                break

    if len(rows) != 5:
        return None
    return pd.DataFrame(rows, columns=["name", "quantity", "cost_usd",
                                        "energy_kw", "land_area_m2", "lifespan_years"])
```

### Pattern 6: Dynamic Scorecard via Callback
**What:** The scorecard `html.Div` gets an `id="scorecard-container"`. A new callback in `scorecard.py` takes `store-hybrid-slots` as Input and outputs updated `scorecard-container` children with the 3-system table (including hybrid column when gate is open).
**When to use:** Any layout element that must update reactively when Dash store changes.
**Example:**
```python
# In scorecard.py — new callback for dynamic update
from dash import callback, Input, Output
from src.layout.shell import _data as shell_data  # or pass via set_data()

@callback(
    Output("scorecard-container", "children"),
    Input("store-hybrid-slots", "data"),
)
def update_scorecard(slots):
    """Rebuild scorecard table when hybrid slot store changes."""
    # Access module-level data (same set_data() pattern as charts.py)
    mechanical_df = _data["mechanical"]
    electrical_df = _data["electrical"]
    hybrid_df = compute_hybrid_df(slots, _data) if slots else None
    return make_scorecard_table(mechanical_df, electrical_df, hybrid_df).children
```

### Pattern 7: Equipment Pool for Dropdowns (Config Fix Required)
**What:** Build `dcc.Dropdown` options per stage by filtering the equipment pool to items assigned to that stage in `PROCESS_STAGES`. The pool is primarily miscellaneous, but Desalination requires items from mechanical/electrical.
**When to use:** Building dropdown options at layout-render time (static options, not callback-driven).
**Example:**
```python
# In config.py — extend miscellaneous to include Desalination items
PROCESS_STAGES = {
    ...
    "miscellaneous": {
        "Water Extraction": ["Piston pump"],
        "Pre-Treatment":    ["Antiscalant (assuming 3g/L of antiscalant)"],
        "Desalination":     [            # ADD THIS — currently empty
            "2 RO membranes in parallel",  # from mechanical
            "RO membranes in parallel",     # from electrical
            "Gear and Booster Pump",        # from mechanical
            "Booster Pump",                 # from electrical
        ],
        "Post-Treatment": [
            "Green blend addition",
            "Activated carbon (annual)",
            "55 gallon container is 2500 USD, for 1 million gal/day lasts about 20 days",
        ],
        "Brine Disposal": ["Evaporation Pond"],
    },
}

# In hybrid_builder.py — build dropdown options per stage
def _build_dropdown_options(stage: str, data: dict) -> list[dict]:
    """Return dropdown options for a given stage from the equipment pool."""
    pool = PROCESS_STAGES.get("miscellaneous", {}).get(stage, [])
    # Search miscellaneous + mechanical + electrical DataFrames
    all_dfs = {
        k: data[k] for k in ["miscellaneous", "mechanical", "electrical"]
    }
    options = []
    seen = set()
    for item_name in pool:
        if item_name in seen:
            continue
        for df in all_dfs.values():
            if item_name in df["name"].values:
                options.append({"label": item_name, "value": item_name})
                seen.add(item_name)
                break
    return options
```

### Pattern 8: Comparison Description Text Generation (SCORE-03)
**What:** Generate factual percentage comparison sentences for all 3 scorecard metrics (cost, land area, efficiency). Output is a string or html.P rendered below the scorecard table.
**When to use:** After gate opens; updates whenever hybrid configuration changes.
**Example:**
```python
# In processing.py — add generate_comparison_text()
def generate_comparison_text(
    hybrid_metrics: dict,
    mech_metrics: dict,
    elec_metrics: dict,
) -> str:
    """Generate factual percentage comparison sentences for SCORE-03.

    Returns a multi-sentence string comparing hybrid against both presets.
    """
    lines = []
    metric_labels = {
        "cost": "cost",
        "land_area": "land area",
        "efficiency": "energy use",
    }
    for metric, label in metric_labels.items():
        h = hybrid_metrics.get(metric)
        m = mech_metrics.get(metric)
        e = elec_metrics.get(metric)
        if h and m:
            pct = abs(h - m) / m * 100
            direction = "less" if h < m else "more"
            lines.append(f"Hybrid has {pct:.0f}% {direction} {label} than Mechanical.")
        if h and e:
            pct = abs(h - e) / e * 100
            direction = "less" if h < e else "more"
            lines.append(f"Hybrid has {pct:.0f}% {direction} {label} than Electrical.")
    return " ".join(lines)

# Example output (verified with real data):
# "Hybrid has 25% less cost than Mechanical. Hybrid has 42% less cost than Electrical.
#  Hybrid has 99% more land area than Mechanical. Hybrid has 99% more land area than Electrical.
#  Hybrid has 31% less energy use than Mechanical. Hybrid has 26% less energy use than Electrical."
```

### Pattern 9: Hybrid Equipment Detail View (HYB-04)
**What:** When gate is open, show the 5 selected equipment items in an accordion (same `_make_accordion_item` pattern from `equipment_grid.py`). Each item is clickable to see its detail data. System key passed to accordion items is "miscellaneous" for items sourced from that sheet, or "mechanical"/"electrical" for RO membrane items.
**When to use:** After gate opens in the Hybrid tab equipment section.
**Example:**
```python
# In equipment_grid.py — modify make_equipment_section() for hybrid case
def make_equipment_section(df, system, all_data):
    if system == "hybrid":
        # Phase 4: hybrid_df comes from slot selections
        # (passed via all_data["hybrid"] or constructed at call site)
        hybrid_df = all_data.get("hybrid_selected")
        if hybrid_df is None:
            return html.Div(html.P("Fill all 5 slots to see equipment details.", className="text-muted"))
        # Reuse existing accordion pattern — one stage section per slot
        sections = []
        for idx, row in hybrid_df.iterrows():
            item = _make_accordion_item(row, "miscellaneous", idx, all_data)
            sections.append(item)
        return html.Div([
            html.H5("Hybrid System Equipment"),
            dbc.Accordion(sections, always_open=False, active_item=None),
        ])
    ...
```

### Anti-Patterns to Avoid
- **Building dropdown options inside a callback:** Options are static (data loaded at startup). Build them in `make_hybrid_builder()` at layout time, not in a callback. This avoids a callback that fires on every page load.
- **Putting hybrid-builder callbacks in system_view.py:** Keep the hybrid builder self-contained in `hybrid_builder.py`. system_view.py only imports `make_hybrid_builder()` and calls it when `active_system == "hybrid"`. Callbacks live in the module that owns the components.
- **Writing store-hybrid-slots from multiple callbacks:** Only one callback should write the slot store — the `update_slot_store` callback that reads all 5 dropdowns. The Clear All button resets dropdown values (not the store directly) to let it cascade through the existing callback. This prevents competing writes.
- **Reusing chart-section IDs in the hybrid tab:** The chart section (`chart-cost`, `chart-land`, etc.) already exists on the page for Mechanical/Electrical tabs. The Hybrid tab must share these same component IDs (since `make_chart_section()` is already called by system_view.py). Do NOT create a separate chart section for the Hybrid tab — the existing charts update via the store. The hybrid tab overlay is added around the existing chart section when viewing the hybrid tab.
- **Computing hybrid DataFrame inside the update_charts callback:** Keep compute_hybrid_df() in processing.py. Call it once in the callback and pass the result to both the scorecard and chart data functions. Don't recompute in each.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dropdown component | Custom HTML select | `dcc.Dropdown` | Handles value state, clearable, placeholder, accessibility |
| Equipment lookup by name | Linear search each time | Build name→row lookup dict at startup | Avoid iterating DataFrames per callback tick |
| Percentage calculation | Custom formula | Standard Python arithmetic with None guards | Simple; just need abs(h-m)/m * 100 |
| Overlay visibility | CSS class toggling | Inline style dict returned from callback | Consistent with existing project style pattern (badge dimming in charts.py) |
| Stage → equipment mapping | Rebuild from DataFrame iteration | `PROCESS_STAGES["miscellaneous"]` dict | Already exists; just extend with Desalination items |

**Key insight:** The entire hybrid data pipeline (slot store → hybrid DataFrame → scorecard metrics → chart data → figures) must complete in <100ms per selection. The bottleneck is DataFrame lookup — pre-build a name→row lookup dict at module level, not inside the callback.

---

## Common Pitfalls

### Pitfall 1: Desalination Stage Has No Miscellaneous Equipment
**What goes wrong:** The `PROCESS_STAGES["miscellaneous"]["Desalination"]` list is empty. The Desalination dropdown renders with no options. The gate can never open.
**Why it happens:** The data.xlsx miscellaneous section contains no desalination-specific equipment. The stage gap was present in config.py from Phase 2 (the miscellaneous key was added for Phase 4 readiness but the Desalination stage was left empty).
**How to avoid:** Add `"Desalination": ["2 RO membranes in parallel", "RO membranes in parallel", "Gear and Booster Pump", "Booster Pump"]` to `PROCESS_STAGES["miscellaneous"]` in `config.py`. These items exist in the mechanical/electrical DataFrames and `compute_hybrid_df()` already searches those when looking up by name.
**Warning signs:** Desalination dropdown renders with no options at all.

### Pitfall 2: Multiple Callbacks Writing to store-hybrid-slots
**What goes wrong:** The Clear All button callback writes `{"Water Extraction": None, ...}` directly to the store, AND the 5-dropdown callback also writes to the store. Both can fire in sequence when Clear All is clicked (button resets dropdowns → dropdown change fires the slot callback → two writes in rapid succession).
**Why it happens:** Trying to write the store from multiple sources.
**How to avoid:** Clear All button ONLY sets dropdown values to None (outputs to `slot-dd-*` `value` props). The dropdowns changing then fires `update_slot_store` which writes the store once. One writer, one path. Never have the Clear All button output to the store directly.
**Warning signs:** Dash warns about `allow_duplicate` or slots reset to wrong values.

### Pitfall 3: chart-section Component IDs Conflict Across Tabs
**What goes wrong:** `make_chart_section()` is called once in `system_view.py` and produces IDs like `chart-cost`, `chart-land`, `store-legend-visibility`. If the hybrid tab calls `make_chart_section()` again, duplicate IDs crash Dash.
**Why it happens:** The same layout factory called more than once creates duplicate component IDs.
**How to avoid:** `make_chart_section()` is only called ONCE in `create_system_view_layout()` (it's already there). The hybrid tab shares the same chart section. The hybrid overlay wraps the existing chart output area. Do not call `make_chart_section()` again in `hybrid_builder.py`.
**Warning signs:** Dash raises `DuplicateIdError` or `ValueError: Duplicate component id found` at startup.

### Pitfall 4: Gate Overlay Blocks Chart Interaction Permanently
**What goes wrong:** The overlay div has `zIndex: 10` and remains in the DOM when gate opens, but `display: none` style is not properly applied. Charts become unclickable/unhoverable.
**Why it happens:** CSS `display: none` not applied (callback missed, or style dict not fully replaced).
**How to avoid:** The callback must return the COMPLETE style dict, not a partial update. Include `display: "none"` when gate is open, `display: "flex"` when closed. Do not use `dash.no_update` when toggling — always return the full style dict.
**Warning signs:** Charts render but hover/click does not work even when all 5 slots are filled.

### Pitfall 5: Hybrid DataFrame Cost Sum Skips Non-Numeric Costs
**What goes wrong:** Some miscellaneous items have non-numeric `cost_usd` values (e.g., `"$50000/year"` for Antiscalant, `"$ 2500 per ton"` for Activated carbon). `pd.to_numeric(..., errors='coerce')` returns NaN for these, so the hybrid cost total excludes them. The scorecard shows an understated cost.
**Why it happens:** The existing `_aggregate()` pattern in `compute_scorecard_metrics` uses `pd.to_numeric(errors='coerce')` which silently drops non-numeric values. Same behavior as mechanical/electrical (those also have some "N/A" cells) but miscellaneous has more non-numeric cost entries.
**How to avoid:** Accept this behavior (it matches the existing pattern for mechanical/electrical). Document in comments that non-numeric costs are excluded from aggregates. This is a data quality limitation, not a code bug. The comparison text will still be factually accurate for the costs it can compute.
**Warning signs:** Hybrid total cost seems lower than expected when Antiscalant or Activated carbon is selected.

### Pitfall 6: Scorecard Callback Circular Dependency
**What goes wrong:** `update_scorecard` callback outputs to `scorecard-container` children. `create_system_view_layout` also populates `scorecard-container` children at render time. Dash may complain if the same Output is set both by a callback and by the layout.
**Why it happens:** Initial layout value + callback Output on the same component.
**How to avoid:** The initial layout sets `scorecard-container` children to the 2-system table (mechanical + electrical only, no hybrid) — this is the default. The callback fires on first load (triggered by `store-hybrid-slots` initial value of all-None) and re-renders the same 2-system table. This is fine — the callback is the authoritative source and overwrites the initial value. Add `prevent_initial_call=False` (default) so the first callback fire syncs the scorecard to the store state.
**Warning signs:** Scorecard flashes on first load, or the hybrid column appears before any slot is filled.

---

## Code Examples

Verified patterns from codebase inspection and live data:

### Slot Store Definition
```python
# In hybrid_builder.py — mirrors store-legend-visibility pattern from charts.py
from dash import dcc

SLOT_STAGES = [
    "Water Extraction",
    "Pre-Treatment",
    "Desalination",
    "Post-Treatment",
    "Brine Disposal",
]

def make_slot_store() -> dcc.Store:
    return dcc.Store(
        id="store-hybrid-slots",
        data={stage: None for stage in SLOT_STAGES},
    )
```

### Pipeline Builder Layout
```python
# In hybrid_builder.py — horizontal pipeline with arrows, responsive wrapping
from dash import html, dcc
import dash_bootstrap_components as dbc

_ARROW = html.Span("→", className="align-self-center mx-1 text-muted fs-4")

def make_hybrid_builder(data: dict) -> html.Div:
    slot_cols = []
    for i, stage in enumerate(SLOT_STAGES):
        options = _build_dropdown_options(stage, data)
        slot_cols.append(
            html.Div(
                [
                    html.Label(stage, className="small fw-bold text-muted mb-1"),
                    dcc.Dropdown(
                        id=f"slot-dd-{stage.lower().replace(' ', '-')}",
                        options=options,
                        value=None,
                        placeholder="Select...",
                        clearable=True,
                        style={"minWidth": "160px"},
                    ),
                ],
                className="flex-shrink-0",
            )
        )
        if i < len(SLOT_STAGES) - 1:
            slot_cols.append(_ARROW)  # Arrow between stages

    return html.Div([
        make_slot_store(),
        html.H5("Hybrid System Builder", className="mb-3"),
        # Slot counter and Clear All button
        html.Div(
            [
                html.Span(id="slot-counter", children="0/5 slots filled", className="text-muted small me-3"),
                dbc.Button("Clear All", id="btn-clear-all", size="sm", color="secondary", outline=True),
            ],
            className="mb-2 d-flex align-items-center",
        ),
        # Pipeline row
        html.Div(
            slot_cols,
            className="d-flex flex-wrap align-items-start gap-1 mb-4",
            style={"rowGap": "1rem"},
        ),
    ])
```

### Slot Counter Update
```python
# In hybrid_builder.py — updates the "X/5 slots filled" counter
@callback(
    Output("slot-counter", "children"),
    Input("store-hybrid-slots", "data"),
)
def update_slot_counter(slots):
    if not slots:
        return "0/5 slots filled"
    filled = sum(1 for v in slots.values() if v is not None)
    return f"{filled}/5 slots filled"
```

### charts.py Modification — Add hybrid_slots Input
```python
# In charts.py — extend update_charts to accept hybrid slots
@callback(
    Output("chart-cost",    "figure"),
    Output("chart-land",    "figure"),
    Output("chart-turbine", "figure"),
    Output("chart-pie",     "figure"),
    Output("label-years",           "children"),
    Output("label-battery-ratio",   "children"),
    Output("label-elec-cost",       "children"),
    Input("slider-time-horizon",    "value"),
    Input("slider-battery",         "value"),
    Input("store-legend-visibility","data"),
    Input("store-hybrid-slots",     "data"),   # NEW in Phase 4
)
def update_charts(years, battery_fraction, visibility, hybrid_slots):
    if _data is None:
        empty = go.Figure()
        return empty, empty, empty, empty, "", "", ""

    # Build hybrid_df if gate is open
    from src.data.processing import compute_hybrid_df
    hybrid_df = compute_hybrid_df(hybrid_slots, _data) if hybrid_slots else None

    cd = compute_chart_data(_data, battery_fraction, years, hybrid_df=hybrid_df)
    ...
```

### compute_chart_data Modification
```python
# In processing.py — extend compute_chart_data to accept hybrid_df
def compute_chart_data(
    data: dict,
    battery_fraction: float = 0.5,
    years: int = 50,
    hybrid_df=None,          # NEW — pd.DataFrame or None
) -> dict:
    ...
    # Replace TODO Phase 4 placeholders:
    if hybrid_df is not None:
        hybrid_cumulative = compute_cost_over_time(hybrid_df, years)
        hybrid_land  = float(pd.to_numeric(hybrid_df["land_area_m2"], errors="coerce").sum())
        hybrid_energy = _energy_by_stage(hybrid_df, "miscellaneous")
        # Turbine count: look for turbine-type equipment in hybrid slots
        hybrid_turbines = 0  # miscellaneous items don't include turbines
    else:
        hybrid_cumulative = np.zeros(years + 1)
        hybrid_land  = 0.0
        hybrid_energy = {}
        hybrid_turbines = 0
    ...
```

### Verified Slot Data Coverage
```
Stage             | Miscellaneous items available
------------------|------------------------------
Water Extraction  | Piston pump  (1 item)
Pre-Treatment     | Antiscalant (assuming 3g/L...) (1 item)
Desalination      | NONE in miscellaneous → add to config.py from mech/elec:
                  |   2 RO membranes in parallel (mechanical)
                  |   RO membranes in parallel (electrical)
                  |   Gear and Booster Pump (mechanical)
                  |   Booster Pump (electrical)
Post-Treatment    | Green blend addition, Activated carbon (annual),
                  | 55 gallon container... (3 items)
Brine Disposal    | Evaporation Pond (1 item)

NOTE: "Multi-Media Filtration" is in config.py PROCESS_STAGES["miscellaneous"]["Pre-Treatment"]
but is NOT in the actual miscellaneous sheet data — it is in the electrical sheet.
This item should be removed from the miscellaneous config or left (it will simply
not appear as an option since the lookup finds 0 matches in miscellaneous).
Resolution: Remove "Multi-Media Filtration" from PROCESS_STAGES["miscellaneous"]["Pre-Treatment"].
```

### Scorecard 3-Column Expansion
```python
# In scorecard.py — modify make_scorecard_table to accept optional hybrid_df
def make_scorecard_table(
    mechanical_df: pd.DataFrame,
    electrical_df: pd.DataFrame,
    hybrid_df: pd.DataFrame | None = None,   # NEW
) -> html.Div:
    metrics = compute_scorecard_metrics(mechanical_df, electrical_df, hybrid_df)
    # metrics now has optional "hybrid" key

    # Table header: add Hybrid column when hybrid_df is not None
    header_cells = [html.Th("Metric"), html.Th("Mechanical", style={"textAlign": "center"}), html.Th("Electrical", style={"textAlign": "center"})]
    if hybrid_df is not None:
        header_cells.append(html.Th("Hybrid", style={"textAlign": "center"}))

    # ... build rows with optional hybrid column, same RAG dot pattern
    # rag_color() already handles 3-system ranking (green/yellow/red)
    ...
```

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| Hybrid tab shows empty-state placeholder (Phase 3 pattern) | Phase 4: Replace with hybrid builder UI | `equipment_grid.py` hybrid case rewritten; `system_view.py` renders builder |
| Scorecard static at layout-render time | Dynamic scorecard via callback on store-hybrid-slots | Add `scorecard-container` id; move scorecard rendering into a callback Output |
| `compute_chart_data()` returns hybrid zeros unconditionally | `compute_chart_data()` accepts `hybrid_df` param; returns real data when provided | Removes all `# TODO Phase 4` comments; hybrid trace shows real data |
| `compute_scorecard_metrics(mech, elec)` — 2 args | `compute_scorecard_metrics(mech, elec, hybrid=None)` — optional 3rd | `rag_color()` already handles 3 systems; just pass the hybrid values |

**Existing TODO comments to resolve (confirmed in codebase):**
- `processing.py` lines: `# TODO Phase 4: replace with actual hybrid system data` (3 locations: cumulative, land, turbines, energy)
- `equipment_grid.py`: `if system == "hybrid": return html.Div([...placeholder...])` — replace with real builder
- `system_view.py`: `scorecard = make_scorecard_table(data["mechanical"], data["electrical"])` — add hybrid_df

---

## Open Questions

1. **Desalination Dropdown: How many options to show?**
   - What we know: 4 Desalination items across mechanical/electrical (2 RO membrane variants, 2 pump variants). Adding all 4 to config gives the student real choices.
   - What's unclear: Are all 4 valid for a hybrid system, or should only 1-2 be offered?
   - Recommendation: Add all 4 to `PROCESS_STAGES["miscellaneous"]["Desalination"]`. Students pick whichever RO/pump combination they want for their hybrid. This matches the educational intent (compare different configurations).

2. **Hybrid Turbine Count in Bar Chart**
   - What we know: The miscellaneous pool has no turbines. A hybrid system built from miscellaneous items will show 0 turbines in the Wind Turbine Count chart.
   - What's unclear: Is 0 turbines accurate (the hybrid may use wind power indirectly) or misleading?
   - Recommendation: Leave turbine count as 0 for hybrid. The hybrid is a custom assembly; if no turbine is in the slot selection, the count is 0 by definition. Add a note in the chart or tooltip if needed.

3. **Activated Carbon Cost ("$ 2500 per ton") and Antiscalant ("$50000/year") as Non-Numeric**
   - What we know: These costs are non-numeric strings and will be excluded from the hybrid cost aggregate by `pd.to_numeric(errors='coerce')`. This is the same behavior as other non-numeric costs in the dataset.
   - What's unclear: Should Phase 4 add special handling to estimate these costs, or is it acceptable to show "N/A" / 0 for them?
   - Recommendation: Accept the existing behavior. Document with a comment in `compute_hybrid_df()`. The educational value is not diminished — students see the numeric costs for the items that can be computed.

---

## Sources

### Primary (HIGH confidence)
- Live codebase inspection — `src/config.py`, `src/data/processing.py`, `src/layout/charts.py`, `src/layout/scorecard.py`, `src/layout/equipment_grid.py`, `src/layout/system_view.py`, `app.py`
- Live data run (`python -c "from src.data.loader import load_data; ..."`) — confirmed miscellaneous equipment names, stages, costs, slot coverage
- Installed package versions confirmed: Dash 4.0.0, DBC 2.0.4, plotly 6.5.2, pandas 2.3.3, numpy 2.3.5
- Dash 4.0 docs (dash.plotly.com/dash-core-components/dropdown) — dcc.Dropdown props (options, value, clearable, placeholder)

### Secondary (MEDIUM confidence)
- Dash 4.0 docs (dash.plotly.com/basic-callbacks) — multiple Input callback pattern (5 dropdowns → 1 store)
- Dash 4.0 docs (dash.plotly.com/interactive-graphing) — pattern-matching callbacks (ALL) vs explicit Inputs

### Tertiary (LOW confidence)
- CSS absolute positioning overlay pattern — standard CSS; not Dash-specific

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages already installed and verified importable
- Architecture: HIGH — all patterns verified against existing codebase; slot schema and gate pattern verified by running Python against live data
- Data coverage (slot options per stage): HIGH — directly inspected data.xlsx via loader, compared against config.py PROCESS_STAGES
- Pitfalls: HIGH — identified by code inspection; Pitfall 1 (Desalination gap) verified with live data run
- Comparison text generation: HIGH — prototype function verified with live scorecard metric values

**Research date:** 2026-02-22
**Valid until:** 2026-03-22 (stable Dash 4.0 + plotly 6.5.2 APIs; data.xlsx format fixed)
