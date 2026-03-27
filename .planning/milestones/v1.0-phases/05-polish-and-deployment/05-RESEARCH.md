# Phase 5: Polish and Deployment - Research

**Researched:** 2026-02-22
**Domain:** Plotly/Dash visual polish, browser print-to-PDF, Dash clientside callbacks, CSS @media print
**Confidence:** HIGH (code audit of existing codebase + verified Dash/Plotly docs)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Scorecard export:**
- Print-to-PDF via browser print dialog triggered by an export button
- Print view includes RAG scorecard table plus all comparison charts (cost over time, land area, turbine count, energy breakdown)
- Does NOT include hybrid builder slot selections — results only, not inputs
- Export button placed at the top of the scorecard section, near the heading

**Student onboarding:**
- No explicit instructions, walkthrough, or step indicators — rely on clear visual hierarchy to guide students
- Landing view opens on the overview with the scorecard visible so students see all three systems at a glance
- Sidebar tabs are text-only labels (no icons) — clean and academic
- Hybrid builder gets a single instruction line above the slots: "Select one piece of equipment for each process stage"

**Visual consistency:**
- Full visual audit across all charts and components — no specific priority, equal pass on everything
- Dollar values abbreviated with K/M suffixes ($1.2M, $45K) on chart axes and labels
- Tooltips show full precision ($1,234,567) even when chart labels are abbreviated
- Subtle cards (light borders or shadows) around content groups for clean separation
- RAG scorecard uses colored dots/icons next to values instead of colored cell backgrounds (already done)
- Standard readable font sizing (default Bootstrap) — no compacting
- Claude conducts thorough audit since user hasn't done a visual pass yet

**Comparison description text:**
- Academic neutral tone: factual, no opinion
- Summary sentence format — one or two sentences covering ranking and biggest differentiator
- Placement at Claude's discretion based on existing layout flow
- Updates live whenever hybrid configuration changes (all 5 slots filled)

### Claude's Discretion
- Chart layout density (2x2 grid vs stacked) — pick based on chart readability
- Comparison description text placement
- Exact print CSS styling for export view
- Specific spacing, alignment, and padding values during visual audit

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VIS-02 | Easy to navigate for students unfamiliar with the tool | Visual hierarchy audit findings: landing page already shows scorecard visible; single instruction line on hybrid builder; no icons needed, text tabs already present |
| EXP-01 | User can export or print the scorecard summary for lab reports | Browser print-to-PDF via clientside_callback + window.print(); CSS @media print to hide nav/sidebar/controls and show scorecard + charts |
| DEP-01 | App runs locally via `python app.py` with no external service dependencies | Already working (phase 1 complete); no new dependencies needed; verify clean startup on fresh state |
</phase_requirements>

---

## Summary

Phase 5 is a refinement phase — no new features or data structures. The codebase is complete through Phase 4 with all functional requirements satisfied. This phase applies three categories of work: (1) browser print-to-PDF export via CSS @media print + Dash clientside_callback, (2) visual polish across all chart axes and UI components, and (3) student navigation polish including the hybrid builder instruction line.

The most technically novel piece is the print/export feature. The chosen approach — browser print dialog — is correct for a local academic tool: zero server-side dependencies, works offline, produces PDF or paper output. The implementation requires a CSS @media print stylesheet in assets/custom.css plus a Dash clientside_callback that calls window.print(). Known Bootstrap/dbc print issue (Chrome loses "layout" option) is fixed with @page { size: auto; } in CSS.

Chart axis formatting is the second significant technical area. The existing `fmt_cost()` function in processing.py already abbreviates dollar values correctly for scorecard text ($1.2M, $45K). For chart y-axes, Plotly's `tickformat="~s"` (d3 SI format) produces K/M suffixes combined with `tickprefix="$"` for the cost chart. This is the confirmed working pattern from the Plotly community. Hover tooltips already use explicit hovertemplate strings and should be updated to full-precision dollar format.

Visual audit work involves adding subtle card wrappers to content sections that currently lack visual separation, ensuring consistent use of `shadow-sm` classes (already on chart cards), and verifying color consistency. The comparison text placement should be directly below the scorecard container (already has `id="comparison-text"` div there). The hybrid builder needs one instruction line added above the pipeline row.

**Primary recommendation:** Implement export first (it is the only unmet v1 requirement), then apply chart axis formatting, then visual audit pass, then hybrid instruction line and onboarding check.

---

## Standard Stack

### Core (no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash | 4.0.0 | Already installed | clientside_callback is a core Dash feature |
| dash-bootstrap-components | 2.0.4 | Already installed | dbc.Button for export trigger; CSS classes for layout |
| plotly (via dash) | bundled | Chart formatting | tickformat, tickprefix, hovertemplate are native Plotly props |

### No New pip Packages Required
The print-to-PDF approach (browser print dialog) requires no server-side PDF libraries (no kaleido, no weasyprint, no pdfkit). This is correct for the local academic tool use case — those libraries add Chrome/headless browser dependencies that would violate DEP-01's "no external service dependencies" spirit for student machines.

### Alternatives Considered
| Instead of | Could Use | Why Not |
|------------|-----------|---------|
| browser print dialog | kaleido + dcc.Download | Kaleido v1 requires Chrome installed; adds a pip dependency; overkill for single scorecard export |
| browser print dialog | flask route returning PDF | Requires weasyprint or reportlab; significant extra dependency |
| clientside_callback | dcc.Link with print target | Less control; no way to hide sidebar/navbar |

---

## Architecture Patterns

### Existing Architecture (do not change)

```
app.py                    # Entry point, data load, set_data() calls
src/
├── config.py             # SYSTEM_COLORS, RAG_COLORS, PROCESS_STAGES
├── data/
│   ├── loader.py         # load_data() → dict of DataFrames
│   └── processing.py     # fmt_cost(), compute_scorecard_metrics(), generate_comparison_text()
└── layout/
    ├── shell.py           # App shell, sidebar, dcc.Store(s), nav callbacks
    ├── overview.py        # Landing page cards
    ├── system_view.py     # Tab view assembly
    ├── scorecard.py       # RAG scorecard table + callbacks
    ├── charts.py          # 4 chart builders + callbacks
    ├── hybrid_builder.py  # Pipeline dropdowns + callbacks
    └── equipment_grid.py  # Equipment accordion
assets/
    custom.css            # Currently: sidebar toggle + sidebar transition
```

### Pattern 1: Export Button + clientside_callback (NEW)

**What:** Add an export button to the scorecard section. A Dash clientside_callback fires on button click and calls window.print(). CSS @media print hides everything except the print-relevant content.

**Where to add the button:** In `system_view.py`, inside the scorecard block near `scorecard_container`. The button should be rendered outside `scorecard-container` (which is dynamically replaced by callback) — place it as a static sibling above the scorecard container div.

**Where to add the callback:** In `scorecard.py` or a new `export.py` file (either works — prefer `scorecard.py` since it owns the scorecard section). Use `clientside_callback` (module-level function, not `app.clientside_callback`, which requires app reference).

**Example:**
```python
# In scorecard.py (add after existing callbacks)
from dash import clientside_callback, Input, Output

clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        window.print();
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-btn", "n_clicks"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)
```

**Button definition (in system_view.py):**
```python
dbc.Button(
    "Export / Print",
    id="export-btn",
    color="secondary",
    outline=True,
    size="sm",
    className="mb-2 no-print",  # hide on print so it doesn't appear in PDF
)
```

### Pattern 2: @media print CSS (NEW — in assets/custom.css)

**What:** CSS rules that apply only when the browser print dialog is active. Hides navigation, sidebar, controls, hybrid builder. Shows only scorecard + charts.

**Critical fix for Bootstrap + dbc print issue (VERIFIED):**
Without `@page { size: auto; }`, Chrome's print dialog loses the "Layout" option. This is a known dbc issue (GitHub dbc-team/dash-bootstrap-components #269).

```css
/* ============================================================
   Print styles — applied only in browser print / PDF dialog
   ============================================================ */

/* Fix Bootstrap dbc Chrome print issue — restores Layout option */
@page {
    size: auto;
}

/* Hide non-report elements */
@media print {
    /* Navigation and sidebar */
    .navbar,
    #sidebar,
    #sidebar-toggle,
    .sidebar-toggle-btn,

    /* System tab bar and breadcrumb */
    #system-tabs,
    #back-to-overview,

    /* Interactive controls (sliders, legend badges) */
    .no-print,
    #export-btn,

    /* Hybrid builder inputs (print results only, not inputs) */
    .hybrid-builder-section,

    /* Chart control panel */
    .chart-controls {
        display: none !important;
    }

    /* Ensure content fills page width */
    #page-content {
        padding: 0 !important;
    }

    /* Keep charts visible and full-width */
    .dcc-graph,
    .js-plotly-plot {
        width: 100% !important;
    }

    /* Page break control */
    .scorecard-print-section {
        page-break-inside: avoid;
    }
}
```

**CSS class assignment strategy:**
- Add `className="no-print"` to: export button, legend badges, sliders panel, time-horizon control card
- Add `className="hybrid-builder-section"` to the hybrid builder wrapper in `system_view.py`
- Add `className="chart-controls"` to the control_panel card in `charts.py`
- Scorecard and chart figures print by default (no class needed — just don't hide them)

### Pattern 3: Chart Axis Formatting (UPDATE existing figure builders)

**What:** Update y-axis tick labels on cost and potentially other charts to show K/M abbreviated dollar values. Hover tooltips keep full precision.

**Confirmed approach for cost chart (VERIFIED — Plotly community):**
```python
# In build_cost_chart(), update_layout call:
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Cumulative Cost (USD)",
    yaxis=dict(
        tickprefix="$",
        tickformat="~s",   # d3 SI prefix: 1000 → "1k", 1000000 → "1M"
    ),
    showlegend=False,
    # ... rest unchanged
)
```

**For land area chart:** No dollar sign needed. `tickformat="~s"` alone gives "m²" values cleaner labeling if values are large enough; check actual data values first — if land area is in tens/hundreds of m², no formatting needed (values already readable). Keep `yaxis_title="Area (m²)"`.

**For turbine count chart:** Integer values, small counts — no SI formatting needed. Current `yaxis=dict(dtick=1)` is correct.

**For pie chart:** No axis, no change needed. Hover uses `%{percent}` already.

**Hover tooltip updates — cost chart:**
The existing hovertemplate is:
```python
hovertemplate=f"{name}: %{{y:$,.0f}} at Year %{{x}}<extra></extra>"
```
This already shows full-precision dollar format (`$,.0f`) — CORRECT, no change needed.

**Land chart hover:**
```python
hovertemplate=f"{name}: %{{y:,.0f}} m<sup>2</sup><extra></extra>"
```
Already correct full precision.

### Pattern 4: Hybrid Builder Instruction Line (SMALL ADDITION)

**Where:** In `make_hybrid_builder()` in `hybrid_builder.py`, add one `html.P` above the pipeline row.

**Exact text (from CONTEXT.md):** "Select one piece of equipment for each process stage"

```python
# Add before `pipeline` in the return html.Div:
html.P(
    "Select one piece of equipment for each process stage",
    className="text-muted small mb-2",
),
```

### Pattern 5: Visual Audit — Card Wrappers

**Current state (observed in code):**
- Chart cards: already have `className="shadow-sm h-100"` (good)
- Scorecard table: rendered inside `scorecard-container` div with no outer card wrapper
- Equipment accordion: no outer card wrapper in `equipment_grid.py`
- Chart control panel: already a `dbc.Card` with `shadow-sm` (good)
- Overview cards: already have `className="h-100 shadow-sm"` (good)

**What needs wrapping:**
- Scorecard section: wrap `scorecard_container` + `comparison_text_div` in a `dbc.Card` with subtle border
- Equipment section header area: ensure consistent padding

```python
# In system_view.py, replace bare scorecard/comparison divs with:
dbc.Card(
    dbc.CardBody([
        html.Div(id="scorecard-container"),
        html.Div(id="comparison-text"),
    ]),
    className="shadow-sm mb-3",
)
```

**Note:** The export button must live OUTSIDE this card wrapper (above it) so it appears at the top of the section as specified in CONTEXT.md decisions.

### Anti-Patterns to Avoid

- **Do NOT use kaleido or server-side PDF generation:** Adds heavy dependencies (Chrome/Chromium required by kaleido v1) that break DEP-01 for student machines without those installed.
- **Do NOT put the export button inside `scorecard-container`:** That div is replaced by the scorecard callback on every hybrid slot change, which would destroy the button each time.
- **Do NOT add @media print rules via Dash `external_stylesheets`:** Those are for remote CDN links. Use assets/custom.css instead — Dash auto-serves everything in the assets/ directory.
- **Do NOT hide dcc.Graph components with `display:none` in print CSS:** Use `visibility:hidden` if you need to hide charts selectively, otherwise `display:none` causes layout reflow that can break adjacent chart sizing.
- **Do NOT use `app.clientside_callback`** (requires app object reference in the module): Use the module-level `clientside_callback` function imported from `dash`, consistent with the pattern already used for `callback` throughout the codebase.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Print trigger from button | Custom JS file in assets/ | clientside_callback inline JS | Simpler, no separate file, already the project's pattern for callbacks |
| K/M axis formatting | Custom ticktext array with computed labels | `tickformat="~s"` + `tickprefix="$"` | Native Plotly, updates automatically when data changes, no manual tick calculation |
| PDF generation | Server-side weasyprint or pdfkit | Browser print dialog CSS | Zero dependencies, works offline, student-friendly |
| Hiding print elements | JavaScript toggles | CSS @media print | Declarative, no runtime overhead, browser handles it |

**Key insight:** For a local academic tool, browser print is the right tool for export. Server-side PDF generation is the right tool for programmatic batch reports. This is a student dashboard — browser print wins.

---

## Common Pitfalls

### Pitfall 1: Bootstrap/dbc Breaks Chrome Print Dialog
**What goes wrong:** When using Bootstrap CSS with dbc, Chrome's print dialog loses the "Layout" dropdown (portrait/landscape selection disappears).
**Why it happens:** Bootstrap sets a `@page` rule that conflicts with Chrome's print settings interface.
**How to avoid:** Add `@page { size: auto; }` to `assets/custom.css` BEFORE the `@media print {}` block. This must be a top-level CSS rule, not inside `@media print`.
**Warning signs:** Open Chrome print preview and the "Layout" option is missing from the sidebar.
**Source:** Verified — dbc-team/dash-bootstrap-components GitHub Issue #269, confirmed resolved by the CSS fix.

### Pitfall 2: Export Button Inside Callback-Updated Container
**What goes wrong:** If the export button is placed inside `scorecard-container`, the button gets destroyed and recreated (losing n_clicks state) every time the hybrid slot store changes.
**Why it happens:** The `update_scorecard` callback replaces `scorecard-container`'s `children` entirely on every trigger.
**How to avoid:** Place the export button as a sibling ABOVE `scorecard-container`, not inside it. In system_view.py, add the button before the `scorecard_container` variable in the layout assembly.
**Warning signs:** Button stops responding after toggling hybrid slots.

### Pitfall 3: `tickformat="~s"` Uses Lowercase k Not K
**What goes wrong:** SI prefix format in d3/Plotly uses lowercase "k" for thousands (100k, not 100K), and uppercase M for millions. This may not match the CONTEXT.md decision which shows "$45K" (uppercase K).
**Why it happens:** d3-format follows SI convention: k (kilo), M (mega).
**How to avoid:** Two options:
  1. Accept lowercase k (simpler, standard) — change CONTEXT.md expectation or note in code comments
  2. Use `tickmode="array"` with manually computed `tickvals` and `ticktext` (more work, full control)
  3. The existing `fmt_cost()` function already uses uppercase K/M for text labels in the scorecard — chart axes can use lowercase k/M without inconsistency since they serve different UI roles
**Recommendation:** Use `tickformat="~s"` (lowercase k) for chart axes. The scorecard text labels use `fmt_cost()` with uppercase K already. Different contexts, acceptable inconsistency for a student tool.

### Pitfall 4: Hiding Plotly Charts in Print CSS
**What goes wrong:** `display: none` on a chart container during print can cause remaining charts to render at wrong sizes.
**Why it happens:** Plotly charts size themselves relative to their container at render time; hiding siblings during print can cause layout reflow.
**How to avoid:** Only hide non-chart UI elements (navbar, sidebar, sliders, buttons). Never hide `dcc.Graph` or `.js-plotly-plot` elements — keep all four charts visible in the print view.
**Warning signs:** One chart appears to fill the full page width while others are tiny in print preview.

### Pitfall 5: window.print() Returns Before Dialog Closes
**What goes wrong:** After calling `window.print()`, the clientside callback returns immediately. If you try to restore any DOM state (like resetting n_clicks), it may happen before the print completes.
**Why it happens:** `window.print()` is blocking in some browsers but asynchronous in others.
**How to avoid:** The chosen approach (return `no_update` to keep n_clicks as-is) avoids this entirely. Do not try to reset the button state after printing.

### Pitfall 6: Print CSS Requires Explicit @page Rule Outside @media print Block
**What goes wrong:** Placing `@page { size: auto; }` inside the `@media print {}` block has no effect in some browsers.
**Why it happens:** `@page` is a separate CSS at-rule from `@media`.
**How to avoid:** Place `@page { size: auto; }` as a top-level CSS rule (outside `@media print`).

---

## Code Examples

Verified patterns for this phase:

### Export Button (system_view.py)
```python
# Source: CONTEXT.md decision + Dash docs pattern
# Place ABOVE scorecard_container in layout assembly
export_btn = dbc.Button(
    "Export / Print",
    id="export-btn",
    color="secondary",
    outline=True,
    size="sm",
    className="mb-2 no-print",
)
```

### clientside_callback for Print (scorecard.py)
```python
# Source: Dash clientside-callbacks docs (verified)
from dash import clientside_callback

clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        window.print();
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-btn", "n_clicks"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)
```

### @page and @media print CSS (assets/custom.css)
```css
/* Fix: Bootstrap breaks Chrome print Layout option */
/* Source: dbc GitHub Issue #269 (verified) */
@page {
    size: auto;
}

@media print {
    /* Hide navigation chrome */
    .navbar,
    #sidebar,
    .sidebar-toggle-btn { display: none !important; }

    /* Hide interactive controls */
    .no-print,
    .chart-controls,
    .hybrid-builder-section { display: none !important; }

    /* Remove page-content padding in print */
    #page-content { padding: 0 !important; }
}
```

### Cost Chart Y-Axis with Dollar + K/M (charts.py)
```python
# Source: Plotly community confirmed; d3-format "~s" = SI prefix with trailing zeros trimmed
# In build_cost_chart(), update the update_layout call:
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Cumulative Cost (USD)",
    yaxis=dict(
        tickprefix="$",
        tickformat="~s",
    ),
    showlegend=False,
    uirevision="static",
    transition=_TRANSITION,
    margin=_MARGIN,
    hovermode="x unified",
)
```

### Hybrid Builder Instruction Line (hybrid_builder.py)
```python
# Source: CONTEXT.md locked decision
# Add to make_hybrid_builder() return html.Div children, before `pipeline`:
html.P(
    "Select one piece of equipment for each process stage",
    className="text-muted small mb-2",
),
```

### Scorecard Section Card Wrapper (system_view.py)
```python
# Source: CONTEXT.md — "subtle cards around content groups"
# Replace bare scorecard + comparison_text divs with:
scorecard_card = dbc.Card(
    dbc.CardBody([
        export_btn,                  # export button at top, inside card body
        html.Div(id="scorecard-container"),
        html.Div(id="comparison-text"),
    ]),
    className="shadow-sm mb-3",
)
```
**Note:** The export button is inside the card body here (above scorecard table), satisfying the "near the heading" placement decision without requiring a separate float/flex container. The button still needs `className="no-print"` so it doesn't appear in the PDF.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| kaleido v0 (bundled Chromium) | kaleido v1 (requires system Chrome) | plotly 6.x / kaleido v1 | Kaleido is now wrong choice for offline student machines |
| `app.clientside_callback` | module-level `clientside_callback` from dash | Dash 2.x | Consistent with project's existing `callback` import pattern |
| Bootstrap @page default | `@page { size: auto; }` custom | dbc issue present in current versions | Required workaround for Chrome print dialog |
| `tickformat=".2s"` | `tickformat="~s"` | d3 convention | `~s` trims trailing zeros; `.2s` keeps 2 significant figures always |

**Deprecated/outdated:**
- `app.clientside_callback`: Still works but requires app reference in module scope; module-level `clientside_callback` is the consistent pattern this project uses everywhere.
- kaleido v0: Do not install; v1 is the current version and requires system Chrome.
- `tickformat="SI"`: This is the `exponentformat` option, not `tickformat`. Setting `tickformat="SI"` is incorrect — use `exponentformat="SI"` on the axis dict. For this phase, use `tickformat="~s"` instead (cleaner output).

---

## Visual Audit Checklist (for planner tasks)

This is a codebase-specific audit list derived from reading all layout files:

**Charts (charts.py):**
- [ ] Cost chart y-axis: add `tickprefix="$"`, `tickformat="~s"`
- [ ] Cost chart hover: already `$,.0f` — confirm no change needed
- [ ] Land chart y-axis: title already "Area (m²)" — verify if values need `~s` formatting (check actual data range first)
- [ ] Turbine chart: `yaxis=dict(dtick=1)` already correct — no change
- [ ] Pie chart: no axis — already shows `%{percent}` on hover — confirm labels are stage names (not truncated)
- [ ] All 4 charts: verify `_MARGIN = dict(l=60, r=20, t=10, b=40)` gives enough space for axis labels

**Scorecard (scorecard.py):**
- [ ] Scorecard already uses `fmt_cost()` for values — uppercase K/M already correct
- [ ] RAG dots already implemented — verify dot size (12px) is legible
- [ ] "Best Overall" summary row already present

**Shell / Navigation (shell.py):**
- [ ] Sidebar already text-only (no icons) — no change
- [ ] Landing overview already opens showing cards — no change
- [ ] Verify sidebar is visible by default (data=False in sidebar-collapsed store) — already correct

**Hybrid builder (hybrid_builder.py):**
- [ ] Add instruction line: "Select one piece of equipment for each process stage"
- [ ] Slot counter already present ("0/5 slots filled") — no change
- [ ] Arrows between slots already present — no change

**Overview (overview.py):**
- [ ] Three cards already `h-100 shadow-sm` — no change
- [ ] Card descriptions are clear for new students — verify text quality

**System view assembly (system_view.py):**
- [ ] Add card wrapper around scorecard section
- [ ] Add export button above scorecard
- [ ] Confirm comparison text placement (already `id="comparison-text"` after scorecard-container)

**CSS (assets/custom.css):**
- [ ] Add `@page { size: auto; }` (top-level)
- [ ] Add `@media print { ... }` block hiding navbar, sidebar, controls, hybrid builder
- [ ] Add `.no-print` class hiding (used by export button and other interactive elements)

---

## Open Questions

1. **Land area data range**
   - What we know: `yaxis_title="Area (m²)"` is already set; data is square meters
   - What's unclear: Are values in hundreds (150 m²) or tens of thousands (15,000 m²)? If small values, `tickformat="~s"` will show "150" not "150k" — which is fine
   - Recommendation: During implementation, check actual land values from data.xlsx before deciding whether to apply `~s` format. If max land area < 5,000 m², leave axis format as default (comma-separated integers). If > 10,000 m², add `~s`.

2. **Comparison text div placement in print**
   - What we know: `comparison-text` div is a sibling of `scorecard-container` in system_view.py
   - What's unclear: If the page is printed from the Mechanical or Electrical tab (no hybrid configured), `comparison-text` is None — will it render as blank space?
   - Recommendation: Ensure the `comparison-text` div has no height when empty (add `style={"minHeight": 0}` or the callback should return `None`/`""` which renders nothing).

3. **Charts in print: static vs interactive**
   - What we know: dcc.Graph renders as SVG via Plotly.js — SVGs print correctly in all modern browsers
   - What's unclear: The chart section is only rendered when a system tab is active (not on the overview landing page). If a student tries to print from the overview page, no charts will be visible.
   - Recommendation: The print feature should only be accessible from the system tab view (where charts are rendered). The export button placement in `system_view.py` (not `overview.py`) naturally enforces this. No additional guard needed.

---

## Sources

### Primary (HIGH confidence)
- Existing codebase (C:/Users/kevin/Downloads/Desalination Project Vibe Code/) — direct code audit of all .py files and assets/custom.css; production code in Phases 1-4
- dbc-team/dash-bootstrap-components GitHub Issue #269 — @page CSS fix for Bootstrap print dialog confirmed resolved
- Dash clientside-callbacks official documentation (dash.plotly.com/clientside-callbacks) — verified window.print() pattern and no_update usage

### Secondary (MEDIUM confidence)
- Plotly community forum (community.plotly.com) — confirmed `tickformat="~s"` for SI prefix abbreviation with d3 format
- Plotly yaxis reference (plotly.com/python/reference/layout/yaxis/) — verified tickprefix, tickformat, exponentformat options

### Tertiary (LOW confidence — verify during implementation)
- WebSearch results on @media print patterns — standard CSS techniques, non-Dash-specific; apply straightforwardly
- The exact behavior of `tickformat="~s"` with `tickprefix="$"` combined was not demonstrated with a runnable example in the docs found — test this combination during implementation and fall back to `tickmode="array"` with computed ticktext if the combination doesn't render as expected

---

## Metadata

**Confidence breakdown:**
- Standard stack (no new deps): HIGH — codebase already has everything needed
- Print export (clientside_callback + CSS): HIGH — official Dash docs confirmed, dbc issue verified
- Chart axis formatting (tickformat): MEDIUM — community-confirmed but exact dollar+SI combination not shown in official docs; test during implementation
- Visual audit items: HIGH — based on direct code reading, all items are concrete and actionable
- Pitfalls: HIGH (dbc issue, button-in-callback pitfall) / MEDIUM (CSS print behavior details)

**Research date:** 2026-02-22
**Valid until:** 2026-04-22 (stable ecosystem — Dash 4.0 and dbc 2.0 are current releases)
