---
phase: 02-system-selection-and-scorecard
plan: 02
subsystem: ui
tags: [dash, dash-bootstrap-components, layout, navigation, scorecard, rag, accordion, equipment-grid]

# Dependency graph
requires:
  - phase: 01-foundation
    provides: shell.py app shell, dcc.Store sidebar, FLATLY theme
  - plan: 02-01
    provides: processing.py (fmt_cost, fmt_num, fmt, rag_color, compute_scorecard_metrics, get_equipment_stage), config.py (PROCESS_STAGES, EQUIPMENT_DESCRIPTIONS)

provides:
  - create_overview_layout() — landing page with 3 coloured system selection cards
  - create_system_view_layout(active_system, data) — tab bar + scorecard + equipment grid
  - make_scorecard_table(mechanical_df, electrical_df) — RAG traffic-light scorecard
  - make_equipment_section(df, system, all_data) — accordion equipment grid with cross-system comparison
  - updated shell.py with active-system dcc.Store and 3 separate navigation callbacks (select_system_from_card, select_system_from_tab, back_to_overview)

affects:
  - Phase 3 charts (will embed chart components inside system_view.py content area)
  - Phase 4 hybrid builder (will replace hybrid empty state with functional builder)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - dcc.Store for navigation state (active-system = None | "mechanical" | "electrical" | "hybrid")
    - Deferred imports inside render_content callback to avoid circular imports at module load time
    - set_data() module-level setter to inject data into shell callbacks without circular imports
    - Static active_tab prop on dbc.Tabs (re-rendered each time) instead of Output callback — avoids circular dependency
    - borderBottom on active tab label (not backgroundColor) per known Dash-Bootstrap tab styling bug
    - pattern-matching Input({"type": "system-card-btn", "index": ALL}) for card navigation
    - allow_duplicate=True for multiple callbacks writing to same dcc.Store output
    - Split callbacks per trigger source (not unified) when triggers don't all exist in initial DOM
    - dbc.Accordion(always_open=False, active_item=None) for one-at-a-time expand behavior
    - Cross-system comparison: find same process stage in other systems via get_equipment_stage

key-files:
  created:
    - src/layout/overview.py
    - src/layout/scorecard.py
    - src/layout/equipment_grid.py
    - src/layout/system_view.py
  modified:
    - src/layout/shell.py
    - app.py

key-decisions:
  - "Deferred imports in render_content callback: from src.layout.overview import ... placed inside callback body, not at top of shell.py — avoids circular import at module load time"
  - "set_data() pattern: module-level _data variable in shell.py, populated by app.py after data loaded — clean alternative to re-loading data inside callbacks"
  - "Static active_tab prop on dbc.Tabs: tabs re-rendered with correct active_tab each call instead of using Output(system-tabs, active_tab) — eliminates circular callback graph"
  - "active_label_style uses borderBottom not backgroundColor: workaround for known Bootstrap + Dash tab active-indicator styling bug"
  - "Cross-system comparison finds equipment in same process stage (not same name) — allows Mechanical Water Extraction to compare with Electrical Water Extraction items"
  - "Split callbacks per trigger source using allow_duplicate=True: unified callback with system-tabs + back-to-overview inputs fails when those elements don't exist in initial DOM (card clicks silently ignored)"

# Metrics
duration: 26min
completed: 2026-02-21
---

# Phase 2 Plan 02: System Selection and Scorecard — UI Layer Summary

**Complete Phase 2 UI: landing overview with system cards, tab navigation, RAG scorecard, and accordion equipment grid with cross-system comparison — all wired via dcc.Store navigation state**

## Performance

- **Duration:** 26 min
- **Started:** 2026-02-21T18:30:00Z
- **Completed:** 2026-02-21T18:56:55Z
- **Tasks:** 3 of 3 (including human-verify checkpoint, approved)
- **Files modified:** 6

## Accomplishments

- Created `src/layout/overview.py` with `create_overview_layout()` — three system selection cards with SYSTEM_COLORS headers, descriptions, and pattern-matched Explore buttons
- Updated `src/layout/shell.py` — added active-system dcc.Store, System Explorer nav link, 3 separate navigation callbacks (select_system_from_card, select_system_from_tab, back_to_overview), `render_content` callback, and `set_data()` module function
- Updated `app.py` to call `set_data(DATA)` after creating the layout
- Created `src/layout/scorecard.py` with `make_scorecard_table()` — RAG dot indicators for cost, land area, and energy; best-overall summary row
- Created `src/layout/equipment_grid.py` with `make_equipment_section()` — accordion items grouped by process stage, detail tables, badge summary rows, cross-system comparison table
- Created `src/layout/system_view.py` with `create_system_view_layout()` — breadcrumb, tab bar with colored active indicators, scorecard + equipment vertical stack
- Human verification approved: full 11-step UI flow confirmed working in browser

## Task Commits

Each task was committed atomically:

1. **Task 1: Create landing overview and update shell with navigation state management** - `13ee285` (feat)
2. **Task 2: Create scorecard table, equipment grid with accordion detail, and system view assembly** - `8da382d` (feat)
3. **Task 3: Verify complete Phase 2 UI flow** - APPROVED (human-verify checkpoint — no code commit)
4. **Post-checkpoint fix: Split monolithic callback in shell.py** - `8a3d01c` (fix)

## Files Created/Modified

- `src/layout/overview.py` — `create_overview_layout()`: 3 system cards with colored headers, Explore buttons using pattern-matched IDs
- `src/layout/shell.py` — Added active-system store, System Explorer nav link, 3 split callbacks (select_system_from_card, select_system_from_tab, back_to_overview) with allow_duplicate=True, `render_content` callback, `set_data()` module function
- `app.py` — Added `set_data(DATA)` call after layout creation
- `src/layout/scorecard.py` — `make_scorecard_table()`: RAG dots, formatted metric values, best-overall summary
- `src/layout/equipment_grid.py` — `make_equipment_section()`: process-stage groups, accordion items, detail tables, cross-system comparison
- `src/layout/system_view.py` — `create_system_view_layout()`: breadcrumb, tabs, scorecard, equipment grid assembly

## Decisions Made

- **Deferred imports in render_content:** `create_overview_layout` and `create_system_view_layout` imported inside the callback body to prevent circular imports when shell.py is loaded.
- **set_data() pattern:** Module-level `_data` variable in shell.py populated from app.py — avoids both circular imports and data re-loading inside callbacks.
- **Static active_tab prop on dbc.Tabs:** Tab bar re-rendered with correct `active_tab` each time `render_content` fires; no `Output("system-tabs", "active_tab")` used — eliminates the circular callback dependency documented in research.
- **borderBottom active tab styling:** Uses `borderBottom: "3px solid {color}"` on `active_label_style` instead of `backgroundColor` — workaround for known Bootstrap Dash tab rendering bug.
- **Cross-system comparison by process stage:** Matches equipment from other systems by their process stage (via `get_equipment_stage`), not by name — allows meaningful comparison across systems with different equipment names.
- **Split callbacks with allow_duplicate=True:** When triggers (system-tabs, back-to-overview) don't exist in the initial DOM, a unified callback silently ignores card clicks. Fix: separate callback per trigger source, each writing to active-system store using allow_duplicate=True.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Split monolithic update_active_system callback into 3 separate callbacks**
- **Found during:** Post-checkpoint verification (after Task 2 commit, before Task 3 approval)
- **Issue:** The plan specified a single `update_active_system` callback with 3 inputs: pattern-matched card buttons, `system-tabs`, and `back-to-overview`. When `system-tabs` and `back-to-overview` don't exist in the initial DOM (landing page renders neither), Dash's callback registration phase encounters missing component IDs and silently fails to fire the callback for card clicks as well.
- **Fix:** Split into 3 callbacks — `select_system_from_card` (pattern-match only), `select_system_from_tab` (`allow_duplicate=True`), and `back_to_overview` (`allow_duplicate=True`). Each callback only references inputs that exist when it fires.
- **Files modified:** `src/layout/shell.py`
- **Verification:** Card clicks navigate to system tab view; tab switches change active system; back link returns to overview. All three paths confirmed working.
- **Committed in:** `8a3d01c` (fix commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug in callback registration due to non-existent initial DOM elements)
**Impact on plan:** Fix required for core navigation to work. No scope creep — only changed callback structure, not functionality.

## Issues Encountered

- Monolithic callback with non-existent DOM element IDs in inputs caused card click navigation to silently fail. Resolved by splitting into 3 callbacks with allow_duplicate=True (see Deviations above).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Navigation state management fully wired — Phase 3 chart components can be embedded in system_view.py content area
- Equipment accordion structure in place — Phase 3 charts can be inserted as additional accordion content
- Hybrid empty state in place — Phase 4 hybrid builder replaces it
- All 5 layout modules exported with clean APIs ready for Phase 3 integration
- allow_duplicate=True pattern established for future multi-source callbacks writing to same dcc.Store

---
*Phase: 02-system-selection-and-scorecard*
*Completed: 2026-02-21*
