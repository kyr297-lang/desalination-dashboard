# Wind-Powered Desalination Dashboard

## What This Is

An interactive dashboard built with Python (Dash/Plotly) that lets engineering students explore and compare three wind-powered desalination system configurations — mechanical, electrical, and custom hybrid — for a municipality of ~10,000 people. Features side-by-side comparison charts, a RAG scorecard, a 5-slot hybrid builder with completion gate, and browser print-to-PDF export.

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

### Active

<!-- No active milestone — use /gsd:new-milestone to start one -->

- [ ] Lifecycle cost (NPV) view with discount rate input
- [ ] Side-by-side equipment comparison table across systems
- [ ] Export charts as PNG/PDF for reports

### Out of Scope

- 3D visualization — 2D dashboard only; clarity over flash
- Real-time wind data integration — static data from spreadsheet; maintenance burden
- Mobile-optimized layout — desktop-first academic tool
- User accounts or saving configurations — stateless dashboard; unnecessary complexity
- AI/LLM explanations — breaks deterministic academic tool contract
- Solar/gravity-fed configurations — not covered by current data.xlsx

## Context

Shipped v1.1 — dashboard deployed to Render free tier at https://github.com/kyr297-lang/desalination-dashboard.
Tech stack: Python 3.11, Dash 4.0, Plotly, dash-bootstrap-components (FLATLY theme), pandas 2.2.3, openpyxl 3.1.5, gunicorn 23.0.0.
Data source: single `data.xlsx` with Electrical, Mechanical, and Miscellaneous sheets (committed to git).
Architecture: Module-level `set_data()` pattern avoids circular imports; `dcc.Store` for client-side state; `server = app.server` for WSGI; `suppress_callback_exceptions=True` for multi-tab DOM.
Deployment: Render free tier with auto-deploy from GitHub main branch. Spins down after ~15min inactivity (expected).
User testing confirmed 30-second comprehension for unfamiliar students.

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

---
*Last updated: 2026-02-24 after v1.1 milestone complete*
