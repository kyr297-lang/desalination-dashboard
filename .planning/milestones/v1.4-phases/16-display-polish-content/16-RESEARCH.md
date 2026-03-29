# Phase 16: display-polish-content - Research

**Researched:** 2026-03-28
**Domain:** Dash layout components, CSS styling, data display cleanup
**Confidence:** HIGH

## Summary

Phase 16 is a pure display/content polish phase. No new libraries, no data layer changes, no callbacks. All 11 requirements (DISP-01 through DISP-11) involve editing existing Python layout modules, config.py constants, CSS rules, and replacing PNG assets. The codebase is a Plotly Dash + dash-bootstrap-components app with a well-established pattern: config.py holds constants, layout modules build component trees, processing.py handles data logic.

The primary risk is string-matching precision: equipment names in config.py use exact byte-level matches (en-dashes, non-breaking spaces, double spaces) against data.xlsx column B values. Any DISPLAY_NAMES mapping or stage regrouping must preserve these exact keys.

**Primary recommendation:** Organize work into three plans: (1) asset replacement + CSS accent, (2) equipment grid restructuring + display names, (3) scorecard/overview content cleanup.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DISP-01 | All 3 system layout photos updated to new PNGs | New PNGs exist at project root with spaces in names; must copy to assets/ with kebab-case names matching _DIAGRAM_FILES in system_view.py |
| DISP-02 | Equipment names with proper title case and unicode cleanup (DISPLAY_NAMES mapping) | config.py EQUIPMENT_DESCRIPTIONS keys show exact xlsx strings; need a new DISPLAY_NAMES dict mapping raw keys to clean display strings |
| DISP-03 | Equipment accordion regrouped into 5 new categories | Current _STAGE_ORDER in equipment_grid.py has 7 stages; PROCESS_STAGES in config.py maps items to stages; both need updating |
| DISP-04 | Hybrid stage headings have accent class | equipment_grid.py lines 407-412 add accent classes for mechanical/electrical but explicitly skip hybrid; add stage-heading-hybrid class + CSS rule |
| DISP-05 | Scorecard shows only Total Capital Cost | scorecard.py already only has cost row (Phase 15 removed land/energy); verify no residual land/power rows remain |
| DISP-06 | Scorecard legend text updated | scorecard.py line 242 has legend text "Green = lowest cost, Red = highest cost"; update to "Lower total cost is better" |
| DISP-07 | Comparison text compares cost only | processing.py generate_comparison_text already only compares cost (lines 293-313); verify no land_area/energy sentences remain |
| DISP-08 | Overview card descriptions remove "land area" references | overview.py _SYSTEM_CARDS descriptions and intro card reference "land area" and "energy" |
| DISP-09 | Equipment detail table shows Name, Quantity, Cost, Lifespan (no power/land) | equipment_grid.py _make_detail_table has Power and Land Area fields (lines 124-125); _make_summary_badges has Power and Land badges (lines 86-88) |
| DISP-10 | Cross-system comparison table shows Cost and Lifespan (no power/land) | equipment_grid.py _make_cross_system_comparison includes Power and Land Area columns (lines 182-183, 211-230) |
| DISP-11 | Equipment descriptions updated for new electrical and hybrid component names | config.py EQUIPMENT_DESCRIPTIONS already has entries for new names (Phase 14/15 additions); verify coverage matches current xlsx |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash | existing | Web framework | Already in project |
| dash-bootstrap-components | existing | UI components (Accordion, Table, Card, Badge) | Already in project |
| pandas | existing | DataFrame operations | Already in project |

No new packages needed. This phase is entirely code/config/asset edits.

## Architecture Patterns

### Current File Organization
```
src/
  config.py              # PROCESS_STAGES, EQUIPMENT_DESCRIPTIONS, SYSTEM_COLORS, etc.
  data/
    processing.py        # compute_scorecard_metrics, generate_comparison_text, fmt helpers
    loader.py            # data.xlsx parser — DO NOT MODIFY
  layout/
    equipment_grid.py    # Accordion grouping by stage, detail tables, cross-system comparison
    scorecard.py         # RAG scorecard table
    overview.py          # Landing page cards + intro
    system_view.py       # System tab assembly (diagram, scorecard, equipment, charts)
    shell.py             # App shell (navbar, sidebar, callbacks)
assets/
  custom.css             # System accent styles, print rules
  mechanical-layout.png  # Current diagram (to be replaced)
  electrical-layout.png  # Current diagram (to be replaced)
  hybrid-layout.png      # Current diagram (to be replaced)
```

### Pattern 1: Config-Driven Display
**What:** All equipment names, stage groupings, and descriptions are driven by dicts in config.py. Layout modules import and iterate over these dicts.
**When to use:** Any display name or grouping change goes in config.py; layout code should not have hardcoded names.

### Pattern 2: Exact String Key Matching
**What:** Equipment names from data.xlsx column B are used as exact dict keys throughout the codebase. Keys contain unicode characters: en-dash (U+2013), non-breaking space (U+00A0), narrow no-break space (U+202F), and double spaces.
**When to use:** Any new mapping dict (like DISPLAY_NAMES) must use these exact raw strings as keys.

### Pattern 3: Stage Heading Accent Classes
**What:** equipment_grid.py applies CSS classes like `stage-heading-mechanical` and `stage-heading-electrical` to H5 elements. The CSS in custom.css defines left-border and bottom-border accents.
**When to use:** DISP-04 adds `stage-heading-hybrid` following the same pattern.

### Anti-Patterns to Avoid
- **Modifying loader.py:** The data layer is stable from Phase 15. Do not change how data is parsed.
- **Adding callbacks for static content:** All DISP requirements are static layout changes, not reactive. Do not introduce new callbacks.
- **Hardcoding display names in layout files:** Put all name mappings in config.py.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Title case conversion | Custom regex/string manipulation | A simple DISPLAY_NAMES dict in config.py | Equipment names have brand names, acronyms, and special chars that generic title-case functions would mangle |
| Stage grouping | Dynamic categorization logic | Static PROCESS_STAGES dict update in config.py | Groupings are fixed by engineering domain, not computed |

## Common Pitfalls

### Pitfall 1: Unicode Key Mismatch
**What goes wrong:** A DISPLAY_NAMES key uses a regular space where the xlsx has a non-breaking space, causing a silent KeyError or fallback to raw name.
**Why it happens:** Unicode whitespace characters are visually identical in editors.
**How to avoid:** Copy keys directly from existing PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS dicts in config.py — they already match the xlsx byte sequences exactly.
**Warning signs:** Equipment items showing raw xlsx names instead of clean display names.

### Pitfall 2: Stale References to Removed Columns
**What goes wrong:** Code references `energy_kw` or `land_area_m2` DataFrame columns that no longer exist after Phase 15.
**Why it happens:** Phase 15 removed these columns from the DataFrame schema (loader.py now returns only name, quantity, cost_usd, lifespan_years).
**How to avoid:** When removing Power/Land Area from display functions, also remove the `row.get("energy_kw")` and `row.get("land_area_m2")` calls — they return None but are dead code.
**Warning signs:** "N/A" displayed for power/land area fields that should have been removed entirely.

### Pitfall 3: PNG Filename Mismatch
**What goes wrong:** New PNGs copied with wrong filename, Dash serves 404 for diagram images.
**Why it happens:** Source files have spaces ("Mechanical System Layout.png"), destination must be kebab-case ("mechanical-layout.png") to match _DIAGRAM_FILES in system_view.py.
**How to avoid:** Copy and rename in the same operation. Verify _DIAGRAM_FILES dict in system_view.py matches exactly.
**Warning signs:** Broken image icons on system tab view.

### Pitfall 4: Stage Regrouping Leaves Orphans
**What goes wrong:** Equipment items fall into "Other" category after stage rename because PROCESS_STAGES wasn't updated to match new stage names.
**Why it happens:** _STAGE_ORDER and PROCESS_STAGES are separate constants that must stay in sync.
**How to avoid:** Update both _STAGE_ORDER (in equipment_grid.py) and PROCESS_STAGES (in config.py) together. Run the app and verify no items appear under "Other".
**Warning signs:** "Other" stage section appearing in the accordion.

### Pitfall 5: Comparison Text Still References Land/Energy
**What goes wrong:** Overview cards or comparison text mention "land area" or "energy" despite those metrics being removed.
**Why it happens:** Text strings in overview.py were written before Phase 15 removed those metrics.
**How to avoid:** Search all .py files for "land area", "land_area", "energy" string literals and remove/rewrite references in display text.
**Warning signs:** UI text mentioning metrics that are no longer shown anywhere.

## Code Examples

### DISP-02: DISPLAY_NAMES mapping pattern (add to config.py)
```python
# Clean display names for equipment items. Keys must match exact data.xlsx
# column B strings (including unicode). Values are the cleaned title-case
# names shown in the UI.
DISPLAY_NAMES: dict[str, str] = {
    "1.5\u202fMW Turbine (GE Vernova 1.5sle)": "1.5 MW Turbine (GE Vernova 1.5sle)",
    "PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)": "PLC (Siemens SIMATIC S7-1200 CPU1215C-1)",
    # ... etc for all items needing cleanup
}
```

### DISP-03: New stage grouping (update _STAGE_ORDER in equipment_grid.py)
```python
_STAGE_ORDER = [
    "Power & Drive",
    "Water Extraction",
    "Desalination",
    "Brine & Storage",
    "Support",
]
```

### DISP-04: Hybrid accent CSS (add to custom.css)
```css
.stage-heading-hybrid {
    border-left: 3px solid #6BAA75;
    padding-left: 0.5rem;
    border-bottom: 1px solid #6BAA75;
    padding-bottom: 0.25rem;
}
```

### DISP-04: Add hybrid branch in equipment_grid.py
```python
# In make_equipment_section, around line 407:
stage_class = "mt-4 mb-2"
if system == "mechanical":
    stage_class += " stage-heading-mechanical"
elif system == "electrical":
    stage_class += " stage-heading-electrical"
elif system == "hybrid":
    stage_class += " stage-heading-hybrid"
```

### DISP-09: Simplified detail table (equipment_grid.py)
```python
def _make_detail_table(row: pd.Series) -> dbc.Table:
    fields = [
        ("Name", fmt(row.get("name"))),
        ("Quantity", fmt_sig2(row.get("quantity"))),
        ("Cost", fmt_cost(row.get("cost_usd"))),
        ("Lifespan", _fmt_lifespan(row.get("lifespan_years"))),
    ]
    # ... rest unchanged
```

### DISP-10: Simplified cross-system comparison
```python
# Remove "Power" and "Land Area" from comparison_rows dict and table columns.
# Keep only: System, Name, Cost, Lifespan
```

## Detailed Requirement Analysis

### DISP-01: Photo Replacement
**Current state:** assets/ contains three PNGs (63KB, 100KB, 333KB) dated Mar 28.
**New files:** Project root has three new PNGs with spaces in names (148KB, 295KB, 307KB) dated Mar 28.
**Action:** Copy new PNGs to assets/, overwriting existing files with same kebab-case names.
**system_view.py impact:** None -- _DIAGRAM_FILES already maps to correct paths.

### DISP-02: Display Names
**Current state:** Equipment names display as raw xlsx strings (with unicode chars).
**Action:** Add DISPLAY_NAMES dict to config.py. In equipment_grid.py, wrap name lookups through DISPLAY_NAMES.get(name, name).
**Scope:** Accordion title, detail table Name field, cross-system comparison Name column.

### DISP-03: Stage Regrouping
**Current stages:** Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal, Control, Other (7 stages).
**New stages:** Power & Drive, Water Extraction, Desalination, Brine & Storage, Support (5 stages).
**Mapping logic:**
- Power & Drive: turbines, gearboxes, HPU, hydraulic motors, batteries (power generation/conversion equipment)
- Water Extraction: pumps that extract groundwater (VTP, submersible pumps)
- Desalination: RO trains, HP pumps, booster pumps, plunger pumps, filtration
- Brine & Storage: brine wells, storage tanks, evaporation ponds
- Support: PLC, pipes/piping, gate valves, calcite contactors, chemicals

**Files to update:** config.py (PROCESS_STAGES keys), equipment_grid.py (_STAGE_ORDER).

### DISP-05: Scorecard Simplification
**Current state:** scorecard.py already renders only Total Cost row (Phase 15 removed land/energy from compute_scorecard_metrics). This requirement may already be satisfied.
**Action:** Verify and confirm. Remove any residual references to land_area or power rows if present.

### DISP-06: Scorecard Legend
**Current state:** Line 242 in scorecard.py: `"Green = lowest cost, Red = highest cost."`
**Action:** Change to `"Lower total cost is better."`

### DISP-07: Comparison Text
**Current state:** processing.py generate_comparison_text already only compares cost (metric_labels has only "cost" key). Already satisfied by Phase 15 changes.
**Action:** Verify and confirm.

### DISP-08: Overview Card Descriptions
**Current state:** overview.py _SYSTEM_CARDS descriptions mention "cost, land area, and energy data". Intro card paragraph 4 mentions "costs, land area, and energy requirements".
**Action:** Rewrite descriptions to mention only cost and equipment comparisons. Remove "land area" and "energy" references.

### DISP-09: Equipment Detail Table
**Current state:** _make_detail_table includes Power and Land Area rows. _make_summary_badges includes Power and Land badges.
**Action:** Remove Power and Land Area from both functions. Keep Name, Quantity, Cost, Lifespan. Also remove _fmt_power and _fmt_land helper functions (dead code after removal).

### DISP-10: Cross-System Comparison Table
**Current state:** _make_cross_system_comparison builds comparison with Cost, Power, Land Area columns.
**Action:** Replace Power and Land Area with Lifespan. Table columns become: System, Name, Cost, Lifespan. Best-value highlighting applies to Cost (lower=better) and Lifespan (higher=better).

### DISP-11: Equipment Descriptions
**Current state:** config.py EQUIPMENT_DESCRIPTIONS has entries for old names (Turbine, PLC, Submersible pump, etc.) AND new Phase 15 names (1.5 MW Turbine, PLC (Siemens...), etc.).
**Action:** Verify all current xlsx equipment names have matching description entries. Old entries for names no longer in xlsx can be left (harmless) or cleaned up.

## Open Questions

1. **DISP-03 exact grouping**
   - What we know: Requirements say 5 groups: Power & Drive / Water Extraction / Desalination / Brine & Storage / Support
   - What's unclear: Exact assignment of borderline items (e.g., does Multi-Media Filtration go in Desalination or Support? Do booster pumps go in Water Extraction or Desalination?)
   - Recommendation: Use engineering logic -- filtration is pre-treatment for desalination so group with Desalination. Booster pumps pressurize for RO so group with Desalination. Keep groupings consistent across all 3 systems.

2. **DISP-02 scope of cleanup**
   - What we know: Unicode chars need cleaning (narrow no-break space, non-breaking space, en-dash, double spaces)
   - What's unclear: Whether ALL equipment names need display mapping or only those with unicode issues
   - Recommendation: Create DISPLAY_NAMES entries only for items that actually need cleanup (have unicode or formatting issues). Use .get(name, name) fallback for items that are already clean.

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection of all target files
- config.py: PROCESS_STAGES, EQUIPMENT_DESCRIPTIONS, SYSTEM_COLORS (exact keys verified)
- equipment_grid.py: _STAGE_ORDER, _make_detail_table, _make_summary_badges, _make_cross_system_comparison (full source read)
- scorecard.py: make_scorecard_table, legend text (full source read)
- overview.py: _SYSTEM_CARDS, create_overview_layout (full source read)
- processing.py: compute_scorecard_metrics, generate_comparison_text (full source read)
- custom.css: existing accent classes (full source read)
- Asset files: verified both old (assets/) and new (project root) PNGs exist with sizes

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new dependencies, purely internal code changes
- Architecture: HIGH - well-established patterns from 15 prior phases; all target files fully read
- Pitfalls: HIGH - unicode key matching and stale column references are documented from prior phase decisions
- Requirements mapping: HIGH - every DISP requirement traced to specific file locations and line numbers

**Research date:** 2026-03-28
**Valid until:** 2026-04-28 (stable -- no external dependency changes)
