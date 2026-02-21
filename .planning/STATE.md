# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-20)

**Core value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs
**Current focus:** Phase 1 — Foundation

## Current Position

Phase: 1 of 5 (Foundation)
Plan: 2 of 2 in current phase — PHASE COMPLETE
Status: Phase 1 complete, ready for Phase 2
Last activity: 2026-02-21 — Completed 01-02-PLAN.md (app shell and entry point)

Progress: [██░░░░░░░░] 20%

## Performance Metrics

**Velocity:**
- Total plans completed: 1
- Average duration: 2 min
- Total execution time: 2 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 2/2 | 27 min | 13.5 min |

**Recent Trend:**
- Last 5 plans: 01-01 (2 min), 01-02 (25 min)
- Trend: —

*Updated after each plan completion*

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

### Pending Todos

None yet.

### Blockers/Concerns

- [Resolved — 01-01]: data.xlsx actual column names, data types, and merged cells — RESOLVED: loader parses correctly
- [Research flag]: Miscellaneous sheet part categorization by process stage needs verification before designing slot dropdowns (Phase 4)
- [Research flag]: Cost-over-time formula needs confirmation against data.xlsx structure before implementing calculations.py (Phase 1/3)

## Session Continuity

Last session: 2026-02-21
Stopped at: Completed 01-02-PLAN.md — app shell and entry point (app.py, shell.py, error_page.py, custom.css)
Resume file: None
