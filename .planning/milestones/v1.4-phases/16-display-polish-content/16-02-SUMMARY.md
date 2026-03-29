---
phase: 16-display-polish-content
plan: "02"
subsystem: config-equipment-grid
tags: [equipment, stages, display-names, accordion, comparison-table]
dependency_graph:
  requires: [16-01]
  provides: [5-stage-equipment-grouping, simplified-detail-table, simplified-comparison]
  affects: [equipment_grid.py, config.py]
tech_stack:
  added: []
  patterns: [DISPLAY_NAMES-lookup, 5-stage-process-grouping, 4-field-tables]
key_files:
  created: []
  modified:
    - src/config.py
    - src/layout/equipment_grid.py
decisions:
  - "PROCESS_STAGES regrouped from 7 stages to 5: Power & Drive, Water Extraction, Desalination, Brine & Storage, Support — matches Phase 15 equipment names"
  - "Cross-system comparison now shows Lifespan instead of Power/Land Area (those columns no longer exist after Phase 15)"
  - "DISPLAY_NAMES added to this worktree as Rule 3 deviation (worktree starts at initial release, not Phase 16-01)"
  - "stage_class conditional added to make_equipment_section for system accent headings (Rule 3 - missing from initial release)"
metrics:
  duration: "12 minutes"
  completed_date: "2026-03-29"
  tasks_completed: 2
  files_modified: 2
---

# Phase 16 Plan 02: Equipment Stage Regrouping and Display Simplification Summary

**One-liner:** Regrouped PROCESS_STAGES from 7 legacy stages to 5 new process stages (Power & Drive, Water Extraction, Desalination, Brine & Storage, Support) with Phase 15 equipment names, and simplified equipment_grid.py detail table and cross-system comparison to 4-column layout using DISPLAY_NAMES.

## Tasks Completed

| # | Task | Commit | Key Files |
|---|------|--------|-----------|
| 1 | Regroup PROCESS_STAGES into 5 new categories | 6b8d18d | src/config.py |
| 2 | Simplify equipment_grid.py: _STAGE_ORDER, detail table, comparison, DISPLAY_NAMES wiring | bb7f093 | src/layout/equipment_grid.py |

## What Was Built

### Task 1: PROCESS_STAGES Regrouping
- Replaced 7-stage PROCESS_STAGES (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal, Control, + miscellaneous system) with 5-stage grouping across mechanical, electrical, and hybrid systems
- New stages: "Power & Drive", "Water Extraction", "Desalination", "Brine & Storage", "Support"
- All equipment names updated to match Phase 15 BOM (e.g., "1 MW Aeromotor Turbine" instead of "250kW aeromotor turbine ")
- Hybrid system added as third system (replacing "miscellaneous" system that had placeholder items)
- Added DISPLAY_NAMES dict with 5 unicode-cleanup mappings (required by Task 2 import; missing from initial-release worktree)
- Total: 41 equipment items across all 3 systems, 0 orphans

### Task 2: equipment_grid.py Simplification
- Updated `_STAGE_ORDER` to new 5-stage list — removes "Pre-Treatment", "Post-Treatment", "Brine Disposal", "Control", "Other"
- Removed `_fmt_power` and `_fmt_land` helper functions (dead code — energy_kw/land_area_m2 columns removed in Phase 15)
- Simplified `_make_summary_badges`: 3 badges (Qty, Cost, Lifespan) instead of 5 (was Qty, Cost, Power, Land, Lifespan)
- Simplified `_make_detail_table`: 4 fields (Name, Qty, Cost, Lifespan) instead of 6; wired DISPLAY_NAMES for name display
- Rewrote `_make_cross_system_comparison`: 4-column table (System, Name, Cost, Lifespan); DISPLAY_NAMES applied to all name cells; best-value logic uses lowest cost + longest lifespan instead of lowest cost/power/land
- Wired `DISPLAY_NAMES.get(name, name)` into accordion item title rendering
- Added `stage_class` conditional for system accent headings (mechanical/electrical/hybrid CSS classes)

## Verification Results

```
All 3 systems have correct 5-stage grouping
Total equipment items across all systems: 41
equipment_grid.py checks passed
PROCESS_STAGES mechanical keys: {'Brine & Storage', 'Desalination', 'Water Extraction', 'Support', 'Power & Drive'}
_STAGE_ORDER: ['Power & Drive', 'Water Extraction', 'Desalination', 'Brine & Storage', 'Support']
No energy_kw or land_area_m2 references remaining: 0
DISPLAY_NAMES imported and used in 4 locations
All dead code (_fmt_power, _fmt_land) removed
```

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added DISPLAY_NAMES to config.py (missing from initial-release worktree)**
- **Found during:** Task 2 (import would have failed without DISPLAY_NAMES in config.py)
- **Issue:** This worktree starts at initial release (0899055). DISPLAY_NAMES was added in commit b35cbbb (Plan 16-01) which is not in this worktree's branch. The Task 2 import `from src.config import EQUIPMENT_DESCRIPTIONS, PROCESS_STAGES, DISPLAY_NAMES` would fail at runtime.
- **Fix:** Added DISPLAY_NAMES dict with the same 5 unicode-cleanup entries as commit b35cbbb to src/config.py as part of Task 1's commit.
- **Files modified:** src/config.py
- **Commit:** 6b8d18d

**2. [Rule 3 - Missing functionality] Added stage_class conditional for system accent headings**
- **Found during:** Task 2 (reviewing make_equipment_section in equipment_grid.py)
- **Issue:** The stage_class conditional (mechanical/electrical/hybrid CSS accent classes) was added by Plan 16-01 in other worktrees but is absent from this worktree's initial release. Without it, stage headings render with no system visual identity.
- **Fix:** Added the three-branch conditional (mechanical + electrical + hybrid) to make_equipment_section as part of Task 2.
- **Files modified:** src/layout/equipment_grid.py
- **Commit:** bb7f093

## Known Stubs

None — all deliverables are fully wired. PROCESS_STAGES uses exact Phase 15 equipment names. DISPLAY_NAMES applied to all 4 display points in equipment_grid.py. Equipment accordion will group into 5 stages with no "Other" fallback.

## Self-Check: PASSED
