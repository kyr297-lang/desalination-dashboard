# Stack Research

**Domain:** Interactive engineering data dashboard (Python, academic tool)
**Researched:** 2026-02-20
**Confidence:** HIGH (versions verified via PyPI JSON API; library choices verified via official docs and community sources)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11+ | Runtime | 3.11 is the oldest version still receiving security updates in 2025; 3.12/3.13 are stable and faster. Dash 4.x requires >= 3.8 but 3.11+ gets you better performance and is universally available on free hosting tiers. |
| Dash | 4.0.0 | Web dashboard framework | Current stable (released Feb 2025). Redesigned core components, cleaner API. Includes `dcc`, `html`, and `callback` directly — no separate package installs needed. The academic Python standard for data dashboards. |
| Plotly | 6.5.2 | Chart rendering | Bundled with Dash 4 but must match: Dash 4 ships with Plotly >= 6.x. Provides bar, pie, line, grouped-bar charts — everything this project needs. |
| pandas | 3.0.1 | Data manipulation and Excel loading | Industry standard for tabular data. `pd.read_excel()` handles `.xlsx` natively with openpyxl as backend. The `DataFrame` model maps directly to Plotly chart inputs. |
| openpyxl | 3.1.5 | Excel file parsing backend | Required by pandas to read `.xlsx` files. Handles multi-sheet workbooks — critical for this project's three-section `data.xlsx` layout. Install separately so pandas can find it. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| dash-bootstrap-components | 2.0.4 | Layout grid, UI components | Always. Provides `dbc.Row`, `dbc.Col`, `dbc.Card`, `dbc.Badge` — the building blocks for the scorecard and layout without custom CSS. Bootstrap 5 grid system prevents layout spaghetti. |
| dash-bootstrap-templates | 2.1.0 | Matching Plotly figure theme to Bootstrap theme | Always, alongside dbc. Syncs chart colors/fonts to whichever Bootstrap theme you pick. Requires Plotly >= 6.0 (matched). |
| gunicorn | 25.1.0 | WSGI production server | Deployment only. Render and Railway both require a WSGI server. Use `gunicorn app:server` as the start command. Not needed for local `python app.py`. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `venv` (stdlib) | Isolated Python environment | Always use. `python -m venv .venv && source .venv/Scripts/activate` on Windows. Prevents version conflicts when the project lives alongside other Python work. |
| `requirements.txt` | Dependency pinning | Pin exact versions for reproducibility: `dash==4.0.0`, `plotly==6.5.2`, etc. Render and Railway both read this file to build the deployment environment. |
| Dash DevTools (built-in) | Hot reload, callback graph | Enabled automatically in debug mode: `app.run(debug=True)`. Shows callback execution order visually — essential when building the multi-callback hybrid slot system. |

---

## Installation

```bash
# Create and activate virtual environment (Windows)
python -m venv .venv
source .venv/Scripts/activate

# Core dashboard stack
pip install dash==4.0.0 plotly==6.5.2 pandas==3.0.1 openpyxl==3.1.5

# Styling
pip install dash-bootstrap-components==2.0.4 dash-bootstrap-templates==2.1.0

# Deployment (add before deploying to Render/Railway)
pip install gunicorn==25.1.0

# Freeze for deployment
pip freeze > requirements.txt
```

---

## Bootstrap Theme Recommendation

For the project's academic visual requirement (clean, professional, not flashy), use the **FLATLY** theme from Bootswatch.

```python
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("flatly")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
)
```

FLATLY is a clean, flat, muted-color academic theme — used widely in scientific and engineering publications contexts. It avoids the aggressive blues of `BOOTSTRAP` and the garish accents of `CYBORG` or `SUPERHERO`. Alternative: **LITERA** (serif-inflected, even more academic feel but slightly less clean in data-dense layouts).

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Dash 4.x | Streamlit | Streamlit if you need zero-callback reactive UI for simple data exploration; avoid for this project — Streamlit cannot handle the hybrid slot state machine (fill 5 slots, then unlock detail view) without ugly workarounds |
| Dash 4.x | Panel (HoloViz) | Panel if your team is already using HoloViz ecosystem; steeper learning curve, less community material for engineering students |
| dash-bootstrap-components | dash-mantine-components | Mantine if you want a more modern SaaS aesthetic; avoid here — it conflicts with academic tone and has less tutorial coverage for beginners |
| pandas + openpyxl | xlrd | xlrd only reads `.xls` (old format); openpyxl is the correct choice for `.xlsx` files |
| FLATLY theme | Custom CSS | Use custom CSS only if FLATLY/LITERA don't meet visual spec; custom CSS adds maintenance burden and is fragile across Dash version upgrades |
| Render/Railway | PythonAnywhere | PythonAnywhere is viable for free Python hosting; Render has better build pipeline, cleaner GitHub integration, and is the most-documented Dash deployment target |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `dash_table.DataTable` | Deprecated in Dash 3.3.0, removed or neutered in Dash 4.x. The official replacement is Dash AG Grid. For this project, equipment data is better displayed in `dbc.Table` (static) or `dbc.Card` components anyway — the equipment detail view is not a spreadsheet, it's a structured display. | `dbc.Table` for simple static display; `dbc.Card` for per-equipment details |
| `dash-core-components` as a separate package | In Dash 2.0+, `dcc` is bundled into the main `dash` package. Installing `dash-core-components` separately installs an old, unmaintained version. | Import via `from dash import dcc` |
| `dash-html-components` as a separate package | Same issue — bundled into `dash` since v2.0. | Import via `from dash import html` |
| Plotly 5.x | dash-bootstrap-templates 2.x requires Plotly >= 6.0. Mixing Plotly 5 with dbt 2.x will cause silent theme failures. | Plotly 6.5.2 as specified |
| Flask directly | Dash wraps Flask internally. Exposing `server = app.server` is enough for gunicorn. Writing raw Flask routes alongside Dash is fragile and unnecessary for this use case. | Use `app.server` for gunicorn, `@app.callback` for interactivity |
| `xlrd` for reading Excel | xlrd dropped `.xlsx` support in v2.0 (2020). Code examples online still use it — they are outdated. | `pandas` + `openpyxl` |

---

## Stack Patterns by Variant

**For local development only (no deployment):**
- Skip `gunicorn` from requirements.txt
- Run with `app.run(debug=True)` for hot reload and DevTools
- No Procfile needed

**For deployment to Render (free tier):**
- Add `gunicorn==25.1.0` to requirements.txt
- Create `Procfile` with: `web: gunicorn app:server`
- In Render dashboard: Start Command = `gunicorn app:server`
- Free tier sleeps after 15 minutes of inactivity; acceptable for academic demo use

**For the hybrid slot completion gate (stateful UI):**
- Store selected equipment in `dcc.Store(id="hybrid-selections", storage_type="session")`
- Use `prevent_initial_call=True` on callbacks that depend on slot state
- Gate the detail view callback: check that all 5 slots are filled before enabling output

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `dash==4.0.0` | `plotly>=6.0.0` | Dash 4 ships a matching Plotly; do not downgrade Plotly below 6.0 |
| `dash-bootstrap-templates==2.1.0` | `plotly>=6.0.0`, `dash-bootstrap-components>=1.0.0` | dbt 2.x dropped Plotly 5 support entirely |
| `dash-bootstrap-components==2.0.4` | `dash>=2.0.0` | dbc 2.x is Bootstrap 5; dbc 1.x was Bootstrap 4 — use 2.x |
| `pandas==3.0.1` | `openpyxl>=3.1.0` | pandas 3.x requires openpyxl to be explicitly installed for `.xlsx` support |
| `gunicorn==25.1.0` | `Python>=3.10` | gunicorn 25 dropped Python 3.9 support; use Python 3.11+ |

---

## Sources

- PyPI JSON API `https://pypi.org/pypi/dash/json` — dash 4.0.0 confirmed (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/plotly/json` — plotly 6.5.2 confirmed (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/pandas/json` — pandas 3.0.1 confirmed (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/openpyxl/json` — openpyxl 3.1.5 confirmed (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/dash-bootstrap-components/json` — dbc 2.0.4 confirmed (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/dash-bootstrap-templates/json` — dbt 2.1.0 confirmed, Plotly >= 6.0 requirement verified (HIGH confidence)
- PyPI JSON API `https://pypi.org/pypi/gunicorn/json` — gunicorn 25.1.0, Python >= 3.10 requirement confirmed (HIGH confidence)
- GitHub `https://github.com/plotly/dash/releases/tag/v4.0.0` — Dash 4.0.0 release: redesigned core components, Feb 3 2025 (HIGH confidence)
- Dash docs `https://dash.plotly.com/` — dcc/html bundling since Dash 2.0, DataTable deprecation in 3.3.0 (HIGH confidence)
- dash-bootstrap-components docs `https://www.dash-bootstrap-components.com/docs/themes/` — FLATLY/LITERA theme availability confirmed (HIGH confidence)
- Render deployment guide `https://community.render.com/t/deploying-dash-by-plotly-app-on-render/3475` — Procfile + gunicorn pattern confirmed (MEDIUM confidence)
- WebSearch: Dash callback patterns, stateful storage with `dcc.Store` — confirmed against official docs (MEDIUM confidence)

---

*Stack research for: Wind-Powered Desalination Dashboard (Python Dash/Plotly)*
*Researched: 2026-02-20*
