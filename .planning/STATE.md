# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-20)

**Core value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs
**Current focus:** Phase 2 — System Selection and Scorecard

## Current Position

Phase: 2 of 5 (System Selection and Scorecard)
Plan: 3 of 4 in current phase
Status: In Progress
Last activity: 2026-02-21 — Completed 02-02-PLAN.md (UI layer: overview, scorecard, equipment grid, system view, shell navigation — human-verify approved)

Progress: [████░░░░░░] 40%

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 10 min
- Total execution time: 55 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 2/2 | 27 min | 13.5 min |
| 2. System Selection | 2/4 | 28 min | 14 min |

**Recent Trend:**
- Last 5 plans: 01-02 (25 min), 02-01 (2 min), 02-02 (26 min)
- Trend: —

*Updated after each plan completion*
| Phase 02-system-selection-and-scorecard P02 | 26 min | 3 tasks | 6 files |

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

### Pending Todos

None yet.

### Blockers/Concerns

- [Resolved — 01-01]: data.xlsx actual column names, data types, and merged cells — RESOLVED: loader parses correctly
- [Resolved — 02-01]: Miscellaneous sheet part categorization by process stage — RESOLVED: categorized in PROCESS_STAGES (miscellaneous key)
- [Research flag]: Cost-over-time formula needs confirmation against data.xlsx structure before implementing calculations.py (Phase 1/3)

## Session Continuity

Last session: 2026-02-21
Stopped at: Completed 02-02-PLAN.md — all 3 tasks done, human-verify approved, shell.py callback split fix committed
Resume file: None
