# Project Research Summary

**Project:** Wind-Powered Desalination Engineering Dashboard
**Domain:** Interactive academic engineering comparison dashboard (Python, Dash/Plotly)
**Researched:** 2026-02-20
**Confidence:** HIGH (stack and architecture verified against official sources; features MEDIUM from multiple sources and analogues)

## Executive Summary

This is an academic, web-based engineering comparison tool built with Python Dash/Plotly. It allows undergraduate students to explore and compare three wind-powered desalination system configurations — Mechanical, Electrical, and Hybrid — using data loaded from a structured Excel workbook (`data.xlsx`). The expert approach is a single-page Dash application organized around tab-based navigation with `dcc.Store` for cross-view state persistence, a clean Bootstrap (FLATLY theme) layout, and pandas for all data manipulation. The entire stack is Python-only, making it accessible to engineering students and locally runnable without infrastructure. SEDAT (Solar Desalination Assessment Tool, built on Dash/Plotly) is the closest academic analogue, confirming this stack is an established, peer-reviewed choice for the domain.

The recommended approach prioritizes data layer correctness first, then static layout, then interactivity, then the most complex component (the Hybrid 5-slot builder). The biggest differentiator is the Hybrid builder: students assemble a custom desalination system by selecting equipment for five process-stage slots (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal), and cannot see comparison results until all five are filled. This completion gate is the core pedagogical mechanism and the most technically complex feature. The battery/tank tradeoff slider for the Electrical system is the second interactive differentiator — it exposes a real design tradeoff by mapping to an 11-row lookup table in the data.

The primary risks are architectural rather than domain-specific. Dash's reactive model punishes common beginner mistakes: mutating global Python state inside callbacks corrupts multi-user behavior; loading the Excel file inside callbacks causes deployment-scale latency; duplicate callback output ownership breaks the app at startup; and `suppress_callback_exceptions=True` used carelessly hides real bugs. All five critical pitfalls identified in research are preventable by establishing correct patterns at project start (immutable module-level data, `dcc.Store` for user state, explicit callback ownership mapping) before any UI work begins.

---

## Key Findings

### Recommended Stack

The stack is fully determined and version-pinned with HIGH confidence from PyPI API verification. Dash 4.0.0 (released February 2025) is the current stable version and the right choice — it bundles `dcc`, `html`, and `callback` directly, eliminating the outdated separate package installs found in most tutorial code. Plotly 6.5.2 is bundled with Dash 4 and must not be downgraded. pandas 3.0.1 with openpyxl 3.1.5 handles the multi-sheet Excel workbook natively. dash-bootstrap-components 2.0.4 with the FLATLY Bootstrap theme provides the academic visual tone (clean, flat, muted colors) appropriate for an engineering tool.

The only significant alternative-consideration decision is Streamlit vs. Dash: Streamlit was explicitly ruled out because its reactive model cannot handle the hybrid slot state machine (fill 5 slots, then unlock results) without ugly workarounds. Dash is the correct choice.

**Core technologies:**
- Python 3.11+: Runtime — 3.11 is still security-supported; gunicorn 25+ requires 3.10+
- Dash 4.0.0: Dashboard framework — academic Python standard; bundled dcc/html; redesigned API
- Plotly 6.5.2: Chart rendering — bar, line, pie charts all needed; must match Dash 4
- pandas 3.0.1: Data layer — `read_excel()` with openpyxl handles multi-sheet `.xlsx`; DataFrame maps directly to Plotly chart inputs
- openpyxl 3.1.5: Excel backend — required for `.xlsx`; must be installed separately; never use xlrd for .xlsx
- dash-bootstrap-components 2.0.4: Layout and UI — Bootstrap 5 grid, Cards, Badges; prevents layout spaghetti
- dash-bootstrap-templates 2.1.0: Theme sync — matches Plotly figure colors to FLATLY Bootstrap theme
- gunicorn 25.1.0: Deployment WSGI server — Render/Railway require it; not needed locally

**What NOT to use:**
- `dash_table.DataTable` — deprecated in Dash 3.3.0; use `dbc.Table` or `dbc.Card` instead
- `dash-core-components` as a separate package — bundled since Dash 2.0; installing separately gets old unmaintained version
- xlrd — dropped `.xlsx` support in 2020; online examples using it are outdated
- Streamlit — cannot handle the hybrid slot state machine

### Expected Features

Research classified features into three tiers. All P1 features are required for the tool to deliver its academic purpose; P2 features enhance learning; P3 features are v2+ scope.

**Must have (table stakes) — all P1:**
- Data loading from data.xlsx — nothing else works; validate all three sheets parse correctly
- System selection interface (Mechanical / Electrical / Hybrid) — the organizing principle of the tool
- Cost/land/efficiency scorecard with RAG (red/yellow/green) color coding — primary at-a-glance comparison
- Cost over time line chart — three systems plotted; user-selectable time horizon (slider/dropdown)
- Land area grouped bar chart — direct physical constraint comparison
- Wind turbine count grouped bar chart — immediately tangible mechanical vs. electrical difference
- Equipment details view — parts list with quantity, cost, energy, land area, lifespan per system
- Energy breakdown pie chart — per-system energy by process action
- Hover tooltips with values and units on all charts — Plotly default, but must configure meaningful content
- Hybrid 5-slot builder — dropdown per process stage from Miscellaneous parts sheet
- Hybrid completion gate — blocks comparison output until all 5 slots are filled
- Electrical battery/tank slider — maps to 11-row tradeoff table; updates electrical series in charts

**Should have (differentiators) — P2:**
- Hybrid vs. preset comparison description — auto-generated text from scorecard rankings
- Academic visual design (FLATLY/LITERA Bootstrap theme) — taken seriously by engineering students
- Deployment to Render/Railway — makes the tool shareable for coursework

**Defer to v2+:**
- Export/print scorecard (useful for lab reports; not needed to validate core concept)
- Lifecycle cost (NPV) view — v1 shows lifespan; v2 could compute net present value
- Additional system configurations (solar, gravity-fed) — out of scope for current data.xlsx

**Anti-features to avoid explicitly:**
- Real-time wind data API integration (out of scope, maintenance burden)
- User accounts / saved configurations (adds auth and database; free tier doesn't support it)
- 3D visualization (obscures data in comparison context; 2D charts are clearer)
- AI/LLM explanation of results (breaks deterministic academic tool contract)

### Architecture Approach

The recommended architecture is a single-page Dash app with tab-based navigation (`dcc.Tabs`), NOT Dash Pages — this is a deliberate choice because Dash Pages destroys and recreates layouts on navigation, losing `dcc.Store` state that must persist when a student moves between the Hybrid Builder and Compare Systems tabs. All cross-tab state lives in `dcc.Store` components in the root layout. The data layer reads `data.xlsx` once at module startup into module-level immutable DataFrames that callbacks reference as read-only. Callbacks are separated by concern into `callbacks/hybrid_callbacks.py`, `callbacks/graph_callbacks.py`, and `callbacks/scorecard_callbacks.py`.

**Major components:**
1. `app.py` — App init, root layout shell (tabs + dcc.Store), server export for gunicorn
2. `data/loader.py` — `pd.read_excel()` called once at startup; DataFrames exposed as module constants
3. `data/calculations.py` — Pure functions: cost-over-time, land area totals, pie slice aggregation
4. `data/models.py` — System data structures, slot definitions, equipment metadata
5. `pages/system_selector.py` — Layout for system overview tab
6. `pages/equipment_detail.py` — Parts list layout per system
7. `pages/hybrid_builder.py` — 5-slot dropdown interface
8. `pages/comparison_graphs.py` — Side-by-side charts layout
9. `callbacks/hybrid_callbacks.py` — Slot selection, Store write, completion gate, comparison text
10. `callbacks/graph_callbacks.py` — Cost-over-time time horizon, battery/tank slider, all chart updates
11. `callbacks/scorecard_callbacks.py` — RAG ranking computation

**Key architectural decisions:**
- Tabs over Dash Pages: preserves cross-tab state in root-level `dcc.Store`
- Module-level data loading: one `read_excel()` call; all callbacks read-only
- `dcc.Store` as the explicit contract between subsystems (not implicit component ID dependencies)
- One callback per logical interaction; no "god callbacks"

### Critical Pitfalls

Research identified 5 critical pitfalls, all preventable if addressed in Phase 1 (foundation) before any callbacks are written.

1. **Mutating global variables in callbacks** — Store all user-specific state in `dcc.Store(storage_type='session')`; never assign to module-level variables inside callback functions. Invisible in single-user dev; breaks silently with two browser tabs open or multiple gunicorn workers.

2. **Loading data.xlsx inside a callback** — Call `pd.read_excel(Path(__file__).parent / 'data.xlsx', engine='openpyxl')` exactly once at module startup. Inside callbacks causes 200-800ms lag per interaction on Render free tier. Always use `pathlib.Path` (not relative string) and always specify `engine='openpyxl'`.

3. **Duplicate callback output ownership** — Each `(component_id, property)` pair can have only one owning callback. Map all callback outputs before coding. Use `callback_context.triggered_id` to branch when one output must respond to multiple input types. `DuplicateCallbackOutput` errors appear at startup, not runtime — treat them as design signals, not annoyances.

4. **Hybrid slot state in DOM instead of dcc.Store** — All 5 slot assignments must live in `dcc.Store(id='hybrid-slots')`. Attempting to read state from component `style`, `children`, or `className` won't work — Dash callbacks cannot read arbitrary DOM state. Design the Store schema before building slot UI.

5. **suppress_callback_exceptions=True as a crutch** — Set this flag only for genuinely dynamic components, with an explicit comment explaining why. Using it to silence startup errors hides real wiring bugs; debugging becomes nearly impossible when panels are blank with no traceback.

**UX pitfalls to watch:**
- Inconsistent colors across graphs for the same system (fix: define `SYSTEM_COLORS` constant, use everywhere)
- Red/green-only RAG without colorblind-safe fallback (fix: add text labels alongside colors)
- Y-axis not starting at 0 in bar/cost charts (fix: always start at 0 for fair magnitude comparison)
- Completion gate that shows a warning but doesn't block rendering (fix: callbacks must return `no_update`, not empty figures)

---

## Implications for Roadmap

The architecture's build-order implications and the pitfall-to-phase mapping align clearly into 5 phases. The dependency chain is strict: data before layout, layout before callbacks, simple callbacks before complex ones, Hybrid builder before comparison graphs (which read from it).

### Phase 1: Foundation — Data Layer and App Shell

**Rationale:** Every other feature depends on data.xlsx parsing correctly and the app shell (tabs, Stores, root layout) existing. The immutable data loading pattern must be established here, before any callbacks exist that could accidentally mutate it. Critical pitfalls 1, 3, and 5 are all prevented in this phase.

**Delivers:** Working `app.py` with tab shell and root-level `dcc.Store` components; `data/loader.py` loading all three Excel sheets into module-level DataFrames; `data/calculations.py` with stub pure functions for cost-over-time and land area totals; `data/models.py` with system and slot data structures; verified `requirements.txt` with pinned versions including `openpyxl` and `gunicorn`.

**Addresses:** Data loading from data.xlsx (table stakes); app initialization foundations.

**Avoids:** Global variable mutation in callbacks (pattern established here); Excel loaded inside callbacks (prohibited here); suppress_callback_exceptions misuse (policy set here).

**Key decisions:** Use `pathlib.Path(__file__).parent / 'data.xlsx'`; always specify `engine='openpyxl'`; load once at module import; `storage_type='session'` for hybrid Store.

### Phase 2: Static Layouts and Scorecard

**Rationale:** Once data is accessible, build the static view layouts and the simplest interactive feature (scorecard RAG ranking) to verify the component structure and callback wiring pattern before tackling complex multi-input callbacks. Validates that the tab navigation and layout architecture work before adding stateful complexity.

**Delivers:** All four `pages/` layout files returning `html.Div` trees (no interactivity yet); system selection interface (3-card/tab selector); equipment detail views for Mechanical and Electrical; scorecard with RAG red/yellow/green ranking via `scorecard_callbacks.py`; fixed `SYSTEM_COLORS` constant applied across all components.

**Addresses:** System selection interface, equipment detail view, scorecard + RAG ranking (all table stakes); academic visual design (FLATLY theme).

**Avoids:** Duplicate callback output conflicts (callback ownership map created here before complex callbacks); color inconsistency across graphs.

**Uses:** dash-bootstrap-components (dbc.Row, dbc.Col, dbc.Card, dbc.Badge); FLATLY Bootstrap theme with `load_figure_template("flatly")`.

### Phase 3: Comparison Charts and Electrical Slider

**Rationale:** Static charts with real data are the second-most-impactful deliverable after the scorecard. The battery/tank slider extends the electrical series without touching hybrid state — making it a clean intermediate step before the more complex Hybrid builder. Validates the full data-to-chart pipeline (loader → calculations → Plotly figure → callback output).

**Delivers:** All four comparison charts (cost over time line chart, land area grouped bar, turbine count grouped bar, energy breakdown pie chart) with data from all three systems; user-selectable time horizon (slider or dropdown); electrical battery/tank fraction slider mapping to 11-row tradeoff table; `graph_callbacks.py` with clean `update_all_comparison_graphs` callback.

**Addresses:** Cost over time chart, land area chart, turbine count chart, energy pie chart, time horizon selector, battery/tank slider (all table stakes and differentiators).

**Avoids:** Battery/tank slider index mismatch (unit test: 0% → row 0, 50% → row 5, 100% → row 10); slider callback storm (use `updatemode='mouseup'`); Y-axis not starting at 0; hover tooltips with unformatted numbers (configure `hovertemplate` with `$` and unit labels).

**Implements:** `data/calculations.py` functions fully; `pages/comparison_graphs.py` layout; `callbacks/graph_callbacks.py`.

### Phase 4: Hybrid Builder and Completion Gate

**Rationale:** The Hybrid builder is the most complex feature and depends on the entire previous stack being solid (data layer, layout patterns, callback patterns, chart rendering). It introduces the most significant stateful interaction: 5-slot selection writing to `dcc.Store`, a completion gate blocking chart output, and hybrid data flowing into the comparison charts built in Phase 3. This is the core pedagogical differentiator.

**Delivers:** 5-slot dropdown interface (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal); each slot populated from `df_misc` Miscellaneous sheet; `dcc.Store(id='hybrid-slots')` with all slot values; completion gate that returns `no_update` (not empty figures) for all 5 comparison chart outputs until all slots are filled; hybrid data series appearing in all comparison charts when complete; hybrid equipment detail view.

**Addresses:** Hybrid 5-slot builder, hybrid completion gate (core differentiators); hybrid column in scorecard.

**Avoids:** Hybrid slot state in DOM instead of Store (all state through `dcc.Store`); completion gate showing warning but not blocking rendering (must return `no_update`); global variable mutation (Store only).

**Implements:** `pages/hybrid_builder.py`; `callbacks/hybrid_callbacks.py`; hybrid slot Store schema.

### Phase 5: Polish, Comparison Text, and Deployment

**Rationale:** Once all core features are verified, add the P2 differentiators (comparison text, visual polish review) and prepare for deployment. Deployment configuration is straightforward but has specific checklist items that are easy to miss (server export, gunicorn in requirements, data.xlsx in repo).

**Delivers:** Auto-generated hybrid vs. preset comparison description (text block from scorecard rankings); visual polish review (consistent colors, tooltip formatting, axis labels with units, colorblind-safe RAG); deployment configuration (`server = app.server`, `Procfile`, `gunicorn` in requirements.txt); smoke test on Render/Railway free tier.

**Addresses:** Hybrid vs. preset comparison description (P2 differentiator); deployment to Render/Railway (P2); academic visual polish.

**Avoids:** Missing `server = app.server`; missing `gunicorn` in requirements.txt; `data.xlsx` not committed to repo; color inconsistency final audit.

**Implements:** Deployment checklist from PITFALLS.md "Looks Done But Isn't" section.

### Phase Ordering Rationale

- **Data before layout before callbacks** is the strict dependency chain from ARCHITECTURE.md's build-order section; violating it means building callbacks against data structures that haven't been validated yet.
- **Simple callbacks before complex ones** prevents callback ownership conflicts from being discovered late — the scorecard (Phase 2) is a single-input single-output pattern; the hybrid builder (Phase 4) is the most complex multi-input multi-output pattern with Store intermediary.
- **Hybrid after charts** means the comparison chart rendering is proven before the most complex feature (Hybrid builder) needs to feed it data, reducing the debugging surface area.
- **Deployment last** aligns with PITFALLS.md guidance: the deployment checklist is straightforward and low-risk, but has several easy-to-forget items best addressed as a dedicated phase rather than distributed across earlier phases where they can be missed.

### Research Flags

Phases with well-documented patterns (can proceed without additional research):
- **Phase 1 (Foundation):** Dash app initialization, Excel loading with pandas/openpyxl, dcc.Store — all covered by official Dash documentation with HIGH confidence.
- **Phase 2 (Static Layouts and Scorecard):** Bootstrap grid layouts, dbc.Card components, RAG ranking logic — standard patterns, excellent community coverage.
- **Phase 3 (Comparison Charts):** Plotly bar, line, pie charts — best-documented part of the entire stack; Plotly docs are thorough.
- **Phase 5 (Deployment):** Render/Railway deployment with gunicorn — well-documented; PITFALLS.md has the exact checklist.

Phases that may benefit from targeted research during planning:
- **Phase 4 (Hybrid Builder):** The 5-slot completion gate using `dcc.Store` + `no_update` gating is a specific stateful pattern. The ARCHITECTURE.md callback examples cover it but implementation details (slot schema design, `prevent_initial_call` on gate callback) may need a focused look at Dash advanced callbacks documentation before coding begins.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All versions verified via PyPI JSON API; official Dash 4.0.0 release notes confirmed; compatibility matrix explicitly verified |
| Features | MEDIUM | Core dashboard patterns HIGH from multiple sources; desalination-specific patterns MEDIUM from cross-reference with SEDAT, SAM, HOMER Pro analogues; no direct feature documentation for this exact tool type |
| Architecture | HIGH | Verified against official Dash documentation for all major patterns (tabs vs. pages, dcc.Store sharing, module-level loading, callback ownership); community consensus aligns with official guidance |
| Pitfalls | HIGH | Critical pitfalls verified against official Dash docs and GitHub issues; UX pitfalls MEDIUM from multiple community sources |

**Overall confidence:** HIGH

### Gaps to Address

- **data.xlsx structure validation:** Research assumes three sheets (Electrical Components, Mechanical Components, Miscellaneous) and an 11-row battery fraction table within the Electrical sheet. The actual column names, data types, and any merged cells need to be verified against the real file before `data/loader.py` is written. Merged cells in Excel are a silent failure mode with pandas.

- **Hybrid slot part categorization:** Research assumes that parts in the Miscellaneous sheet are categorized by process stage (Water Extraction, Pre-Treatment, etc.) so that each slot's dropdown can be filtered to valid parts. If the sheet does not have this categorization, the slot filtering logic will need to be hand-coded or the sheet will need preprocessing. Validate the Miscellaneous sheet structure before designing the slot dropdown population logic.

- **Cost over time formula:** FEATURES.md and PITFALLS.md both flag the cost-over-time calculation as needing careful spot-checking against manual calculations. The exact formula (capital cost + operational cost × years, or NPV-based) should be confirmed against the data.xlsx structure and any project specification document before `calculations.py` is implemented.

---

## Sources

### Primary (HIGH confidence)
- PyPI JSON API (dash, plotly, pandas, openpyxl, dbc, dbt, gunicorn) — version verification
- Dash official docs (dash.plotly.com) — app lifecycle, callbacks, dcc.Store, tabs vs. pages, sharing data between callbacks, advanced callbacks, duplicate outputs, partial properties, performance
- Dash GitHub release notes (v4.0.0, Feb 2025) — redesigned core components
- dash-bootstrap-components docs — FLATLY/LITERA themes, Bootstrap 5 grid
- pandas docs — read_excel engine parameter
- xlrd GitHub repository — xlrd .xlsx support dropped in v2.0 (2020)

### Secondary (MEDIUM confidence)
- SEDAT paper (Nature Scientific Data) — Dash/Plotly for academic desalination analysis confirmed as peer-reviewed approach
- Render Community forums — Dash on Render deployment pattern (Procfile + gunicorn)
- Plotly Community Forum — tabs vs. pages community consensus
- Dashboard Design Patterns (dashboarddesignpatterns.github.io) — RAG scorecard, comparison patterns
- Bernard Marr — RAG rating industry practice
- Pencil & Paper UX Pattern Analysis — dashboard UX patterns
- HOMER Pro, SAM (NREL) product pages — comparable tool analysis

### Tertiary (LOW confidence)
- FasterCapital — cost visualization best practices (single commercial source; validated by Plotly docs)
- WebDataRocks — line chart for cost comparison over time (single source; verified by general pattern research)

---

*Research completed: 2026-02-20*
*Ready for roadmap: yes*
