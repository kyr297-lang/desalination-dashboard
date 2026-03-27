# Research Summary: Wind-Powered Desalination Dashboard v1.3

**Project:** Wind-Powered Desalination Dashboard v1.3 UI/UX Overhaul
**Researched:** 2026-03-26
**Confidence:** HIGH (architecture/pitfalls from direct codebase analysis; stack from official Dash 4.0 and DBC 2.0 docs)

---

## Stack Additions

No new packages. All v1.3 features use capabilities already in `requirements.txt`.

- `dcc.Loading(type="circle", delay_show=200)` — wrap every `dcc.Graph`; `delay_show` prevents visual noise on fast slider drags
- `dash.get_asset_url("filename.png")` — use the module-level function, not `app.get_asset_url`; handles `requests_pathname_prefix` on Render without circular import risk
- `dcc.Slider` tooltip `template` prop (e.g., `"template": "{value} PPM"`) — Dash 4.0 native; no JS file needed for simple unit labels
- `allow_direct_input=False` on all sliders — Dash 4.0 defaults to rendering a text input box beside sliders; set this explicitly to suppress it
- `assets/slider_transforms.js` with `window.dccFunctions` — optional; only needed if comma-formatted numbers are required in tooltips (e.g., "10,000 PPM")
- DBC 2.0 prop renames: `Spinner(spinner_style=...)` and `spinnerClassName=` replace the old `style=` and `class_name=` — already on DBC 2.0.4; use the new names in any new code
- Do not add `dash_table.DataTable` — deprecated in Dash 4.0; avoid in v1.3

---

## Feature Table Stakes

Must-have UX fixes and content updates before v1.3 is usable.

- **Fix the loader first** — app is currently broken; `data.xlsx` Part 1 no longer has a "Miscalleneous" section; update `SECTION_HEADERS` in `loader.py` before touching anything else
- **Battery slider endpoint labels** — add `marks={0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}`, `tooltip={"always_visible": True}`, and `updatemode="drag"`; the only slider currently missing these
- **System diagram hero card** — move the 3 PNGs into `assets/` with hyphenated names; render each as `html.Img` inside a `dbc.Card` at the top of its system page, above the scorecard
- **System page heading** — add `html.H2` or `html.H3` with the system name at the top of each page; tab label and badge alone are not sufficient for screenshots and lab reports
- **3-system scorecard on initial load** — hybrid data is now static; pass `data["hybrid"]` directly to `make_scorecard_table` at layout time; do not depend on a store-change callback that never fires
- **Loading spinners on charts and page transitions** — wrap the chart grid container and `#page-content` in `dcc.Loading`; charts currently show a blank white box during callback execution
- **Empty state for comparison text** — `comparison-text` renders as invisible blank space; add a default `html.P("Complete the hybrid builder to see a comparison.", className="text-muted fst-italic")`
- **Student-facing error messages** — rewrite `error_page.py` strings; currently surfaces raw `ValueError` text like `"Missing section(s) in 'Part 1': ['miscellaneous']"` directly to users

---

## Architecture Changes

Key structural changes required for v1.3.

- **`loader.py`** — replace `"Miscalleneous"` key in `SECTION_HEADERS` and `required` with `"hybrid"`; update `_parse_section` stop-row logic so `hybrid_start` bounds the mechanical section; add `_parse_energy_sheet(wb)` if Energy sheet data is needed for v1.3 charts
- **`hybrid_builder.py`** — delete the entire file; three `@callback` decorators register at import time and silently fire against missing DOM IDs if only the UI is removed; deletion plus removing all imports is the only safe approach
- **`shell.py`** — remove `store-hybrid-slots` dcc.Store and the `SLOT_STAGES` import; this store was the sole driver of 4 downstream callbacks across 3 modules
- **`scorecard.py`** — delete `update_gate_overlay` and `update_hybrid_equipment` callbacks entirely; simplify `update_scorecard` to always render 3-column from `_data["hybrid"]`, or render the scorecard statically at layout time to eliminate the callback entirely
- **`charts.py`** — remove `Input("store-hybrid-slots", "data")` from `update_charts`; use `_data["hybrid"]` directly; reduces inputs from 6 to 5
- **`config.py`** — replace `PROCESS_STAGES["miscellaneous"]` key with `"hybrid"`; update `PROCESS_STAGES["mechanical"]` with new hydraulic component names; add `SYSTEM_LAYOUT_IMAGES` dict; extract the 4 magic name strings from `processing.py` into named constants
- **`system_view.py`** — refactor `create_system_view_layout` to dispatch to `_build_mechanical_content`, `_build_electrical_content`, and `_build_hybrid_content` helper functions; remove gate overlay divs; render hybrid equipment statically from `data["hybrid"]`
- **`processing.py`** — delete `compute_hybrid_df`; it assembled a user-driven hybrid from slot selections — no longer applicable with a static hybrid BOM

---

## Watch Out For

Top 5 pitfalls with one-line prevention each.

1. **Loader crashes on startup right now** — `data.xlsx` Part 1 no longer has the "Miscalleneous" section; fix `SECTION_HEADERS` before writing any other code or every change will be untestable.

2. **Deleting the hybrid builder UI is not enough** — `hybrid_builder.py` registers three `@callback` decorators at import time; delete the file entirely and then run `grep -rn "hybrid_builder\|SLOT_STAGES" src/` to catch all surviving imports.

3. **Removing `store-hybrid-slots` before fixing its consumers produces wrong data silently** — with the store's sole writer gone, `update_charts` receives `{stage: None}` forever and hybrid charts show zeros; refactor all 4 consuming callbacks to use `_data["hybrid"]` directly before removing the store from `shell.py`.

4. **PROCESS_STAGES name mismatches cause silent wrong groupings** — `get_equipment_stage()` falls back to `"Other"` with no error when a name is not matched; after fixing the loader, run `print(data["mechanical"]["name"].tolist())` and cross-reference every string in `PROCESS_STAGES["mechanical"]` exactly, including trailing spaces.

5. **`dcc.Loading` causes spinner flicker on drag-mode sliders** — TDS and depth sliders fire the chart callback on every pixel of movement; switch both to `updatemode="mouseup"` before wrapping any chart in `dcc.Loading`, otherwise the entire chart section flickers continuously during slider drags.

---

## Implications for Roadmap

### Suggested Phase Structure

**Phase 1 — Data Layer + Hybrid Builder Removal**
Unblocks everything else. Fix the loader, update `PROCESS_STAGES` in config with new hydraulic component names, delete `hybrid_builder.py`, refactor all 4 store-hybrid-slots consumers to use `_data["hybrid"]` directly, and verify the 3-system scorecard renders on initial load. Nothing else is testable until this phase is complete.

**Phase 2 — Layout Images + Per-System Differentiation**
Move the 3 PNGs to `assets/` with hyphenated names, add `SYSTEM_LAYOUT_IMAGES` to config, refactor `system_view.py` into per-system builder functions, add the diagram hero card and system heading (`html.H2`) to each page. Use static `html.Img` only — no callbacks needed, no ID collision risk.

**Phase 3 — UX Quality Pass**
Add `dcc.Loading` wrappers (after switching TDS and depth sliders to `updatemode="mouseup"`), fix battery slider marks and tooltip, fix heading hierarchy (`html.Strong` to `html.H5` throughout), add RAG dot aria-labels and text legend, rewrite error messages, add empty state for comparison text.

**Phase 4 — Polish**
Collapsible diagram sections with `dcc.Store` memory, "Affects:" microcopy under sliders, legend badge `title` and `role="button"`, print stylesheet audit, diagram-to-accordion name consistency review.

### Research Flags

- Phase 1 (data + cleanup): No research needed — direct code changes with known targets from ARCHITECTURE.md and PITFALLS.md
- Phase 2 (images): No research needed — `dash.get_asset_url` pattern confirmed HIGH confidence; static images require no callbacks
- Phase 3 (UX): Test actual `compute_chart_data` latency before finalizing spinner wrap strategy; if under 200ms, skip per-chart spinners and wrap page transitions only
- Phase 4: Standard patterns throughout; skip research-phase

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All features use packages already in requirements.txt; APIs confirmed from official Dash 4.0 and DBC 2.0 docs |
| Features | MEDIUM-HIGH | Table stakes derived from direct UI Review audit of this codebase; differentiators from established dashboard UX literature |
| Architecture | HIGH | All recommendations from direct analysis of all 11 source modules; no assumptions; line numbers cited for every change |
| Pitfalls | HIGH | All critical pitfalls verified against actual code with specific line numbers; not theoretical risks |

**Overall confidence:** HIGH

### Gaps to Address During Implementation

- **Exact hybrid section header string** — the text in column B of the updated `data.xlsx` that marks the hybrid BOM must be read from the actual file before updating `SECTION_HEADERS`; one character difference causes a loader crash
- **Battery lookup table position** — verify the J3:P14 range in Part 1 has not shifted now that the mechanical BOM expanded to row 31
- **Energy sheet scope** — determine whether the new Energy sheet's turbine/efficiency data is needed for v1.3 charts or can be deferred to v1.4; currently no parser exists for it
- **Spinner latency threshold** — measure `compute_chart_data` wall time before deciding whether per-chart `dcc.Loading` wrappers add value or only add flicker

---

## Sources

### Primary (HIGH confidence)
- Direct codebase analysis, all 11 source modules (8,218 LOC) — architecture, pitfalls, callback line numbers
- [Dash External Resources](https://dash.plotly.com/external-resources) — static asset serving pattern
- [dcc.Loading docs](https://dash.plotly.com/dash-core-components/loading) — spinner API and overlay_style
- [dcc.Slider docs](https://dash.plotly.com/dash-core-components/slider) — tooltip template, allow_direct_input
- [DBC Changelog](https://www.dash-bootstrap-components.com/changelog/) — 2.0 prop renames

### Secondary (MEDIUM confidence)
- [Dash GitHub Releases](https://github.com/plotly/dash/releases) — Dash 4.0 component redesign notes
- Dashboard UX literature (Pencil & Paper, UXPin, Smashing Magazine, GoodData) — feature differentiation and discoverability patterns
- `.planning/UI-REVIEW.md` (2026-03-26) — direct audit findings for this project

---

*Research completed: 2026-03-26*
*Ready for roadmap: yes*
