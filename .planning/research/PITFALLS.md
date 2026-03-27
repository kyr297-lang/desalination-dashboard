# Domain Pitfalls: v1.3 Systems Overhaul & UX Redesign

**Project:** Wind-Powered Desalination Dashboard
**Researched:** 2026-03-26
**Confidence:** HIGH -- all findings derived from direct codebase analysis against the planned v1.3 changes

---

## Critical Pitfalls

Mistakes that cause crashes, silent data corruption, or require significant rework.

---

### Pitfall 1: Hybrid Builder Removal Leaves Orphaned Callback Registrations

**What goes wrong:** `hybrid_builder.py` registers three `@callback` decorators at module import time. These callbacks reference 8 component IDs that will no longer exist in the DOM once the builder UI is removed:
- 5 dropdown IDs: `slot-dd-water-extraction`, `slot-dd-pre-treatment`, `slot-dd-desalination`, `slot-dd-post-treatment`, `slot-dd-brine-disposal`
- `btn-clear-all` (Clear All button)
- `slot-counter` (counter label)
- `store-hybrid-slots` (as an Output of `update_slot_store`)

Because `suppress_callback_exceptions=True` is set in `app.py` (line 62), Dash will **silently swallow** errors when these callbacks fire against missing DOM elements. The callbacks remain registered in Dash's callback graph and attempt to execute on every page load. Simply removing the builder component from the layout is **not sufficient** -- the module's `@callback` decorators still register if the module is imported anywhere (even transitively through `system_view.py` line 19).

**Consequences:** Wasted callback cycles, confusing callback graph during debugging, and future risk if `suppress_callback_exceptions` is ever disabled.

**Phase to address:** Phase 1 (Data Layer + Hybrid Builder Removal).

**Prevention:**
1. Delete `src/layout/hybrid_builder.py` entirely -- do not just remove its layout call.
2. Remove `from src.layout.hybrid_builder import SLOT_STAGES` in `shell.py` (line 21). The `SLOT_STAGES` list is used in `store-hybrid-slots` initialization (shell.py line 95) -- move this constant to `config.py` or inline it.
3. Remove `from src.layout.hybrid_builder import make_hybrid_builder` in `system_view.py` (line 19).
4. Remove `set_hybrid_builder_data(DATA)` in `app.py` (line 77).
5. Run `grep -rn "hybrid_builder\|SLOT_STAGES" src/` after deletion to catch stragglers.

---

### Pitfall 2: `store-hybrid-slots` Is a Cross-Cutting Dependency Used by 6 Callbacks in 3 Modules

**What goes wrong:** The `store-hybrid-slots` dcc.Store (created in `shell.py` line 93) is consumed as an `Input` by callbacks across three modules:

| Module | Callback | Line | Role |
|--------|----------|------|------|
| `charts.py` | `update_charts` | 626 | Input -- drives hybrid chart data |
| `scorecard.py` | `update_scorecard` | 321 | Input -- triggers 2-vs-3 system scorecard |
| `scorecard.py` | `update_gate_overlay` | 381 | Input -- shows/hides gate overlay |
| `scorecard.py` | `update_hybrid_equipment` | 425 | Input -- renders hybrid equipment section |
| `hybrid_builder.py` | `update_slot_store` | 249 | Output -- sole writer |
| `hybrid_builder.py` | `update_slot_counter` | 313 | Input -- displays "X/5 slots filled" |

If you remove the hybrid builder (the sole **writer** to this store) but keep the store in the DOM, the downstream callbacks still fire but receive the store's initial value `{stage: None}` forever. This means:
- `update_charts` always sets `hybrid_df = None`, producing zero-valued hybrid charts (wrong -- v1.3 wants preset hybrid data in charts).
- `update_scorecard` always renders a 2-system scorecard (wrong -- v1.3 wants 3-system comparison).
- `update_gate_overlay` always shows the gate overlay (wrong -- there is no gate concept anymore).

If you remove `store-hybrid-slots` entirely, all 4 consuming callbacks fail at **registration time** (Dash 4.0 raises `NonExistentIdException` for callback Inputs even with `suppress_callback_exceptions=True`).

**Phase to address:** Phase 1 -- resolve store semantics before touching any downstream callbacks.

**Prevention strategy (two options):**

**Option A (minimal change):** Keep `store-hybrid-slots` in the DOM but pre-populate it with the fixed hybrid preset (all 5 stages filled). This makes the downstream callbacks produce correct 3-system results without any callback refactoring. Then remove `update_slot_store` (its only writer) from hybrid_builder.py.

**Option B (clean break):** Remove `store-hybrid-slots` entirely. Refactor all 4 consuming callbacks to read hybrid data from `_data["hybrid"]` directly (loaded at startup). This eliminates the reactive store pattern for hybrid data but requires touching every consumer.

**Recommendation:** Option B is cleaner for v1.3 since the "build your own" concept is gone permanently.

---

### Pitfall 3: Loader Crash on Missing "Miscalleneous" Section Header (Currently Broken)

**What goes wrong:** `loader.py` lines 35-38 define three required section headers in Part 1, including `"Miscalleneous"` (deliberate typo matching the old Excel). Lines 244-252 validate all three are present and raise `ValueError` if any are missing.

The updated `data.xlsx` has restructured Part 1: rows 33-50 are now "Hybrid BOM" (per memory context), replacing the old "Miscalleneous" section. The loader cannot find the expected header and raises:
```
ValueError: Missing section(s) in 'Part 1': ['miscellaneous'].
```

**This is the currently broken state of the app.** Nothing works until this is fixed.

**Phase to address:** Phase 1 -- first thing to fix.

**Prevention:**
1. Open the actual `data.xlsx` and inspect the exact header text in column B for the hybrid section (exact string, exact spelling, exact row).
2. Update `SECTION_HEADERS` in `loader.py` to match the new header text, mapping it to a canonical key (either keep `"miscellaneous"` for minimal downstream changes, or rename to `"hybrid"` for clarity).
3. If renaming the key, update every reference to `data["miscellaneous"]` across: `processing.py` (`compute_hybrid_df` line 305 search order), `config.py` (`PROCESS_STAGES["miscellaneous"]`), `hybrid_builder.py` (`_build_dropdown_options` line 101), and `equipment_grid.py` (line 393 uses `"miscellaneous"` as the system key for hybrid items).
4. The mechanical BOM section has also changed (rows 15-31 with new hydraulic components). Verify the mechanical header string still matches `"Mechanical Components"`.
5. Parse the new "Energy" sheet if needed (see Pitfall 10).
6. Test that `load_data()` returns valid DataFrames before touching any other code.

---

### Pitfall 4: PROCESS_STAGES Has Stale Equipment Names After Mechanical System Overhaul

**What goes wrong:** `config.py` lines 46-113 define `PROCESS_STAGES` with exact-match equipment name strings. The mechanical system is being overhauled to use hydraulic components (HPU, manifold, motors, VTP, plunger pump per PROJECT.md). The current strings include:
- `"250kW aeromotor turbine "` (trailing space)
- `"Submersible pump "` (trailing space)
- `"Wind turbine rotor lock"`
- `"Pipes"`, `"Gate valve"`
- `"2 RO membranes in parallel"`, `"Gear and Booster Pump"`
- `"Calcite bed contactors"`, `"Extra storage tank"`

If these names change in the updated Excel but `PROCESS_STAGES` is not updated:
- `get_equipment_stage()` returns `"Other"` for every mechanical item (silent, no error).
- Energy breakdown bar chart shows all mechanical power under "Other".
- Equipment grid groups everything under "Other".
- Cross-system comparison finds no stage matches.

**This fails completely silently.** The dashboard renders with wrong data groupings and no error message.

**Phase to address:** Phase 1 -- update alongside loader changes.

**Prevention:**
1. After fixing the loader, dump new names: `print(data["mechanical"]["name"].tolist())`.
2. Update `PROCESS_STAGES["mechanical"]` to match exactly (watch for trailing spaces, capitalization).
3. Update `EQUIPMENT_DESCRIPTIONS` (config.py lines 118-249) -- add descriptions for new hydraulic components, remove obsolete ones.
4. Add a startup validation function that logs warnings for any equipment name not found in `PROCESS_STAGES`.

---

### Pitfall 5: Hardcoded Magic Strings in processing.py Break Silently

**What goes wrong:** `processing.py` contains 4 hardcoded equipment name strings used for special-case logic:

| String | Location | Purpose |
|--------|----------|---------|
| `"Battery (1 day of power)"` | Line 623 | Override cost for battery slider interpolation |
| `"250kW aeromotor turbine "` | Line 642 | Mechanical turbine count lookup |
| `"Turbine"` | Line 647 | Electrical turbine count lookup |
| `"Battery (1 day of power)"` | Line 690 | Exclude battery from electrical base cost |

If any name changes in the updated Excel, the DataFrame filter `df[df["name"] == "old name"]` returns an empty result. The code handles this with fallback zeros -- **no error, just wrong numbers**.

For the mechanical system overhaul: if the turbine is no longer named `"250kW aeromotor turbine "`, the mechanical turbine count will always show 0.

**Phase to address:** Phase 1.

**Prevention:**
1. Extract all magic strings to named constants in `config.py`.
2. After updating the loader, verify each constant matches the actual data.
3. Consider a startup check: `assert MECH_TURBINE_NAME in data["mechanical"]["name"].values`.

---

## Moderate Pitfalls

Issues that cause incorrect behavior or require careful coordination.

---

### Pitfall 6: Callback ID Collisions When Adding Per-System Conditional Layouts

**What goes wrong:** v1.3 adds per-system layout images and per-system UI differentiation. The `render_content` callback (shell.py line 232) replaces all `page-content` children on every system switch. Callbacks are registered globally at import time, not at render time.

If per-system layouts define components with IDs that exist only when that system is active (e.g., `id="mech-diagram"` only rendered on the mechanical tab), callbacks targeting those IDs fail silently when another tab is active (suppressed by `suppress_callback_exceptions=True`).

The real collision risk: if both mechanical and electrical layouts use the same generic ID (e.g., `id="system-diagram"`), Dash treats them as the same component. If a callback targets this ID, it will fire on whichever system is currently rendered -- potentially with wrong context.

**Phase to address:** Phase 2 (Layout images).

**Prevention:**
1. For static layout images, use `html.Img(src="/assets/images/...")` -- no callbacks needed, no ID collision risk.
2. If interactive per-system elements need callbacks, use pattern-matching IDs: `{"type": "diagram", "system": "mechanical"}`.
3. Never reuse a flat string ID across conditionally-rendered layout branches.
4. Place image files in `assets/images/` with hyphenated names (avoid spaces -- they cause issues on Linux/Render).

---

### Pitfall 7: dcc.Loading Wrappers Cause Spinner Flicker on Drag-Mode Sliders

**What goes wrong:** The `update_charts` callback (charts.py line 612) has **9 outputs** (4 chart figures + 5 labels) and **6 inputs** (4 sliders + legend store + hybrid store). Two sliders use `updatemode="drag"` (TDS at line 474, depth at line 503), firing the callback on every pixel of slider movement.

Wrapping any chart in `dcc.Loading` makes its spinner activate whenever the callback fires -- which means rapid flicker during slider drags. Wrapping the entire chart section in a single `dcc.Loading` makes the whole section flash on every interaction.

Additional gotchas:
- **Loading state propagation:** In Dash 4.0, `dcc.Loading` shows its spinner when *any* child component's callback is in progress. The multi-output `update_charts` callback triggers all 4 chart spinners simultaneously even if only one slider changed.
- **Nested Loading:** If you nest `dcc.Loading` inside `dcc.Loading`, the outer wrapper also activates, causing double-spinner effects.
- **Initial load:** If a callback has `prevent_initial_call=True`, a `dcc.Loading` wrapper may show its spinner indefinitely because the callback never fires to signal completion.

**Phase to address:** Phase 3 (UI/UX overhaul).

**Prevention:**
1. Before adding `dcc.Loading`, measure actual callback latency. If `compute_chart_data` runs in <200ms, spinners are unnecessary and purely annoying.
2. Switch TDS and depth sliders from `updatemode="drag"` to `updatemode="mouseup"` before adding spinners (time-horizon and battery sliders already use mouseup).
3. If spinners are warranted, wrap only the 2x2 chart grid container (not individual charts, not labels).
4. Use `dcc.Loading(type="dot", fullscreen=False, parent_style={"minHeight": "400px"})` to prevent layout collapse during loading.

---

### Pitfall 8: Gate Overlay and Hybrid Equipment Callbacks Become Orphaned

**What goes wrong:** Two callbacks in `scorecard.py` target IDs that only exist when the hybrid tab is active AND the hybrid builder is present:
- `update_gate_overlay` (line 379): targets `Output("hybrid-gate-overlay", "style")` -- this div is only rendered in system_view.py lines 149-185 when `active_system == "hybrid"`.
- `update_hybrid_equipment` (line 423): targets `Output("hybrid-equipment-container", "children")` -- rendered in system_view.py line 139 only for hybrid.

In v1.3, the hybrid builder gate concept is removed (hybrid is a fixed preset). If these callbacks and their target components are not removed together:
- The callbacks fire on every `store-hybrid-slots` change, targeting nonexistent IDs.
- `suppress_callback_exceptions=True` hides the failure.
- If anyone later disables suppression for debugging, these produce confusing `InvalidCallbackReturnValue` errors.

**Phase to address:** Phase 1 (alongside hybrid builder removal).

**Prevention:**
1. Delete `update_gate_overlay` callback from `scorecard.py`.
2. Delete `update_hybrid_equipment` callback from `scorecard.py`.
3. Remove `hybrid-gate-overlay` div from `system_view.py` (lines 149-185).
4. Remove `hybrid-equipment-container` div from `system_view.py` (line 139).
5. Replace the conditional hybrid equipment rendering in `system_view.py` with direct rendering from `data["hybrid"]`.

---

### Pitfall 9: Scorecard Hardcoded to 2-System Initial Render

**What goes wrong:** `system_view.py` line 117:
```python
initial_scorecard = make_scorecard_table(data["mechanical"], data["electrical"])
```

This always renders a 2-system scorecard on first load. The 3-system version only appears when `update_scorecard` fires from a `store-hybrid-slots` change. In v1.3, where hybrid is a fixed preset (the store never changes from user action), the callback may fire once on initial load with the default `{stage: None}` value, taking the "gate closed" branch and re-rendering the same 2-system scorecard.

Result: **hybrid never appears in the scorecard** unless the store is pre-populated or the callback logic is changed.

**Phase to address:** Phase 1.

**Prevention (depends on store strategy):**
- If keeping `store-hybrid-slots` (Option A from Pitfall 2): pre-populate with all 5 stages filled so the callback's initial fire produces a 3-system scorecard.
- If removing the store (Option B): update the initial render to pass hybrid_df directly: `make_scorecard_table(data["mechanical"], data["electrical"], data["hybrid"])`.
- Also update the `update_scorecard` callback or remove it entirely if the scorecard is now static (no user-driven hybrid changes).

---

### Pitfall 10: New "Energy" Sheet Has No Parser -- Data Silently Absent

**What goes wrong:** The memory context documents a new "Energy" sheet in `data.xlsx` with shaft powers, drivetrain efficiencies, and turbine sizes for all three systems. The current `loader.py` only parses "Part 1" and "Part 2" -- it does not know about the Energy sheet.

If the milestone plan expects turbine counts, efficiency data, or energy breakdowns to come from this new sheet, those values will simply be absent. The hardcoded turbine name lookups in `processing.py` (Pitfall 5) may return zeros if the mechanical BOM no longer contains a row identifiable as "the turbine."

**Phase to address:** Phase 1.

**Prevention:**
1. Determine whether the Energy sheet data is needed for v1.3 (turbine sizing, per-system efficiency metrics, shaft power comparisons).
2. If needed, add `_parse_energy_sheet(wb)` to `loader.py`, include the result in the returned data dict, and wire it into `compute_chart_data`.
3. If deferred, document this explicitly so future phases know the data exists but is not yet consumed.

---

## Minor Pitfalls

---

### Pitfall 11: Image Filenames with Spaces Break on Linux Deployment

**What goes wrong:** The untracked PNG files have spaces in their names: `Electrical System Layout.png`, `Hybrid System Layout.png`, `Mechanical System Layout.png`. Dash serves static files from `assets/`. While filenames with spaces work on Windows, they can cause URL-encoding issues on Linux (Render's runtime environment). The browser requests `/assets/Mechanical%20System%20Layout.png` which may or may not resolve depending on the web server configuration.

**Phase to address:** Phase 2.

**Prevention:** Rename files to use hyphens (`mechanical-system-layout.png`) before committing to `assets/images/`.

---

### Pitfall 12: `suppress_callback_exceptions=True` Masks All Refactoring Errors

**What goes wrong:** During the v1.3 refactor (removing callbacks, changing IDs, adding new components), this flag (app.py line 62) hides:
- Typos in new component IDs
- Callbacks targeting removed components
- Missing Inputs from refactored callbacks
- Output-less callbacks that should have been deleted

Every bug that would normally throw a clear error becomes a silent no-op.

**Phase to address:** All phases.

**Prevention:**
1. During development, temporarily set `suppress_callback_exceptions=False`.
2. Navigate all tabs and interact with all controls -- errors surface immediately.
3. Re-enable before deployment (still needed for the multi-tab DOM pattern where not all component IDs exist simultaneously).
4. PROJECT.md line 96 already flags this for review. v1.3 is the right time to consider `validation_layout` as an alternative (a flat layout registered with all possible IDs, used only for callback validation).

---

### Pitfall 13: Forgetting `set_data()` for New Modules

**What goes wrong:** The project uses a `set_data()` pattern in 4 modules (`shell.py`, `charts.py`, `scorecard.py`, `hybrid_builder.py`). `app.py` lines 70-77 call each one sequentially. If a new module with callbacks is added and its `set_data()` call is forgotten in `app.py`, its `_data` stays `None` and all callbacks return early with empty results -- silently.

**Phase to address:** All phases when adding new modules.

**Prevention:**
1. Add `set_data()` call to `app.py` immediately when creating any new module with data-dependent callbacks.
2. Consider refactoring to a shared data module (`src/data/store.py`) that any module can import directly, eliminating the per-module initialization pattern.

---

### Pitfall 14: Electrical BOM Formula Cache Staleness

**What goes wrong:** The electrical BOM uses Excel formulas (unit cost x quantity = total), and `openpyxl` with `data_only=True` returns the **last cached** computed value. If `data.xlsx` is edited in a tool that doesn't evaluate formulas (or if formulas are changed but the file isn't recalculated), the loader returns stale or `None` values for electrical costs.

**Phase to address:** Phase 1 (after any Excel modifications).

**Prevention:** After modifying `data.xlsx`, always open it in Excel and save to refresh cached formula values. Add a loader check that warns if any electrical cost_usd values are None.

---

## Phase-Specific Risk Summary

| Phase | Pitfall | Severity | Key Mitigation |
|-------|---------|----------|----------------|
| **Phase 1: Data Layer** | #3 Loader crash (BROKEN NOW) | CRITICAL | Update SECTION_HEADERS to match new Excel |
| **Phase 1: Data Layer** | #4 Stale PROCESS_STAGES names | CRITICAL | Dump new names, update config.py |
| **Phase 1: Data Layer** | #5 Magic strings in processing.py | CRITICAL | Extract to config.py constants |
| **Phase 1: Builder Removal** | #1 Orphaned callback registrations | CRITICAL | Delete entire module + all imports |
| **Phase 1: Builder Removal** | #2 store-hybrid-slots consumers | CRITICAL | Refactor all 4 consumers before removing store |
| **Phase 1: Builder Removal** | #8 Gate overlay + equipment callbacks | MODERATE | Delete callbacks + target components together |
| **Phase 1: Hybrid Preset** | #9 Scorecard stuck on 2-system | MODERATE | Pre-populate store or pass hybrid_df directly |
| **Phase 1: Energy Data** | #10 Energy sheet not parsed | MODERATE | Add parser if needed for v1.3 |
| **Phase 2: Images** | #6 Callback ID collisions | MODERATE | Use static images, no callbacks needed |
| **Phase 2: Images** | #11 Filenames with spaces | MINOR | Rename with hyphens before committing |
| **Phase 3: UX** | #7 Spinner flicker on drag sliders | MODERATE | Switch to mouseup first; measure latency |
| **All Phases** | #12 suppress_callback_exceptions | MODERATE | Disable during dev, re-enable for deploy |
| **All Phases** | #13 set_data() forgotten | MINOR | Centralize data access pattern |
| **All Phases** | #14 Formula cache staleness | MINOR | Save from Excel after edits |

---

## Recommended Phase 1 Execution Order

Based on dependency analysis, Phase 1 changes must happen in this sequence:

1. **Fix the loader** -- update `SECTION_HEADERS`, verify section parsing against actual Excel, add Energy sheet parser if needed. Confirm `load_data()` succeeds.
2. **Update config.py** -- update `PROCESS_STAGES` and `EQUIPMENT_DESCRIPTIONS` with new equipment names. Extract magic strings from `processing.py` to named constants.
3. **Refactor store-hybrid-slots consumers** -- update or remove `update_charts`, `update_scorecard`, `update_gate_overlay`, `update_hybrid_equipment` to work with the fixed hybrid preset.
4. **Delete hybrid_builder.py** -- remove the module file, all imports, and the `set_data()` call in `app.py`.
5. **Clean up system_view.py** -- remove gate overlay, hybrid-equipment-container, and hybrid builder conditional rendering. Render hybrid equipment from data layer directly.
6. **Update initial scorecard render** -- pass hybrid DataFrame to `make_scorecard_table` for 3-system display.
7. **Verify** with `suppress_callback_exceptions=False` -- navigate all tabs, interact with all sliders, confirm no errors.

---

## Sources

- Direct analysis of all 11 Python source modules (`app.py`, `src/config.py`, `src/data/loader.py`, `src/data/processing.py`, `src/layout/shell.py`, `src/layout/system_view.py`, `src/layout/charts.py`, `src/layout/scorecard.py`, `src/layout/hybrid_builder.py`, `src/layout/equipment_grid.py`, `src/layout/overview.py`)
- `.planning/PROJECT.md` v1.3 milestone definition and documented known issues
- Memory context files documenting data.xlsx structural changes (March 2026)
- Dash 4.0 callback registration behavior: HIGH confidence from direct code observation and established framework semantics
