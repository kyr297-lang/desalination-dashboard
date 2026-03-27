# Phase 13: System Layout Images & Creative Differentiation - Research

**Researched:** 2026-03-26
**Domain:** Dash layout composition, static asset serving, CSS-based visual differentiation
**Confidence:** HIGH

## Summary

This phase adds three PNG architecture diagrams to their respective system pages and introduces structural visual differentiation between the mechanical and electrical pages. The implementation is entirely within the existing Dash/dash-bootstrap-components stack -- no new libraries are needed. The work breaks down into two concerns: (1) a file-copy + layout insertion task that is identical for all three systems, and (2) a creative differentiation task that applies CSS and layout adjustments to mechanical vs electrical pages only.

The PNG images reveal important character differences. The **mechanical diagram** is visually dense -- a complex hydraulic manifold with branching flows to three motors, a vertical turbine pump, and multiple downstream process stages. It has significant vertical and horizontal spread. The **electrical diagram** is a clean left-to-right linear pipeline with fewer components and no branching. The **hybrid diagram** combines elements of both, falling between them in complexity. These visual characteristics should drive the differentiation approach: the mechanical page should emphasize the complexity and density of its hydraulic drivetrain, while the electrical page should emphasize the simplicity and control-oriented nature of its power budget.

**Primary recommendation:** Copy PNGs to `assets/` with URL-safe names, insert a diagram `dbc.Card` before the scorecard card in `create_system_view_layout`, and differentiate mechanical vs electrical via card header styling and equipment section heading treatment -- using `active_system` conditional logic in the existing layout factory function rather than separate factory functions.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: PNGs must be copied from project root to `assets/` (Dash serves assets/ automatically)
- D-02: URL-safe filenames: `mechanical-layout.png`, `electrical-layout.png`, `hybrid-layout.png`
- D-03: Diagram appears at top of system page, before scorecard. Order: Diagram Card -> Scorecard Card -> Equipment Card -> Charts
- D-04: Diagram wrapped in `dbc.Card` / `dbc.CardBody` with `shadow-sm mb-3`
- D-05: Plain full-width image -- `html.Img` with `style={"width": "100%", "height": "auto"}` and `className="d-block"`
- D-06: No caption, no modal, no toggle
- D-07: Diagrams included in print/PDF export (do NOT add `no-print` class)
- D-08: Section order is SAME for mechanical and electrical (Diagram -> Scorecard -> Equipment -> Charts). Do NOT reorder sections
- D-09: Differentiation approach is Claude's Discretion -- researcher examines PNG contents and proposes approach
- D-10: Mechanical = hydraulic force/flow (complex multi-stage, many components). Electrical = power budget/control (cleaner, fewer specialized components with battery and PLC). Differentiation must reflect this
- D-11: Must deliver something additional and structural beyond the existing color border-top from Phase 9

### Claude's Discretion
- Specific implementation of VISUAL-04 (how mechanical and electrical differ visually)
- Whether CSS goes in `custom.css` vs inline styles
- Whether `system_view.py` uses conditional logic per `active_system` or separate layout factory functions

### Deferred Ideas (OUT OF SCOPE)
- Collapsible diagram toggle -- deferred to future milestone
- Figure captions -- could add later if academic reviewers request
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VISUAL-01 | Mechanical system layout image displayed on mechanical page | D-01 through D-07: copy PNG to assets/, insert as html.Img in dbc.Card before scorecard |
| VISUAL-02 | Electrical system layout image displayed on electrical page | Same pattern as VISUAL-01, different PNG file |
| VISUAL-03 | Hybrid system layout image displayed on hybrid page | Same pattern as VISUAL-01, different PNG file |
| VISUAL-04 | Mechanical and electrical pages have creatively distinct layouts | Differentiation approach detailed in Architecture Patterns section below |
</phase_requirements>

## Standard Stack

### Core (already in project)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dash | 2.x (installed) | Web framework | Already the project framework |
| dash-bootstrap-components | 1.x (installed) | Card, Badge, layout components | Already used for all page structure |
| dash html | (built-in) | html.Img for image rendering | Part of Dash core |

### Supporting
No new libraries needed. All work uses existing Dash components and CSS.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| html.Img in dbc.Card | dcc.Graph with static image | Unnecessary complexity; html.Img is the correct tool for a static PNG |
| CSS classes in custom.css | All inline styles | CSS classes are better for print rules and maintainability; recommendation below uses a mix |

## Architecture Patterns

### File Copy Pattern
```
assets/
  custom.css          (existing)
  mechanical-layout.png   (new -- copy from project root)
  electrical-layout.png   (new -- copy from project root)
  hybrid-layout.png       (new -- copy from project root)
```

Dash serves everything in `assets/` at `/assets/filename`. The `html.Img` src attribute should use the path `/assets/mechanical-layout.png` (leading slash, relative to Dash app root).

### Pattern 1: Diagram Card Insertion
**What:** Add a diagram card to the `main_content_children` list in `create_system_view_layout`, before `scorecard_card`.
**When to use:** All three systems.
**Example:**
```python
# In create_system_view_layout, after tab_bar and system_badge, before scorecard
_DIAGRAM_FILES = {
    "mechanical": "/assets/mechanical-layout.png",
    "electrical": "/assets/electrical-layout.png",
    "hybrid": "/assets/hybrid-layout.png",
}

diagram_src = _DIAGRAM_FILES.get(active_system)
diagram_card = dbc.Card(
    dbc.CardBody(
        html.Img(
            src=diagram_src,
            style={"width": "100%", "height": "auto"},
            className="d-block",
            alt=f"{active_system.capitalize()} system layout diagram",
        )
    ),
    className="shadow-sm mb-3",
)

# Insert before scorecard_card in main_content_children
main_content_children = [
    diagram_card,
    scorecard_card,
    equipment_card,
]
```

### Pattern 2: Creative Differentiation via Conditional Styling (VISUAL-04)
**What:** Apply system-specific CSS classes and minor layout adjustments to the diagram card and equipment section headings based on `active_system`. This uses the existing conditional rendering path -- no separate factory functions needed.
**When to use:** Mechanical and electrical pages only. Hybrid gets the default/neutral treatment.

**Recommended Differentiation Approach (based on PNG analysis):**

Having examined the three diagrams:

1. **Mechanical diagram card -- "Engineering Blueprint" treatment:**
   - The mechanical PNG is visually dense with branching hydraulic flows, a manifold distributing to three motors, and significant vertical spread. It warrants visual emphasis on its complexity.
   - Diagram card gets a subtle left border accent (4px solid in mechanical color #5B8DB8) to echo a technical specification/blueprint feel.
   - Equipment section stage headings get a left-border accent bar (matching the mechanical color), reinforcing the "pipeline of stages" concept. This complements the dense stage-grouped accordion.

2. **Electrical diagram card -- "Clean Schematic" treatment:**
   - The electrical PNG is a clean, linear left-to-right flow with fewer components. The system's character is precision and control (battery, PLC).
   - Diagram card gets a thin top-border accent (2px solid in electrical color #D4A84A) -- a cleaner, more restrained accent that matches the diagram's linear simplicity.
   - Equipment section stage headings use a bottom-border underline style (thin line in electrical color) instead of the left-bar, reflecting the linear flow character.

3. **Hybrid -- neutral (no extra treatment):**
   - The hybrid diagram is already the most complex visually. It gets the standard card with no extra accent (just the shadow-sm baseline). The existing green border-top from Phase 9 is sufficient identity.

**Implementation approach -- CSS classes in custom.css:**
```css
/* Mechanical system -- blueprint accent */
.system-card-mechanical {
    border-left: 4px solid #5B8DB8;
}

.system-card-mechanical .card-body {
    background-color: rgba(91, 141, 184, 0.03);
}

/* Electrical system -- clean schematic accent */
.system-card-electrical {
    border-top: 2px solid #D4A84A;
}

/* Equipment stage headings per system */
.stage-heading-mechanical {
    border-left: 3px solid #5B8DB8;
    padding-left: 0.5rem;
}

.stage-heading-electrical {
    border-bottom: 2px solid #D4A84A;
    padding-bottom: 0.25rem;
}
```

**In system_view.py -- conditional class application:**
```python
# Diagram card gets system-specific class for mech/elec
diagram_extra_class = ""
if active_system == "mechanical":
    diagram_extra_class = " system-card-mechanical"
elif active_system == "electrical":
    diagram_extra_class = " system-card-electrical"

diagram_card = dbc.Card(
    dbc.CardBody(
        html.Img(
            src=diagram_src,
            style={"width": "100%", "height": "auto"},
            className="d-block",
            alt=f"{active_system.capitalize()} system layout diagram",
        )
    ),
    className=f"shadow-sm mb-3{diagram_extra_class}",
)
```

**In equipment_grid.py -- stage heading classes:**
```python
# In the stage section loop, add system-specific class to the H5
stage_class = "mt-4 mb-2"
if system == "mechanical":
    stage_class += " stage-heading-mechanical"
elif system == "electrical":
    stage_class += " stage-heading-electrical"

html.H5(stage, className=stage_class)
```

### Anti-Patterns to Avoid
- **Reordering sections per system (D-08 violation):** User explicitly rejected section-order flip. Do not move scorecard above diagram for one system and below for another.
- **Decorative-only differentiation:** Adding gradients, shadows, or visual effects that have no connection to the system's engineering character. The differentiation must be structural and meaningful.
- **Separate layout factory functions:** The changes are small enough (a few conditional class names) that splitting into `_make_mechanical_layout()` / `_make_electrical_layout()` would duplicate code unnecessarily. Use conditional logic within the existing function.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Static image serving | Custom Flask route for PNGs | Dash `assets/` folder auto-serving | Dash serves assets/ contents at `/assets/` URL automatically; zero config |
| Responsive images | JavaScript resize observer | CSS `width: 100%; height: auto` | Standard CSS handles this perfectly for a desktop-first app |
| Print inclusion of images | Custom print JS | Absence of `no-print` class | The existing print CSS only hides elements with `.no-print`; omitting the class is sufficient |

## Common Pitfalls

### Pitfall 1: Spaces in Asset Filenames
**What goes wrong:** Dash may fail to serve files with spaces in the name, or URLs will need encoding.
**Why it happens:** The source PNGs have spaces: `Mechanical System Layout.png`.
**How to avoid:** Copy to assets/ with URL-safe names per D-02: `mechanical-layout.png`, etc.
**Warning signs:** 404 errors when loading the image on the page.

### Pitfall 2: Incorrect Image src Path
**What goes wrong:** Image shows broken icon or 404.
**Why it happens:** Using a filesystem path instead of Dash URL path, or missing leading slash.
**How to avoid:** Use `/assets/mechanical-layout.png` (with leading slash). Dash maps the `assets/` directory to the `/assets/` URL prefix automatically.
**Warning signs:** Image element rendered in DOM but no image displayed.

### Pitfall 3: Print CSS Accidentally Hiding Diagram
**What goes wrong:** Diagram disappears in print/PDF output.
**Why it happens:** Adding `no-print` class to the diagram card, or a CSS rule that hides card elements in print.
**How to avoid:** Do NOT add `no-print` class to diagram card (D-07). Verify print output includes diagram.
**Warning signs:** Missing diagram in browser print preview.

### Pitfall 4: New CSS Classes Conflicting with Bootstrap
**What goes wrong:** Custom border styles get overridden by Bootstrap card defaults.
**Why it happens:** Bootstrap card has its own border rules with moderate specificity.
**How to avoid:** Use class selectors specific enough to override (e.g., `.system-card-mechanical` on the card element itself). If needed, add `!important` but try specificity first.
**Warning signs:** Border accent not appearing despite class being applied.

### Pitfall 5: Forgetting to Pass system to equipment_grid
**What goes wrong:** Stage headings don't get system-specific classes.
**Why it happens:** `make_equipment_section` already receives `system` parameter -- this is not actually a risk. But modifying the H5 inside `equipment_grid.py` without testing could break the stage header layout.
**How to avoid:** The `system` parameter is already available in `make_equipment_section` and the stage section loop. Just add the conditional class.
**Warning signs:** All systems show the same stage heading style.

## Code Examples

### Copying PNGs to assets/ (shell task)
```bash
cp "Mechanical System Layout.png" assets/mechanical-layout.png
cp "Electrical System Layout.png" assets/electrical-layout.png
cp "Hybrid System Layout.png" assets/hybrid-layout.png
```

### Complete Diagram Card Integration in system_view.py
```python
# At module level, after imports
_DIAGRAM_FILES = {
    "mechanical": "/assets/mechanical-layout.png",
    "electrical": "/assets/electrical-layout.png",
    "hybrid": "/assets/hybrid-layout.png",
}

_DIAGRAM_CARD_CLASSES = {
    "mechanical": "shadow-sm mb-3 system-card-mechanical",
    "electrical": "shadow-sm mb-3 system-card-electrical",
    "hybrid": "shadow-sm mb-3",
}

# Inside create_system_view_layout, before scorecard_card construction:
diagram_src = _DIAGRAM_FILES.get(active_system, "")
diagram_card = dbc.Card(
    dbc.CardBody(
        html.Img(
            src=diagram_src,
            style={"width": "100%", "height": "auto"},
            className="d-block",
            alt=f"{active_system.capitalize()} system layout diagram",
        )
    ),
    className=_DIAGRAM_CARD_CLASSES.get(active_system, "shadow-sm mb-3"),
)

# Update main_content_children to include diagram first:
main_content_children = [
    diagram_card,
    scorecard_card,
    equipment_card,
]
```

### CSS Additions to custom.css
```css
/* ── System layout diagram differentiation (Phase 13) ─────────── */

/* Mechanical: blueprint-style left accent bar + very subtle tinted background */
.system-card-mechanical {
    border-left: 4px solid #5B8DB8;
}
.system-card-mechanical .card-body {
    background-color: rgba(91, 141, 184, 0.03);
}

/* Electrical: clean top-line accent */
.system-card-electrical {
    border-top: 2px solid #D4A84A;
}

/* Stage heading accents for equipment sections */
.stage-heading-mechanical {
    border-left: 3px solid #5B8DB8;
    padding-left: 0.5rem;
}

.stage-heading-electrical {
    border-bottom: 2px solid #D4A84A;
    padding-bottom: 0.25rem;
}

/* Ensure diagram card prints with accent borders */
@media print {
    .system-card-mechanical,
    .system-card-electrical {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```

## State of the Art

No technology migration or deprecated APIs involved. This phase uses standard Dash HTML components and CSS -- stable and well-documented.

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| N/A | html.Img in dbc.Card | Stable | Standard Dash pattern for static images |

## Open Questions

1. **PNG file sizes / load performance**
   - What we know: The PNGs are standard architecture diagrams. Desktop-first app, so bandwidth is not a major concern.
   - What's unclear: Exact file sizes. If any PNG exceeds ~2MB, it could slow page loads.
   - Recommendation: Check file sizes during implementation. If large, consider running through an image optimizer (outside scope of this phase but worth noting).

2. **Background tint on mechanical card**
   - What we know: The proposed `rgba(91, 141, 184, 0.03)` is extremely subtle -- 3% opacity.
   - What's unclear: Whether it will be perceptible enough on different monitors to be worth including.
   - Recommendation: Include it; if imperceptible, it does no harm. The left border accent is the primary differentiator.

## Sources

### Primary (HIGH confidence)
- **Codebase inspection** -- `src/layout/system_view.py`, `src/layout/equipment_grid.py`, `src/config.py`, `assets/custom.css` read directly
- **PNG visual analysis** -- all three layout diagrams examined for visual character and complexity
- **Dash documentation** (training data) -- `assets/` folder auto-serving is a core Dash feature documented in all versions

### Secondary (MEDIUM confidence)
- **CSS print-color-adjust** -- standard CSS property for preserving colors in print; widely supported

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries; existing Dash/dbc patterns only
- Architecture: HIGH -- single function modification with well-understood conditional logic; file copy is trivial
- Pitfalls: HIGH -- all pitfalls are well-known Dash patterns (asset paths, print CSS)
- Differentiation approach: MEDIUM -- creative judgment call based on PNG visual analysis; may need refinement during UAT

**Research date:** 2026-03-26
**Valid until:** 2026-04-26 (stable -- no fast-moving dependencies)
