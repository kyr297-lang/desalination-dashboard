---
phase: 09-system-page-differentiation
plan: 01
subsystem: ui
tags: [dash, dbc, css, system-identity, visual-design]

# Dependency graph
requires:
  - phase: 08-parameter-sliders
    provides: System tabs (mechanical/electrical/hybrid) and active-system store wired up
provides:
  - System name badge pill below tab bar in system_view.py
  - 4px colored top border on #page-content driven by render_content callback
  - Print-safe accent via print-color-adjust: exact in custom.css
affects: [10-comparison-view, 11-pdf-report]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "render_content returns 2-tuple (children, style) — Output page-content children + style from one callback"
    - "System identity via border-top not background-color — avoids contrast issues with sidebar and top bar"
    - "dbc.Badge with pill=True and explicit backgroundColor for system color chips"

key-files:
  created: []
  modified:
    - src/layout/system_view.py
    - src/layout/shell.py
    - assets/custom.css

key-decisions:
  - "Border-top (4px solid hex) chosen over background-color tint — tint looked out of place next to sidebar and top bar; border is less intrusive and still gives clear per-system identity"
  - "Overview page returns transparent border (borderTop: 4px solid transparent) so layout does not shift between views"
  - "_hex_to_rgba() removed after tint approach was dropped — no remaining callers"

patterns-established:
  - "System color lookup: label = active_system.capitalize(); SYSTEM_COLORS.get(label, fallback)"
  - "Badge insertion: append after tab_bar in top_level_children, before main content div"

requirements-completed: [DIFF-01, DIFF-02]

# Metrics
duration: 25min
completed: 2026-03-01
---

# Phase 9 Plan 01: System Page Differentiation Summary

**System name badge (pill) in system_view.py and a 4px colored top border on #page-content, both print-safe, giving Mechanical/Electrical/Hybrid tabs clear visual identity without a full-page background tint**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-03-01T00:00:00Z
- **Completed:** 2026-03-01T00:25:00Z
- **Tasks:** 3 (including checkpoint with design iteration)
- **Files modified:** 3

## Accomplishments

- System name badge (dbc.Badge, pill-shaped, system color) injected below tab bar in all three system views
- render_content callback extended to output both children and style — 4px solid top border matching system hex color
- Overview returns transparent border so the content area height stays stable across navigation
- CSS comment updated; print-color-adjust: exact ensures the border renders in PDF export

## Task Commits

Each task was committed atomically:

1. **Task 1: System badge in create_system_view_layout()** - `1ebf609` (feat)
2. **Task 2: Page-wide tint via render_content callback + print CSS** - `23b6198` (feat)
3. **Task 3 (design change): Replace background tint with 4px border-top** - `4c75088` (fix)

## Files Created/Modified

- `src/layout/system_view.py` — System badge component added after tab_bar, before main content
- `src/layout/shell.py` — render_content outputs (children, style); borderTop: 4px solid hex_color for system pages; transparent border for Overview; _hex_to_rgba() removed
- `assets/custom.css` — print-color-adjust: exact on #page-content; comment updated to reflect border approach

## Decisions Made

- Border-top chosen over full-page background tint after user review at checkpoint — the rgba tint looked "out of place" with the neutral sidebar and dark top bar. A 4px accent line is visually clean and unambiguous.
- Overview page uses `borderTop: "4px solid transparent"` rather than removing the property entirely, so the content area does not shift height between views.
- `_hex_to_rgba()` helper removed after the tint approach was abandoned — no other callers remain.

## Deviations from Plan

### Design Change at Checkpoint (user-directed, not an auto-fix)

**Background tint replaced with 4px top border**
- **Found during:** Task 3 checkpoint — human visual review
- **Issue:** Full-page rgba tint on #page-content looked visually inconsistent next to the neutral sidebar and dark navbar
- **Fix:** Replaced `backgroundColor: rgba(...)` with `borderTop: "4px solid {hex}"` in render_content; removed `_hex_to_rgba()` helper; updated CSS comment
- **Files modified:** `src/layout/shell.py`, `assets/custom.css`
- **Verification:** `from src.layout.shell import create_layout` — import OK; border approach confirmed correct
- **Committed in:** `4c75088`

---

**Total deviations:** 1 user-directed design change at checkpoint
**Impact on plan:** Must-have truths still satisfied — system pages have distinct visual identity, badge is present, Overview returns to plain styling, sidebar stays neutral, print-color-adjust ensures the border survives PDF export.

## Issues Encountered

None beyond the checkpoint design change above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 9 Plan 01 complete — system visual identity established
- Phase 10 (comparison view) and Phase 11 (PDF report) can proceed
- Phase 11 PDF report should verify the 4px border prints correctly (covered by print-color-adjust but worth smoke-testing)

---
*Phase: 09-system-page-differentiation*
*Completed: 2026-03-01*
