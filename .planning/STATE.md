# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-20)

**Core value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs
**Current focus:** Phase 3 — Comparison Charts and Electrical Slider

## Current Position

Phase: 3 of 5 (Comparison Charts and Electrical Slider)
Plan: 2 of 2 in current phase
Status: In Progress
Last activity: 2026-02-22 — Completed 03-01-PLAN.md (chart data computation layer and figure builders)

Progress: [█████░░░░░] 50%

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 9 min
- Total execution time: 58 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 2/2 | 27 min | 13.5 min |
| 2. System Selection | 2/4 | 28 min | 14 min |
| 3. Comparison Charts | 1/2 | 3 min | 3 min |

**Recent Trend:**
- Last 5 plans: 01-02 (25 min), 02-01 (2 min), 02-02 (26 min), 03-01 (3 min)
- Trend: Fast (data+figure layer, no callbacks)

*Updated after each plan completion*
| Phase 02-system-selection-and-scorecard P02 | 26 min | 3 tasks | 6 files |
| Phase 03-comparison-charts-and-electrical-slider P01 | 3 min | 2 tasks | 2 files |

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

### Pending Todos

None yet.

### Blockers/Concerns

- [Resolved — 01-01]: data.xlsx actual column names, data types, and merged cells — RESOLVED: loader parses correctly
- [Resolved — 02-01]: Miscellaneous sheet part categorization by process stage — RESOLVED: categorized in PROCESS_STAGES (miscellaneous key)
- [Resolved — 03-01]: Cost-over-time formula confirmed and implemented — replacement cycle model verified against data.xlsx, all values match RESEARCH.md benchmarks

## Session Continuity

Last session: 2026-02-22
Stopped at: Completed 03-01-PLAN.md — data layer + figure builders done, ready for 03-02 callback wiring
Resume file: None
