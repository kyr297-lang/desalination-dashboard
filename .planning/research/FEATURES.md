# Feature Research: v1.3 UI/UX Overhaul

**Domain:** Engineering education dashboard -- UI/UX patterns for system page differentiation, interactive control discoverability, diagram integration, and baseline UX quality
**Researched:** 2026-03-26
**Scope:** NEW features only -- existing functionality (tabs, charts, scorecard, sliders, accordion) is assumed working
**Confidence:** MEDIUM-HIGH -- patterns drawn from established dashboard UX literature and Dash-specific documentation

---

## Question 1: Making Two Pages With the Same Data Feel Visually Distinct

The Mechanical (hydraulic drive) and Electrical (battery storage) pages show identical data categories (scorecard, equipment, charts) but represent fundamentally different engineering philosophies. The goal is: a student glancing at the screen knows instantly which system they are on without reading the tab label.

### Table Stakes

| Pattern | Description | Complexity | Current State |
|---------|-------------|------------|---------------|
| **System accent color** | Each page uses its system color (steel blue / burnt orange) on key landmarks: top border, tab highlight, badge | LOW | Already implemented via `borderTop: 4px solid` and `dbc.Badge`. Sufficient as a baseline. |
| **System name in page heading** | An `H3` or `H4` at the top of page content reading "Mechanical System" / "Electrical System" | LOW | Missing. Currently only the tab label and badge identify the system. A student screenshotting for a report has no page title. |
| **Consistent data layout** | Both pages must have the same section order (scorecard, equipment, charts) so students can compare them mentally | LOW | Already implemented. Do not change section order between pages. |

### Differentiators

These are the creative layout patterns that make the pages feel experientially distinct -- not just color-swapped clones.

| Pattern | Description | Complexity | Why It Works |
|---------|-------------|------------|--------------|
| **Hero diagram placement** | Mechanical page leads with its hydraulic system layout diagram (PNG) as a full-width hero image above the scorecard. Electrical page leads with its battery storage layout diagram in the same position. The diagram is the first thing the student sees and it sets the mental model for everything below. | LOW | System architecture diagrams are the strongest visual differentiator because the two systems look completely different physically. A hydraulic manifold diagram and a battery bank diagram share zero visual similarity. This is free differentiation. |
| **Section ordering: diagram-first vs controls-first** | Mechanical page: diagram at top, then scorecard, then equipment, then charts with sliders. Electrical page: same order, but the battery/tank slider control panel is promoted to sit directly below the diagram (before scorecard) because the slider actively changes the electrical system data. Mechanical has no equivalent interactive control, so its flow is diagram-then-data. | MEDIUM | The battery slider is unique to the electrical page. Promoting it visually signals "this system has a parameter you control." On the mechanical page, the absence of that control panel makes the layout feel different without adding anything artificial. |
| **Diagram annotation callouts** | On each system diagram PNG, overlay 2-3 labeled callout badges pointing to key components (e.g., "HPU" on mechanical, "Battery Bank" on electrical). These use the system accent color. | MEDIUM | Callouts connect the abstract diagram to the equipment accordion below. Students learn component names by seeing them in spatial context, then encounter the same names in the data table. This bridges visual understanding to quantitative data. |
| **Equipment section framing** | Mechanical equipment accordion groups items by hydraulic process stage (HPU, manifold, motors). Electrical accordion groups by electrical subsystem (generation, storage, distribution). Use the stage name as a subheading with a subtle left-border accent in the system color. | LOW | Different grouping labels make the accordions feel distinct even though they use the same UI component. The content itself is the differentiator. |
| **Background texture hint** | Mechanical page uses a very subtle (#f7f9fb) cool-tinted background on the diagram card. Electrical page uses a very subtle (#fdf8f4) warm-tinted background on its diagram card. Rest of the page stays white. | LOW | Barely perceptible but registers subconsciously. The UI Review confirmed border-top works well; extending this to a background tint only on the diagram hero card avoids the earlier concern about tint "looking out of place" (which applied to full-page tint, not a single card). |

### Anti-Features for Differentiation

| Pattern | Why Avoid |
|---------|-----------|
| **Different chart types per page** (e.g., bar chart on mechanical, radar chart on electrical) | Breaks comparability. Students need to see the same chart shapes to compare values mentally across pages. |
| **Different navigation structures per page** | Confusing. Both pages should have the same tab bar, same section flow. Differentiation comes from content and visual cues, not from structural changes. |
| **Animated page transitions** | Dash does not support native page transitions well; custom JavaScript is fragile and adds maintenance burden. Instant re-render is fine. |
| **Completely different color schemes** | The muted academic triad (blue/orange/green) is already well-chosen and accessible. Each page should use its accent color, not a whole separate palette. |

---

## Question 2: Making Interactive Controls Discoverable to First-Time Users

The UI Review identified that the battery slider has no endpoint labels, no tooltip during drag, and no units. More broadly, first-time students need to immediately understand: (a) what is interactive, (b) what it controls, and (c) what the current value means.

### Table Stakes

| Pattern | Description | Complexity | Implementation in Dash |
|---------|-------------|------------|----------------------|
| **Endpoint labels on all sliders** | Every `dcc.Slider` must have `marks={}` with human-readable labels at min, midpoint, and max. Example: battery slider needs `{0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}`. | LOW | Already done on TDS and Depth sliders. Battery slider is the gap. Add `marks` dict. |
| **Always-visible tooltips during drag** | All sliders use `tooltip={"always_visible": True, "placement": "bottom"}` and `updatemode="drag"`. Students must see the value changing as they drag, not only on mouseup. | LOW | TDS and Depth already correct. Battery slider needs `tooltip={"always_visible": True}` and `updatemode="drag"`. |
| **Control label + purpose subtitle** | Every interactive control has a bold label followed by a muted em-dash subtitle explaining what it does. Example: **"Battery / Tank Tradeoff** -- Adjust electrical system storage mix". | LOW | Already implemented on all three sliders. This is the project's best copy pattern; maintain it. |
| **Units on all displayed values** | The live-updating value label next to each slider must include units: "950 PPM", "950 m", "50% Battery / 50% Tank". Never show a naked number. | LOW | Already done. Maintain. |
| **Dropdown placeholder text** | All `dcc.Dropdown` components use specific placeholder text, not generic "Select...". Example: "Select equipment..." for hybrid builder slots. | LOW | Flagged in UI Review as generic. Change to "Select equipment..." or stage-specific text like "Choose desalination method...". |

### Differentiators

| Pattern | Description | Complexity | Why It Works |
|---------|-------------|------------|--------------|
| **Control panel card with distinct background** | Group all interactive controls (sliders, dropdowns) inside a visually distinct card with a light gray background (#f8f9fa) and a "Controls" or "Adjust Parameters" header. Separate from the data display cards. | LOW | Already partially implemented (`chart-controls` card with gray background). Formalize with a heading so the control panel is self-describing. Students see a labeled box that says "these are the things you can change." |
| **First-visit tooltip callouts** | On first page load (detected via `dcc.Store` with a `first_visit` boolean), show a brief callout banner above the control panel: "Drag the sliders below to see how system parameters affect cost and performance." Dismiss on click, remember dismissal in `dcc.Store`. | MEDIUM | Progressive disclosure pattern. Students who need guidance get it; returning users are not annoyed. Dash supports this with a `dcc.Store` + conditional rendering in a callback. No JavaScript needed. |
| **Slider interaction preview** | When a slider value changes, briefly highlight (via CSS class toggle) the chart cards that update in response. A 1-second border-color pulse on the affected chart card signals cause-and-effect. | MEDIUM | Builds mental model of which control affects which output. Implementation: callback adds a CSS class to the chart card wrapper, which has a CSS transition that fades back. Dash clientside callback can handle the class toggle. |
| **"What does this control?" microcopy** | Below each slider, a single line of small muted text: "Affects: Cost Over Time, Land Area, Scorecard". Lists exactly which output sections change. | LOW | Removes guesswork. Students know before dragging whether this slider matters for the metric they care about. Static text, no callback needed. |
| **Interactive element visual affordance** | All sliders have their track and thumb styled with the system accent color (blue for mechanical-affecting controls, orange for electrical-affecting controls). Dropdowns have a left-border accent matching their system. | LOW | Color-coding controls by which system they affect helps students understand scope. The battery slider is orange because it only affects the electrical system. The TDS/Depth sliders are neutral (gray) because they affect all systems. |

### Anti-Features for Discoverability

| Pattern | Why Avoid |
|---------|-----------|
| **Step-by-step guided tour overlay** (e.g., intro.js-style walkthrough) | Requires JavaScript library integration into Dash; brittle with Dash's callback-based DOM updates; students skip guided tours 70%+ of the time. The first-visit banner is sufficient. |
| **Animated bouncing arrows pointing at controls** | Unprofessional for an academic tool. Undermines the engineering-paper aesthetic. |
| **Disabling charts until a slider is moved** | Breaks the "immediate value" principle. Students should see data immediately and then discover they can change it. Gating content behind interaction is appropriate for the hybrid builder (pedagogical purpose) but not for parameter sliders. |

---

## Question 3: Presenting System Architecture Diagrams Alongside Data

The project has three PNG diagrams (Mechanical, Electrical, Hybrid System Layout). The question is where and how they appear relative to the data.

### Table Stakes

| Pattern | Description | Complexity | Notes |
|---------|-------------|------------|-------|
| **Diagram visible on the system page** | Each system page shows its own layout diagram. The diagram must not require navigation to a separate page or modal to view. | LOW | Render as `html.Img` inside a `dbc.Card`. |
| **Diagram has a caption** | Below the image, a brief caption: "Hydraulic drive system layout showing wind turbine, HPU, manifold, and RO membrane connections." | LOW | `html.P` with `className="text-muted small text-center"` below the image. |
| **Diagram is zoomable or viewable at full resolution** | Engineering diagrams have details that matter. A 300px-tall thumbnail is not enough. Students need to see labels on the diagram. | LOW | Wrap the image in an `html.A` with `href` pointing to the same image file and `target="_blank"`, so clicking opens full-size in a new tab. Add `title="Click to view full size"`. |

### Differentiators

| Pattern | Description | Complexity | Why It Works |
|---------|-------------|------------|--------------|
| **Diagram as page hero** | Place the system diagram as the first content element on each system page, full-width inside a card with a subtle system-tinted background. This establishes spatial context before the student encounters any numbers. | LOW | Engineering education research (and common patterns in tools like HOMER Pro and SAM) show that schematic-first presentation builds the mental model that data alone cannot. Students who see the physical layout first ask better questions about the numbers. |
| **Diagram-to-accordion linkage** | Equipment names in the accordion match labels visible in the diagram. Use consistent naming between `config.py` PROCESS_STAGES and the diagram labels. If the diagram shows "HPU", the accordion should have a stage or item labeled "HPU" (not "Hydraulic Power Unit" in one place and "HPU" in another without explanation). | LOW | Reduces cognitive load. Students visually identify a component in the diagram, then find its data in the accordion by the same name. |
| **Side-by-side diagram comparison on the Comparison tab** | On the scorecard/comparison view (when all three systems are visible), show all three diagrams in a row (`dbc.Row` with three `dbc.Col(width=4)`), scaled to fit. This is the only place where diagrams appear simultaneously. | MEDIUM | Enables visual comparison of physical complexity: mechanical has more components, electrical has fewer but includes battery banks, hybrid is a mix. This visual comparison complements the numerical scorecard. |
| **Collapsible diagram section** | Wrap the diagram card in a `dbc.Collapse` with a toggle button: "Show/Hide System Diagram". Default to expanded on first visit, collapsed on subsequent visits (via `dcc.Store`). | LOW | Students who have already studied the diagram can collapse it to focus on data. Returning users get more screen real estate for charts. |

### Anti-Features for Diagrams

| Pattern | Why Avoid |
|---------|-----------|
| **Interactive SVG diagram with clickable components** | Requires converting PNGs to SVGs with element IDs, writing click handlers, and mapping clicks to accordion sections. HIGH complexity for marginal benefit. The static PNG + matching names pattern achieves 80% of the value at 10% of the cost. |
| **Diagram as a background watermark behind data** | Looks clever but makes both the diagram and the data harder to read. Separation of diagram and data into distinct visual regions is better. |
| **Animated diagram showing data flow** | Out of scope. Would require custom JavaScript animation, SVG conversion, and significant development time. Static diagrams with good captions are sufficient for an academic tool. |

---

## Question 4: Table-Stakes UX Patterns for Any Data Dashboard

These are patterns that any competent data dashboard must have. Their absence is noticed; their presence is not. The UI Review scored Experience Design at 1/4, which means most of these are currently missing.

### Table Stakes

| Pattern | Description | Complexity | Current State | Fix |
|---------|-------------|------------|---------------|-----|
| **Loading spinners on charts** | Wrap every `dcc.Graph` in `dcc.Loading(type="circle")`. When Dash callbacks are computing, show a spinner instead of an empty white box. | LOW | Missing entirely. UI Review flagged this. | Add `dcc.Loading` wrapper around each chart. Dash provides this natively -- zero dependencies. |
| **Loading spinner on page transitions** | When switching between system tabs, show a spinner on the content area until the new layout renders. | LOW | Missing. Tab switches show a brief flash of empty content. | Wrap `#page-content` children in `dcc.Loading`. |
| **Empty state for comparison text** | When the comparison text area has no content (e.g., before hybrid is complete), show a placeholder message instead of blank space. | LOW | Missing. The `comparison-text` div renders as invisible empty space. | Add a default child: `html.P("Complete the hybrid builder to see a comparison.", className="text-muted fst-italic")`. |
| **Error state with human-readable messages** | When data fails to load, show a message a student can act on: "Something went wrong loading the data. Try refreshing the page." Not: "Missing section(s) in 'Part 1': ['miscellaneous']". | LOW | Partially implemented. Error page exists but shows developer-facing messages. UI Review flagged this. | Rewrite error message strings in `error_page.py`. |
| **Control labels with units** | Every slider displays its unit inline. "Salinity (PPM)", "Depth (meters)", "Battery Ratio (%)". | LOW | Partially done. Units appear in the live value labels but not always in the slider title itself. | Add units to the `html.Strong` label text. |
| **Axis labels with units on every chart** | Every Plotly chart axis must have a label that includes the unit: "Cost (USD)", "Land Area (m2)", "Power (kW)". | LOW | Mostly done. Verify consistency after the v1.3 data layer changes. | Audit all `fig.update_layout(xaxis_title=..., yaxis_title=...)` calls. |
| **Consistent number formatting** | All numbers use the `fmt_sig2` pattern (2 significant figures, comma-separated thousands). No raw floats with 8 decimal places. | LOW | Implemented in v1.2. Maintain. | No change needed. |
| **Accessible color usage** | Never use color alone to convey information. RAG dots in the scorecard must also have text labels or aria-labels. | LOW | Missing. UI Review flagged that RAG dots are empty spans with no text alternative. | Add `aria-label="Best"` / `"Worst"` / `"Middle"` to RAG dot spans. Also add a text legend row above the scorecard: "Green = Best, Yellow = Middle, Red = Worst". |
| **Print/export compatibility** | The `window.print()` flow should produce a clean output. Charts should not be cut off; the gate overlay should not print. | LOW | Partially done. Print CSS exists in `custom.css`. Verify hybrid gate overlay has `@media print { display: none }`. | Audit print stylesheet. |
| **Responsive minimum width** | Set `min-width: 900px` on the main content area so the dashboard degrades gracefully (horizontal scroll) rather than collapsing into unreadable mobile layout. | LOW | Not explicitly set. Desktop-first is a stated constraint. | Add `min-width` to `#page-content` style. |

### Differentiators (Above-Baseline UX)

| Pattern | Description | Complexity | Why It Works |
|---------|-------------|------------|--------------|
| **Page-level heading hierarchy** | Every page has a clear heading: `H2` for the page title ("Mechanical System"), `H4` for sections ("System Scorecard", "Equipment Details", "System Comparison Charts"), `H5` for subsections (stage names). | LOW | UI Review flagged flat heading hierarchy. Fixing this costs nothing and dramatically improves screen-reader navigation and visual scannability. |
| **Breadcrumb with system context** | The "Back to Overview" breadcrumb already exists. Enhance it: "Overview > Mechanical System" so students always know their location. | LOW | Standard navigation pattern. Helps students who arrive via a shared link understand where they are in the app structure. |
| **Chart card titles as semantic headings** | Replace `html.Strong("Cost Over Time")` with `html.H5("Cost Over Time", className="card-title")` inside chart cards. | LOW | Screen readers can navigate by heading. `Strong` is invisible to heading navigation. |
| **Tooltip on legend badges** | The clickable system-visibility badges in the chart section need `title="Click to show/hide Mechanical"` and `role="button"`. | LOW | UI Review flagged this. Students do not know the badges are interactive without this hint. |
| **Confirmation on destructive actions** | The hybrid builder "Clear All" button should have a `title="Clear all equipment selections"` tooltip. A modal confirmation is overkill, but the tooltip sets expectations. | LOW | Prevents accidental resets. |
| **Keyboard accessibility for sliders** | Verify that all `dcc.Slider` components are keyboard-navigable (arrow keys to adjust). Dash sliders support this natively, but custom styling can break it. | LOW | Academic labs may have students using keyboard navigation. Test and verify, do not assume. |
| **Export guard on incomplete hybrid** | Disable or hide the "Export / Print" button on the Hybrid tab when the gate is active (not all 5 slots filled). Printing an incomplete hybrid is misleading. | LOW | UI Review flagged that printing with the gate overlay produces a confusing output. |

---

## Feature Dependencies (v1.3 UI/UX Overhaul)

```
[System layout PNG files available]
    required by --> [Diagram hero card on each system page]
    required by --> [Side-by-side diagram comparison]
    required by --> [Diagram annotation callouts]

[Diagram hero card]
    required by --> [Collapsible diagram section]
    required by --> [Background texture hint]
    enhances   --> [Equipment accordion] (visual-to-data linkage)

[dcc.Loading wrappers]
    independent -- can be added to any existing component

[First-visit tooltip banner]
    requires   --> [dcc.Store("first-visit")]
    independent of all other features

[Slider fixes (battery endpoint labels, tooltip, updatemode)]
    independent -- pure prop changes on existing components

[Heading hierarchy fix]
    independent -- pure HTML element swaps

[Control panel "Affects:" microcopy]
    independent -- static text additions

[RAG dot accessibility]
    independent -- aria-label additions
```

### Dependency Notes

- **Diagram integration is the highest-dependency feature.** The hero placement, callouts, and collapsible behavior all depend on the PNG files being available and correctly sized. These PNGs already exist (listed in git status as untracked). They need to be moved to `assets/` for Dash to serve them.
- **Most UX fixes are independent.** Loading spinners, slider fixes, heading hierarchy, accessibility labels, and tooltip additions can all be implemented in parallel with no inter-dependencies.
- **First-visit banner depends on a new `dcc.Store`.** This is a small addition but introduces a new piece of client-side state. Test that it does not interfere with existing `dcc.Store` components (hybrid slot store, etc.).

---

## Implementation Priority for v1.3

### P0: Fix Before Anything Else

1. **Data layer fix** -- restore or handle missing miscellaneous sheet (app does not load without this)
2. **Battery slider fix** -- add endpoint marks, always-visible tooltip, drag updatemode

### P1: Core Visual Differentiation

3. **System diagram hero cards** -- embed PNGs as first content element on each system page
4. **System page heading** -- add H2/H3 with system name at top of each page
5. **Background tint on diagram card** -- cool for mechanical, warm for electrical

### P2: Interactive Control Clarity

6. **dcc.Loading wrappers** on all charts and page transitions
7. **Control panel heading** -- add "Adjust Parameters" heading to the control card
8. **"Affects:" microcopy** below each slider
9. **Dropdown placeholder specificity** -- "Select equipment..." instead of "Select..."
10. **First-visit callout banner** above control panel

### P3: Baseline UX Quality

11. **Heading hierarchy fix** -- H2 > H4 > H5 throughout
12. **Chart card titles as H5** instead of html.Strong
13. **RAG dot aria-labels** and text legend
14. **Legend badge tooltips and role="button"**
15. **Error message rewrite** -- student-facing language
16. **Empty state for comparison text div**
17. **Export guard on incomplete hybrid**
18. **Hamburger button aria-label and title**

### P4: Polish

19. **Diagram-to-accordion name consistency audit**
20. **Collapsible diagram section** with dcc.Store memory
21. **Slider interaction preview** (chart border pulse)
22. **Side-by-side diagram comparison** on overview/comparison view
23. **Print stylesheet audit**

---

## Sources

- [Pencil & Paper -- Dashboard UX Patterns](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards) -- MEDIUM confidence (comprehensive pattern catalogue)
- [Dash dcc.Loading Documentation](https://dash.plotly.com/dash-core-components/loading) -- HIGH confidence (official Plotly docs)
- [Dash Loading States](https://dash.plotly.com/loading-states) -- HIGH confidence (official Plotly docs)
- [UXPin -- Dashboard Design Principles 2025](https://www.uxpin.com/studio/blog/dashboard-design-principles/) -- MEDIUM confidence
- [Smashing Magazine -- UX Strategies for Real-Time Dashboards](https://www.smashingmagazine.com/2025/09/ux-strategies-real-time-dashboards/) -- MEDIUM confidence
- [Justinmind -- Dashboard Design Best Practices](https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux) -- MEDIUM confidence
- [UX Design Institute -- Onboarding Best Practices 2025](https://www.uxdesigninstitute.com/blog/ux-onboarding-best-practices-guide/) -- MEDIUM confidence
- [Eleken -- Dashboard Design Examples](https://www.eleken.co/blog-posts/dashboard-design-examples-that-catch-the-eye) -- LOW confidence (commercial examples)
- [GoodData -- Dashboard Information Architecture](https://www.gooddata.com/blog/six-principles-of-dashboard-information-architecture/) -- MEDIUM confidence
- UI Review findings (`.planning/UI-REVIEW.md`, 2026-03-26) -- HIGH confidence (direct code audit of this project)

---

*Feature research for: v1.3 UI/UX Overhaul -- Wind-Powered Desalination Dashboard*
*Researched: 2026-03-26*
