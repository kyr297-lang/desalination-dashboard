# UI Review — Wind-Powered Desalination Dashboard

**Audited:** 2026-03-26
**Baseline:** Abstract 6-pillar standards (no UI-SPEC.md found)
**Screenshots:** Partially captured — dev server running on port 8050, but app is currently in an error state due to a missing 'miscellaneous' sheet in data.xlsx (data.xlsx is modified per git status). Visual scoring supplemented by full code audit of all layout files.
**Runtime state note:** The live app shows "Unable to Load Dashboard — Missing section(s) in 'Part 1': ['miscellaneous']". This is a data integrity issue unrelated to the UI code quality, but it is scored under Experience Design as a first-user encounter problem.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | Card descriptions are genuinely helpful; slider labels are strong. Generic "Select..." dropdown placeholder and one raw internal string exposed to users. |
| 2. Visuals | 3/4 | Clean academic aesthetic, good card structure. The hamburger button has no visible label or tooltip, and the sidebar link "System Explorer" is a dead end. |
| 3. Color | 4/4 | Disciplined muted triad (blue/orange/green) used only for system identity; RAG palette is separate and correct; no hardcoded hex colors in layout files. |
| 4. Typography | 3/4 | Consistent small/muted/bold hierarchy throughout. Stage headers (`html.H5`) use the same weight as the scorecard header, creating a flat hierarchy when both are visible at once. |
| 5. Spacing | 3/4 | Spacing is generally consistent via Bootstrap classes. The hybrid builder pipeline wraps on narrow screens but the arrow characters (`→`) remain inline, creating orphaned arrows mid-row. |
| 6. Experience Design | 1/4 | App is currently broken for first-time users due to the data.xlsx schema mismatch. The hybrid gate system is thoughtful, but: no loading spinner during callback round-trips, the battery slider has no endpoint labels, and the error page shows a raw Python exception string in a collapsed accordion that a student will click. |

**Overall: 17/24**

---

## Top 3 Priority Fixes

1. **data.xlsx is missing the 'miscellaneous' sheet — the app does not load at all** — A student opening this link for the first time sees "Unable to Load Dashboard" and a red error box. Restore the 'miscellaneous' sheet to data.xlsx or update the loader to handle its absence gracefully before any presentation or sharing.

2. **The battery/tank slider (slider-battery) has no endpoint labels, no units, and no contextual explanation of what "0" and "1" mean** (`charts.py` line 432–444) — A student moving this slider has no idea whether moving it left means "more battery" or "more tank," and the `label-battery-ratio` span only updates after mouseup, so during drag the slider appears to do nothing. Add `marks={0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}` and enable `tooltip={"always_visible": True}`.

3. **The sidebar "System Explorer" NavLink is non-functional** (`shell.py` line 131–134) — It has `href="#"` and no callback, so clicking it does nothing. A student trying to navigate via the sidebar is silently stuck. Either wire it to set `active-system` to the last visited system, or remove it from the sidebar entirely to avoid confusion.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)

**What works well:**
- The landing page card descriptions (`overview.py` lines 27–50) are the best copy in the app. Each card tells the user what they will see AND what makes that system different. The Hybrid card's "Select one piece of equipment for each process stage" is immediately actionable.
- Slider labels use the dash em `—` convention to separate the control name from its purpose (e.g., "Time Horizon — Adjust the projection period"), which is clearer than most dashboard tooling.
- The "About This Project" intro card (`overview.py` lines 105–132) frames context well for a student audience.
- The scorecard legend note ("Green = best of the compared systems, Red = worst. Lower cost, less land, and less energy are better.") removes ambiguity from the RAG dots.

**Issues found:**
- `hybrid_builder.py` line 146: `placeholder="Select..."` is generic. Given the dropdown labels already say the stage name (e.g., "Desalination"), the placeholder should match: `"Select equipment..."` so users understand they are picking a component, not a category.
- `equipment_grid.py` line 244: The raw equipment name `"55 gallon container is 2500 USD, for 1 million gal/day lasts about 20 days"` is both an internal cost note and a displayed accordion item title in the hybrid builder options. A student will see this as the dropdown label. It should be shortened to something like `"Chemical Drum (55 gal)"` with the cost detail moved to the description.
- `scorecard.py` line 283: "Best Overall: Tied" — if all three systems score the same, this sentence reads awkwardly. "No clear winner" or "Systems tied" reads more naturally for a student audience.
- The `comparison_text_div` (scorecard.py line 124) is populated by `generate_comparison_text()` which is in `processing.py` and not reviewed here, but the div itself has no heading, so generated text appears as orphaned italic prose below the scorecard table with no visual anchor.

---

### Pillar 2: Visuals (3/4)

**What works well:**
- The system color accent (`borderTop: 4px solid {hex_color}`) on `#page-content` (`shell.py` line 264) is a subtle but effective system-identity signal. Users can orient themselves ("I am in the orange/electrical system") without large visual interruptions.
- The colored `dbc.Badge` pill next to the tab bar (`system_view.py` lines 217–227) reinforces the system identity when switching between Mechanical and Electrical tabs.
- The gate overlay on the hybrid chart section (`system_view.py` lines 148–191) is well-designed — semi-transparent, centered, warning symbol + explanation.
- The accordion pattern for equipment details is appropriate. It avoids dumping a wall of tables on the user.

**Issues found:**
- **Hamburger button** (`shell.py` line 103–108): The sidebar toggle is a bare Unicode `☰` character with no `title` attribute and no aria-label. Screen readers announce nothing. Sighted users who are unfamiliar with the hamburger convention have no affordance that this opens a sidebar. Add `title="Toggle sidebar"` and `aria-label="Toggle sidebar"`.
- **Sidebar "System Explorer" link** (`shell.py` line 131–134): This link has `href="#"` and no callback binding. It scrolls the user to the top of the page and does nothing else. It creates a second navigation path that appears to exist but is broken. This will confuse first-time users who expect clicking it to take them somewhere.
- **No page-level heading on the landing view**: The overview layout (`overview.py` lines 105–139) starts directly with an "About This Project" card. There is no `<h1>` or prominent visual title on the landing page itself. The app title lives only in the navbar brand (`shell.py` line 111), which is small and shares space with the hamburger toggle. A student screenshot for a report would show a page with no obvious title.
- **Chart cards have no height set**: The four `dcc.Graph` components in `charts.py` (lines 378–379) use default Plotly height (~450px). On a 1440px desktop this leaves significant blank space below the charts in each card; on mobile they overflow. Consider `style={"height": "300px"}` for the graph components.
- **Tab active_label_style logic is backwards** (`system_view.py` lines 93–96): The ternary applies `active_label_style` only `if is_active`, but when a tab is not active it receives the same inactive `{"color": "#6c757d"}` as its `label_style`. The `active_label_style` prop in dbc is supposed to be the style applied when a tab becomes active dynamically; applying it statically during layout build means the tab color highlight may flicker or fail on tab switch.

---

### Pillar 3: Color (4/4)

**What works well:**
- The three system colors in `config.py` (lines 14–18) are a well-chosen muted academic triad. They are perceptually distinct and pass basic colorblindness checks (blue/orange/green is a standard accessible combination).
- The RAG colors (`config.py` lines 36–40) use standard Bootstrap alert hex values and are explicitly separated from the system colors in a comment — good defensive documentation.
- Stage colors (`config.py` lines 23–31) are a further distinct set of seven muted colors, none of which collide with the system triad.
- Color is used consistently and sparingly: the system colors appear only on card headers, badges, tab highlights, chart traces, and the accent border. They are never used as backgrounds for content areas or text.
- The badge toggle (opacity 0.4 + line-through for hidden systems, `charts.py` lines 774–791) is a clean two-state visual without introducing a new color.

**Minor observation (not a deduction):**
- The `#28A745` green used for cross-system best-value highlighting in `equipment_grid.py` line 255 is the RAG green from `RAG_COLORS`. It should be imported from `config.RAG_COLORS["green"]` rather than hardcoded inline to stay in sync if the palette changes.

---

### Pillar 4: Typography (3/4)

**Type scale observed:**
- `html.H4` — "System Comparison" section heading (`charts.py` line 599)
- `html.H5` — Stage group headings, scorecard heading, hybrid builder heading
- `html.H6` — Cross-system comparison subheading (`equipment_grid.py` line 269)
- `html.Strong` — Chart card titles, slider labels
- `html.P` + `className="small"` — body descriptions
- `html.Small` — Slider subtitles
- `dbc.Badge` with `style={"fontSize": "0.75rem"}` — Equipment summary badges

**What works well:**
- The `small` + `text-muted` combination is used consistently for supplemental text across all files. This produces a reliable visual hierarchy between primary data and explanatory prose.
- `fw-bold` and `fw-semibold` are used for emphasis rather than font-size jumps, which is appropriate for a data-dense layout.

**Issues found:**
- The scorecard section uses `html.H5("System Scorecard", ...)` (`scorecard.py` line 304), the stage group headings also use `html.H5` (`equipment_grid.py` line 434), and the hybrid builder uses `html.H5("Hybrid System Builder", ...)` (`hybrid_builder.py` line 227). When a student lands on the Mechanical system view, they see three separate `<h5>` elements at the same weight with no `<h4>` or `<h3>` above them to establish a parent level. The page visual hierarchy is flat between these sections. The scorecard title should be bumped to `html.H4` or the section titles demoted to `html.H6`.
- `html.Strong` is used for chart card titles (`charts.py` line 376) while `html.H5` is used for section headings. `Strong` inside a `CardBody` renders as bold inline text, not a semantic heading, which breaks screen-reader document outline and makes the chart titles feel lighter than the stage headings above the accordion.
- The `label-years` and `label-battery-ratio` spans use `className="fw-bold ms-2"` which is not a heading — this is appropriate for a live label but makes the slider current-value and the static section headings visually indistinguishable in weight.

---

### Pillar 5: Spacing (3/4)

**Spacing patterns observed:**
- `g-3` gutter on the overview card row (`overview.py` line 137)
- `mb-3` on most cards and sections as the vertical rhythm unit
- `mt-4 mb-2` on stage headings in equipment grid
- `mt-3` separating major sections in system_view assembly
- `gap-2` in the hybrid pipeline flexbox
- `padding: "1.5rem"` on `#page-content` (inline style, `shell.py` line 29)
- `padding: "1rem 0"` on the sidebar (inline style, `shell.py` line 41)

**What works well:**
- The consistent use of `mb-3` as the vertical rhythm unit throughout the layout produces a predictable reading pace.
- The `g-3` gutter on the overview cards and chart grid cards provides appropriate breathing room at desktop widths.

**Issues found:**
- **Arrow orphaning in hybrid pipeline** (`hybrid_builder.py` lines 210–217): The `→` arrows are `html.Span` elements in a `flex-wrap` container (`d-flex flex-wrap`). When the viewport is narrow (tablet or small desktop) and the five dropdowns wrap to a second line, an arrow character remains at the end of the first row or beginning of the second with no adjacent dropdown, looking like stray punctuation. The arrows should either be CSS `::after` pseudo-elements on each slot (and thus stay with their left sibling), or the entire pipeline should switch to a vertical `flex-direction: column` layout below a breakpoint with no arrows at all.
- **`_MARGIN = dict(l=75, r=20, t=10, b=40)` in charts** (`charts.py` line 60): The left margin of 75px is applied to all four chart figures. On mobile (375px viewport), this leaves only ~280px of chart area, compressing bar charts significantly. The cost line chart's y-axis labels may clip. Consider `l=50` or using Plotly's `automargin=True` on the y-axis.
- **Scorecard card and equipment card share `mb-3`** (`system_view.py` lines 204, 210) but the scorecard card has no top padding in its `CardBody` since the export button sits flush at top. The export button appears crowded against the card edge on first render.
- **The sidebar link padding** (`shell.py` line 138, `className="px-2"`) is applied to the `dbc.Nav` container, not the individual `NavLink` items. Bootstrap's `dbc.NavLink` with `pills=True` already applies its own internal padding, causing the Mechanical/Electrical pill indicators to have inconsistent outer whitespace compared to the hamburger button zone above.

---

### Pillar 6: Experience Design (1/4)

**Critical: App does not load for first-time users**
The live app currently shows an error page because data.xlsx is missing the 'miscellaneous' sheet (visible in git status: `M data.xlsx`). Every student visiting the link today sees the error state before any content. The error page itself (`error_page.py`) is well-structured — it uses a collapsed accordion to hide the technical traceback. However, the message "Missing section(s) in 'Part 1': ['miscellaneous']. Found: ['electrical', 'mechanical']. Check that data.xlsx has not been modified." is a developer-facing message, not a student-facing one. A first-year student does not know what 'Part 1' or 'miscellaneous' means. The alert text should be: "The data file is missing required content. Please contact the project team to restore the original data.xlsx."

**Loading states:**
- There is no loading spinner or skeleton shown while Dash callbacks are computing on initial page load. On a cold Dash startup the charts are empty white boxes for several seconds. Dash provides `dcc.Loading` wrappers; none are present in any layout file. The four chart `dcc.Graph` elements in `charts.py` lines 373–387 could each be wrapped with `dcc.Loading(type="circle")`.
- The hybrid gate overlay is an excellent micro-interaction — it appears immediately (no callback delay) and disappears reactively when all five slots fill. This pattern is the best UX in the app.

**Interaction feedback:**
- The battery/tank slider (`charts.py` line 432) has `updatemode="mouseup"` and `tooltip={"always_visible": False}`. During drag, the slider thumb moves but nothing on the page updates and no tooltip shows. A student dragging this slider has no indication their interaction is being registered until they release. This is particularly harmful because the slider also lacks endpoint labels (see Top 3 Priority Fix #2).
- The TDS and Depth sliders (`charts.py` lines 471, 497) use `updatemode="drag"` and `tooltip={"always_visible": True}`, which is correct. The battery slider should match this pattern for consistency.
- The legend toggle badges (`charts.py` lines 519–557) have `cursor: pointer` but no `role="button"` attribute and no hover state other than the cursor change. A student scanning the chart section may not realize these are clickable. Adding a `title` attribute like `"Click to show/hide Mechanical"` would provide both a tooltip and an accessibility hint.

**Empty states:**
- The equipment grid handles the hybrid empty state with a message ("Fill all 5 slots to see equipment details.") at `equipment_grid.py` line 383. This is functional.
- The `comparison-text` div (`system_view.py` line 124) renders as empty whitespace when there is no comparison text. Because it has no height and no placeholder, the layout does not visually shift, which is correct — but on the Hybrid tab before gate open, the area between the scorecard and equipment card appears to have extra blank space with no explanation.

**Destructive actions:**
- The "Clear All" button in the hybrid builder (`hybrid_builder.py` lines 194–203) resets all five dropdown selections without any confirmation dialog. While this is not catastrophic (dropdowns can be re-selected), a student mid-build who accidentally clicks it loses all five selections instantly. A simple `title="Clear all equipment selections"` tooltip sets expectation; a `dbc.Modal` confirmation would be overkill for this use case.

**Error recovery:**
- The "Export / Print" button (`system_view.py` lines 127–134) triggers `window.print()` via a clientside callback. If a student clicks this on the Hybrid tab before all 5 slots are filled, they will print the page with an empty equipment section and a gate overlay message. There is no guard that checks whether hybrid is complete before allowing print. On non-Hybrid tabs this is not an issue.

**Accessibility gaps (compound Experience Design impact):**
- The hamburger button lacks aria-label (shell.py line 103–108).
- The legend badges lack role="button" and aria-pressed state (charts.py lines 521–555).
- The RAG colored dots in the scorecard (`scorecard.py` lines 98–109) are empty `html.Span` elements — screen readers will announce nothing for these. They convey information (green = best, red = worst) that is not conveyed through any other channel on the same row. Each dot should have `aria-label="Best"` / `aria-label="Worst"` / `aria-label="Middle"`.

---

## Registry Safety

No `components.json` found — shadcn not initialized. Registry audit skipped.

---

## Files Audited

| File | Lines | Role |
|------|-------|------|
| `src/layout/shell.py` | 266 | App shell, sidebar, navigation callbacks |
| `src/layout/overview.py` | 139 | Landing page, system selection cards |
| `src/layout/system_view.py` | 245 | System tab view assembly |
| `src/layout/charts.py` | 793 | Chart figures, control panel, legend callbacks |
| `src/layout/scorecard.py` | 421 | RAG scorecard table, hybrid gate overlay callback |
| `src/layout/equipment_grid.py` | 451 | Equipment accordion, cross-system comparison |
| `src/layout/hybrid_builder.py` | 332 | Hybrid pipeline dropdowns, slot store callbacks |
| `src/layout/error_page.py` | 64 | Error display for data-load failures |
| `src/config.py` | 249 | Color palettes, stage mappings, equipment descriptions |
| `assets/custom.css` | 97 | Sidebar transition, print styles |

Screenshots captured to `.planning/ui-reviews/01-20260326-161203/` (app in error state; screenshots show error page only).
