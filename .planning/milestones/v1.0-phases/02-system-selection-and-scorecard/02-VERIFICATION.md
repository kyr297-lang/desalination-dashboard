---
phase: 02-system-selection-and-scorecard
verified: 2026-02-21T00:00:00Z
status: human_needed
score: 5/5 must-haves verified
re_verification: false
human_verification:
  - test: "Click Mechanical card then click Electrical tab — confirm equipment list changes to electrical items"
    expected: "Tab view shows Electrical equipment grouped by process stage (Water Extraction, Pre-Treatment, etc.) with electrical-specific items like Turbine, Battery, PLC"
    why_human: "Requires browser interaction to confirm the active-system dcc.Store callback chain fires correctly and re-renders equipment grid on tab click"
  - test: "Expand one accordion item, then click a second accordion item"
    expected: "First item collapses automatically, second item expands — only one open at a time"
    why_human: "always_open=False accordion behavior requires browser interaction to confirm mutual exclusivity at runtime"
  - test: "Confirm RAG indicator dots are visually distinct and clearly visible next to metric values"
    expected: "12px colored circles (green #28A745 or red #DC3545) appear inline before cost/land/energy values, easy to read at a glance"
    why_human: "Visual prominence and legibility cannot be confirmed programmatically"
  - test: "Click the Hybrid tab after navigating into a system view"
    expected: "Empty state message appears: 'Build your hybrid system to see equipment here. The hybrid builder will be available in a future update.'"
    why_human: "Requires browser interaction to confirm tab callback fires for Hybrid and correct empty state renders"
  - test: "Click the '← Overview' breadcrumb link from within any system tab view"
    expected: "Page returns to the landing overview showing the three system cards"
    why_human: "back_to_overview callback sets active-system to None — requires browser confirmation that render_content re-renders the overview"
---

# Phase 2: System Selection and Scorecard — Verification Report

**Phase Goal:** Students can select a system, browse its equipment list, and see an at-a-glance RAG scorecard comparing all three systems
**Verified:** 2026-02-21
**Status:** human_needed (all automated checks passed; 5 browser-interaction items remain)
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can click Mechanical, Electrical, or Hybrid and see the correct equipment list appear | ? HUMAN | Navigation callbacks wired (select_system_from_card, select_system_from_tab, render_content). Requires browser confirmation |
| 2 | Equipment list shows quantity, cost, energy, land area, and lifespan for each component | ✓ VERIFIED | DataFrame has all 6 columns (name, quantity, cost_usd, energy_kw, land_area_m2, lifespan_years). _make_summary_badges() renders all 5 metrics with units. _make_detail_table() renders all 6 fields |
| 3 | User can click an individual piece of equipment and see its detailed description and data | ? HUMAN | AccordionItem with always_open=False, EQUIPMENT_DESCRIPTIONS.get() wired, detail table and cross-system comparison rendered in expanded content. Requires browser interaction to confirm expand/collapse |
| 4 | Scorecard displays cost, land area, and efficiency values for Mechanical and Electrical systems (Hybrid deferred to Phase 4 per user decision) | ✓ VERIFIED | make_scorecard_table() computes and displays all 3 metrics for Mechanical and Electrical. Hybrid column explicitly omitted per plan line 176: "Hybrid column omitted per user decision" |
| 5 | Each scorecard metric has a clearly visible red or green indicator relative to the other systems | ? HUMAN | rag_color() produces correct hex assignments (mechanical cost → green #28A745, electrical cost → red #DC3545; electrical land/energy → green, mechanical land/energy → red). 12px dot spans rendered via _make_rag_dot(). Visual prominence requires browser confirmation |

**Score:** 5/5 truths have valid implementation (2 need human confirmation of runtime behavior)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/data/processing.py` | Formatting helpers, RAG logic, scorecard computation | ✓ VERIFIED | 240 lines, 6 exported functions (fmt_cost, fmt_num, fmt, rag_color, compute_scorecard_metrics, get_equipment_stage). Pure data/logic module, no UI imports |
| `src/config.py` | PROCESS_STAGES, EQUIPMENT_DESCRIPTIONS, RAG_COLORS | ✓ VERIFIED | All 4 constants present. PROCESS_STAGES covers mechanical (5 stages, 9 items), electrical (6 stages including Control, 10 items), miscellaneous (4 stages, 6 items). EQUIPMENT_DESCRIPTIONS has 24 entries |
| `src/layout/overview.py` | Landing page with three system selection cards | ✓ VERIFIED | 113 lines, create_overview_layout() returns html.Div with intro text and dbc.Row of 3 cards. Each card has colored header (SYSTEM_COLORS), description, and pattern-matched Explore button |
| `src/layout/system_view.py` | Tab bar + content area assembling scorecard and equipment grid | ✓ VERIFIED | 118 lines, create_system_view_layout() assembles breadcrumb, dbc.Tabs (3 tabs with active_tab prop), scorecard, and equipment section |
| `src/layout/scorecard.py` | RAG scorecard comparison table | ✓ VERIFIED | 196 lines, make_scorecard_table() builds bordered table with RAG dot indicators, 3 metric rows, best-overall summary row |
| `src/layout/equipment_grid.py` | Equipment card grid with accordion detail and cross-system comparison | ✓ VERIFIED | 428 lines, make_equipment_section() groups equipment by process stage, renders dbc.Accordion(always_open=False) with full detail including description, badges, data table, and cross-system comparison |
| `src/layout/shell.py` | Updated shell with active-system store and navigation callbacks | ✓ VERIFIED | dcc.Store(id="active-system") in layout, set_data() function, 3 separate navigation callbacks (select_system_from_card, select_system_from_tab, back_to_overview), render_content callback |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/layout/shell.py` | `src/layout/overview.py` | render_content callback imports create_overview_layout | ✓ WIRED | Deferred import inside callback body confirmed present |
| `src/layout/shell.py` | `src/layout/system_view.py` | render_content callback imports create_system_view_layout | ✓ WIRED | Deferred import inside callback body confirmed present |
| `src/layout/system_view.py` | `src/layout/scorecard.py` | imports make_scorecard_table | ✓ WIRED | Top-level import at line 16, called at line 100 |
| `src/layout/system_view.py` | `src/layout/equipment_grid.py` | imports make_equipment_section | ✓ WIRED | Top-level import at line 17, called at line 104 |
| `src/layout/scorecard.py` | `src/data/processing.py` | imports compute_scorecard_metrics, rag_color, fmt_cost | ✓ WIRED | `from src.data.processing import compute_scorecard_metrics, rag_color, fmt_cost` confirmed |
| `src/layout/equipment_grid.py` | `src/data/processing.py` | imports fmt_cost, fmt_num, fmt, get_equipment_stage | ✓ WIRED | `from src.data.processing import fmt_cost, fmt_num, fmt, get_equipment_stage` confirmed |
| `src/layout/equipment_grid.py` | `src/config.py` | imports EQUIPMENT_DESCRIPTIONS for detail view | ✓ WIRED | `from src.config import EQUIPMENT_DESCRIPTIONS, PROCESS_STAGES` confirmed |
| `src/data/processing.py` | `src/config.py` | imports RAG_COLORS | ✓ WIRED | `from src.config import PROCESS_STAGES, RAG_COLORS` confirmed |
| `app.py` | `src/layout/shell.py` | calls set_data(DATA) after layout creation | ✓ WIRED | Lines 67-68: `from src.layout.shell import set_data; set_data(DATA)` inside `if DATA is not None` block |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| SEL-01 | 02-02 | User can select between Mechanical, Electrical, or Hybrid system from a clear selector interface | ✓ SATISFIED | Three-card landing overview with pattern-matched Explore buttons; tab bar with 3 tabs; active-system dcc.Store drives navigation |
| SEL-02 | 02-02 | Selecting Mechanical or Electrical shows equipment list with quantity, cost, energy, land area, and lifespan | ✓ SATISFIED | DataFrame has all 5 metric columns; _make_summary_badges() renders all 5 with units; _make_detail_table() renders all 6 fields |
| SEL-03 | 02-02 | User can click/select individual equipment for detailed description and data | ✓ SATISFIED | dbc.AccordionItem per equipment; expanded content includes EQUIPMENT_DESCRIPTIONS text, detail table, and cross-system comparison |
| SCORE-01 | 02-01, 02-02 | Dashboard displays cost, land area, and efficiency scorecard for all systems | ✓ SATISFIED (2 of 3 systems; Hybrid deferred by user decision) | compute_scorecard_metrics() aggregates all 3 metrics; make_scorecard_table() renders them for Mechanical and Electrical |
| SCORE-02 | 02-01, 02-02 | Each metric has red/yellow/green (RAG) ranking relative to the three systems | ✓ SATISFIED (green/red for 2-system case; yellow logic implemented for Phase 4) | rag_color() correctly assigns green to lower-cost/land/energy system and red to higher. Yellow logic verified for 3-system case in code: `rag_color({'a':10,'b':20,'c':30}, 'cost')` returns yellow for middle |
| VIS-01 | 02-02 | Academic styling — clean, professional, muted colors (FLATLY Bootstrap theme) | ✓ SATISFIED | `dbc.themes.FLATLY` in app.py; shadow-sm classes; muted color palette; h-100 cards; text-muted paragraph styling |
| VIS-02 | 02-02 | Easy to navigate for students unfamiliar with the tool | ? HUMAN | Intro text present; "Explore" buttons labeled; breadcrumb link back; empty state for Hybrid. Learnability requires human judgment |

**Note on SCORE-01/SCORE-02:** The ROADMAP success criteria say "all three systems" but the plan (line 176) explicitly documents "Hybrid column omitted per user decision — hidden until Phase 4." This is an acknowledged scope decision, not an implementation gap. The yellow RAG color logic is implemented and verified; it will activate when Hybrid data flows in Phase 4.

**Note on orphaned requirements:** No Phase 2 requirements in REQUIREMENTS.md are unmapped. All 7 requirement IDs (SEL-01, SEL-02, SEL-03, SCORE-01, SCORE-02, VIS-01, VIS-02) appear in one or both plan frontmatter sections.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/data/processing.py` | 32 | `XXX` in docstring | ℹ️ Info | Not code — appears in docstring format string `"$X,XXX"` to illustrate the thousands formatting pattern. Zero impact |
| `src/data/processing.py` | 142 | `return {}` | ℹ️ Info | Guard clause in rag_color() — returns empty dict when no valid (non-None) values are provided. Correct defensive programming, not a stub |

No blocker or warning-level anti-patterns found.

### Human Verification Required

#### 1. System card navigation

**Test:** Run `python app.py`, open browser to http://127.0.0.1:8050. Click "Explore" on the Mechanical card.
**Expected:** Page switches to tab view showing Mechanical active (colored bottom border), scorecard visible above equipment list grouped by stage (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal).
**Why human:** The select_system_from_card callback fires via pattern-matching Input — requires browser to confirm DOM event propagation and callback chain through dcc.Store.

#### 2. Tab switching between systems

**Test:** From the Mechanical tab view, click the "Electrical" tab.
**Expected:** Equipment list re-renders with electrical system items (Turbine, Battery, PLC, etc.). Electrical tab gains colored border in Electrical system color (#D4854A).
**Why human:** select_system_from_tab callback writes to active-system store which triggers render_content — requires browser to confirm no circular callback errors and correct re-render.

#### 3. Accordion one-at-a-time expansion

**Test:** Click any equipment item to expand it, then click a second different equipment item.
**Expected:** First item collapses automatically before second expands. Only one item is open at any time.
**Why human:** always_open=False is a dbc.Accordion prop — requires browser interaction to confirm Dash Bootstrap Components implements mutual exclusion at runtime.

#### 4. RAG dot visual clarity

**Test:** View the System Scorecard table with Mechanical and Electrical columns.
**Expected:** Clearly visible 12px colored circles (green or red) appear to the left of each formatted value. The color distinction is immediately apparent.
**Why human:** Visual prominence and legibility of the dot indicators cannot be verified programmatically.

#### 5. Back to Overview navigation

**Test:** From any system tab view, click the "← Overview" breadcrumb link.
**Expected:** Page returns to the landing overview with three system cards visible.
**Why human:** back_to_overview callback sets active-system store to None, triggering render_content to call create_overview_layout() — requires browser to confirm the link element is clickable and callback fires.

### Implementation Quality Notes

- **Real data verified:** Mechanical total cost $11.9M, Electrical total cost $15.4M. RAG correctly assigns green to Mechanical (lower cost), green to Electrical (lower land area: 1,347 vs 1,815 m²), green to Electrical (lower energy: 559 vs 596 kW).
- **All 9 mechanical + 10 electrical equipment items** are covered in PROCESS_STAGES and EQUIPMENT_DESCRIPTIONS.
- **Cross-system comparison** in expanded accordion finds equipment in the same process stage from the other system — implemented and wired via get_equipment_stage().
- **Circular import prevention** via deferred imports inside render_content callback body — clean pattern documented in SUMMARY.
- **split callbacks pattern** (allow_duplicate=True) prevents the DOM-missing-element bug where system-tabs and back-to-overview don't exist on the initial landing page.
- **app.py loads cleanly** with no import errors; DATA is non-None; app layout is set.

---

_Verified: 2026-02-21_
_Verifier: Claude (gsd-verifier)_
