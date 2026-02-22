# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-20)

**Core value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs
**Current focus:** Phase 4 — Hybrid Builder

## Current Position

Phase: 4 of 5 (Hybrid Builder)
Plan: 1 of 2 in current phase
Status: In Progress
Last activity: 2026-02-22 — Completed 04-01-PLAN.md (hybrid builder foundation: config, processing helpers, pipeline layout)

Progress: [███████░░░] 70%

## Performance Metrics

**Velocity:**
- Total plans completed: 7
- Average duration: 10 min
- Total execution time: 76 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 2/2 | 27 min | 13.5 min |
| 2. System Selection | 2/4 | 28 min | 14 min |
| 3. Comparison Charts | 2/2 | 18 min | 9 min |
| 4. Hybrid Builder | 1/2 | 3 min | 3 min |

**Recent Trend:**
- Last 5 plans: 02-02 (26 min), 03-01 (3 min), 03-02 (15 min), 04-01 (3 min)
- Trend: Fast (config + processing helpers + self-contained layout module)

*Updated after each plan completion*
| Phase 02-system-selection-and-scorecard P02 | 26 min | 3 tasks | 6 files |
| Phase 03-comparison-charts-and-electrical-slider P01 | 3 min | 2 tasks | 2 files |
| Phase 03-comparison-charts-and-electrical-slider P02 | 15 min | 2 tasks | 3 files |
| Phase 04-hybrid-builder P01 | 3 min | 2 tasks | 3 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Use tabs over Dash Pages to preserve dcc.Store cross-tab state
- [Roadmap]: Load data.xlsx once at module startup as immutable DataFrames — never inside callbacks
- [Roadmap]: Hybrid builder is Phase 4 (depends on proven chart rendering from Phase 3)
- [Roadmap]: Phase 4 (Hybrid Builder) flagged for targeted pre-planning research on dcc.Store slot schema and completion gate pattern
- [01-01]: Use pandas 2.3.3 (already installed) instead of 2.2.3 — matches installed environment, no compatibility issues
- [01-01]: data_only=True in openpyxl.load_workbook — returns computed values not formula strings
- [01-01]: Row 33 note text included in miscellaneous DataFrame (6 rows); column B is not None so name guard does not skip it
- [01-02]: debug=False in app.run() prevents Flask reloader from opening two browser tabs on auto-open
- [01-02]: Use 127.0.0.1 not localhost in browser URL to avoid DNS resolution delay on Windows
- [01-02]: Sidebar state stored in dcc.Store (client-side) so collapse persists across tab navigations
- [01-02]: suppress_callback_exceptions=True set globally for multi-page readiness
- [02-01]: RAG "efficiency" key holds total energy_kw (lower is better); label clarity handled in UI not processing.py
- [02-01]: Electrical system gets a "Control" stage for PLC (beyond standard 5 stages)
- [02-01]: Miscellaneous equipment included in PROCESS_STAGES for Phase 4 hybrid builder readiness
- [02-01]: fmt_cost thresholds: >=1M -> $X.XM, >=1K -> $X.XK, <1K -> $X,XXX
- [02-02]: Deferred imports in render_content callback prevent circular imports at shell.py module load time
- [02-02]: set_data() pattern: module-level _data in shell.py populated from app.py — avoids circular imports and callback data loading
- [02-02]: Static active_tab prop on dbc.Tabs (not Output callback) eliminates circular callback dependency in system navigation
- [02-02]: Split callbacks with allow_duplicate=True — unified callback with system-tabs/back-to-overview inputs silently fails when those elements absent from initial DOM; separate callbacks per trigger source fix card click navigation
- [03-01]: Battery override via override_costs dict in compute_cost_over_time() — injects interpolated cost for all battery replacement cycles (years 0, 12, 24, 36, 48), avoiding double-counting pitfall
- [03-01]: Hybrid placeholder is zeros/empty dicts throughout Phase 3 — no KeyError risk from data dict; TODO comments mark Phase 4 integration points
- [03-01]: Empty energy dict for hybrid pie uses ["No data"]/[1] grey slice to avoid go.Pie(values=[]) error
- [03-01]: External HTML legend (dbc.Badge) is authoritative for visibility state — no reliance on restyleData (known Dash bug #2037)
- [03-02]: update_charts() master callback consolidates all four chart outputs + three labels — single callback avoids state fragmentation across figures
- [03-02]: ctx.triggered_id with dict map to system key in toggle_legend() — cleaner than if/else per Input, extends easily for a fourth system
- [03-02]: Badge dimming uses opacity 0.4 + text-decoration: line-through — line-through makes toggle-off state unambiguous vs opacity alone
- [03-02]: set_data() pattern extended to charts.py exactly mirroring shell.py — consistent module-level data access, no data loading inside callbacks
- [04-01]: Desalination dropdown items sourced from mechanical/electrical DataFrames (not miscellaneous) — hybrid builder allows cross-system equipment selection
- [04-01]: Multi-Media Filtration removed from miscellaneous Pre-Treatment — exists only in electrical sheet, leaving it would produce unresolvable dropdown option
- [04-01]: clear_all_slots callback cascades through update_slot_store — single writer pattern maintained for store-hybrid-slots
- [04-01]: hybrid_energy in compute_chart_data uses miscellaneous system key for stage lookup — hybrid items are mapped via that stage config

### Pending Todos

None yet.

### Blockers/Concerns

- [Resolved — 01-01]: data.xlsx actual column names, data types, and merged cells — RESOLVED: loader parses correctly
- [Resolved — 02-01]: Miscellaneous sheet part categorization by process stage — RESOLVED: categorized in PROCESS_STAGES (miscellaneous key)
- [Resolved — 03-01]: Cost-over-time formula confirmed and implemented — replacement cycle model verified against data.xlsx, all values match RESEARCH.md benchmarks

## Session Continuity

Last session: 2026-02-22
Stopped at: Completed 04-01-PLAN.md — hybrid builder foundation complete; config extended, processing helpers added, pipeline layout and callbacks self-contained in hybrid_builder.py
Resume file: None
