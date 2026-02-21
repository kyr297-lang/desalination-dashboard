# Architecture Research

**Domain:** Interactive multi-view Dash/Plotly dashboard (Python, academic data tool)
**Researched:** 2026-02-20
**Confidence:** HIGH — Verified against official Dash documentation and multiple authoritative community sources

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER (Client)                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  dash-renderer (React.js)                                │    │
│  │  ┌──────────┐  ┌───────────┐  ┌─────────────────────┐  │    │
│  │  │ Nav/Tabs │  │  Graphs   │  │  dcc.Store (state)  │  │    │
│  │  └──────────┘  └───────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         HTTP (JSON)                              │
├─────────────────────────────────────────────────────────────────┤
│                     PYTHON SERVER (Flask)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  app.py — Dash app init, root layout, startup data load  │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  pages/ — View layouts (one .py per major view)          │   │
│  │    system_selector.py                                    │   │
│  │    equipment_detail.py                                   │   │
│  │    hybrid_builder.py                                     │   │
│  │    comparison_graphs.py                                  │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  callbacks/ — Interactivity logic (per view)             │   │
│  │    hybrid_callbacks.py                                   │   │
│  │    graph_callbacks.py                                    │   │
│  │    scorecard_callbacks.py                                │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  data/ — Data loading and transformation                 │   │
│  │    loader.py  (reads data.xlsx once at startup)          │   │
│  │    models.py  (dataclasses or dicts for each system)     │   │
│  │    calculations.py (cost-over-time, land area calcs)     │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                                │
│  ┌────────────────┐                                              │
│  │  data.xlsx     │  (read-only, single source of truth)         │
│  │  - Electrical  │                                              │
│  │  - Mechanical  │                                              │
│  │  - Misc/Hybrid │                                              │
│  └────────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `app.py` | App init, root layout shell, dcc.Store, startup data load | `Dash(__name__)`, `app.layout`, `server = app.server` |
| `pages/` | View-specific layout (what users see per tab/view) | Functions returning `html.Div` trees |
| `callbacks/` | All interactivity logic — maps inputs to outputs | `@callback(Output(...), Input(...))` decorated functions |
| `data/loader.py` | Read data.xlsx into DataFrames at startup | `pd.read_excel()` called once at module level |
| `data/calculations.py` | Compute derived values (cost over time, totals, comparisons) | Pure functions that take DataFrames and parameters, return dicts/DataFrames |
| `data/models.py` | System data structures (mechanical, electrical, hybrid state) | Dataclasses or typed dicts holding equipment configs |
| `assets/` | Static CSS, images (optional but standard) | Automatically served by Dash from `/assets/` folder |

## Recommended Project Structure

```
app.py                    # Entry point — init, root layout, server export
data.xlsx                 # Source data (DO NOT rename — referenced by loader)
requirements.txt          # Python dependencies
pages/
    system_selector.py    # View 1: Choose mechanical / electrical / hybrid
    equipment_detail.py   # View 2: Parts list + specs for selected system
    hybrid_builder.py     # View 3: 5-slot builder interface
    comparison_graphs.py  # View 4: Side-by-side graphs (cost, land, turbines, pie)
callbacks/
    hybrid_callbacks.py   # Slot selection, completion gate, comparison text
    graph_callbacks.py    # Cost-over-time time horizon, battery/tank slider
    scorecard_callbacks.py# Red/yellow/green ranking computation
data/
    loader.py             # pd.read_excel() — called at startup, imported by callbacks
    calculations.py       # Cost-over-time, land totals, turbine counts, pie slices
    models.py             # System configs, slot definitions, equipment metadata
assets/
    custom.css            # Optional: academic color palette, font overrides
```

### Structure Rationale

- **`pages/`**: Each `.py` returns a layout function. Dash's `register_page(__name__)` registers the URL route automatically. Keeps layout definition separate from logic.
- **`callbacks/`**: Callbacks imported in `app.py` after layout is defined. Separating per feature area prevents any one file growing unwieldy.
- **`data/`**: The single `loader.py` module reads Excel once at startup. Calculations are pure functions — easy to test independently of Dash.
- **`assets/`**: Automatically served by Dash — drop in CSS and Dash picks it up without configuration.

## Architectural Patterns

### Pattern 1: Tabs-Based Single-Page Layout (recommended for this project)

**What:** All views live in one page as `dcc.Tabs` / `dbc.Tabs`. Navigation switches tab content in-memory without URL changes or state loss.

**When to use:** When views share state (e.g., a hybrid configuration built in one tab needs to appear in comparison graphs in another tab). Also simpler than Dash Pages for a focused academic tool.

**Trade-offs:** Simpler routing, state preserved across tab switches; no bookmarkable URLs. For this project, preserving the user's hybrid slot selections when switching to graphs is critical — tabs are the right choice over `dash.pages`.

**Example:**
```python
# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand="Wind Desalination Dashboard", color="primary", dark=True),
    dbc.Container([
        dcc.Tabs(id="main-tabs", value="system-selector", children=[
            dcc.Tab(label="System Overview",   value="system-selector"),
            dcc.Tab(label="Equipment Detail",  value="equipment-detail"),
            dcc.Tab(label="Build Hybrid",      value="hybrid-builder"),
            dcc.Tab(label="Compare Systems",   value="comparison"),
        ]),
        html.Div(id="tab-content"),
        # Global state store — lives in root layout, persists across tab switches
        dcc.Store(id="hybrid-config-store", storage_type="memory"),
        dcc.Store(id="selected-system-store", storage_type="memory"),
    ])
])
```

### Pattern 2: Module-Level Data Loading

**What:** Read `data.xlsx` once when the Python module first imports, not inside a callback. Store as module-level DataFrames that callbacks reference as read-only.

**When to use:** Always, for static data files. This project's data.xlsx does not change at runtime.

**Trade-offs:** Startup takes a moment to load; data is shared across all users (safe because read-only). If data.xlsx changed at runtime, you would need a different approach — but for this academic tool it does not.

**Example:**
```python
# data/loader.py
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data.xlsx"

# Load once at import time — all callbacks reference these directly
df_electrical   = pd.read_excel(DATA_PATH, sheet_name="Electrical Components")
df_mechanical   = pd.read_excel(DATA_PATH, sheet_name="Mechanical Components")
df_misc         = pd.read_excel(DATA_PATH, sheet_name="Miscellaneous")
df_battery_tradeoff = pd.read_excel(DATA_PATH, sheet_name="Electrical Components",
                                     header=...) # battery fraction rows
```

### Pattern 3: dcc.Store for Cross-Tab State

**What:** The user's hybrid slot selections and chosen time horizon live in a `dcc.Store` component placed in the root layout (not inside any tab). Callbacks read from and write to the Store.

**When to use:** Any time data must survive a tab switch, or when multiple callbacks need the same derived state. For this project: hybrid slot configuration, battery/tank slider value, selected time horizon.

**Trade-offs:** Data must be JSON-serializable; large DataFrames should not be stored (store indices or computed summary dicts instead). Storage type `"memory"` is correct for a session-scoped academic tool — no persistence across page refresh needed.

**Example:**
```python
# callbacks/hybrid_callbacks.py
from dash import callback, Output, Input, State, no_update
from data.loader import df_misc

@callback(
    Output("hybrid-config-store", "data"),
    Input("slot-water-extraction", "value"),
    Input("slot-pre-treatment",    "value"),
    Input("slot-desalination",     "value"),
    Input("slot-post-treatment",   "value"),
    Input("slot-brine-disposal",   "value"),
)
def update_hybrid_config(water_ext, pre_treat, desal, post_treat, brine):
    return {
        "water_extraction": water_ext,
        "pre_treatment":    pre_treat,
        "desalination":     desal,
        "post_treatment":   post_treat,
        "brine_disposal":   brine,
    }

@callback(
    Output("hybrid-detail-panel", "children"),
    Output("hybrid-complete-gate", "style"),
    Input("hybrid-config-store", "data"),
)
def render_hybrid_detail(config):
    all_filled = all(v is not None for v in config.values())
    gate_style = {"display": "none"} if all_filled else {"display": "block"}
    # Build detail panel only when complete
    ...
```

### Pattern 4: One Callback Per Logical Interaction

**What:** Each distinct user interaction (slider move, tab change, dropdown select) owns one callback. A single callback can output to multiple components but should serve one cohesive purpose.

**When to use:** Always. Avoid "god callbacks" that accept 10 inputs and update 8 outputs based on complex conditional branching.

**Trade-offs:** More callbacks = slightly more HTTP overhead; but readability and debuggability are worth it at this project's scale.

**Example:**
```python
# Single callback updating all comparison graphs when time horizon changes
@callback(
    Output("cost-over-time-graph",  "figure"),
    Output("land-area-graph",       "figure"),
    Output("turbine-count-graph",   "figure"),
    Output("energy-pie-chart",      "figure"),
    Input("time-horizon-slider",    "value"),
    Input("battery-fraction-slider","value"),
    State("hybrid-config-store",    "data"),
)
def update_all_comparison_graphs(years, battery_fraction, hybrid_config):
    ...
    return fig_cost, fig_land, fig_turbines, fig_pie
```

## Data Flow

### Startup Flow

```
python app.py
    |
    +--> data/loader.py imports
    |       pd.read_excel("data.xlsx")  [once]
    |       df_electrical, df_mechanical, df_misc available in memory
    |
    +--> app.layout built (tabs, dcc.Store, NavBar)
    |
    +--> All @callbacks registered (from callbacks/ imports)
    |
    +--> Flask dev server starts on localhost:8050
```

### User Interaction Flow (Tab Switch)

```
User clicks "Compare Systems" tab
    |
    +--> dcc.Tabs Input fires
    |
    +--> Tab content callback renders comparison_graphs layout
    |
    +--> Graph callbacks fire (initial_call) with current Store values
    |       Read df_electrical, df_mechanical from loader.py
    |       Read hybrid-config-store for hybrid system
    |       Call calculations.compute_cost_over_time(df, years)
    |       Return Plotly Figure objects
    |
    +--> Graphs rendered in browser
```

### Hybrid Builder Flow

```
User selects part in "Desalination" slot dropdown
    |
    +--> update_hybrid_config callback fires
    |       Aggregates all 5 slot values into dict
    |       Writes to hybrid-config-store
    |
    +--> render_hybrid_detail callback fires (Store changed)
    |       Checks if all 5 slots filled
    |       If NOT complete: shows "fill all slots" gate message
    |       If complete: renders equipment detail panel
    |
    +--> (Later, when user switches to Compare tab)
         graph callbacks read hybrid-config-store
         Hybrid system appears in side-by-side comparison
```

### Battery/Tank Slider Flow

```
User drags battery fraction slider (0% to 100%)
    |
    +--> update_all_comparison_graphs callback fires
    |       Reads battery fraction value
    |       Looks up matching row in df_battery_tradeoff (11-row table)
    |       Recomputes cost, land for electrical system
    |       Returns updated figures for all 4 graphs
    |
    +--> All comparison graphs re-render simultaneously
```

### State Management Summary

```
dcc.Store("hybrid-config-store")    -- Which parts fill each hybrid slot
dcc.Store("selected-system-store")  -- Which preset system is active (mech/elec)
dcc.Store("time-horizon-store")     -- NOT needed: slider value passed directly as Input

State flows:
  hybrid_builder page → hybrid-config-store → comparison_graphs page
  battery_slider Input → update_all_comparison_graphs callback → all graphs Output
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 1 local user | Current flat structure is perfect — no changes needed |
| 5-20 students simultaneously | Add `gunicorn` with 2-4 workers; module-level data loading is safe (read-only) |
| 50+ concurrent users | Add Flask-Caching (filesystem or Redis) for computed figures; module-level DataFrames already handle this well |
| Production hosted (Render/Railway) | Use `server = app.server` export; add `gunicorn app:server` Procfile |

### Scaling Priorities

1. **First bottleneck:** Callback latency on `update_all_comparison_graphs` if calculations are slow — fix by caching computed DataFrames with `@cache.memoize()` from Flask-Caching (not needed for this project's scale).
2. **Second bottleneck:** Memory if df_misc grows large — not a concern for a fixed spreadsheet; Excel files under 10MB are fine in module-level variables.

## Anti-Patterns

### Anti-Pattern 1: Modifying Global Variables in Callbacks

**What people do:** Store user state in a module-level Python dict or list, then mutate it inside a callback.

**Why it's wrong:** In multi-worker deployments (gunicorn), each worker has its own memory. Worker A's mutation is invisible to Worker B. Even in single-worker dev mode, all concurrent users share and corrupt each other's state.

**Do this instead:** Use `dcc.Store` for all user-specific state. The Store lives in the browser and is session-isolated.

### Anti-Pattern 2: Tabs-inside-Dash-Pages Hybrid

**What people do:** Use `dash.pages` for top-level routing AND `dcc.Tabs` inside pages, then try to share state across page navigations.

**Why it's wrong:** Dash Pages destroys and recreates page layouts on navigation. State in `dcc.Store` components inside a page is lost when you leave that page. Cross-page state sharing requires the Store to be in the root `app.layout`, which conflicts with the Pages pattern.

**Do this instead:** For this project, use Tabs only (no Dash Pages). All views as tabs in a single-page layout; root-level `dcc.Store` components persist state across tab switches without any special handling.

### Anti-Pattern 3: Chaining Callbacks Across Files

**What people do:** Callback in `hybrid_callbacks.py` outputs to a component that becomes the input of a callback defined in `graph_callbacks.py`, creating an invisible dependency chain across files.

**Why it's wrong:** Hard to trace, debug, or test. When a graph doesn't update, you have to trace across files to find where the chain broke.

**Do this instead:** Use `dcc.Store` as the explicit handoff point between subsystems. The hybrid builder writes to `hybrid-config-store`; graph callbacks read from `hybrid-config-store`. The Store is the declared contract, not an implicit component ID dependency.

### Anti-Pattern 4: suppress_callback_exceptions=True

**What people do:** Set `app = Dash(__name__, suppress_callback_exceptions=True)` globally to silence errors about missing component IDs, often because they have dynamic layouts.

**Why it's wrong:** This hides real bugs. If a component ID in a callback no longer exists in the layout, you want an error, not silent failure.

**Do this instead:** Use `allow_optional=True` on specific `Input`/`State` objects for genuinely optional components, or structure layouts so required components always exist (even if hidden via `display: none`).

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| `data.xlsx` | `pd.read_excel()` at module load in `data/loader.py` | Use `openpyxl` engine; specify `sheet_name` explicitly |
| Render/Railway deployment | `server = app.server` in `app.py`; `gunicorn app:server` Procfile | No code changes needed; same file runs locally and in cloud |
| Dash Bootstrap Components | `external_stylesheets=[dbc.themes.BOOTSTRAP]` in `Dash()` init | Provides Grid, Card, Navbar, Tabs with Bootstrap styling |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `data/` module ↔ `callbacks/` | Direct import (`from data.loader import df_electrical`) | DataFrames are read-only; safe to share across callbacks |
| `pages/` layout ↔ `callbacks/` | Component `id=` strings act as the contract | IDs must match exactly; define ID constants in a shared `ids.py` if they proliferate |
| Tab views ↔ Tab views | `dcc.Store` in root layout | Never communicate directly; always through Store |
| Hybrid builder ↔ Comparison graphs | `hybrid-config-store` Store | Hybrid writes, graphs read; decoupled |

## Build Order Implications

The architecture implies this construction sequence:

1. **Data layer first** (`data/loader.py`, `data/calculations.py`) — callbacks depend on data functions; build and test data loading before any UI.
2. **Root layout shell** (`app.py`) — tabs structure, dcc.Store components, NavBar. No callbacks yet.
3. **Static view layouts** (`pages/equipment_detail.py`, `pages/system_selector.py`) — layouts only, no interactivity; verify visual structure.
4. **Simple callbacks** (`scorecard_callbacks.py`) — single input, single output; builds callback confidence before complex chains.
5. **Hybrid builder** (`pages/hybrid_builder.py` + `callbacks/hybrid_callbacks.py`) — most complex stateful interaction; requires Store pattern working correctly.
6. **Comparison graphs** (`pages/comparison_graphs.py` + `callbacks/graph_callbacks.py`) — reads from Store; only buildable after hybrid builder populates it.
7. **Battery/tank slider** (extension of graph callbacks) — modifies electrical system calculation; final interactive layer.

## Sources

- [Dash Multi-Page Apps and URL Support — official docs](https://dash.plotly.com/urls) — HIGH confidence
- [Sharing Data Between Callbacks — official docs](https://dash.plotly.com/sharing-data-between-callbacks) — HIGH confidence
- [Dash App Lifecycle — official docs](https://dash.plotly.com/app-lifecycle) — HIGH confidence
- [All-in-One Components — official docs](https://dash.plotly.com/all-in-one-components) — HIGH confidence
- [Advanced Callbacks — official docs](https://dash.plotly.com/advanced-callbacks) — HIGH confidence
- [Dash callbacks best practices — dash-resources.com](https://dash-resources.com/dash-callbacks-best-practices-with-examples/) — MEDIUM confidence (community, verified against official docs)
- [Multi-page apps or tabs discussion — Plotly Community Forum](https://community.plotly.com/t/multi-page-apps-or-tabs/40813) — MEDIUM confidence (community consensus)
- [Plotly Dash Structured Multi-Page Dashboard — Towards Data Science / Medium (Nov 2025)](https://medium.com/data-science-collective/plotly-dash-a-structured-framework-for-a-multi-page-dashboard-16151a99bbb7) — MEDIUM confidence (community article, recent)
- [Dash Bootstrap Components docs](https://dash-bootstrap-components.opensource.faculty.ai/) — HIGH confidence

---
*Architecture research for: Wind-Powered Desalination Dashboard (Dash/Plotly, Python)*
*Researched: 2026-02-20*
