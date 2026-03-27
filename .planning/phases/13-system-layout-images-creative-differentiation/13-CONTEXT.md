# Phase 13: System Layout Images & Creative Differentiation - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Embed the three PNG architecture diagrams (Mechanical, Electrical, Hybrid) on their respective system pages as prominent, full-width visuals — and make the mechanical and electrical pages structurally distinct beyond the color border-top already established in Phase 9. Hybrid only needs its diagram (VISUAL-03); structural differentiation applies to mechanical vs electrical only (VISUAL-04).

</domain>

<decisions>
## Implementation Decisions

### PNG File Location (technical prerequisite)
- **D-01:** The three PNGs currently sit at the project root (`Mechanical System Layout.png`, `Electrical System Layout.png`, `Hybrid System Layout.png`). They must be copied/moved into `assets/` so Dash's static file server can serve them (Dash serves `assets/` automatically; root-level files are not accessible via URL).
- **D-02:** File names in `assets/` should be URL-safe (no spaces) — e.g., `mechanical-layout.png`, `electrical-layout.png`, `hybrid-layout.png`.

### Image Placement (VISUAL-01, VISUAL-02, VISUAL-03)
- **D-03:** Diagram appears at the **top of the system page**, before the scorecard. Page order becomes: Diagram Card → Scorecard Card → Equipment Card → Charts. This applies to all three systems.
- **D-04:** Diagram is wrapped in a `dbc.Card` / `dbc.CardBody` with `shadow-sm mb-3` to match the existing card pattern for scorecard and equipment sections.

### Image Display Style
- **D-05:** Plain full-width image — `html.Img` with `style={"width": "100%", "height": "auto"}` and `className="d-block"`. No caption, no modal, no toggle. Academic, clean.
- **D-06:** No extra label or figure caption — the system identity is already clear from the tab bar and system badge.
- **D-07:** Diagrams are **included** in print/PDF export (do NOT add `no-print` class). Students can print the system layout alongside the scorecard for lab reports.

### Creative Layout Differentiation (VISUAL-04)
- **D-08:** Section order is the SAME for mechanical and electrical (Diagram → Scorecard → Equipment → Charts). Do NOT reorder sections. User explicitly rejected section-order flip.
- **D-09:** The differentiation approach is **Claude's Discretion** — the researcher should examine the actual PNG contents (visual complexity, component density, flow patterns) and propose an approach that reflects each system's engineering character. Possible directions to explore: diagram sizing/weight, card styling differences (border treatment, header style, background tint), equipment section presentation (mechanical's stage-grouped table vs electrical's component grid), or typographic emphasis.
- **D-10:** Mechanical system character = hydraulic/mechanical force and flow (complex multi-stage pipeline, many physical components). Electrical system character = power budget and control (cleaner electrical diagram, fewer but more specialized components including battery and PLC). The differentiation should reflect this, not just apply decorative styling.
- **D-11:** The existing color border-top (Phase 9, `#page-content`) is a baseline — this phase must deliver something additional and structural beyond that.

### Claude's Discretion
- Specific implementation of VISUAL-04 (how exactly mechanical and electrical differ visually) — researcher examines PNG contents and existing page layouts, then proposes the most fitting approach
- Whether any CSS is added to `custom.css` vs inline styles
- Whether `system_view.py` uses conditional logic per `active_system` or separate layout factory functions

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Layout
- `src/layout/system_view.py` — Main file to modify; assembles all system page sections; contains the layout order, card pattern, and system-conditional rendering
- `src/config.py` — SYSTEM_COLORS dict (Mechanical: #5B8DB8, Electrical: #D4A84A, Hybrid: #6BAA75); PROCESS_STAGES for equipment grouping

### Styling
- `assets/custom.css` — Existing custom styles; print rules are here; new diagram/differentiation CSS goes here

### PNG Source Files
- `Mechanical System Layout.png` — at project root; must be copied to `assets/`
- `Electrical System Layout.png` — at project root; must be copied to `assets/`
- `Hybrid System Layout.png` — at project root; must be copied to `assets/`

### Phase 9 Prior Work
- Phase 9 added `border-top` per system color on `#page-content` (in `render_content` callback in `app.py`) — this is the existing differentiation baseline; Phase 13 must go beyond this

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Patterns
- All three system pages render via `create_system_view_layout(active_system, data)` in `system_view.py` — this is the single function to modify
- Current card pattern: `dbc.Card(dbc.CardBody(...), className="shadow-sm mb-3")` used for scorecard and equipment — diagram card should match this pattern
- `html.Img` does not currently appear anywhere in the codebase — this is new
- `active_system` string ("mechanical" / "electrical" / "hybrid") is available in `create_system_view_layout` — can be used for conditional rendering

### Integration Points
- `assets/` folder already exists (contains `custom.css`) — Dash serves it automatically; just copy PNGs there
- `app.py` `render_content` callback sets the `borderTop` on `#page-content` per system (Phase 9 work) — no change needed here for diagram placement
- Print CSS in `custom.css` currently hides `.no-print` elements — diagram should NOT have `no-print` class

### Known Constraints
- Academic tone — no flashy UI; diagram should look like an engineering reference, not a hero image
- Desktop-first — no mobile layout concern
- `suppress_callback_exceptions=True` in app — removed IDs won't error, but new IDs must be consistent

</code_context>

<specifics>
## Specific User Inputs

- Diagram placement: **top of page, before scorecard** — user selected this as the visual priority point
- Image style: **plain full-width image** — `width: 100%`, no caption, no modal, no toggle
- Print export: **include diagrams** — students should be able to print system layout with scorecard
- Layout differentiation: **Claude's Discretion** — user does not want to prescribe the approach; wants researcher to investigate PNG contents and determine what fits each system's character. User explicitly said: "don't just make it a different order."

</specifics>

<deferred>
## Deferred Ideas

- **Collapsible diagram toggle** — mentioned as an option but not chosen; deferred to future milestone (listed in REQUIREMENTS.md future requirements)
- **Figure captions** — clean without them; could add later if academic reviewers request it

</deferred>

---

*Phase: 13-system-layout-images-creative-differentiation*
*Context gathered: 2026-03-26*
