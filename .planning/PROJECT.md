# Wind-Powered Desalination Dashboard

## What This Is

An interactive dashboard built with Python (Dash/Plotly) that lets engineering students explore and compare three wind-powered desalination system configurations — mechanical, electrical, and custom hybrid — for a municipality of ~10,000 people. Features side-by-side comparison charts, a RAG scorecard, a 5-slot hybrid builder, interactive salinity/depth energy sliders, and a project landing page with contributor context.

## Core Value

Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs — and build intuition for real engineering decisions.

## Requirements

### Validated

- ✓ Three-system selection interface (mechanical, electrical, hybrid) — v1.0
- ✓ Equipment detail view with parts, data, and descriptions — v1.0
- ✓ Hybrid "build your own" with 5 functional slots — v1.0
- ✓ Hybrid completion gate (all slots required) — v1.0
- ✓ Equipment selection with detailed data per part — v1.0
- ✓ Cost/land/efficiency scorecard with RAG ranking — v1.0
- ✓ Comparison description of hybrid vs. preset systems — v1.0
- ✓ Cost over time graph with time horizon slider — v1.0
- ✓ Land area comparison graph — v1.0
- ✓ Wind turbine count per system graph — v1.0
- ✓ Energy percentage pie chart by action — v1.0
- ✓ All graphs compare 3 systems side-by-side — v1.0
- ✓ Electrical battery/tank tradeoff slider — v1.0
- ✓ Academic visual design (FLATLY Bootstrap theme) — v1.0
- ✓ Data sourced from data.xlsx — v1.0
- ✓ Runs locally via `python app.py` — v1.0
- ✓ Export/print scorecard for lab reports — v1.0
- ✓ Deployable to Render free tier for sharing with classmates — v1.1
- ✓ Salinity (TDS) slider affecting RO desalination energy requirement — v1.2
- ✓ Depth slider affecting pump energy requirement — v1.2
- ✓ Distinct visual identity for Mechanical vs Electrical system pages — v1.2
- ✓ Project landing section with contributors and senior design context — v1.2
- ✓ "Energy" → "Power" label correction where units are in kW — v1.2
- ✓ Power breakdown chart changed from pie to grouped bar chart — v1.2
- ✓ Consistent 2 significant figures for numeric values throughout — v1.2

### Active

(None — define next milestone requirements with `/gsd:new-milestone`)

### Out of Scope

- 3D visualization — 2D dashboard only; clarity over flash
- Real-time wind data integration — static data from spreadsheet; maintenance burden
- Mobile-optimized layout — desktop-first academic tool
- User accounts or saving configurations — stateless dashboard; unnecessary complexity
- AI/LLM explanations — breaks deterministic academic tool contract
- Solar/gravity-fed configurations — not covered by current data.xlsx

## Context

Shipped v1.2 — dashboard with interactive parameter exploration and polished presentation.
Tech stack: Python 3.11, Dash 4.0, Plotly, dash-bootstrap-components (FLATLY theme), pandas 2.2.3, openpyxl 3.1.5, gunicorn 23.0.0.
Codebase: 8,218 LOC Python across 11 modules.
Data source: `data.xlsx` with two sheets — "Part 1" (Electrical, Mechanical, Miscellaneous equipment + battery lookup) and "Part 2" (TDS vs kW for RO desalination; Depth vs kW for pump energy). Committed to git.
Architecture: Module-level `set_data()` pattern avoids circular imports; `dcc.Store` for client-side state; `server = app.server` for WSGI; `suppress_callback_exceptions=True` for multi-tab DOM. `interpolate_energy()` uses np.interp for slider-driven lookups.
Deployment: Render free tier with auto-deploy from GitHub main branch at https://github.com/kyr297-lang/desalination-dashboard.
User testing confirmed 30-second comprehension for unfamiliar students.
Contributors: Amogh Herle, Sofia Ijazi, Kevin Ren, Kyler Sanders — Fall 2025/Spring 2026 senior design class.

## Constraints

- **Tech stack**: Python with Dash/Plotly — academic standard, students likely familiar
- **Data source**: Must read from existing `data.xlsx` — single source of truth
- **Audience**: Engineering students — academic tone, no flashy UI
- **Deployment**: Must work locally (`python app.py`) and be deployable to free hosting

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dash/Plotly for dashboard | Academic standard, good data viz, Python ecosystem | ✓ Good — clean charts, easy callbacks |
| 5 hybrid functional slots | Maps to real desalination process stages | ✓ Good — intuitive pipeline metaphor |
| User-selectable time horizon for cost graph | Allows exploration of short vs. long-term economics | ✓ Good — students explore 5-50yr ranges |
| Red/yellow/green ranking system | Intuitive at-a-glance comparison for students | ✓ Good — immediate comprehension |
| Tabs over Dash Pages | Preserve dcc.Store cross-tab state | ✓ Good — hybrid slots persist across tabs |
| Module-level data loading with set_data() | Avoid circular imports and data loading in callbacks | ✓ Good — clean, consistent pattern |
| data_only=True in openpyxl | Returns computed values not formula strings | ✓ Good — correct numeric parsing |
| debug=False in app.run() | Prevents Flask reloader double browser tabs | ✓ Good — clean single-tab launch |
| suppress_callback_exceptions=True | Multi-tab DOM where not all elements exist initially | ⚠️ Revisit — masks real errors; consider targeted PreventUpdate |
| Browser print-to-PDF for export | No server-side PDF dependency; works everywhere | ✓ Good — simple, reliable |
| Python 3.11 over 3.14 for Render | No pre-built wheels for pandas/scipy on 3.14 | ✓ Good — stable, all packages have wheels |
| gunicorn with --workers 2 --timeout 120 | Fits Render free tier 512MB RAM; timeout covers cold start | ✓ Good — reliable startup |
| data.xlsx committed to git | Static dataset, simplest approach for educational project | ✓ Good — no external data source needed |
| np.interp for slider interpolation | Mirrors interpolate_battery_cost pattern; generic col_x/col_y params | ✓ Good — reusable for both TDS and depth lookups |
| TDS slider max 35,000 PPM (not 1,900) | Seawater salinity ~35,000 mg/L; np.interp clamps at lookup boundary | ✓ Good — realistic range, approved by reviewer |
| Border-top over background tint for system identity | Tint looked out of place next to sidebar; border is clean and unambiguous | ✓ Good — user-directed pivot |
| Grouped bar over stacked bar for power breakdown | Side-by-side bars more readable than stacked for engineering comparison | ✓ Good — clearer stage comparison |
| fmt_sig2 using Python .2g format | Consistent 2-sig-fig display; large integers comma-formatted | ✓ Good — clean numeric presentation |
| Internal data keys unchanged (energy_kw) | Only user-facing labels renamed to Power; minimizes regression risk | ✓ Good — safe refactor boundary |

---
*Last updated: 2026-03-01 after v1.2 milestone*
