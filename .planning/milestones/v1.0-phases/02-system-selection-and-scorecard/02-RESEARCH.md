# Phase 2: System Selection and Scorecard - Research

**Researched:** 2026-02-21
**Domain:** Dash/dbc tab navigation, equipment card grid with accordion expand, RAG scorecard table
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**System selector & navigation:**
- Horizontal tab bar across the top of the main content area for switching between Mechanical, Electrical, and Hybrid
- Tabs use clean names only ("Mechanical", "Electrical", "Hybrid") — no metrics on the tab itself
- Active tab uses the system's assigned color (from Phase 1) for strong visual reinforcement
- Sidebar from Phase 1 stays separate — not involved in system selection
- Scorecard on top, equipment list below — vertical stack layout
- Same-page content swap when switching tabs — no page transitions

**Landing / Overview state:**
- On first load, show a landing overview (no system pre-selected)
- Landing has a brief intro line (e.g., "Select a desalination system to explore")
- Three cards in a horizontal row — one per system
- Each card: system name + brief 1-2 sentence description, text only (no icons/images)
- Cards have a colored header/top bar using the system's assigned color
- Clicking a card enters the tab view for that system
- "Back to Overview" breadcrumb/link (not a fourth tab) to return to the landing state

**Hybrid tab (before Phase 4):**
- Empty state with message: "Build your hybrid system to see equipment here"
- Points students to the builder (which is Phase 4 work)

**Equipment list layout:**
- Card/tile format — each equipment item is a card, not a table row
- Cards arranged in a grid (2-3 cards per row)
- All five metrics visible on each card at a glance: quantity, cost, energy, land area, lifespan
- Cards grouped by process stage (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal) with section headers

**Equipment detail view:**
- Clicking a card expands it in place (accordion style) — other cards shift down
- Only one card expanded at a time — expanding a new card auto-collapses the previous
- Expanded view shows: full text description + all raw data fields from the spreadsheet
- Explicit close button (X or "Close") in the expanded area
- Cross-system comparison: small comparison table showing this equipment vs. equivalents from other systems for the same process stage
- Comparison table highlights the best value per metric (bold or green)
- Missing/empty data fields show "N/A"

**Data formatting:**
- Costs: abbreviated large numbers ($42.5K, $1.2M)
- Units inline with each value ("450 kWh", "$42.5K", "2.3 acres")

**Scorecard presentation:**
- Horizontal comparison table: systems as columns, metrics (cost, land area, efficiency) as rows
- RAG indicators: colored dots/circles next to each value
- Actual numeric values displayed alongside RAG dots
- RAG logic: relative ranking — green = best of systems, yellow = middle, red = worst
- With only 2 systems (Hybrid not built): green and red only, no yellow
- Hybrid column hidden until Hybrid system is fully assembled (Phase 4)
- Scorecard has a title + brief explanation of RAG meaning (green = best, red = worst)
- Includes an overall ranking/summary row showing which system "wins" overall

### Claude's Discretion

- Exact card spacing, padding, shadows, and typography
- Animation/transitions for card expand/collapse
- Exact wording of the landing page intro and empty state messages
- How the overall ranking row is calculated (equal weight, weighted, etc.)
- Loading states and error handling

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SEL-01 | User can select between Mechanical, Electrical, or Hybrid system from a clear selector interface | dbc.Tabs with active_tab callback + landing overview state pattern; tab_id per system |
| SEL-02 | Selecting Mechanical or Electrical shows equipment list with quantity, cost, energy, land area, and lifespan | dbc.Card grid per equipment row from DataFrame; format_metric() helper for units; process-stage grouping |
| SEL-03 | User can click/select individual equipment for detailed description and data | dbc.Accordion with active_item controlled via callback; one item open at a time; cross-system comparison table embedded in expanded view |
| SCORE-01 | Dashboard displays cost, land area, and efficiency scorecard for all systems | dbc.Table (manual html.Thead/html.Tbody) with systems as columns, metrics as rows; aggregate calculations from DataFrames |
| SCORE-02 | Each metric has red/yellow/green (RAG) ranking relative to the three systems | rag_color() helper comparing metric values; html.Span with borderRadius "50%" for colored dot; pre-defined RAG_COLORS from config.py |
| VIS-01 | Academic styling — clean, professional, muted colors (FLATLY Bootstrap theme or similar) | FLATLY already applied from Phase 1; dbc.Card with shadow-sm class; muted SYSTEM_COLORS from config.py |
| VIS-02 | Easy to navigate for students unfamiliar with the tool | Landing overview with clear system cards; "Back to Overview" breadcrumb; Hybrid empty state with instructions |
</phase_requirements>

---

## Summary

Phase 2 builds entirely on the Dash 4.0 / dash-bootstrap-components 2.x stack established in Phase 1. No new packages are needed: tabs, cards, accordions, and tables are all native dbc components. The phase has three distinct UI regions: (1) a landing overview with three system-selection cards, (2) a tab-based view per system with a scorecard and equipment list, and (3) an in-place accordion expansion for individual equipment detail.

The central architectural challenge is state management: the app must know whether the user is in the landing state or a system-selected state, and which equipment card (if any) is expanded. Both are well-solved with a `dcc.Store` holding `{"view": "overview" | "mechanical" | "electrical" | "hybrid"}` and the `active_item` property on `dbc.Accordion` respectively. The tab bar itself uses `dbc.Tabs` with `active_tab` driven by a callback that also responds to landing card clicks.

The scorecard is a static HTML table built with `html.Thead`/`html.Tbody` components, not a `dash_table.DataTable`. This gives full control over embedded RAG dot components (colored `html.Span` circles) inside table cells. RAG logic is simple relative ranking across the two present systems (Mechanical and Electrical), with Hybrid column omitted until Phase 4.

**Primary recommendation:** Use `dcc.Store(id="active-system")` as the single source of truth for which view is shown. Drive both the tab selection and the content area from that store via a single callback. Use `dbc.Accordion` with `active_item` for the equipment expand/collapse — do not build a custom accordion with pattern-matching callbacks.

---

## Standard Stack

### Core (unchanged from Phase 1 — no new packages needed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash | 4.0.0 | dcc.Store, callbacks, html.* components | Already installed |
| dash-bootstrap-components | 2.0.4 | dbc.Tabs, dbc.Card, dbc.Accordion, dbc.Table | Already installed |
| pandas | 2.3.3 | DataFrame operations for scorecard aggregation | Already installed |

### No New Installations Required

```bash
# All packages already in requirements.txt from Phase 1
# dash==4.0.0
# dash-bootstrap-components==2.0.4
# openpyxl==3.1.5
# pandas==2.3.3
```

---

## Architecture Patterns

### Recommended File Structure for Phase 2

```
src/
├── data/
│   ├── loader.py          # (Phase 1) — unchanged
│   └── processing.py      # NEW: format_metric(), rag_color(), compute_scorecard()
├── layout/
│   ├── shell.py           # (Phase 1) — minor edit: add "System Explorer" NavLink
│   ├── error_page.py      # (Phase 1) — unchanged
│   ├── overview.py        # NEW: landing overview with three system cards
│   ├── system_view.py     # NEW: tab bar + scorecard + equipment list (tabs content)
│   ├── equipment_grid.py  # NEW: card grid grouped by process stage
│   └── scorecard.py       # NEW: RAG scorecard table
└── config.py              # (Phase 1) — SYSTEM_COLORS, RAG_COLORS already defined
```

### Pattern 1: Single dcc.Store Drives Landing vs. System View

**What:** One `dcc.Store(id="active-system", data=None)` holds the current view state. `None` = landing overview. `"mechanical"` / `"electrical"` / `"hybrid"` = system selected. The `page-content` area swaps between `overview.py` layout and `system_view.py` layout based on this store.

**Why not use dbc.Tabs alone:** Clicking a landing card must also set the active tab. A `dcc.Store` as the single source of truth avoids circular callbacks — the store is updated by either landing card clicks or tab changes, and the content renders from the store.

**Example:**
```python
# In shell.py or a top-level layout function — add store to existing layout
dcc.Store(id="active-system", data=None),

# Callback: landing card OR tab change → update store
@callback(
    Output("active-system", "data"),
    Input({"type": "system-card-btn", "index": ALL}, "n_clicks"),
    Input("system-tabs", "active_tab"),
    State("active-system", "data"),
    prevent_initial_call=True,
)
def update_active_system(card_clicks, active_tab, current):
    triggered = ctx.triggered_id
    if triggered is None:
        return current
    if isinstance(triggered, dict) and triggered.get("type") == "system-card-btn":
        return triggered["index"]   # "mechanical", "electrical", or "hybrid"
    return active_tab               # tab_id matches system key

# Callback: store → render content area
@callback(
    Output("page-content", "children"),
    Input("active-system", "data"),
)
def render_content(active_system):
    if active_system is None:
        return create_overview_layout()
    return create_system_view_layout(active_system, DATA)
```

**Note:** `ctx` is `dash.ctx` (Dash 2.4+, included in Dash 4.0). `ctx.triggered_id` returns `None` on initial load, a string for string IDs, or a dict for pattern-matching IDs.

### Pattern 2: dbc.Tabs with Active Color Styling

**What:** `dbc.Tabs` with one `dbc.Tab` per system. Active tab uses `active_label_style` to set the system's color. Tab bar is driven by `active-system` store — set `active_tab` via callback Output.

**Key discovery:** `active_tab_style` has a known bug where `backgroundColor` does not apply correctly (confirmed community reports). Use `active_label_style` for text/font styling and target the `.nav-tabs .nav-link.active` CSS selector in `custom.css` for background color per system. Since background color must vary per system (not a fixed color), the CSS-class approach won't work for per-system colors — use a callback that sets `tab_style` on each `dbc.Tab` dynamically.

**Simpler alternative (recommended):** Apply a bottom border color to the active tab using `active_label_style={"borderBottom": "3px solid <color>", "fontWeight": "bold"}`. This avoids the background-color bug entirely and looks clean.

```python
# system_view.py
from src.config import SYSTEM_COLORS

def create_tab_bar(active_system: str) -> dbc.Tabs:
    tabs = []
    for key, label in [("mechanical", "Mechanical"), ("electrical", "Electrical"), ("hybrid", "Hybrid")]:
        color = SYSTEM_COLORS[label]
        tabs.append(
            dbc.Tab(
                label=label,
                tab_id=key,
                label_style={"color": "#495057"},
                active_label_style={
                    "color": color,
                    "fontWeight": "bold",
                    "borderBottom": f"3px solid {color}",
                },
            )
        )
    return dbc.Tabs(tabs, id="system-tabs", active_tab=active_system)
```

### Pattern 3: Equipment Card Grid Grouped by Process Stage

**What:** Equipment items from the DataFrame displayed as `dbc.Card` tiles in a `dbc.Row`/`dbc.Col` grid, grouped by process stage with `html.H5` section headers.

**Process stages (to be assigned per equipment item):** Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal. The data.xlsx does NOT include a process stage column — stage assignment must be hard-coded as a mapping dict in `config.py` or `processing.py`.

**Stage assignment:** Must be manually defined based on knowledge of each equipment item's function. This is not derivable from the data — it is domain knowledge that must be hard-coded. Example:

```python
# src/config.py or src/data/processing.py
PROCESS_STAGES = {
    "mechanical": {
        "Water Extraction": ["Wind Turbine", "Water Pump"],
        "Pre-Treatment": ["Multi-Media Filtration", "Cartridge Filter"],
        "Desalination": ["Reverse Osmosis Membrane"],
        "Post-Treatment": ["UV Disinfection"],
        "Brine Disposal": ["Brine Well"],
    },
    "electrical": {
        # ... same structure
    },
}
```

**Card layout (each equipment item):**
```python
# Each card: metric badges + click target
def make_equipment_card(row: dict, system: str, idx: int) -> dbc.Col:
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(row["name"], className="fw-bold"),
            dbc.CardBody([
                html.P(f"Qty: {fmt(row['quantity'])}", className="mb-1 small"),
                html.P(f"Cost: {fmt_cost(row['cost_usd'])}", className="mb-1 small"),
                html.P(f"Energy: {fmt_num(row['energy_kw'])} kW", className="mb-1 small"),
                html.P(f"Land: {fmt_num(row['land_area_m2'])} m²", className="mb-1 small"),
                html.P(f"Lifespan: {fmt(row['lifespan_years'])}", className="mb-1 small"),
            ]),
        ],
        id={"type": "equipment-card", "system": system, "index": idx},
        className="h-100 shadow-sm",
        style={"cursor": "pointer"},
        ),
        width=4,  # 3 per row on md+
        className="mb-3",
    )
```

### Pattern 4: Accordion-Style Expand (One Card at a Time)

**What:** The built-in `dbc.Accordion` with `active_item` controlled via callback. `always_open=False` (default) ensures only one item is open at a time. Each `dbc.AccordionItem` gets `item_id` matching the equipment index.

**Why use dbc.Accordion over custom pattern-matching:** `dbc.Accordion` is purpose-built for this. It handles collapse/expand animations, keyboard accessibility, and the "one open at a time" constraint natively. The custom pattern-matching accordion pattern (from community Show & Tell) is 40+ lines of boilerplate — unnecessary when `dbc.Accordion` handles it in 5 lines.

```python
def make_equipment_accordion(df: pd.DataFrame, system: str) -> dbc.Accordion:
    items = []
    for idx, row in df.iterrows():
        items.append(
            dbc.AccordionItem(
                children=make_equipment_detail(row, system),
                title=html.Div([
                    html.Span(row["name"], className="fw-bold"),
                    html.Span(f" — {fmt_cost(row['cost_usd'])}", className="text-muted small ms-2"),
                ]),
                item_id=f"item-{idx}",
            )
        )
    return dbc.Accordion(
        items,
        id={"type": "equipment-accordion", "system": system},
        active_item=None,       # none expanded on load
        always_open=False,      # close others on open (default but explicit)
        flush=False,            # keep card border styling
    )
```

**Note on dbc.AccordionItem title:** As of dbc 1.x+, `title` accepts Dash components (not just strings). This was fixed in dbc 1.0.0rc1 — confirmed safe to use with the current dbc 2.0.4.

### Pattern 5: Equipment Detail View (Expanded Content)

**What:** Content of each `dbc.AccordionItem`. Shows full description + all fields + cross-system comparison table.

**Description text:** The data.xlsx does NOT include a description column for equipment. Descriptions must be either hard-coded in a dict or omitted (showing only raw data fields). Recommendation: hard-code brief descriptions for each equipment type in `config.py`. This is the only way to satisfy SEL-03 ("detailed description").

```python
def make_equipment_detail(row: dict, system: str) -> html.Div:
    description = EQUIPMENT_DESCRIPTIONS.get(row["name"], "No description available.")
    fields = [
        ("Name", row["name"]),
        ("Quantity", fmt(row["quantity"])),
        ("Cost", fmt_cost(row["cost_usd"])),
        ("Energy", f"{fmt_num(row['energy_kw'])} kW"),
        ("Land Area", f"{fmt_num(row['land_area_m2'])} m²"),
        ("Lifespan", fmt(row["lifespan_years"])),
    ]
    return html.Div([
        html.P(description, className="text-muted fst-italic mb-3"),
        dbc.Table(
            [html.Tbody([
                html.Tr([html.Th(label, style={"width": "35%"}), html.Td(value or "N/A")])
                for label, value in fields
            ])],
            bordered=True, size="sm", className="mb-3",
        ),
        make_cross_system_comparison(row["name"], system),
    ])
```

### Pattern 6: RAG Scorecard Table

**What:** `html.Table` built manually (not `dbc.Table.from_dataframe`) with `html.Thead`/`html.Tbody`. Systems are columns, metrics are rows. Each value cell contains an `html.Span` colored dot + value text.

**RAG logic:** Relative ranking. For each metric: the system with the best value gets green, worst gets red, middle (if 3 systems) gets yellow. "Best" means lowest cost and land area; efficiency is the only metric where higher = better. With Hybrid absent, only green and red apply.

```python
# src/data/processing.py

RAG_BETTER_IS_LOWER = {"cost", "land_area"}   # for these metrics, lower = better
RAG_BETTER_IS_HIGHER = {"efficiency"}          # for this metric, higher = better

def rag_color(values: dict[str, float], metric: str) -> dict[str, str]:
    """
    Returns {"mechanical": "green"|"yellow"|"red", ...}
    values: {system_key: numeric_value}  — None values excluded from ranking
    """
    present = {k: v for k, v in values.items() if v is not None}
    ranked = sorted(present, key=lambda k: present[k],
                    reverse=(metric in RAG_BETTER_IS_HIGHER))
    result = {}
    n = len(ranked)
    for i, key in enumerate(ranked):
        if n <= 2:
            result[key] = "green" if i == 0 else "red"
        else:
            result[key] = ["green", "yellow", "red"][i]
    return result

def make_rag_dot(color_key: str) -> html.Span:
    """Colored circle indicator. color_key: "green" | "yellow" | "red"."""
    from src.config import RAG_COLORS
    return html.Span(
        style={
            "display": "inline-block",
            "width": "12px",
            "height": "12px",
            "borderRadius": "50%",
            "backgroundColor": RAG_COLORS[color_key],
            "marginRight": "6px",
            "verticalAlign": "middle",
        }
    )
```

**Scorecard table structure:**
```python
def make_scorecard_table(mechanical_df, electrical_df) -> html.Div:
    systems = ["mechanical", "electrical"]  # hybrid excluded until Phase 4
    labels = {"mechanical": "Mechanical", "electrical": "Electrical"}

    # Compute aggregate metrics per system
    scores = compute_scorecard_metrics(mechanical_df, electrical_df)
    # scores = {
    #   "mechanical": {"cost": 1234567, "land_area": 45.2, "efficiency": 0.78},
    #   "electrical": {"cost": 987654,  "land_area": 38.1, "efficiency": 0.82},
    # }

    metrics = [
        ("Total Cost", "cost", "$"),
        ("Total Land Area", "land_area", "m²"),
        ("Efficiency", "efficiency", ""),
    ]

    header = html.Thead(html.Tr([
        html.Th("Metric"),
        *[html.Th(labels[s], style={"textAlign": "center"}) for s in systems],
    ]))

    rows = []
    for metric_label, metric_key, unit in metrics:
        rag = rag_color({s: scores[s].get(metric_key) for s in systems}, metric_key)
        cells = [html.Td(metric_label, className="fw-semibold")]
        for s in systems:
            val = scores[s].get(metric_key)
            display = fmt_cost(val) if metric_key == "cost" else (f"{val:.1f} {unit}".strip() if val is not None else "N/A")
            cells.append(html.Td(
                [make_rag_dot(rag.get(s, "yellow")), display],
                style={"textAlign": "center"},
            ))
        rows.append(html.Tr(cells))

    return html.Div([
        html.H5("System Scorecard"),
        html.P("Green = best, Yellow = middle, Red = worst", className="text-muted small"),
        dbc.Table(
            [header, html.Tbody(rows)],
            bordered=True, hover=True, responsive=True, className="mt-2",
        ),
    ])
```

### Pattern 7: Number Formatting Helper

**What:** A single `format_metric()` / `fmt_cost()` helper in `processing.py`. No external library needed.

```python
# src/data/processing.py

def fmt_cost(value) -> str:
    """Format numeric cost as abbreviated string. Non-numeric returned as-is."""
    import pandas as pd
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return str(value) if value is not None else "N/A"
    if abs(numeric) >= 1_000_000:
        return f"${numeric / 1_000_000:.1f}M"
    if abs(numeric) >= 1_000:
        return f"${numeric / 1_000:.1f}K"
    return f"${numeric:,.0f}"

def fmt_num(value) -> str:
    """Format a general numeric value. Non-numeric returned as-is."""
    import pandas as pd
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return str(value) if value is not None else "N/A"
    return f"{numeric:,.1f}"

def fmt(value) -> str:
    """Pass-through formatter: numeric to comma-formatted, strings as-is, None → 'N/A'."""
    if value is None:
        return "N/A"
    import pandas as pd
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return str(value)
    return f"{numeric:,}"
```

### Pattern 8: Scorecard Aggregate Calculations

**What:** Computing the scorecard values from the DataFrames. Cost and land area are straightforward sums. Efficiency is NOT a column in the data — it needs a definition.

**Critical gap:** The data.xlsx has no "efficiency" column. The SCORE-01 requirement lists efficiency as a scorecard metric. Options:
1. Derive efficiency from energy (kW) relative to water output (no water output column in data)
2. Define efficiency as a ratio: `energy_kw / land_area_m2` (output density proxy)
3. Use total energy as the "efficiency" metric (lower energy = more efficient)

Recommendation: Use total energy consumption (sum of `energy_kw`) as the efficiency metric, displayed as "Total Energy (kW)" on the scorecard. For this metric, lower is better. This is honest to the data and avoids fabricating a formula. Add a footnote: "Lower energy consumption = more efficient."

```python
def compute_scorecard_metrics(mechanical_df: pd.DataFrame, electrical_df: pd.DataFrame) -> dict:
    result = {}
    for key, df in [("mechanical", mechanical_df), ("electrical", electrical_df)]:
        cost_numeric = pd.to_numeric(df["cost_usd"], errors="coerce")
        land_numeric = pd.to_numeric(df["land_area_m2"], errors="coerce")
        energy_numeric = pd.to_numeric(df["energy_kw"], errors="coerce")
        result[key] = {
            "cost": cost_numeric.sum(skipna=True),
            "land_area": land_numeric.sum(skipna=True),
            "efficiency": energy_numeric.sum(skipna=True),  # total kW — lower = more efficient
        }
    return result
```

### Anti-Patterns to Avoid

- **Building a custom accordion with pattern-matching callbacks:** Unnecessary; `dbc.Accordion` with `active_item` handles single-open-at-a-time natively in 5 lines vs. 40+.
- **Using `dash_table.DataTable` for the scorecard:** DataTable cannot contain arbitrary Dash components inside cells (no colored dot spans). Use manual `html.Table` structure.
- **Setting active tab color with `active_tab_style={"backgroundColor": color}`:** Known bug — background color does not apply. Use `active_label_style` with `borderBottom` instead.
- **Calling scorecard calculations inside the render callback:** Keep `compute_scorecard_metrics()` in `processing.py` so it can be tested independently. The callback just calls the function.
- **Using `dcc.Location` + `dbc.NavLink` for system switching:** Violates the architectural decision to use tabs (not Dash Pages) to preserve `dcc.Store` cross-tab state. Stay with single-page tab pattern.
- **Storing DataFrames in `dcc.Store`:** Module-level `DATA` dict from Phase 1 is the right read-only data source. Never serialize DataFrames into stores.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Accordion expand/collapse | Custom pattern-matching callback accordion | `dbc.Accordion` with `active_item` | Built-in, accessible, animates, one-open-at-a-time is native |
| Tab navigation | `dcc.Tabs` or custom nav buttons | `dbc.Tabs` | Already in stack; Bootstrap-styled; `active_tab` + `active_label_style` |
| Card grid layout | Custom CSS grid | `dbc.Row` + `dbc.Col(width=4)` | Bootstrap 5 col-4 = 3 per row; responsive out of the box |
| Table with embedded components | `dash_table.DataTable` | Manual `html.Table` structure | DataTable cells cannot contain arbitrary Dash components; manual table rows can |
| Number abbreviation | External library (babel, etc.) | Simple Python helper `fmt_cost()` | 10 lines of Python covers $K/$M; no dep needed |
| RAG indicator graphic | Image, icon library | `html.Span` with `borderRadius: "50%"` | Pure CSS circle; no dependencies; works inline in table cells |

---

## Common Pitfalls

### Pitfall 1: Process Stage Not in Data

**What goes wrong:** Code tries to read a "process_stage" or "category" column from the DataFrame and gets a KeyError.

**Why it happens:** The data.xlsx has no process stage column. The equipment grouping into Water Extraction / Pre-Treatment / Desalination / Post-Treatment / Brine Disposal is domain knowledge.

**How to avoid:** Define a hard-coded `PROCESS_STAGES` dict in `config.py` mapping system + equipment names to their stage. Use this dict when rendering the equipment grid. If an equipment item's name is not found in the mapping, place it in a catch-all "Other" group.

**Warning signs:** `KeyError: 'process_stage'` or all cards appearing in one ungrouped list.

### Pitfall 2: Description Text Not in Data

**What goes wrong:** The expanded equipment detail view has no descriptive text to show beyond raw numbers, making SEL-03 only partially satisfied.

**Why it happens:** The data.xlsx contains no description column. The only text data is equipment names and numeric fields.

**How to avoid:** Hard-code a `EQUIPMENT_DESCRIPTIONS` dict in `config.py` with a brief 1-2 sentence description per equipment name. If a name is not found, fall back to "No description available." This is the only path to satisfying SEL-03.

**Warning signs:** Empty expanded views with just a table of numbers.

### Pitfall 3: active_tab_style backgroundColor Bug

**What goes wrong:** `active_tab_style={"backgroundColor": "#5B8DB8"}` has no visible effect on the active tab background.

**Why it happens:** Known bug in dbc.Tab component confirmed in community issue #86819 — the backgroundColor applied via `active_tab_style` does not propagate correctly to the rendered element.

**How to avoid:** Use `active_label_style` for text-level styling (color, fontWeight). For a visible active state indicator, use a colored `borderBottom` on the label or add a CSS rule in `custom.css` targeting `.nav-tabs .nav-link.active`. For per-system colors, set `active_label_style` dynamically in the layout factory rather than CSS (since CSS can't vary per system).

**Warning signs:** Active tab looks identical to inactive tabs despite setting active_tab_style.

### Pitfall 4: Circular Callback with dcc.Store + dbc.Tabs

**What goes wrong:** Setting `active_tab` via a callback Output, while also using `active_tab` as a callback Input, creates a circular dependency that Dash raises as a `circular-callback` error.

**Why it happens:** Both the landing card click and the tab click must update the `active-system` store, and the store must update `active_tab`. If the tab also feeds back into the store, there's a cycle.

**How to avoid:** Use the store as the single source of truth with a ONE-WAY data flow:
1. User clicks landing card OR tab → `update_active_system` callback → writes store
2. `render_content` callback reads store → renders content (including tab bar re-created with correct `active_tab` set statically in the component)
3. The tab bar is re-rendered (not updated in-place) on each store change, so `active_tab` is a static prop on the new `dbc.Tabs` component, not an `Output`.

**Warning signs:** `Circular dependencies in the callback graph` error in the Dash console.

### Pitfall 5: Non-Numeric Data in Scorecard Calculations

**What goes wrong:** `df["cost_usd"].sum()` raises TypeError or returns incorrect totals when cells contain strings like "$ 2500 per ton".

**Why it happens:** Miscellaneous data has string-formatted costs. Electrical and Mechanical sections have numeric costs but may have occasional None or string values.

**How to avoid:** Always use `pd.to_numeric(df["cost_usd"], errors="coerce").sum(skipna=True)`. This silently converts non-numeric to NaN and skips them in the sum. Add a note in the scorecard footnote if any values were excluded.

**Warning signs:** Scorecard showing 0 or wildly incorrect totals.

### Pitfall 6: dbc.AccordionItem title Only Accepted Strings in Older dbc

**What goes wrong:** Passing a `html.Div` or `html.Span` as the `title` property of `dbc.AccordionItem` raises a component validation error.

**Why it happens:** Earlier versions of dbc only accepted strings as AccordionItem titles. This was fixed in dbc 1.0.0rc1.

**How to avoid:** With dbc 2.0.4 (the installed version), Dash components are supported as `title`. Safe to use. Confirmed by issue #717 resolution.

**Warning signs:** `Invalid prop` error mentioning AccordionItem title.

---

## Code Examples

Verified patterns from official sources and direct inspection:

### dbc.Tabs with System Color Active Indicator

```python
# Source: dbc docs style.py + community issue #86819 confirmed approach
from dash import html
import dash_bootstrap_components as dbc
from src.config import SYSTEM_COLORS

def make_system_tabs(active_system: str) -> dbc.Tabs:
    tab_defs = [
        ("mechanical", "Mechanical"),
        ("electrical", "Electrical"),
        ("hybrid", "Hybrid"),
    ]
    tabs = []
    for key, label in tab_defs:
        color = SYSTEM_COLORS[label]
        tabs.append(
            dbc.Tab(
                label=label,
                tab_id=key,
                label_style={"color": "#6c757d"},
                active_label_style={
                    "color": color,
                    "fontWeight": "bold",
                    "borderBottom": f"3px solid {color}",
                },
            )
        )
    return dbc.Tabs(tabs, id="system-tabs", active_tab=active_system, className="mb-3")
```

### Scorecard RAG Dot in Table Cell

```python
# Source: Confirmed pattern — html.Span with borderRadius produces CSS circle
from dash import html
from src.config import RAG_COLORS

def make_rag_dot(status: str) -> html.Span:
    """status: 'green' | 'yellow' | 'red'"""
    return html.Span(
        style={
            "display": "inline-block",
            "width": "12px",
            "height": "12px",
            "borderRadius": "50%",
            "backgroundColor": RAG_COLORS[status],
            "marginRight": "6px",
            "verticalAlign": "middle",
        }
    )

# Usage in table cell:
html.Td([make_rag_dot("green"), "$1.2M"], style={"textAlign": "center"})
```

### dbc.Accordion One-Item-Open at a Time

```python
# Source: dbc.Accordion docs — always_open=False is default; active_item controls which opens
import dash_bootstrap_components as dbc
from dash import html

accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            children=html.P("Equipment detail content here"),
            title="Wind Turbine — $1.2M",
            item_id="item-0",
        ),
        dbc.AccordionItem(
            children=html.P("Equipment detail content here"),
            title="Water Pump — $45K",
            item_id="item-1",
        ),
    ],
    id="equipment-accordion",
    active_item=None,    # none expanded initially
    always_open=False,   # close others when one opens (default)
)
```

### ctx.triggered_id for Multi-Input Callback

```python
# Source: dash.plotly.com/determining-which-callback-input-changed (Dash 2.4+)
from dash import callback, Input, Output, State, ctx, ALL

@callback(
    Output("active-system", "data"),
    Input({"type": "system-card-btn", "index": ALL}, "n_clicks"),
    Input("system-tabs", "active_tab"),
    State("active-system", "data"),
    prevent_initial_call=True,
)
def update_active_system(card_clicks, active_tab, current):
    triggered = ctx.triggered_id
    if triggered is None:
        return current
    # Dict ID = pattern-matching (landing card click)
    if isinstance(triggered, dict) and triggered.get("type") == "system-card-btn":
        return triggered["index"]
    # String ID = tab click
    return active_tab
```

### Landing Overview Card (System Selection)

```python
# Three clickable system overview cards — text only, colored header strip
from dash import html
import dash_bootstrap_components as dbc
from src.config import SYSTEM_COLORS

SYSTEM_DESCRIPTIONS = {
    "mechanical": "Uses wind-driven mechanical pumps to directly pressurize seawater through reverse osmosis membranes.",
    "electrical": "Converts wind energy to electricity to power pumps and support battery or tank storage for continuous operation.",
    "hybrid": "Combine components from both systems to create a custom desalination solution.",
}

def make_system_overview_card(system_key: str, label: str) -> dbc.Col:
    color = SYSTEM_COLORS[label]
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(
                label,
                className="fw-bold fs-5",
                style={"backgroundColor": color, "color": "white"},
            ),
            dbc.CardBody([
                html.P(SYSTEM_DESCRIPTIONS[system_key], className="text-muted"),
                dbc.Button(
                    "Explore",
                    id={"type": "system-card-btn", "index": system_key},
                    color="secondary",
                    outline=True,
                    size="sm",
                    className="mt-2",
                ),
            ]),
        ], className="h-100 shadow-sm"),
        width=4,
    )
```

---

## Critical Data Finding: No Process Stage Column, No Description Column

Both of these discoveries directly affect task scope:

1. **No process stage column in data.xlsx:** The equipment grid must be grouped by process stage (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal) but the data file has no such column. Stage assignment must be hard-coded. The planner must include a task to define `PROCESS_STAGES` mapping dict with the correct assignment for all ~10 electrical and ~9 mechanical equipment items.

2. **No description column in data.xlsx:** The equipment detail view (SEL-03) requires "detailed description" of each equipment item. This text does not exist in the data file. The planner must include a task to write brief (1-2 sentence) descriptions for all equipment items and store them in a `EQUIPMENT_DESCRIPTIONS` dict in `config.py`.

3. **No "efficiency" metric in data.xlsx:** The scorecard (SCORE-01) lists "efficiency" as a metric. The data has energy (kW) and cost and land area, but no efficiency value. Resolution: use total energy (kW) as the efficiency proxy metric. Lower energy = more efficient. Label it "Total Energy (kW)" on the scorecard to be transparent.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom accordion with `dbc.Collapse` + pattern-matching | `dbc.Accordion` with `active_item` | dbc 1.0 (2022) | Much simpler; built-in animation; accessibility |
| `dash.callback_context.triggered[0]["prop_id"]` string parsing | `ctx.triggered_id` dict | Dash 2.4 (2022) | Cleaner; no string splitting; pattern-match IDs come back as dicts |
| `import dash_core_components as dcc` | `from dash import dcc` | Dash 2.0 | Old import still works in 4.x but deprecated |
| `dbc.Tab(label="...", id="...")` | `dbc.Tab(label="...", tab_id="...")` | dbc 1.x | `tab_id` is the correct prop; `id` is for the tab panel wrapper |

---

## Open Questions

1. **Process stage assignment for all equipment items**
   - What we know: 5 stages required; ~9 mechanical, ~10 electrical items from data.xlsx
   - What's unclear: Which exact equipment items exist in each system (need to read actual DataFrame values)
   - Recommendation: The planner should create a task to print/inspect the actual equipment names from the loaded DataFrame and define the `PROCESS_STAGES` mapping. This is content work, not engineering work.

2. **Equipment description text**
   - What we know: No descriptions in data.xlsx; hard-coded dict is the only option
   - What's unclear: Whether brief descriptions are acceptable or if they need to be domain-accurate
   - Recommendation: Claude writes 1-2 sentence technically accurate descriptions for each equipment type. Flag for user review if accuracy is critical.

3. **"Efficiency" metric definition**
   - What we know: data.xlsx has no efficiency column; energy (kW) is available
   - What's unclear: Whether the instructor has a specific efficiency formula in mind
   - Recommendation: Use total energy (kW) as the proxy and label it clearly. Leave a TODO comment for the instructor to confirm or specify a different formula.

4. **"Back to Overview" breadcrumb placement**
   - What we know: It is a link/button, not a fourth tab
   - What's unclear: Exact location — above the tab bar? In the content area?
   - Recommendation (Claude's discretion): Place it above the tab bar as a small breadcrumb text: `← Overview` styled as a link. Clicking it sets `active-system` store to `None`.

---

## Sources

### Primary (HIGH confidence)
- Direct inspection of `data.xlsx` via openpyxl (Phase 1 research) — equipment columns and structure confirmed
- `src/config.py` in project — `SYSTEM_COLORS` and `RAG_COLORS` already defined
- `src/data/loader.py` — DataFrame structure and column names confirmed
- [Dash Pattern-Matching Callbacks official docs](https://dash.plotly.com/pattern-matching-callbacks) — `ctx.triggered_id`, `ALL`, `MATCH` patterns
- [dbc Tabs docs](https://www.dash-bootstrap-components.com/docs/components/tabs/) — `active_tab`, `tab_id`, `active_label_style` confirmed
- [dbc GitHub style.py example](https://github.com/dbc-team/dash-bootstrap-components/blob/main/docs/components_page/components/tabs/style.py) — `label_style`, `tab_style` usage confirmed

### Secondary (MEDIUM confidence)
- [dbc GitHub issue #86819](https://community.plotly.com/t/change-background-color-of-active-tab/86819) — `active_tab_style` backgroundColor bug confirmed by community
- [dbc GitHub PR #491](https://github.com/dbc-team/dash-bootstrap-components/pull/491) — `active_label_style` property added (merged Dec 2020)
- [dbc GitHub issue #717](https://github.com/dbc-team/dash-bootstrap-components/issues/717) — AccordionItem title accepts components in dbc 1.0.0rc1+
- [Dash determining-which-callback-input-changed docs](https://dash.plotly.com/determining-which-callback-input-changed) — `ctx.triggered_id` available from Dash 2.4; Dash 4.0 confirmed ≥ 2.4

### Tertiary (LOW confidence)
- Community forum post on custom accordion with pattern-matching (Show & Tell, 2022) — used only to confirm that `dbc.Accordion` is the superior alternative

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages; all Phase 1 packages verified
- Tab navigation pattern: HIGH — official dbc docs + confirmed code examples
- Accordion expand pattern: HIGH — dbc.Accordion with active_item is the documented approach
- Active tab color styling: MEDIUM — active_label_style confirmed but backgroundColor bug means workaround needed (borderBottom approach)
- Scorecard RAG table: HIGH — html.Table with embedded html.Span is standard Dash pattern
- Process stage / description content: LOW (engineering) / HIGH (pattern) — the pattern is clear; the actual content (which equipment belongs to which stage, what descriptions say) must be hand-crafted

**Research date:** 2026-02-21
**Valid until:** 2026-03-21 (stable Dash 4.0 / dbc 2.0.4 ecosystem)
