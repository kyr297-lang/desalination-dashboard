# Phase 1: Foundation - Research

**Researched:** 2026-02-21
**Domain:** Python Dash/Plotly app scaffolding, Excel data parsing, app shell layout
**Confidence:** HIGH (stack well-documented; data.xlsx directly inspected)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**System colors:**
- Academic muted palette — soft, professional tones suitable for academic paper charts
- Cohesive palette — colors should look good together and be distinguishable, no specific semantic associations required
- Colorblind accessibility is nice to have but not a hard requirement
- RAG scorecard indicators (red/yellow/green) use separate standard traffic-light colors, independent from system palette

**App shell structure:**
- Sidebar navigation layout — dashboard-style with sidebar and main content area
- Sidebar only shows nav items for features that are actually built (grows as phases complete)
- Sidebar is collapsible — toggle button to show/hide, giving more room for charts
- Top header bar with project title (e.g., "Wind-Powered Desalination Dashboard")

**Data validation UX:**
- Silent success — if data loads fine, just show the app with no success message
- Full-page error on failure — if data.xlsx is missing or a sheet fails to parse, show a clear error page and render nothing else
- Error messages show both levels: high-level message for students, expandable "Details" section with specifics (which sheet, which column/row)
- Also log validation info to the terminal/console for whoever launched `python app.py`

**Tech stack:**
- Dash (Plotly) framework — interactive dashboard with callback-driven chart interactions
- dash-bootstrap-components with FLATLY theme — clean, flat, professional academic styling
- Auto-open browser tab when `python app.py` is run

### Claude's Discretion

- Exact muted color values for the three systems
- Sidebar width and toggle button design
- Error page layout and styling
- Project file structure and module organization
- Dash app configuration details

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DATA-01 | App loads and parses data.xlsx at startup (Electrical, Mechanical, Miscellaneous sheets) | Data file inspected: single "Sheet1" with three embedded sections; parsing strategy documented below |
| DATA-02 | Data validation ensures all three sheets parse correctly before rendering UI | openpyxl row-range parsing approach identified; validation hook pattern documented |
| DATA-03 | Consistent color mapping per system (Mechanical/Electrical/Hybrid) across all charts | Python dict pattern for color map; academic muted palette values recommended |
| DEP-01 | App runs locally via `python app.py` with no external service dependencies | Dash `app.run()` + `webbrowser`/`threading.Timer` pattern documented |
</phase_requirements>

---

## Summary

Phase 1 establishes the data layer and app shell. The Dash 4.0 / dash-bootstrap-components 2.x stack is confirmed as the correct choice for this project. The standard pattern — `app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])` with a fixed sidebar and `dcc.Store` for shared state — is well-established in the community and requires no custom solutions.

**Critical discovery: data.xlsx is a single sheet, not three.** The file contains one sheet named "Sheet1" with three logically separate sections stacked vertically (Electrical rows 1–14, Mechanical rows 15–25, Miscellaneous rows 27–33). The requirements describe "three Excel sheets" but the actual file uses section headers within one sheet. The parser must locate these sections by scanning for their header rows rather than switching sheets. Several cells also contain non-numeric data that requires explicit handling: "indefinite" lifespans, "~15 tons" quantities, and string-formatted costs like "$ 2500 per ton". The battery/tank lookup table lives at columns J–P, rows 3–14, co-located with the Electrical section.

**Primary recommendation:** Use openpyxl directly (not pandas `read_excel`) to scan Sheet1 for section headers by name, then slice rows into DataFrames manually. This gives full control over the non-standard structure and makes validation precise.

---

## Critical Finding: Actual data.xlsx Structure

**REQUIREMENT MISMATCH — Must be resolved in planning.**

The REQUIREMENTS.md and ROADMAP.md say "All three Excel sheets (Electrical, Mechanical, Miscellaneous)". The actual file has **one sheet** named "Sheet1" with three embedded sections:

| Section | Header Row | Data Rows | Total Row | Notes |
|---------|-----------|-----------|-----------|-------|
| Electrical Components | Row 1 | Rows 2–11 | Row 12 | Battery/tank lookup at cols J–P, rows 3–14 |
| Mechanical Components | Row 15 | Rows 16–24 | Row 25 | |
| Miscellaneous | Row 27 | Rows 28–33 | (none) | Row 33 is a note merged across cols A–G |

**Battery/Tank Lookup Table** (col J=Battery Fraction, K=Tank Fraction, L=Battery kWh, M=Tank Gal, N=Battery Cost, O=Tank Cost, P=Total Cost):
- Rows 4–14: 11 rows, Battery Fraction 0.0 to 1.0 in 0.1 steps
- Header labels at row 3 (cols J–P)

**Data Quality Issues Confirmed:**
- `Quantity`: Row 28 (Activated carbon) = `'~15 tons'` (string)
- `Cost`: Row 28 = `'$ 2500 per ton'`, Row 32 (Antiscalant) = `'$50000/year'` (strings)
- `Lifespan`: Rows 10 and 30 = `'indefinite'`, Row 32 = `'~9 containers per year'` (strings)
- Row 33 is a free-text note (merged cells A32:A33, etc.) — not equipment data
- Row 9 (Multi-Media Filtration): Quantity is `None` (blank)

The loader must handle all of these without crashing. String costs and quantities should be stored as-is (they are descriptive, not for calculation). "indefinite" lifespan should be preserved as a string or mapped to a sentinel value.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash | 4.0.0 | Web app framework, callback system, component tree | Current stable (Feb 3, 2025); standard for Python dashboards |
| plotly | (bundled with dash) | Chart rendering engine | Included when you install dash |
| dash-bootstrap-components | 2.0.4 (latest) | Bootstrap layout, FLATLY theme, nav components | Requires `dash>=3.0.4`; 2.x is latest stable as of Aug 2025 |
| openpyxl | 3.1.5 | Excel file reading | Already installed; required by pandas for .xlsx |
| pandas | 2.3.3 | DataFrame manipulation after parsing | Already installed; used post-parse for calculations |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| dash-bootstrap-templates | latest | Applies Bootstrap theme colors to Plotly figures | Use if chart colors should match the FLATLY theme palette |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| openpyxl (direct) | pandas `read_excel` with skiprows/nrows | pandas simpler but less control over non-standard structure; openpyxl is clearer for section-based parsing |
| Fixed sidebar | dbc.Offcanvas | Offcanvas is overlay-style (mobile-first); fixed sidebar is better for desktop academic tool |
| threading.Timer for browser | subprocess.Popen | Timer is standard and sufficient; subprocess adds complexity |

**Installation:**
```bash
pip install dash dash-bootstrap-components openpyxl pandas
```

Note: `dash` 4.0.0 was released Feb 3, 2025. `dash-bootstrap-components` 2.0.4 requires `dash>=3.0.4`. Both are compatible. Verify with `pip show dash dash-bootstrap-components` after install.

---

## Architecture Patterns

### Recommended Project Structure

```
project_root/
├── app.py                  # Entry point: creates app, opens browser, runs server
├── data.xlsx               # Data source (exists — do not move)
├── requirements.txt        # Pin versions for reproducibility
├── assets/                 # Dash auto-serves files here (CSS, favicon)
│   └── custom.css          # Override sidebar/header styles if needed
└── src/
    ├── __init__.py
    ├── data/
    │   ├── __init__.py
    │   ├── loader.py       # Reads Sheet1, slices sections into DataFrames
    │   └── validator.py    # Validates parsed data, raises structured errors
    ├── layout/
    │   ├── __init__.py
    │   ├── shell.py        # App shell: header, sidebar, content wrapper
    │   └── error_page.py   # Full-page error component
    └── config.py           # SYSTEM_COLORS, DATA_FILE path, constants
```

The `data/loader.py` runs once at module import time (not inside callbacks). Its output — three DataFrames and the battery lookup table — is module-level state that callbacks reference as read-only. This matches the documented architectural decision in STATE.md: "Load data.xlsx once at module startup as immutable DataFrames — never inside callbacks."

### Pattern 1: Section-Based Excel Parsing

**What:** Scan Sheet1 row by row looking for section header cells, then slice subsequent rows into DataFrames with explicit column mappings.

**When to use:** When Excel data is structured as stacked sections within one sheet rather than separate sheets.

**Example:**
```python
# src/data/loader.py
import openpyxl
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent.parent / "data.xlsx"

COLUMNS = ["name", "quantity", "cost_usd", "energy_kw", "land_area_m2", "lifespan_years"]

SECTION_HEADERS = {
    "Electrical Components": "electrical",
    "Mechanical Components": "mechanical",
    "Miscalleneous": "miscellaneous",   # Note: typo in actual file
}

def _parse_section(ws, header_row: int, stop_rows: set) -> list[dict]:
    """Parse equipment rows from header_row+1 until a blank name or stop row."""
    rows = []
    for r in range(header_row + 1, ws.max_row + 1):
        if r in stop_rows:
            break
        name = ws.cell(r, 2).value
        if name is None or name == "Total":
            continue
        rows.append({
            "name": name,
            "quantity": ws.cell(r, 3).value,   # may be None or string
            "cost_usd": ws.cell(r, 4).value,   # may be string
            "energy_kw": ws.cell(r, 5).value,
            "land_area_m2": ws.cell(r, 6).value,
            "lifespan_years": ws.cell(r, 7).value,  # may be 'indefinite'
        })
    return rows

def load_data() -> dict:
    """
    Returns:
        {
          "electrical": pd.DataFrame,
          "mechanical": pd.DataFrame,
          "miscellaneous": pd.DataFrame,
          "battery_lookup": pd.DataFrame,
        }
    Raises: FileNotFoundError, ValueError (with context on which section failed)
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"data.xlsx not found at {DATA_PATH}")

    wb = openpyxl.load_workbook(DATA_PATH)
    ws = wb["Sheet1"]

    # Locate section header rows
    section_row_map = {}
    for row in ws.iter_rows(min_col=2, max_col=2):
        cell = row[0]
        if cell.value in SECTION_HEADERS:
            section_row_map[SECTION_HEADERS[cell.value]] = cell.row

    required = {"electrical", "mechanical", "miscellaneous"}
    missing = required - set(section_row_map.keys())
    if missing:
        raise ValueError(f"Missing sections in Sheet1: {missing}")

    # Parse each section
    elec_start = section_row_map["electrical"]
    mech_start = section_row_map["mechanical"]
    misc_start = section_row_map["miscellaneous"]

    electrical_rows = _parse_section(ws, elec_start, stop_rows={mech_start})
    mechanical_rows = _parse_section(ws, mech_start, stop_rows={misc_start})
    miscellaneous_rows = _parse_section(ws, misc_start, stop_rows=set())

    # Battery/tank lookup: header at row 3 (col J=10), data rows 4-14
    battery_rows = []
    for r in range(4, 15):  # rows 4–14 inclusive
        battery_rows.append({
            "battery_fraction": ws.cell(r, 10).value,
            "tank_fraction": ws.cell(r, 11).value,
            "battery_kwh": ws.cell(r, 12).value,
            "tank_gal": ws.cell(r, 13).value,
            "battery_cost": ws.cell(r, 14).value,
            "tank_cost": ws.cell(r, 15).value,
            "total_cost": ws.cell(r, 16).value,
        })

    return {
        "electrical": pd.DataFrame(electrical_rows),
        "mechanical": pd.DataFrame(mechanical_rows),
        "miscellaneous": pd.DataFrame(miscellaneous_rows),
        "battery_lookup": pd.DataFrame(battery_rows),
    }
```

### Pattern 2: Startup Validation Gate

**What:** Call `load_data()` at module level in `app.py`. If it raises, catch the exception and replace the app layout with a full-page error component. If it succeeds, proceed with normal layout. Never call `load_data()` inside a callback.

**Example:**
```python
# app.py
import sys
import threading
import webbrowser
from src.data.loader import load_data
from src.layout.shell import create_layout
from src.layout.error_page import create_error_page

try:
    DATA = load_data()
    print("[OK] data.xlsx loaded — all sections parsed successfully")
except (FileNotFoundError, ValueError) as e:
    print(f"[ERROR] Failed to load data.xlsx: {e}", file=sys.stderr)
    DATA = None

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

if DATA is None:
    app.layout = create_error_page(error=str(e))
else:
    app.layout = create_layout(DATA)

if __name__ == "__main__":
    port = 8050
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(debug=False, port=port)
```

### Pattern 3: Sidebar with Collapsible Toggle

**What:** Fixed-width sidebar using `dbc.Nav` with `dcc.Store` to persist collapse state. A callback toggles a CSS class or style dict.

**When to use:** Whenever persistent desktop sidebar navigation is needed.

**Example:**
```python
# src/layout/shell.py
import dash_bootstrap_components as dbc
from dash import html, dcc

SIDEBAR_WIDTH = "220px"
SIDEBAR_COLLAPSED_WIDTH = "0px"

def create_layout(data):
    sidebar = html.Div(
        id="sidebar",
        children=[
            html.H6("Navigation", className="sidebar-heading"),
            dbc.Nav(
                [
                    dbc.NavLink("Overview", href="/", active="exact"),
                    # Future phases add nav items here
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={
            "width": SIDEBAR_WIDTH,
            "minHeight": "100vh",
            "padding": "1rem",
            "backgroundColor": "#f8f9fa",
            "transition": "width 0.2s",
            "overflow": "hidden",
        },
    )

    header = dbc.Navbar(
        dbc.Container([
            html.Button("☰", id="sidebar-toggle", className="me-3"),
            html.Span("Wind-Powered Desalination Dashboard", className="navbar-brand"),
        ], fluid=True),
        color="primary",
        dark=True,
        className="mb-0",
    )

    return html.Div([
        dcc.Store(id="sidebar-collapsed", data=False),
        header,
        html.Div([sidebar, html.Div(id="page-content", style={"flex": 1, "padding": "1.5rem"})],
                 style={"display": "flex"}),
    ])
```

### Pattern 4: System Color Map

**What:** A module-level dict mapping system names to hex colors. Defined once in `config.py`, imported everywhere.

**Example:**
```python
# src/config.py

# Academic muted palette (Claude's discretion — picked from Okabe-Ito accessible palette,
# desaturated for academic paper feel)
SYSTEM_COLORS = {
    "Mechanical": "#5B8DB8",   # muted steel blue
    "Electrical": "#D4854A",   # muted terra cotta / burnt orange
    "Hybrid":     "#6BAA75",   # muted sage green
}

# Used in Plotly figures:
# fig.update_traces(marker_color=SYSTEM_COLORS["Mechanical"])
# Or in discrete color sequence for px charts:
# color_discrete_map=SYSTEM_COLORS
```

Color choice rationale: These three are visually distinct, work well together, are readable on white academic backgrounds, and are distinguishable by most forms of colorblindness (blue/orange/green is a standard accessible triad). They are not primary-bright, fitting the "muted academic" constraint.

### Anti-Patterns to Avoid

- **Calling `load_data()` inside a Dash callback:** Reads the file on every interaction. Load once at startup.
- **Using `pd.read_excel()` with `skiprows/nrows` for this file:** Works but requires knowing exact row numbers at coding time; fragile if rows shift. Section-header scanning is more robust.
- **Using `app.run(debug=True)` in production or with auto-browser-open:** Debug mode causes double-execution of startup code (Flask reloader), which fires `webbrowser.open()` twice and opens two tabs. Use `debug=False` for the auto-open pattern, or guard with `if os.environ.get("WERKZEUG_RUN_MAIN") != "true"`.
- **Storing DataFrames in `dcc.Store`:** Serializes to JSON on every callback. Module-level globals are the right approach for read-only startup data.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Bootstrap layout/grid | Custom CSS flex grid | `dbc.Row`, `dbc.Col`, `dbc.Container` | Bootstrap 5 handles breakpoints, spacing, alignment |
| Sidebar nav | Custom `<nav>` with `<a>` tags | `dbc.Nav`, `dbc.NavLink` | Active state, accessibility, Bootstrap styling built-in |
| Theme application | Custom CSS overrides | `dbc.themes.FLATLY` in `external_stylesheets` | Applies consistent Bootstrap tokens across all dbc components |
| Error display | Raw Python `print` to page | `dbc.Alert` or full error layout component | Proper Dash component tree; allows styling |
| Browser auto-open | Custom server polling | `threading.Timer` + `webbrowser.open` | Established community pattern; simple and reliable |

**Key insight:** dash-bootstrap-components eliminates nearly all custom CSS for structure. The FLATLY theme is selected once and applies everywhere. Resist the temptation to write custom layout CSS beyond minor overrides.

---

## Common Pitfalls

### Pitfall 1: Assuming Three Separate Excel Sheets

**What goes wrong:** Code does `wb["Electrical"]`, `wb["Mechanical"]`, `wb["Miscellaneous"]` — all raise `KeyError` because the actual sheet name is `"Sheet1"`.

**Why it happens:** Requirements say "three sheets" but the file uses one sheet with section headers.

**How to avoid:** Always scan for section headers within `Sheet1`. Use the approach shown in Pattern 1 above. Document the actual file structure in a code comment so future maintainers understand.

**Warning signs:** `KeyError: 'Electrical'` or `KeyError: 'Mechanical'` on first run.

### Pitfall 2: Non-Numeric Data in Numeric Columns

**What goes wrong:** Code does `float(row["cost_usd"])` — crashes on "$ 2500 per ton", "$50000/year".

**Why it happens:** The Miscellaneous section has two items with string-formatted costs/quantities that are descriptive rather than calculable values.

**How to avoid:** Store these as-is (strings). When computing totals or charts, filter to rows where the field is numeric using `pd.to_numeric(df["cost_usd"], errors="coerce")`. The Phase 1 loader just needs to store them faithfully — downstream phases handle calculation.

**Warning signs:** `ValueError: could not convert string to float` during parsing.

### Pitfall 3: Auto-Browser-Open Fires Twice in Debug Mode

**What goes wrong:** `webbrowser.open()` opens two browser tabs.

**Why it happens:** Dash's `debug=True` activates Flask's reloader, which runs `app.py` twice (parent process + reloader child).

**How to avoid:** Use `debug=False` in `app.run()` for the v1 local deployment, or guard with:
```python
import os
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.server.debug:
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
```

**Warning signs:** Two browser tabs open on startup.

### Pitfall 4: Dash 4.0 dcc.Dropdown `optionHeight` Default Change

**What goes wrong:** Dropdown option rows look different than expected if you relied on fixed-pixel height.

**Why it happens:** Dash 4.0 changed `optionHeight` default from a fixed pixel value to `'auto'`.

**How to avoid:** Phase 1 doesn't use dcc.Dropdown. Note for Phase 2 planning.

### Pitfall 5: Missing `assets/` Folder for CSS

**What goes wrong:** Custom CSS file is not served; sidebar styling breaks.

**Why it happens:** Dash only auto-serves files from the `assets/` directory in the same folder as `app.py`. Files in subdirectories are not picked up automatically.

**How to avoid:** Place `assets/custom.css` at `project_root/assets/custom.css`. No additional config needed — Dash discovers and serves it automatically.

---

## Code Examples

Verified patterns from official documentation and direct inspection:

### Dash App Initialization with FLATLY Theme
```python
# Source: https://www.dash-bootstrap-components.com/docs/themes/
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
)
```

### Auto-Open Browser on Startup
```python
# Source: community.plotly.com/t/auto-open-browser-window-with-dash/31948
import threading
import webbrowser

PORT = 8050

def open_browser():
    webbrowser.open(f"http://127.0.0.1:{PORT}")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, port=PORT)
```

### Pandas-Compatible Numeric Coercion for Mixed Columns
```python
# Converts numeric values to float, leaves strings as NaN (not crash)
import pandas as pd

df["cost_numeric"] = pd.to_numeric(df["cost_usd"], errors="coerce")
df["qty_numeric"] = pd.to_numeric(df["quantity"], errors="coerce")
```

### dcc.Store for Cross-Tab Shared State
```python
# Source: STATE.md architectural decision — "Use tabs over Dash Pages to preserve dcc.Store cross-tab state"
# dcc.Store at app level (not inside a tab) persists across tab switches
from dash import dcc

# Place in app.layout at top level, before the tab component
dcc.Store(id="system-data-store", storage_type="memory")
```

### Full-Page Error Layout Pattern
```python
# src/layout/error_page.py
import dash_bootstrap_components as dbc
from dash import html

def create_error_page(error: str, details: str = "") -> html.Div:
    return html.Div(
        dbc.Container([
            dbc.Row(dbc.Col([
                html.H2("Unable to Load Dashboard", className="text-danger mt-5"),
                html.P("The dashboard could not start because the data file could not be read."),
                dbc.Alert(error, color="danger"),
                dbc.Accordion([
                    dbc.AccordionItem(
                        html.Pre(details, style={"fontSize": "0.85em"}),
                        title="Details (for technical users)",
                    )
                ], start_collapsed=True) if details else html.Div(),
            ], width=8), justify="center"),
        ], fluid=True),
        style={"minHeight": "100vh", "paddingTop": "5rem"},
    )
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `import dash_core_components as dcc` | `from dash import dcc` | Dash 2.0 | Old import still works in 4.x but deprecated |
| `import dash_html_components as html` | `from dash import html` | Dash 2.0 | Same |
| `app.run_server()` | `app.run()` | Dash 2.x | `run_server()` still works as alias |
| `dash_bootstrap_components` v0.x (Bootstrap 4) | `dash_bootstrap_components` v1+/2.x (Bootstrap 5) | dbc v1.0 | Bootstrap 5 syntax; some component props renamed |
| `dcc.Tab` labels must be strings | `dcc.Tab` labels can be Dash components | Dash 4.0 | More flexible tab headers (not relevant to Phase 1) |

**Deprecated/outdated:**
- `dash_core_components` as separate package: Merged into `dash`. Installing separately is unnecessary.
- `dash_html_components` as separate package: Same — merged into `dash`.
- `app.run_server(debug=True)`: Works but `app.run()` is the current API.

---

## Open Questions

1. **Row 33 Note Text** — Row 33 ("55 gallon container is 2500 USD...") spans merged cells and describes Antiscalant. The loader needs to decide: skip it entirely (it's not equipment data) or store it as a `description` field on the Antiscalant row. Phase 2 will need description text for the equipment detail view; storing it now avoids re-parsing later. Recommendation: skip it in Phase 1; address when the equipment detail view is built in Phase 2.

2. **Miscellaneous Cost Calculation** — Activated carbon ("~15 tons" at "$2500/ton") and Antiscalant ("$50000/year") have costs that cannot be summed directly. The hybrid builder (Phase 4) will need to handle these. Phase 1 just needs to store them faithfully as strings. No action needed in Phase 1, but flag for Phase 4 planning.

3. **"indefinite" Lifespan** — Brine Well (Electrical) and Evaporation Pond (Miscellaneous) have `'indefinite'` lifespans. For the lifespan display in Phase 2 and cost-over-time calculations in Phase 3, this needs a convention. Recommendation: store as the string `"indefinite"` in the DataFrame; chart calculations treat it as a very large number (e.g., 999) or exclude it from replacement cost computation. Not a Phase 1 decision, but the loader should not silently coerce it to NaN.

4. **Mechanical `Land Area` Column Header** — The Electrical section uses `"Land Area (m^2)"` but Mechanical uses `"Land Area"` (no unit). The loader normalizes this by position (column 6), not by column name, so no impact. Worth noting for documentation.

---

## Sources

### Primary (HIGH confidence)
- Direct inspection of `data.xlsx` via openpyxl 3.1.5 — all row/column positions verified
- [PyPI: dash 4.0.0](https://pypi.org/project/dash/) — current version confirmed
- [PyPI: dash-bootstrap-components 2.0.4](https://pypi.org/project/dash-bootstrap-components/) — current version confirmed
- [Dash GitHub CHANGELOG](https://github.com/plotly/dash/blob/dev/CHANGELOG.md) — Dash 4.0 breaking changes verified

### Secondary (MEDIUM confidence)
- [dbc Simple Sidebar Example](https://www.dash-bootstrap-components.com/examples/simple-sidebar/) — sidebar pattern confirmed
- [Plotly Community: Auto-open browser](https://community.plotly.com/t/auto-open-browser-window-with-dash/31948) — threading.Timer pattern; double-open issue confirmed by community
- [dbc Themes Documentation](https://www.dash-bootstrap-components.com/docs/themes/) — FLATLY theme usage confirmed
- [AnnMarieW dash-bootstrap-templates](https://github.com/AnnMarieW/dash-bootstrap-templates) — chart theming option verified

### Tertiary (LOW confidence)
- WebSearch result claiming Dash 4.0 released "November 2025" — CONTRADICTED by GitHub releases (actual date: Feb 3, 2025). The GitHub release page is authoritative.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — versions directly checked on PyPI and GitHub
- Data file structure: HIGH — directly inspected with openpyxl; all rows printed and verified
- Architecture patterns: HIGH — patterns confirmed via official dbc examples and Plotly docs
- Pitfalls: HIGH — pitfalls derived from direct file inspection and confirmed community reports
- Color palette: MEDIUM — specific hex values are Claude's discretion; academic palette choice is reasonable but not empirically validated

**Research date:** 2026-02-21
**Valid until:** 2026-03-21 (stable ecosystem; Dash 4.x unlikely to break in 30 days)
