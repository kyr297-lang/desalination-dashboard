---
phase: 01-foundation
plan: 02
subsystem: ui
tags: [dash, dash-bootstrap-components, flatly, sidebar, layout, error-handling]

# Dependency graph
requires:
  - phase: 01-01
    provides: load_data() function, config.py with SYSTEM_COLORS, validated Excel parser
provides:
  - Dash app shell with FLATLY theme, collapsible sidebar, and top header bar
  - app.py entry point: loads data at module level, auto-opens browser on startup
  - Full-page error component with expandable details accordion for missing/corrupt data
  - assets/custom.css with sidebar toggle button styles and transition rules
affects: [02-overview, 03-charts, 04-hybrid-builder, 05-polish]

# Tech tracking
tech-stack:
  added: [dash-bootstrap-components (dbc.themes.FLATLY, dbc.Navbar, dbc.Nav, dbc.Alert, dbc.Accordion), webbrowser, threading]
  patterns:
    - Module-level data loading (load_data() called once at import time, never inside callbacks)
    - Conditional layout assignment (shell layout vs. error page based on data load result)
    - Sidebar collapse via dcc.Store boolean + callback updating inline style width
    - Auto-open browser via threading.Timer(1.0, ...) before app.run()
    - suppress_callback_exceptions=True set globally for multi-page readiness

key-files:
  created:
    - app.py
    - src/layout/__init__.py
    - src/layout/shell.py
    - src/layout/error_page.py
    - assets/custom.css
  modified: []

key-decisions:
  - "debug=False in app.run() prevents Flask reloader from opening two browser tabs"
  - "Use 127.0.0.1 not localhost in browser auto-open URL to avoid DNS resolution delay on Windows"
  - "Sidebar state stored in dcc.Store (client-side) so collapse persists across tab navigations without server round-trips"
  - "suppress_callback_exceptions=True set at app creation time to support future multi-page layouts"

patterns-established:
  - "Layout pattern: all layout functions take data dict as parameter for future child component use"
  - "Error display pattern: create_error_page(error, details) — high-level message in Alert, full traceback in collapsed Accordion"
  - "Import style: from dash import html, dcc, callback, Input, Output, State (Dash 4.0 style)"

requirements-completed: [DEP-01, DATA-02]

# Metrics
duration: 25min
completed: 2026-02-21
---

# Phase 1 Plan 02: App Shell and Entry Point Summary

**Dash app with FLATLY Bootstrap theme, collapsible sidebar, auto-open browser, and full-page error handling wired to the data layer**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-02-21T08:02:05Z
- **Completed:** 2026-02-21T08:02:29Z (tasks 1-2) + human verification approved
- **Tasks:** 3 (2 auto + 1 human-verify checkpoint)
- **Files modified:** 5

## Accomplishments

- `app.py` entry point: loads data.xlsx at module level, creates Dash app with FLATLY theme, sets layout conditionally (shell on success, error page on failure), auto-opens browser via threading.Timer
- `src/layout/shell.py`: `create_layout(data)` returns full app shell — dbc.Navbar header with hamburger toggle, collapsible sidebar with smooth CSS transition, main content area
- `src/layout/error_page.py`: `create_error_page(error, details)` returns full-page error with dbc.Alert and collapsed dbc.Accordion for expandable technical details
- `assets/custom.css`: sidebar toggle button styles (no border, white text, pointer cursor) and transition rules
- Human verification confirmed: app launches to http://127.0.0.1:8050, header displays correctly, sidebar collapses/expands, terminal logs data validation status

## Task Commits

Each task was committed atomically:

1. **Task 1: Create app shell layout with collapsible sidebar and error page** - `1615661` (feat)
2. **Task 2: Create app.py entry point with data loading and browser auto-open** - `94da625` (feat)
3. **Task 3: Verify app launches and displays correctly** - Human-verify checkpoint, approved by user

**Plan metadata:** (docs commit — this summary)

## Files Created/Modified

- `app.py` — Entry point: module-level data load, Dash app creation, conditional layout, browser auto-open, server start
- `src/layout/__init__.py` — Empty package init
- `src/layout/shell.py` — `create_layout(data)`: header navbar with toggle, dcc.Store for sidebar state, collapsible sidebar (220px/0px), content area; sidebar toggle callback
- `src/layout/error_page.py` — `create_error_page(error, details)`: full-page error with dbc.Alert + collapsed dbc.Accordion for traceback
- `assets/custom.css` — Sidebar toggle button styles and transition rules

## Decisions Made

- `debug=False` in `app.run()` — Flask reloader in debug mode opens two browser tabs; disabled to prevent duplicate auto-open
- `127.0.0.1` not `localhost` in browser URL — avoids DNS resolution delay on Windows systems
- Sidebar state in `dcc.Store` — client-side persistence means collapse state survives future tab navigation without server callbacks
- `suppress_callback_exceptions=True` set at app creation — required for future multi-page layouts where IDs may not all be present at validation time

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None — all imports resolved cleanly, data layer from Plan 01 integrated without modification.

## User Setup Required

None - no external service configuration required. App runs with `python app.py` from project root.

## Next Phase Readiness

- Phase 1 foundation complete: data layer (Plan 01) + app shell (Plan 02) are both done
- Phase 2 can start immediately: `create_layout(data)` accepts the full data dict, child components can be added to the content area
- Sidebar `dbc.Nav` has a comment marking where future nav items should be added as phases are built
- Error handling is in place — any future data issues will surface with a human-readable message

---
*Phase: 01-foundation*
*Completed: 2026-02-21*
