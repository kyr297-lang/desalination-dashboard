---
phase: 02-system-selection-and-scorecard
plan: 01
subsystem: data
tags: [pandas, formatting, rag, scorecard, desalination, config]

# Dependency graph
requires:
  - phase: 01-foundation
    provides: loader.py returning mechanical/electrical/miscellaneous DataFrames, config.py with RAG_COLORS and SYSTEM_COLORS

provides:
  - fmt_cost, fmt_num, fmt formatting helpers for display layer
  - rag_color RAG traffic-light assignment logic (2 or 3 systems)
  - compute_scorecard_metrics aggregate cost/land/energy from DataFrames
  - get_equipment_stage equipment-to-process-stage lookup
  - PROCESS_STAGES config mapping all 9 mechanical + 10 electrical equipment items to process stages
  - EQUIPMENT_DESCRIPTIONS config with 1-2 sentence technical descriptions for all 24 equipment items

affects:
  - 02-02 scorecard UI (consumes compute_scorecard_metrics, rag_color, fmt_cost)
  - 02-03 equipment table UI (consumes get_equipment_stage, EQUIPMENT_DESCRIPTIONS, fmt helpers)
  - Phase 3 charts (consumes scorecard metrics for visualization)
  - Phase 4 hybrid builder (consumes PROCESS_STAGES for slot categorization)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - pd.to_numeric with errors='coerce' for safe numeric aggregation from mixed-type DataFrame cells
    - Separate data/logic module (processing.py) from layout modules — pure Python + pandas, no UI imports
    - RAG color assignment sorted by value direction (lower-is-better vs higher-is-better)

key-files:
  created:
    - src/data/processing.py
  modified:
    - src/config.py

key-decisions:
  - "RAG_BETTER_IS_LOWER = {cost, land_area, efficiency} — efficiency key holds total energy_kw, lower is better; label clarity handled in UI"
  - "PROCESS_STAGES uses 'Control' stage for electrical PLC (beyond the standard 5 stages) — keeps categorization accurate"
  - "Miscellaneous equipment included in PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS for Phase 4 hybrid builder readiness"
  - "fmt_cost abbreviation thresholds: >=1M -> $X.XM, >=1K -> $X.XK, <1K -> $X,XXX"

patterns-established:
  - "Pattern 1: All numeric aggregation uses pd.to_numeric(col, errors='coerce') — never assume DataFrame cells are numeric"
  - "Pattern 2: RAG colors imported from RAG_COLORS dict in config.py — never hardcode hex values in logic modules"
  - "Pattern 3: processing.py is a pure data/logic module — zero imports from layout or UI modules"

requirements-completed: [SCORE-01, SCORE-02]

# Metrics
duration: 2min
completed: 2026-02-22
---

# Phase 2 Plan 01: System Selection and Scorecard — Data Processing Layer Summary

**Pandas-based formatting helpers, RAG traffic-light logic, and scorecard aggregation from real Excel DataFrames, plus PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS config covering all 24 equipment items**

## Performance

- **Duration:** 2 min
- **Started:** 2026-02-22T00:24:30Z
- **Completed:** 2026-02-22T00:26:34Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Created `src/data/processing.py` with 6 exported functions (fmt_cost, fmt_num, fmt, rag_color, compute_scorecard_metrics, get_equipment_stage) — the complete data/logic foundation for all Phase 2 UI components
- Extended `src/config.py` with PROCESS_STAGES (mapping all mechanical and electrical equipment to their functional process stage) and EQUIPMENT_DESCRIPTIONS (24 technical descriptions for engineering students)
- Verified real data outputs: mechanical total cost $11.9M vs electrical $15.4M, RAG correctly assigns green to lower-cost mechanical system

## Task Commits

Each task was committed atomically:

1. **Task 1: Add process stage mappings and equipment descriptions to config.py** - `997b183` (feat)
2. **Task 2: Create processing.py with formatting helpers, RAG logic, and scorecard computation** - `f58c26a` (feat)

**Plan metadata:** (docs commit — created after summary)

## Files Created/Modified

- `src/data/processing.py` — 6 functions: fmt_cost, fmt_num, fmt, rag_color, compute_scorecard_metrics, get_equipment_stage. Pure data/logic module, no UI imports
- `src/config.py` — Added PROCESS_STAGES (mechanical, electrical, miscellaneous) and EQUIPMENT_DESCRIPTIONS (24 items) alongside existing SYSTEM_COLORS, RAG_COLORS, DATA_FILE

## Decisions Made

- **RAG efficiency key stores energy_kw (not an efficiency ratio):** "efficiency" key in scorecard metrics holds total energy consumption (kW); lower is better. Label clarity (e.g. "Total Energy") handled in the UI layer, not processing.py.
- **Electrical system gets a "Control" stage:** PLC is a control/automation component that does not fit the standard Water Extraction / Pre-Treatment / Desalination / Post-Treatment / Brine Disposal stages, so a "Control" stage was added for the electrical system only.
- **Miscellaneous equipment covered in PROCESS_STAGES:** Even though miscellaneous items are not part of mechanical or electrical comparison, they were added to PROCESS_STAGES to support Phase 4 hybrid builder slot categorization.
- **fmt_cost thresholds:** >=1M -> "$X.XM", >=1K -> "$X.XK", <1K -> "$X,XXX" — single decimal for abbreviated forms.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All 6 processing.py functions verified against real data from data.xlsx
- Plan 02-02 (scorecard UI) can import compute_scorecard_metrics, rag_color, and fmt_cost immediately
- Plan 02-03 (equipment table UI) can import get_equipment_stage, EQUIPMENT_DESCRIPTIONS, and fmt helpers immediately
- PROCESS_STAGES miscellaneous section ready for Phase 4 hybrid builder slot categorization

---
*Phase: 02-system-selection-and-scorecard*
*Completed: 2026-02-22*
