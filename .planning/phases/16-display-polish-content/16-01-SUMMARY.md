---
phase: 16-display-polish-content
plan: "01"
subsystem: assets-config
tags: [css, assets, config, display-names, unicode]
dependency_graph:
  requires: []
  provides: [DISPLAY_NAMES, stage-heading-hybrid, layout-PNGs]
  affects: [equipment_grid.py, overview, scorecard]
tech_stack:
  added: []
  patterns: [config-driven-display, exact-string-key-matching, stage-heading-accent-classes]
key_files:
  created:
    - assets/mechanical-layout.png
    - assets/electrical-layout.png
    - assets/hybrid-layout.png
  modified:
    - assets/custom.css
    - src/config.py
    - src/layout/equipment_grid.py
decisions:
  - "Added mechanical+electrical+hybrid stage heading CSS in worktree (worktree at initial release, not main branch head)"
  - "DISPLAY_NAMES uses .get(raw_name, raw_name) pattern — harmless entries for Phase 14 names not yet in PROCESS_STAGES"
metrics:
  duration: "8 minutes"
  completed_date: "2026-03-29"
  tasks_completed: 2
  files_modified: 6
---

# Phase 16 Plan 01: Asset Replacement, Hybrid Accent CSS, and DISPLAY_NAMES Summary

**One-liner:** Replaced layout PNGs with new 148KB/295KB/306KB versions, added `.stage-heading-hybrid` CSS with green #6BAA75 accent, and added DISPLAY_NAMES dict with 5 unicode-cleanup mappings to config.py.

## Tasks Completed

| # | Task | Commit | Key Files |
|---|------|--------|-----------|
| 1 | Replace system layout PNGs and add hybrid accent CSS | a515e2d | assets/*.png, assets/custom.css, src/layout/equipment_grid.py |
| 2 | Add DISPLAY_NAMES mapping and verify EQUIPMENT_DESCRIPTIONS coverage | b35cbbb | src/config.py |

## What Was Built

### Task 1: Layout PNGs and Stage Heading CSS
- Copied 3 new system layout PNGs from project root to `assets/` with kebab-case names:
  - `mechanical-layout.png`: 306,761 bytes (was absent)
  - `electrical-layout.png`: 148,027 bytes (was absent)
  - `hybrid-layout.png`: 294,508 bytes (was absent)
- Added `.stage-heading-mechanical`, `.stage-heading-electrical`, `.stage-heading-hybrid` CSS rules to `assets/custom.css` with left-border and bottom-border accents matching SYSTEM_COLORS
- Added print preservation rules for all three accent classes inside `@media print`
- Updated `equipment_grid.py` Build stage sections loop: added `stage_class` conditional (mechanical/electrical/hybrid) that applies the accent class to H5 stage headings

### Task 2: DISPLAY_NAMES in config.py
- Added `DISPLAY_NAMES: dict[str, str]` constant after `EQUIPMENT_DESCRIPTIONS`
- 5 entries covering all known unicode/formatting issues:
  1. `1.5\u202fMW Turbine (GE Vernova 1.5sle)` — narrow no-break space U+202F before "MW"
  2. `PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)` — non-breaking space U+00A0 before "CPU"
  3. `Gearbox (Winergy  PEAB series)` — double space in brand name
  4. `Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)` — en-dash U+2013
  5. `High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)` — missing closing paren
- Verified all current PROCESS_STAGES items have EQUIPMENT_DESCRIPTIONS entries (0 missing)

## Verification Results

```
PNG sizes OK: {'mechanical-layout.png': 306761, 'electrical-layout.png': 148027, 'hybrid-layout.png': 294508}
CSS checks: PASSED (.stage-heading-hybrid, border-left: 3px solid #6BAA75)
equipment_grid.py check: PASSED (stage_class += " stage-heading-hybrid")
All PROCESS_STAGES items have EQUIPMENT_DESCRIPTIONS entries
DISPLAY_NAMES entries: 5
```

## Deviations from Plan

### Auto-added Missing Functionality

**1. [Rule 2 - Missing functionality] Added mechanical/electrical stage heading CSS alongside hybrid**
- **Found during:** Task 1
- **Issue:** Worktree is at initial release (0899055), not main branch — `.stage-heading-mechanical` and `.stage-heading-electrical` CSS rules did not exist in the worktree's custom.css. The plan assumed they already existed (written against main branch at 5821b1b).
- **Fix:** Added all three accent rules (mechanical, electrical, hybrid) in one CSS block to make the worktree self-contained. This ensures the hybrid accent is correctly visible against the same baseline.
- **Files modified:** `assets/custom.css`
- **Commit:** a515e2d

**2. [Rule 2 - Missing functionality] Added full stage_class conditional block (mechanical+electrical+hybrid)**
- **Found during:** Task 1
- **Issue:** equipment_grid.py in worktree used `className="mt-4 mb-2"` hardcoded — no stage_class variable existed. Plan instructed adding only the hybrid branch "after line 411" but the mechanical/electrical branches did not exist either.
- **Fix:** Implemented the full three-branch conditional (mechanical + electrical + hybrid) as shown in the plan's "makes lines 407-413 read" code block.
- **Files modified:** `src/layout/equipment_grid.py`
- **Commit:** a515e2d

## Known Stubs

None — all deliverables are fully wired. DISPLAY_NAMES has entries for Phase 14 unicode names (e.g., `1.5\u202fMW Turbine`) that are not yet in the worktree's PROCESS_STAGES but these are forward-compatible lookups using `.get(name, name)` fallback — no stub behavior in UI.

## Self-Check: PASSED
