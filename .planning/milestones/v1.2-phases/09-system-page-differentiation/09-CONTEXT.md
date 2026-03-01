# Phase 9: System Page Differentiation - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Give the Mechanical and Electrical system pages a distinct, page-wide visual identity so students can tell which system they are viewing from the visual styling alone, without reading the tab or header text. Hybrid page differentiation is out of scope. This phase does not change the data, layout structure, or interactive behavior of either page.

</domain>

<decisions>
## Implementation Decisions

### Primary differentiation mechanism
- A light background tint (15–25% opacity) of the system's existing SYSTEM_COLORS fills the main content area (`#page-content`) when a Mechanical or Electrical system tab is active
- Tint is applied to the content area only — the sidebar stays neutral
- This creates a genuine page-wide color identity, not just a subtle accent on one element

### System badge
- A small badge displaying the system name only (e.g. "Mechanical", "Electrical") appears below the tab bar and above the scorecard
- Badge uses the system color (text or background) to reinforce the identity with a text label
- Badge is minimal — no description text, no icon required

### Print/PDF behavior
- Both the background tint and the system badge must appear in the exported PDF / print view
- The existing `no-print` CSS class must NOT be applied to these elements — they are intentional print identifiers

### Claude's Discretion
- Exact CSS implementation of the tint (background-color with rgba vs. overlay div vs. class on page-content)
- Badge component type (dbc.Badge, dbc.Alert with color, or custom html.Span)
- Exact shade/opacity within the 15–25% range — tune for readability against FLATLY cards
- Whether the Hybrid tab also gets a tint (not discussed — Claude may apply the existing Hybrid SYSTEM_COLOR at the same opacity for visual consistency, or leave it neutral)

</decisions>

<specifics>
## Specific Ideas

- User described this as needing "a decent overhaul" — the intent is a real, unmistakable page-wide color shift, not a border or a single widget
- The effect should be immediately perceptible when a student switches between Mechanical and Electrical tabs

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SYSTEM_COLORS` in `src/config.py`: Mechanical = `#5B8DB8` (muted steel blue), Electrical = `#D4854A` (muted terra cotta) — use these as the tint source colors
- `create_system_view_layout(active_system, data)` in `src/layout/system_view.py` — this is where the badge and tint injection will happen; `active_system` is already available as a parameter

### Established Patterns
- Active tab already uses `SYSTEM_COLORS` via `borderBottom` highlight — the tint extends this color language to the full page
- `assets/custom.css` is minimal, with room for new page-level rules
- Cards use `dbc.Card` with `className="shadow-sm mb-3"` — they will float visually on the tinted background

### Integration Points
- The tint likely targets `#page-content` (the main content div) — `style` prop or a dynamic CSS class based on `active_system`
- The badge is inserted into `top_level_children` in `create_system_view_layout()`, between `tab_bar` and the main content section
- Print CSS in `custom.css` currently hides `.no-print` elements; the badge and tint elements must NOT carry that class

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 09-system-page-differentiation*
*Context gathered: 2026-03-01*
