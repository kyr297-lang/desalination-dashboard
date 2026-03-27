# Phase 3: Comparison Charts and Electrical Slider - Research

**Researched:** 2026-02-21
**Domain:** Plotly graph_objects, Dash callbacks, dcc.Slider, chart layout
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Chart layout & arrangement**
- 2x2 grid layout, all four charts visible at once
- All charts equal size in the grid
- Grid position: Cost over time (top-left), Land area (top-right), Wind turbines (bottom-left), Energy pie (bottom-right)
- Same page as scorecard, below it — no separate tab
- Section heading: "System Comparison" to separate charts from scorecard above
- Each chart has a bold title and a one-line description of what it shows
- Charts in card containers with white background, shadow/border — matching existing scorecard card style
- Clean dashboard aesthetic (modern, card-based containers with subtle borders)
- Responsive layout — reflows to single column on narrow screens
- Shared legend above the chart grid showing all system colors
- Clicking a system name in the shared legend toggles that system's visibility across all four charts

**Control panel**
- Both sliders (time horizon + battery/tank) in a distinct control panel above the chart grid
- Control panel has light background or subtle border to visually group controls
- Both sliders arranged side by side within the control panel
- Both sliders have same visual style for consistency
- Each slider has a label AND short help text explaining what it does

**Battery/tank slider interaction**
- Free movement with interpolation between the 11 lookup table rows (not snapping to discrete positions)
- Live ratio label showing percentages: "70% Battery / 30% Tank" — percentages only, no unit counts
- No endpoint labels — ratio label is sufficient
- Charts update instantly on drag (real-time)
- Default starting position: middle (50/50)
- No reset button — students drag back to middle themselves
- No visual highlight on affected charts — charts update silently
- Live total cost readout for the electrical system displayed next to the slider, updating in real time

**Time horizon slider**
- Slider control (matching battery/tank slider style)
- Range: 1 to 50 years
- Default: 50 years
- 1-year step increments
- Live year label (e.g., "25 years") updating as user drags
- Cost-over-time chart X-axis adjusts to only show up to the selected horizon year
- Cost shown as cumulative (running total from year 1 to selected year)

**Chart detail & style**
- Tooltips on cost-over-time: system name + dollar amount (e.g., "Mechanical: $45.2K at Year 5")
- Bar charts: values on hover only (no labels on bars)
- Energy breakdown: 3 pie charts side by side (one per system), not a single pie with selector
- Each pie has system name as subtitle below it
- Pie chart slices: hover only for percentage labels (no labels on slices)
- Smooth animation transitions when data updates (slider moves)
- Dollar values abbreviated for large numbers (e.g., "$45.2K")
- Cost-over-time lines: smooth lines without data point markers
- Cost-over-time shows cumulative cost per year

### Claude's Discretion
- Color strategy: system colors vs per-chart palette — Claude picks based on visual clarity
- Bar chart width/spacing — Claude picks appropriate sizing
- Exact animation duration and easing
- Chart padding and internal margins
- Tooltip positioning and styling details

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CHART-01 | Cost over time line chart comparing all three systems side-by-side | go.Scatter with mode='lines', cumulative cost via numpy.cumsum + lifespan replacement cycles; x-axis truncated by time horizon slider |
| CHART-02 | User can select time horizon for cost-over-time chart (slider or input) | dcc.Slider(min=1, max=50, step=1, updatemode='drag'); callback reads value and rebuilds line chart x-range |
| CHART-03 | Land area grouped bar chart comparing all three systems | go.Bar with barmode='group'; one trace per system; Hybrid shows 0 until Phase 4 |
| CHART-04 | Wind turbine count grouped bar chart comparing all three systems | go.Bar with barmode='group'; Mechanical qty=4 turbines, Electrical qty=1 turbine, Hybrid=0 placeholder |
| CHART-05 | Pie chart showing energy percentage by action per system | 3x go.Pie traces side by side using domain positioning; textinfo='none', hoverinfo='label+percent' |
| CTRL-01 | Battery/tank tradeoff slider maps to 11-row lookup table | dcc.Slider(min=0, max=1, step=None); numpy.interp() against battery_lookup DataFrame for continuous interpolation |
| CTRL-02 | Slider updates electrical system cost and all related charts in real-time | Single callback with updatemode='drag' on both sliders; outputs all four dcc.Graph figures + live labels |
| VIS-03 | All charts have labeled axes with units, hover tooltips with formatted values | xaxis_title/yaxis_title on go.Layout; hovertemplate on each trace using fmt_cost pattern |
</phase_requirements>

---

## Summary

Phase 3 builds on the existing Dash + Bootstrap foundation. The project already has `plotly==6.5.2` and `numpy==2.3.5` installed alongside `dash==4.0.0` and `dash-bootstrap-components==2.0.4` — no new packages are needed. All charts use `plotly.graph_objects` (not Plotly Express) to maintain the same low-level control pattern established in previous phases.

The most critical architectural decision is how to handle the shared legend toggle across four separate `dcc.Graph` components. Research confirms that Plotly's built-in `legendgroup` only synchronizes within a single figure — not across multiple figures. The correct approach is a `dcc.Store("legend-visibility")` holding a dict `{system_key: bool}`, updated by a callback listening to any graph's `restyleData`, which then propagates visibility to all four graph outputs. This is the only pattern that reliably syncs visibility across separate graph components.

The battery/tank slider uses `numpy.interp()` against the 11-row battery_lookup DataFrame for smooth continuous interpolation. The cost-over-time calculation uses equipment `lifespan_years` to model replacement cycles (an item replaced at year 0, then every N years thereafter), with cumulative costs built via `numpy.cumsum`. The existing `fmt_cost()` helper in `processing.py` covers dollar abbreviation for tooltips.

**Primary recommendation:** Build a single `charts.py` module in `src/layout/` containing all four figure-building functions plus a `compute_chart_data()` function in `src/data/processing.py`. Wire everything through one master callback that takes both slider values and the legend visibility store as inputs, and outputs all four figures plus the live labels.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| plotly | 6.5.2 (installed) | Build all four chart figures | Already a Dash dependency; graph_objects gives full API control |
| dash | 4.0.0 (installed) | dcc.Slider, dcc.Graph, dcc.Store, callbacks | Project foundation |
| numpy | 2.3.5 (installed) | numpy.interp() for battery interpolation, numpy.cumsum() for cumulative cost | Fastest path; no extra install |
| dash-bootstrap-components | 2.0.4 (installed) | dbc.Card, dbc.Row, dbc.Col for 2x2 grid layout | Project foundation |
| pandas | 2.3.3 (installed) | Read battery_lookup, equipment DataFrames | Already loaded at startup |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| plotly.subplots.make_subplots | bundled | 3-pie energy chart in single figure | Required for placing 3 pies in one dcc.Graph |
| plotly.graph_objects | bundled | All chart trace construction | Consistent with project style |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| plotly.graph_objects | plotly.express | px is faster to write but offers less control over tooltips, trace properties, and subplot specs. Project already avoids px. |
| dcc.Store for legend sync | restyleData only | restyleData doesn't reset when cleared (known Dash bug #2037) — Store pattern is more reliable |
| numpy.interp | scipy.interpolate | scipy not installed; numpy.interp is sufficient for linear interpolation across 11 points |

**Installation:** No new packages needed. All dependencies already installed.

---

## Architecture Patterns

### Recommended Project Structure
```
src/
├── data/
│   ├── processing.py      # ADD: compute_cost_over_time(), compute_chart_data()
│   └── loader.py          # no changes
├── layout/
│   ├── charts.py          # NEW: build_cost_chart(), build_land_chart(), build_turbine_chart(), build_pie_chart(), make_chart_section()
│   ├── system_view.py     # MODIFY: import and append make_chart_section() below scorecard
│   └── shell.py           # no changes
└── config.py              # no changes (SYSTEM_COLORS already defined)
```

### Pattern 1: Single Master Callback
**What:** One callback takes both sliders + legend visibility store as Inputs, outputs all four figures + two live labels (year label, electrical cost label). This avoids circular dependencies and keeps chart state consistent.
**When to use:** Multiple charts that share the same input sliders — one callback is simpler than four.
**Example:**
```python
# Source: Dash docs - multiple outputs pattern
from dash import callback, Input, Output, State

@callback(
    Output("chart-cost", "figure"),
    Output("chart-land", "figure"),
    Output("chart-turbine", "figure"),
    Output("chart-pie", "figure"),
    Output("label-years", "children"),
    Output("label-elec-cost", "children"),
    Input("slider-time-horizon", "value"),
    Input("slider-battery", "value"),
    Input("store-legend-visibility", "data"),
)
def update_charts(years, battery_fraction, visibility):
    ...
```

### Pattern 2: dcc.Slider with updatemode='drag'
**What:** Both sliders fire callbacks on every drag position, enabling real-time chart updates.
**When to use:** Any slider that needs live-updating labels or chart data.
**Example:**
```python
# Source: https://dash.plotly.com/dash-core-components/slider
dcc.Slider(
    id="slider-battery",
    min=0,
    max=1,
    step=0.001,          # fine-grained for smooth interpolation
    value=0.5,           # default 50/50
    marks={},            # no marks - ratio label replaces them
    tooltip={"always_visible": False},
    updatemode="drag",   # fire on every mouse move
)
```

### Pattern 3: Battery Interpolation via numpy.interp
**What:** Converts a continuous slider value (0.0-1.0) to interpolated cost by reading the 11-row battery_lookup DataFrame.
**When to use:** Any slider that maps to a discrete lookup table with continuous values between.
**Example:**
```python
import numpy as np

def interpolate_battery_cost(battery_fraction: float, battery_lookup_df) -> float:
    """
    Interpolate total storage cost from battery_lookup table.
    battery_fraction: 0.0 (all tank) to 1.0 (all battery)
    Returns interpolated total_cost (battery_cost + tank_cost).
    """
    fractions = battery_lookup_df["battery_fraction"].astype(float).values
    costs = battery_lookup_df["total_cost"].astype(float).values
    return float(np.interp(battery_fraction, fractions, costs))

# Example: slider at 0.35 → interpolated cost = $535,000
```

### Pattern 4: Cumulative Cost Over Time
**What:** For each system, model capital cost at year 0, then re-purchase each equipment item every `lifespan_years`. `numpy.cumsum` over the annual cost array gives cumulative running total.
**When to use:** Cost-over-time line chart (CHART-01/CHART-02).
**Example:**
```python
import numpy as np
import pandas as pd

def compute_cost_over_time(df: pd.DataFrame, years: int = 50,
                            override_costs: dict = None) -> np.ndarray:
    """
    Returns cumulative cost array of length (years+1) for indices 0..years.
    override_costs: dict of {equipment_name: replacement_cost} for battery slider.
    'indefinite' lifespan = year-0 purchase only (no replacement).
    """
    annual = np.zeros(years + 1)
    for _, row in df.iterrows():
        cost = pd.to_numeric(row["cost_usd"], errors="coerce")
        if pd.isna(cost):
            continue
        if override_costs and row["name"] in override_costs:
            cost = override_costs[row["name"]]
        lifespan = row["lifespan_years"]
        if lifespan == "indefinite":
            annual[0] += cost
        else:
            lifespan = int(float(lifespan))
            for yr in range(0, years + 1, lifespan):
                annual[yr] += cost
    return np.cumsum(annual)

# Verified output: Year 50 Mechanical ~$79.4M, Electrical (50/50) ~$82.7M
```

### Pattern 5: Shared Legend via dcc.Store + restyleData
**What:** A `dcc.Store("store-legend-visibility")` holds `{"mechanical": true, "electrical": true, "hybrid": true}`. A separate callback reads any graph's `restyleData` to detect legend toggles and updates the store. The master chart callback reads the store and sets `visible=True` or `visible="legendonly"` on traces.
**When to use:** When clicking a legend item on one chart must hide the same system on all four charts.
**Example:**
```python
# Source: Plotly community pattern - store-based sync
@callback(
    Output("store-legend-visibility", "data"),
    Input("chart-cost", "restyleData"),
    State("store-legend-visibility", "data"),
    prevent_initial_call=True,
)
def sync_legend(restyle_data, current_visibility):
    """Update visibility store when user toggles a legend item on any chart."""
    if restyle_data is None:
        return current_visibility
    # restyleData format: [{"visible": ["legendonly"]}, [trace_index]]
    edits, indices = restyle_data
    # Map trace index back to system key (order: mechanical=0, electrical=1, hybrid=2)
    system_order = ["mechanical", "electrical", "hybrid"]
    for idx in indices:
        if idx < len(system_order):
            new_vis = edits.get("visible", [None])[0]
            current_visibility[system_order[idx]] = (new_vis is True or new_vis is None)
    return current_visibility

# In build_cost_chart(), apply stored visibility:
# trace.update(visible=True if visibility["mechanical"] else "legendonly")
```

### Pattern 6: Three Pie Charts Side by Side in One Figure
**What:** Three `go.Pie` traces with domain positioning in one figure. `textinfo='none'` hides slice labels. `hovertemplate` shows label + percent.
**When to use:** Energy breakdown chart (CHART-05) — one pie per system.
**Example:**
```python
import plotly.graph_objects as go

def build_pie_chart(mech_energy, elec_energy, hybrid_energy, visibility):
    fig = go.Figure()
    spacing = 0.02
    width = (1 - 2 * spacing) / 3

    systems = [
        ("Mechanical", mech_energy, 0),
        ("Electrical", elec_energy, 1),
        ("Hybrid",     hybrid_energy, 2),
    ]
    for label, energy_dict, i in systems:
        x_start = i * (width + spacing)
        x_end = x_start + width
        vis = True if visibility.get(label.lower(), True) else "legendonly"
        fig.add_trace(go.Pie(
            labels=list(energy_dict.keys()),
            values=list(energy_dict.values()),
            name=label,
            domain=dict(x=[x_start, x_end], y=[0.1, 1.0]),
            textinfo="none",           # no labels on slices
            hovertemplate="%{label}: %{percent}<extra></extra>",
            showlegend=False,          # shared legend handled separately
            visible=vis,
        ))
    # Annotations for system subtitles below each pie
    fig.update_layout(
        annotations=[
            dict(text="Mechanical", x=width/2, y=0.05, showarrow=False),
            dict(text="Electrical",  x=width + spacing + width/2, y=0.05, showarrow=False),
            dict(text="Hybrid",      x=2*(width+spacing) + width/2, y=0.05, showarrow=False),
        ]
    )
    return fig
```

### Pattern 7: 2x2 Chart Grid Layout
**What:** Four `dbc.Card` components each containing a `dcc.Graph`, arranged in a `dbc.Row` with two `dbc.Col(width=6)` per row. `dbc.Row` x2 stacked.
**When to use:** The 2x2 chart grid.
**Example:**
```python
def make_chart_section():
    def chart_card(title, description, graph_id):
        return dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Strong(title),
                    html.P(description, className="text-muted small mb-1"),
                    dcc.Graph(id=graph_id, config={"displayModeBar": False}),
                ])
            ], className="shadow-sm h-100"),
            width=6, className="mb-3",
        )
    return html.Div([
        html.H5("System Comparison", className="mt-4 mb-2"),
        # control panel ...
        dbc.Row([
            chart_card("Cost Over Time", "Cumulative capital cost per year", "chart-cost"),
            chart_card("Land Area", "Total footprint per system (m²)", "chart-land"),
        ]),
        dbc.Row([
            chart_card("Wind Turbine Count", "Number of turbines per system", "chart-turbine"),
            chart_card("Energy Breakdown", "Energy use by process stage (kW)", "chart-pie"),
        ]),
    ])
```

### Pattern 8: Shared Legend Component (HTML-based)
**What:** A row of clickable badges/buttons above the chart grid, one per system, using system SYSTEM_COLORS. Clicking a badge fires a callback that toggles the store — separate from Plotly's built-in legend. This is more reliable than wiring all four charts' restyleData.
**When to use:** When the user decision requires "shared legend above the chart grid."
**Recommendation:** Build a custom HTML legend row (not relying on Plotly's in-chart legend) with clickable `dbc.Badge` or `html.Span` elements per system. Each click toggles the visibility store. Charts are then rebuilt with correct `visible` values from the store.
**Example:**
```python
# Custom legend row
html.Div([
    html.Strong("Systems: ", className="me-2"),
    dbc.Badge(
        "Mechanical", id="legend-btn-mechanical",
        color="primary", style={"cursor": "pointer", "backgroundColor": SYSTEM_COLORS["Mechanical"]},
        className="me-2",
    ),
    dbc.Badge(
        "Electrical", id="legend-btn-electrical",
        color="warning", style={"cursor": "pointer", "backgroundColor": SYSTEM_COLORS["Electrical"]},
        className="me-2",
    ),
    dbc.Badge(
        "Hybrid", id="legend-btn-hybrid",
        color="success", style={"cursor": "pointer", "backgroundColor": SYSTEM_COLORS["Hybrid"]},
    ),
], className="mb-3")

# Toggle callback
@callback(
    Output("store-legend-visibility", "data"),
    Input("legend-btn-mechanical", "n_clicks"),
    Input("legend-btn-electrical", "n_clicks"),
    Input("legend-btn-hybrid", "n_clicks"),
    State("store-legend-visibility", "data"),
    prevent_initial_call=True,
)
def toggle_legend_system(n_mech, n_elec, n_hybrid, visibility):
    triggered_id = ctx.triggered_id
    key_map = {
        "legend-btn-mechanical": "mechanical",
        "legend-btn-electrical": "electrical",
        "legend-btn-hybrid": "hybrid",
    }
    key = key_map.get(triggered_id)
    if key:
        visibility[key] = not visibility[key]
    return visibility
```

### Anti-Patterns to Avoid
- **Calling load_data() inside a callback:** Project decision — data loaded at module level only. Access via `_data` set by `set_data()`.
- **Depending on Plotly's in-chart legendgroup for cross-figure sync:** Only works within one figure. Known to have inconsistent behavior in subplots (issue #4946). Use store-based toggle instead.
- **Relying on restyleData alone for legend state:** restyleData is not cleared when selection resets (Dash bug #2037). Store-based toggle is authoritative.
- **Using make_subplots for the 2x2 grid:** The 2x2 layout uses separate dcc.Graph components (one per card), not subplots in a single figure. make_subplots IS used inside build_pie_chart() for 3 pies in one figure.
- **Heavy callback per slider tick:** The master callback should be fast. Pre-compute all chart data from raw arrays — avoid iterating DataFrames inside callbacks. Move DataFrame aggregation to `compute_chart_data()` in processing.py.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Linear interpolation | Manual lerp between lookup rows | `numpy.interp()` | Handles edge cases, extrapolation clamping, vectorized |
| Cumulative sum | Manual loop accumulator | `numpy.cumsum()` | One line, correct, fast |
| Dollar abbreviation | Custom formatter | Existing `fmt_cost()` in processing.py | Already tested, handles K/M/N/A |
| Chart animation on update | Manual JS transitions | Plotly `layout.transition` dict | `{"duration": 300, "easing": "cubic-in-out"}` on the Figure layout |
| Grouped bar arrangement | Manual x-offset calculation | `barmode='group'` on layout | Plotly handles spacing automatically |
| Pie label suppression | CSS hacks | `textinfo='none'` on go.Pie | Built-in, supported |

**Key insight:** The entire chart-rendering stack (interpolation → cost computation → figure building) must complete in <200ms per slider tick for drag to feel responsive. Keep computation in numpy arrays, not pandas row-level operations inside callbacks.

---

## Common Pitfalls

### Pitfall 1: Battery Slider Replaces Only the Storage Cost
**What goes wrong:** Developer subtracts entire `Battery (1 day of power)` cost ($1,800,000 from data.xlsx) and replaces it with the interpolated `total_cost` from the lookup table. But the lookup table `total_cost` covers both battery and tank storage — it already includes everything. The base electrical cost without storage = $13,562,241; at 50/50 slider the storage cost is $700,000 → total = $14,262,241.
**Why it happens:** The battery row in electrical DataFrame ($1,800,000) does not equal the lookup table values. They represent different scenarios.
**How to avoid:** In `compute_chart_data()`, exclude `Battery (1 day of power)` from the electrical sum, then add the interpolated `total_cost` from battery_lookup separately.
**Warning signs:** Electrical cost at slider=50% is ~$16M instead of ~$14.2M — the base battery cost was double-counted.

### Pitfall 2: Hybrid System Has No Data Yet
**What goes wrong:** Phase 4 builds the hybrid system. In Phase 3, attempting to read `data["hybrid"]` raises a KeyError. Charts must show Hybrid as a zero/empty placeholder that looks intentional.
**Why it happens:** Hybrid is not in the data dict (only "electrical", "mechanical", "miscellaneous", "battery_lookup").
**How to avoid:** In `compute_chart_data()`, hard-code hybrid cost=0, land_area=0, turbine_count=0, energy_dict={} for Phase 3. Add a TODO comment. In the energy pie chart, if a system has empty energy_dict, either show "No data" or hide that pie trace.
**Warning signs:** KeyError on `data["hybrid"]` at first callback invocation.

### Pitfall 3: Chart Figures Recreated on Every Drag Tick → Blinking
**What goes wrong:** When a figure is fully replaced via callback, Plotly re-renders the entire chart, causing a visible flash/blink instead of smooth animation.
**Why it happens:** The callback returns a new `go.Figure` object, resetting all state.
**How to avoid:** Set `uirevision` on all figures to a stable constant (e.g., `"static"`). This preserves camera/zoom state across figure updates. Also set `layout.transition = {"duration": 300, "easing": "cubic-in-out"}` on each figure.
**Warning signs:** Charts blink or axes reset to default zoom on every slider drag.

### Pitfall 4: updatemode='drag' Blocks UI Thread on Slow Callbacks
**What goes wrong:** With `updatemode='drag'`, the callback fires on every mouse-move pixel. If `update_charts` takes >100ms, events queue up and the UI freezes.
**Why it happens:** Heavy pandas operations inside the callback function.
**How to avoid:** Keep callback logic to: (1) interpolate battery cost via numpy.interp (fast), (2) call pre-built helper functions that return numpy arrays (fast), (3) build figures from arrays not DataFrames. Move all DataFrame aggregation to module-level helpers called at startup.
**Warning signs:** Slider feels "sticky" or lags visibly behind mouse position.

### Pitfall 5: Pie Chart with Empty Energy Data for Hybrid
**What goes wrong:** `go.Pie(values=[])` raises an error or renders as a blank circle with confusing tooltip.
**Why it happens:** Hybrid has no energy data in Phase 3.
**How to avoid:** When energy dict is empty, use a single "No data" slice or set `visible=False` on the hybrid pie trace. Revisit in Phase 4 when hybrid has real data.
**Warning signs:** JavaScript error in browser console about empty Pie values.

### Pitfall 6: restyleData Legend Sync Does Not Reset
**What goes wrong:** `restyleData` persists the last event, so if you try to use it to read current visibility state, you get stale data.
**Why it happens:** Known Dash bug #2037 — restyleData property is not cleared after graph rerenders.
**How to avoid:** Use the custom HTML badge legend (Pattern 8) as the single source of truth for visibility. Do not use restyleData for state. The dcc.Store is authoritative.
**Warning signs:** Toggling a system off, then moving the slider, causes the system to reappear because the callback re-reads stale restyleData.

---

## Code Examples

Verified patterns from official sources and data investigation:

### Battery Interpolation
```python
# Source: numpy.interp docs + verified against battery_lookup data
import numpy as np

def interpolate_battery_cost(battery_fraction: float, battery_lookup_df) -> float:
    fractions = battery_lookup_df["battery_fraction"].astype(float).values  # [0.0, 0.1, ..., 1.0]
    costs = battery_lookup_df["total_cost"].astype(float).values             # [150000, 260000, ..., 1250000]
    return float(np.interp(battery_fraction, fractions, costs))

# Examples:
# interpolate_battery_cost(0.0, bl) = 150,000   (all tank)
# interpolate_battery_cost(0.5, bl) = 700,000   (50/50)
# interpolate_battery_cost(0.35, bl) = 535,000  (35% battery)
# interpolate_battery_cost(1.0, bl) = 1,250,000 (all battery)
```

### Ratio Label Generation
```python
def battery_ratio_label(battery_fraction: float) -> str:
    """Format the live ratio label shown next to the battery/tank slider."""
    pct_batt = int(round(battery_fraction * 100))
    pct_tank = 100 - pct_batt
    return f"{pct_batt}% Battery / {pct_tank}% Tank"

# battery_ratio_label(0.5) → "50% Battery / 50% Tank"
# battery_ratio_label(0.7) → "70% Battery / 30% Tank"
```

### Line Chart with Hover Tooltip
```python
# Source: plotly.com/python/line-charts/ + project fmt_cost pattern
import plotly.graph_objects as go
from src.data.processing import fmt_cost

def build_cost_chart(years: int, mech_cumulative, elec_cumulative, hybrid_cumulative,
                     visibility: dict) -> go.Figure:
    x = list(range(0, years + 1))
    fig = go.Figure()

    systems = [
        ("Mechanical", mech_cumulative, SYSTEM_COLORS["Mechanical"]),
        ("Electrical", elec_cumulative, SYSTEM_COLORS["Electrical"]),
        ("Hybrid",     hybrid_cumulative, SYSTEM_COLORS["Hybrid"]),
    ]
    for name, cumulative, color in systems:
        vis = True if visibility.get(name.lower(), True) else "legendonly"
        fig.add_trace(go.Scatter(
            x=x[:years+1],
            y=cumulative[:years+1],
            mode="lines",
            name=name,
            line=dict(color=color, width=2),
            visible=vis,
            hovertemplate=f"{name}: %{{y:.3s}} at Year %{{x}}<extra></extra>",
            # %{y:.3s} uses SI prefix notation: 45200000 → "45.2M"
            # For custom fmt_cost style, precompute y_text array and use text= parameter
        ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Cost (USD)",
        uirevision="static",
        transition={"duration": 300, "easing": "cubic-in-out"},
        margin=dict(l=50, r=20, t=20, b=40),
        legend=dict(visible=False),  # Legend handled externally
        hovermode="x unified",
    )
    return fig
```

### Grouped Bar Chart
```python
# Source: plotly.com/python/bar-charts/ + project patterns
def build_land_chart(mech_land, elec_land, hybrid_land, visibility: dict) -> go.Figure:
    fig = go.Figure()
    systems = [
        ("Mechanical", mech_land, SYSTEM_COLORS["Mechanical"]),
        ("Electrical", elec_land, SYSTEM_COLORS["Electrical"]),
        ("Hybrid",     hybrid_land, SYSTEM_COLORS["Hybrid"]),  # 0 until Phase 4
    ]
    for name, value, color in systems:
        vis = True if visibility.get(name.lower(), True) else "legendonly"
        fig.add_trace(go.Bar(
            x=["Land Area"],
            y=[value],
            name=name,
            marker_color=color,
            visible=vis,
            hovertemplate=f"{name}: %{{y:,.0f}} m²<extra></extra>",
            text=None,  # no labels on bars
        ))
    fig.update_layout(
        barmode="group",
        yaxis_title="Area (m²)",
        xaxis_title="",
        uirevision="static",
        transition={"duration": 300},
        legend=dict(visible=False),
    )
    return fig
```

### dcc.Slider Setup
```python
# Source: dash.plotly.com/dash-core-components/slider
# Battery/tank slider
dcc.Slider(
    id="slider-battery",
    min=0, max=1, step=0.001,
    value=0.5,
    marks={},
    tooltip={"always_visible": False},
    updatemode="drag",
)

# Time horizon slider
dcc.Slider(
    id="slider-time-horizon",
    min=1, max=50, step=1,
    value=50,
    marks={1: "1yr", 25: "25yr", 50: "50yr"},
    tooltip={"always_visible": True, "placement": "bottom",
             "template": "{value} years"},
    updatemode="drag",
)
```

### Figure animation transition
```python
# Source: Plotly layout.transition docs
# Set on every figure returned from callback to get smooth updates:
fig.update_layout(
    transition={"duration": 300, "easing": "cubic-in-out"},
    uirevision="static",   # prevents axis/zoom reset on update
)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `app.callback` decorator | `@callback` (Dash 2.0+, used by this project) | Dash 2.0 | No `app` import required in layout modules |
| `dcc.Graph` with `animate=True` | `layout.transition` dict | Dash 3.x | `animate=True` conflicts with `showlegend` updates (bug #668); `transition` is preferred |
| Manual px-offset for grouped bars | `barmode='group'` | Plotly 4+ | Automatic, correct |
| Pie chart in `make_subplots` | Domain positioning or `make_subplots` with `specs=[{'type':'domain'}]` | Plotly 4+ | Both work; domain positioning avoids subplot overhead for simple 3-pie layout |

**Deprecated/outdated:**
- `app.callback` with app import in layout modules: replaced by `from dash import callback` (Dash 2.0+); already used in this project
- `animate=True` on dcc.Graph: known bug with dynamic showlegend; use `layout.transition` dict instead

---

## Open Questions

1. **Cost-over-time formula for battery replacement cycle**
   - What we know: Battery lifespan_years=12 in data.xlsx. The lookup table total_cost covers initial storage cost. For years 12, 24, 36, 48 — the storage cost is replaced using the current slider position.
   - What's unclear: Does the replacement cost in year 12+ use the same slider-interpolated value (assume yes — slider represents the chosen configuration), or always default to 50/50?
   - Recommendation: Use current slider value for all replacement years (slider represents ongoing configuration choice). This makes the chart respond dynamically to the slider as intended.

2. **Wind turbine count for Hybrid placeholder**
   - What we know: Hybrid has no data until Phase 4. Bar chart must show all 3 systems.
   - What's unclear: Should Hybrid show 0 or be hidden/greyed out?
   - Recommendation: Show Hybrid as 0 with a faded/greyed bar (via `opacity=0.3` or `marker_pattern_shape='/'`). Add a note "Hybrid data available in builder". This is visible but clearly differentiated from real data.

3. **Energy pie for Hybrid placeholder**
   - What we know: Hybrid has no energy breakdown data in Phase 3.
   - What's unclear: Show empty pie or "No data" annotation?
   - Recommendation: Show a single "No data" pie slice for Hybrid using a neutral grey color. Avoids empty-values error from go.Pie.

---

## Sources

### Primary (HIGH confidence)
- Dash docs (dash.plotly.com/dash-core-components/slider) — dcc.Slider properties, updatemode, tooltip
- Plotly docs (plotly.com/python/subplots/) — make_subplots specs for mixed chart types
- Plotly docs (plotly.com/python/pie-charts/) — domain positioning, textinfo, hovertemplate
- Plotly docs (plotly.com/python/bar-charts/) — barmode='group', hovertemplate
- Direct data inspection (python -c ...) — battery_lookup values, equipment costs, lifespans, turbine counts — HIGH confidence

### Secondary (MEDIUM confidence)
- Plotly community (community.plotly.com/t/39626) — restyleData format [edits, indices] pattern
- Dash docs (dash.plotly.com/clientside-callbacks) — clientside callbacks limitations
- Dash docs (dash.plotly.com/interactive-graphing) — dcc.Graph interactive properties

### Tertiary (LOW confidence)
- GitHub issue plotly/dash #2037 — restyleData not cleared on graph update (bug report, not official docs)
- GitHub issue plotly/plotly.py #4946 — legendgroupclick inconsistency across subplots (bug report)
- Community pattern for dcc.Store-based legend sync — no official doc, but consistent across multiple forum discussions

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages already installed and verified importable
- Architecture: HIGH — patterns verified against Dash 4.0 + plotly 6.5.2 installed versions
- Data calculations: HIGH — verified by running actual data through numpy/pandas in dev environment
- Pitfalls: HIGH (items 1-4) / MEDIUM (items 5-6) — most verified by code inspection or official bug reports
- Legend sync via store: MEDIUM — no official Dash 4.0 doc explicitly endorses this pattern, but it is the most commonly cited workaround and fits Dash's data-flow model

**Research date:** 2026-02-21
**Valid until:** 2026-03-21 (stable Plotly/Dash APIs)
