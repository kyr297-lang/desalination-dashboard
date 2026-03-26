# Phase 12: Data Layer & Hybrid Builder Removal - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix the data loading layer so the app starts without crashing, wire the updated Part 1 section headers (Electrical Components / Mechanical Components / Hybrid Components), parse the new Energy sheet into a full DataFrame, wire Energy sheet values into the power breakdown chart and turbine count chart, and remove the hybrid builder entirely — replacing it with a static equipment table and immediate scorecard rendering.

</domain>

<decisions>
## Implementation Decisions

### Loader Fix (DATA-01)
- **D-01:** Update `SECTION_HEADERS` in `src/data/loader.py` to match the actual Part 1 headers in the updated `data.xlsx`: `"Electrical Components"` → `"electrical"`, `"Mechanical Components"` → `"mechanical"`, `"Hybrid Components"` → `"hybrid"`
- **D-02:** Replace `"miscellaneous"` with `"hybrid"` everywhere in the loader (required set, return dict, parse logic)
- **D-03:** All three section keys (`electrical`, `mechanical`, `hybrid`) are required — crash if any is missing (same validation behavior as before)

### Energy Sheet Parsing (DATA-04)
- **D-04:** Parse the `Energy` sheet into a full DataFrame — all columns: System/Subsystem, Shaft Power (kW), Drive Type, Drivetrain Efficiency, Turbine Input (kW), Notes
- **D-05:** Expose parsed Energy data as a key in the `load_data()` return dict (e.g., `"energy"`)
- **D-06:** Group rows by system (Mechanical, Electrical, Hybrid) — preserve the multi-level structure so charts can filter by system
- **D-07:** Power breakdown chart is driven entirely from Energy sheet — per-subsystem shaft power rows (GW Extraction, RO Feed, Brine) replace any existing hardcoded or calculated values
- **D-08:** Turbine count chart uses selected turbine size from Energy sheet per system (850 kW mechanical, 1500 kW electrical, 850 kW hybrid). Turbine count = total turbine input ÷ selected turbine size, read from the `Selected Turbine (kW)` row in Energy sheet

### Hybrid BOM (DATA-02, DATA-03)
- **D-09:** Hybrid BOM reads from the `"hybrid"` section of Part 1 (rows 33–50 in current data.xlsx) — same parsing logic as mechanical (plain total cost per row, no unit cost formula)
- **D-10:** Hybrid equipment table on the hybrid page is a static display — same component, identical style to mechanical and electrical equipment tables

### Hybrid Preset Display (CONTENT-03)
- **D-11:** Static equipment table only — no banner, no "preset configuration" label, no explanatory text. Matches mechanical/electrical visual style exactly.
- **D-12:** Scorecard renders all three system columns immediately on page load — no gate, no slot-fill requirement. Hybrid column treated the same as mechanical and electrical.

### Hybrid Builder Removal
- **D-13:** `src/layout/hybrid_builder.py` is deleted entirely from the codebase
- **D-14:** All imports of `hybrid_builder` removed from `app.py` and `src/layout/system_view.py`
- **D-15:** `dcc.Store(id="store-hybrid-slots")` removed from `src/layout/shell.py`
- **D-16:** Gate overlay div (`hybrid-gate-overlay`) removed from `system_view.py`
- **D-17:** `hybrid-equipment-container` div removed from `system_view.py`
- **D-18:** Any callbacks referencing `store-hybrid-slots`, `slot-counter`, `slot-dd-*` IDs removed

### Claude's Discretion
- How the Energy sheet DataFrame is structured internally (flat vs. grouped) — researcher/planner should choose the cleanest approach
- Exact key name in the `load_data()` return dict for energy data
- Whether Energy sheet parsing reuses existing `_parse_section()` helpers or uses a separate function

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Data Layer
- `src/data/loader.py` — Current loader implementation with SECTION_HEADERS, load_data(), _parse_section(), Part 2 parsing
- `data.xlsx` — Updated spreadsheet: Part 1 (Electrical/Mechanical/Hybrid BOMs), Part 2 (TDS/depth lookup tables), Energy (three-system power breakdown)

### Hybrid Builder (for removal)
- `src/layout/hybrid_builder.py` — Full builder implementation to be deleted; contains all slot callbacks and dcc.Store references
- `src/layout/system_view.py` — Imports make_hybrid_builder; contains gate overlay and hybrid-equipment-container divs to remove
- `app.py` — Imports set_hybrid_builder_data; entry point for set_data() pattern
- `src/layout/shell.py` — Contains dcc.Store(id="store-hybrid-slots") to remove

### Charts to Update
- `src/layout/charts.py` — Power breakdown chart and turbine count chart; these receive data from the processing layer and must be updated to consume Energy sheet values

### Processing Layer
- `src/data/processing.py` — Intermediate data transformation layer between loader and charts; Energy sheet data will likely flow through here

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `_parse_section(ws, start_row, stop_rows)` in loader.py: Can be reused for hybrid section; NOT suitable for Energy sheet (different structure — multi-system, header rows interspersed)
- `EQUIPMENT_COLUMNS` constant: Used for electrical/mechanical/hybrid DataFrames — hybrid uses same columns
- `set_data()` pattern: All layout modules expose `set_data()` called by app.py at startup — Energy data should flow through this same pattern

### Established Patterns
- BOM parsing: Electrical uses unit cost × quantity formula; Mechanical and Hybrid use plain total cost per row — loader must handle both formats correctly
- Data flow: `load_data()` → `set_data()` in each layout module → callbacks use module-level data — Energy data should follow the same chain
- `suppress_callback_exceptions=True` in app: Means removed IDs (slot-dd-*, slot-counter, hybrid-gate-overlay) won't cause errors if callbacks reference non-existent elements — but the callbacks themselves should still be removed

### Integration Points
- `app.py` startup sequence calls `set_data()` on all layout modules — Energy parsing result must be accessible here
- Scorecard callback currently reads `store-hybrid-slots` to calculate hybrid totals — this callback must be rewritten to read hybrid BOM directly from data dict
- Power breakdown chart callback receives processed data — needs to accept Energy sheet subsystem rows instead of (or in addition to) BOM-derived values
- Turbine count chart callback uses turbine size — must read `Selected Turbine (kW)` from Energy sheet per system

</code_context>

<specifics>
## Specific Ideas

- The Energy sheet row structure: section headers are in column A (e.g., "Mechanical System"), subsystem rows follow, then summary rows ("Total Shaft Power", "Total at Turbine Shaft", "Design Power (+10% margin)", "Selected Turbine (kW)"). Parser must distinguish section headers from data rows and summary rows from subsystem rows.
- Selected turbine sizes confirmed: 850 kW (mechanical), 1500 kW (electrical), 850 kW (hybrid)
- Hybrid BOM total: ~$16.3M (from data.xlsx rows 33–50) — parser should validate this is non-empty

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 12-data-layer-hybrid-builder-removal*
*Context gathered: 2026-03-26*
