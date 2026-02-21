# Feature Research

**Domain:** Interactive engineering comparison dashboard — academic tool for wind-powered desalination systems
**Researched:** 2026-02-20
**Confidence:** MEDIUM — Core comparison dashboard patterns are HIGH confidence from multiple sources; desalination-specific academic tool patterns are MEDIUM (limited direct analogues, cross-referenced with SEDAT, SAM, and HOMER Pro tools)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features students and instructors assume exist in any engineering comparison tool. Missing these = the tool feels broken or incomplete before any learning happens.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| System selection interface (Mechanical / Electrical / Hybrid) | Any comparison tool needs a way to choose what you're comparing; absence breaks the core premise | LOW | Three-option selector, clearly labeled; must persist across the session |
| Side-by-side metric display for all three systems | Engineers expect simultaneous comparison, not sequential; otherwise students tab-switch and lose context | LOW | Columns or cards showing the same metrics per system |
| Cost/land/efficiency scorecard with RAG color coding | Traffic-light (red/yellow/green) ranking is industry-standard for quick at-a-glance status; students expect it from any comparison framework | LOW | Must rank each system within the trio, not against an external threshold; low = green for cost/land, high = green for efficiency |
| Cost over time chart | Time-horizon economics is the #1 design tradeoff in infrastructure; any cost analysis tool needs temporal view | MEDIUM | Line chart with three systems plotted; x-axis = years |
| Land area comparison chart | Physical footprint is a direct design constraint municipalities face; expected in any siting decision tool | LOW | Grouped bar chart by system is clearest |
| Wind turbine count chart | Turbine count is an immediate physical reality students grasp; expected given mechanical vs. electrical system differences | LOW | Grouped bar chart; large numerical difference between 4x mechanical vs 1x electrical is pedagogically significant |
| Equipment details view per system | Any configuration tool must let users "look inside" a system; black-box systems frustrate engineering students | MEDIUM | Table or card layout showing quantity, cost, energy, land area, lifespan per part |
| Hover tooltips on charts | Standard in any Plotly Dash output; absence feels like a broken chart | LOW | Plotly provides this by default; ensure meaningful content (values, units) |
| Readable, consistent layout with labeled axes and units | Engineering students expect SI or stated units on every axis; unlabeled charts are academically unacceptable | LOW | Every chart must have axis labels, units (USD, m², kW, years) |
| Data loaded from structured source (data.xlsx) | Academic tools must be reproducible and auditable; hardcoded data is not credible | LOW | pandas + openpyxl reads Excel; single source of truth |

### Differentiators (Competitive Advantage)

Features that make this tool specifically valuable for learning desalination system tradeoffs — not available in generic comparison tools like SAM or HOMER Pro, which are too complex for undergraduate use.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hybrid "build your own" interface with 5 functional process slots | Forces students to think in process stages (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal) — maps engineering decisions to system structure, building real mental models | HIGH | Each slot = dropdown of valid parts from Miscellaneous sheet; must validate completeness before showing results; this is the core pedagogical differentiator |
| Hybrid completion gate | Prevents partial analysis — students can't see results until they've made all five decisions; teaches that incomplete designs can't be evaluated | MEDIUM | Gate shows progress (e.g., "3 of 5 slots filled") and blocks the scorecard/charts until complete |
| Electrical system battery/tank tradeoff slider | Makes the storage sizing tradeoff tangible — students see how shifting from battery to tank changes cost and land area in real time; directly tied to the 11-row tradeoff table in data.xlsx | MEDIUM | Slider maps to the 0–100% battery fraction table; re-renders relevant charts on change via Dash callback |
| Energy breakdown pie chart by action | Shows where energy actually goes (water extraction vs. desalination) — not just total energy; builds intuition about which process steps dominate | LOW | Per-system pie chart using energy (kW) from component data |
| Hybrid vs. preset comparison description | Contextualizes the student's custom hybrid choice against mechanical and electrical — explains tradeoffs in plain text, not just numbers | MEDIUM | Auto-generated text block based on scorecard rankings; e.g., "Your hybrid costs 20% less than mechanical but uses 40% more land than electrical" |
| User-selectable time horizon for cost chart | Students can explore short-term vs. long-term economics — a key dimension of infrastructure decision-making that static tables can't show | LOW | Slider or dropdown for years (5, 10, 20, 30, 50); updates line chart via callback |
| Equipment data displayed with lifespan column | Lifespan is rarely shown in simplified tools but is critical for lifecycle cost reasoning; including it teaches students to think beyond capital cost | LOW | Add lifespan (years) column to equipment detail views |
| Academic visual design (clean, professional) | Engineering students take tools more seriously when they look like engineering tools, not business BI dashboards; clean design also improves learnability | MEDIUM | Bootstrap theme (e.g., FLATLY or LITERA from dash-bootstrap-components); no gradients, no dark backgrounds, white/light gray base |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem valuable but would break the scope, add disproportionate complexity, or undermine the academic purpose.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time wind data integration | "Make it realistic" — students may ask for live wind speeds | Requires API keys, rate limits, data pipeline maintenance; completely outside the stated scope; data.xlsx is the single source of truth | Use representative calculated values from data.xlsx; label clearly as "design-basis values" |
| User accounts / saved configurations | "I want to save my hybrid design" — natural student request | Adds authentication, database, session management; the tool is stateless by design; free hosting tiers don't support persistent storage well | Add a "print/screenshot this page" note in the UI; or export scorecard as text |
| Mobile-optimized layout | Accessibility concern — students may use tablets | The dashboard has dense side-by-side comparison charts that are inherently desktop-width; mobile layout requires separate responsive design work and testing | Explicitly scope as desktop-first; add min-width constraint so it degrades gracefully rather than breaking |
| 3D visualization | "It would look cooler in 3D" | 3D adds interaction complexity (rotation, occlusion) that obscures data for engineering comparison; Plotly 3D charts are harder to read than 2D equivalents | Use 2D bar/line charts which convey the same data more clearly |
| Drag-and-drop hybrid builder | More "engaging" than dropdowns | Drag-and-drop in Dash requires JavaScript callbacks and custom components (e.g., dash-draggable); adds implementation complexity for no educational benefit over labeled dropdowns | Use clearly labeled dropdowns per slot; label slots with process stage names for equivalent cognitive scaffolding |
| Natural language / AI explanation | "Explain why mechanical is better" | LLM integration is out of scope, requires API keys/costs, and breaks the deterministic academic tool contract | Write static contextual descriptions triggered by scorecard rank outcomes; good enough for MVP |
| Sensitivity / parametric analysis | Advanced engineering students may want to vary wind speed or water demand | HOMER Pro and SAM already do this; replicating it here would require major scope expansion and obscures the three-system comparison goal | Keep tool focused on the fixed 10,000-person municipality scenario; document as future scope |
| Animated transitions between states | "Looks more professional" | Dash animations add callback complexity and can make the tool feel slow on lower-end academic lab machines | Use instant re-render (Dash default); clean layout makes up for lack of animation |

---

## Feature Dependencies

```
[System selection: Mechanical/Electrical/Hybrid]
    └──required by──> [Equipment detail view]
    └──required by──> [Scorecard + RAG ranking]
    └──required by──> [Cost over time chart]
    └──required by──> [Land area chart]
    └──required by──> [Turbine count chart]
    └──required by──> [Energy pie chart]

[data.xlsx loaded + parsed]
    └──required by──> ALL features (nothing works without data)

[Hybrid: 5-slot component selection]
    └──required by──> [Hybrid completion gate]
    └──required by──> [Hybrid vs. preset comparison description]
    └──required by──> [Scorecard: hybrid column]
    └──required by──> [Charts: hybrid data series]

[Hybrid completion gate (all 5 slots filled)]
    └──gates──> [Hybrid scorecard display]
    └──gates──> [Hybrid chart data series]
    └──gates──> [Hybrid vs. preset comparison description]

[Scorecard + RAG ranking]
    └──enhances──> [Hybrid vs. preset comparison description]

[Electrical system battery/tank slider]
    └──requires──> [data.xlsx: 11-row battery fraction table]
    └──updates──> [Cost over time chart: electrical series]
    └──updates──> [Land area chart: electrical series]
    └──updates──> [Scorecard: electrical cost/land metrics]

[Time horizon selector]
    └──updates──> [Cost over time chart]
```

### Dependency Notes

- **data.xlsx must be loaded first:** All features derive their values from the spreadsheet. If parsing fails, nothing works. This is the first thing to implement and test.
- **System selection gates everything:** The rest of the dashboard is meaningless without knowing which systems to compare. The three-system framing is the top-level organizing principle.
- **Hybrid slot selection gates hybrid outputs:** The completion gate is not optional — showing partial hybrid results would produce misleading comparisons.
- **Battery/tank slider is electrical-system-specific:** It only affects the electrical system series in charts. The slider should be visually scoped to the electrical system section, not treated as a global control.
- **Scorecard enhances comparison description:** The auto-generated text can reference which system ranked best/worst per dimension, but requires scorecard rankings to be computed first.

---

## MVP Definition

### Launch With (v1)

The minimum needed for a student to meaningfully compare the three systems and build intuition for design tradeoffs.

- [ ] **Data loading from data.xlsx** — nothing else works without this; validate all three sheets load correctly
- [ ] **System selection interface** — mechanical, electrical, hybrid cards/tabs
- [ ] **Equipment detail view for mechanical and electrical** — table of parts with quantity, cost, energy, land area, lifespan
- [ ] **Cost/land/efficiency scorecard with RAG ranking** — the primary at-a-glance comparison for all three systems
- [ ] **Cost over time chart** — line chart, three systems, user-selectable time horizon
- [ ] **Land area comparison chart** — grouped bar chart
- [ ] **Wind turbine count chart** — grouped bar chart
- [ ] **Energy breakdown pie chart** — per system, by action category
- [ ] **Hybrid 5-slot builder** — dropdowns per process stage from Miscellaneous parts
- [ ] **Hybrid completion gate** — block hybrid results until all 5 slots filled
- [ ] **Electrical battery/tank slider** — maps to 11-row tradeoff table

### Add After Validation (v1.x)

Features that enhance learning once core comparison works.

- [ ] **Hybrid vs. preset comparison description** — text block auto-generated from scorecard; add when core scorecard logic is stable
- [ ] **Hover tooltip content review** — ensure tooltips show values with units, not just raw numbers
- [ ] **Deployment to Render/Railway** — once local version is confirmed correct

### Future Consideration (v2+)

Features to defer until academic utility of v1 is confirmed.

- [ ] **Equipment lifespan emphasis** — dedicated lifecycle cost view (v1 shows lifespan in table; v2 could compute NPV)
- [ ] **Print/export scorecard** — useful for lab reports; not needed to validate the comparison tool concept
- [ ] **Additional system configurations** — e.g., solar-powered, gravity-fed; out of scope for current data

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Data loading from data.xlsx | HIGH | LOW | P1 |
| System selection interface | HIGH | LOW | P1 |
| Scorecard + RAG ranking | HIGH | LOW | P1 |
| Cost over time chart | HIGH | MEDIUM | P1 |
| Equipment detail view | HIGH | LOW | P1 |
| Hybrid 5-slot builder | HIGH | HIGH | P1 |
| Hybrid completion gate | HIGH | MEDIUM | P1 |
| Land area chart | HIGH | LOW | P1 |
| Turbine count chart | MEDIUM | LOW | P1 |
| Energy pie chart | MEDIUM | LOW | P1 |
| Battery/tank slider | HIGH | MEDIUM | P1 |
| Time horizon selector | MEDIUM | LOW | P1 |
| Hybrid vs. preset description | MEDIUM | MEDIUM | P2 |
| Academic visual polish | MEDIUM | MEDIUM | P2 |
| Deployment configuration | LOW | LOW | P2 |
| Export/print scorecard | LOW | MEDIUM | P3 |
| Lifecycle cost (NPV) view | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Comparable Tool Analysis

Analogous tools in the academic engineering domain that inform what patterns users will arrive with:

| Feature | HOMER Pro (Hybrid energy) | SAM / NREL (Renewable systems) | SEDAT (Solar desalination) | Our Approach |
|---------|--------------------------|-------------------------------|---------------------------|--------------|
| System selection | Topology diagram builder (complex) | Technology dropdown + financial model | Region + technology selectors | Simple 3-card/tab selector — lower barrier than HOMER/SAM |
| Comparison output | Optimization results table, hourly charts | Financial metrics table, annual production chart | Map + summary table | Side-by-side scorecard + charts — more visual than HOMER/SAM |
| Interactive controls | Many sliders, input fields | Many input panels | Map + dropdowns | Targeted: 1 slider (battery/tank) + 1 selector (time horizon) |
| Configuration builder | Full topology diagram | N/A | N/A | 5 functional-slot dropdown builder — novel for this domain |
| Learnability | LOW (complex; requires training) | LOW–MEDIUM (requires engineering background) | MEDIUM (web-based, simpler) | HIGH (target: first-time engineering student) |
| Deployment | Desktop app | Desktop app | Web app (Dash/Plotly) | Web app (Dash/Plotly), locally runnable |

Key takeaway: HOMER Pro and SAM are the genre leaders but are far too complex for undergraduate first exposure. SEDAT is the closest technical analogue (Dash/Plotly for academic desalination analysis) — confirming the stack is appropriate. Our tool differentiates on simplicity: three fixed systems, targeted interactive controls, and a guided hybrid builder that scaffolds the design process rather than asking students to configure from scratch.

---

## Sources

- Dashboard design patterns research: [Dashboard Design Patterns](https://dashboarddesignpatterns.github.io/patterns.html) — MEDIUM confidence (academic design research, multiple authors)
- Traffic-light / RAG scorecard patterns: [Bernard Marr — Performance Reporting with RAG Ratings](https://bernardmarr.com/performance-reporting-how-to-use-traffic-light-colours-and-rag-ratings-in-dashboards/) — MEDIUM confidence (widely cited industry practice)
- Dashboard UX patterns (delta/comparison): [Pencil & Paper — UX Pattern Analysis: Data Dashboards](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards) — MEDIUM confidence
- Dash/Plotly capabilities: [Plotly Dash Documentation](https://dash.plotly.com/) and [Plotly Examples](https://plotly.com/examples/) — HIGH confidence (official documentation)
- HOMER Pro: [HOMER Energy](https://www.homerenergy.com/products/pro/index.html) — MEDIUM confidence (product marketing page, limited interface detail)
- SAM parametric analysis: [SAM Simulation Options](https://sam.nlr.gov/simulation-options) — MEDIUM confidence (official NREL documentation)
- SEDAT (solar desalination Dash tool): [Nature Scientific Data — SEDAT paper](https://www.nature.com/articles/s41597-022-01331-4) — MEDIUM confidence (peer-reviewed; Dash/Plotly for academic desalination confirmed as validated approach)
- Cost visualization best practices: [FasterCapital — Cost Visualization](https://fastercapital.com/content/Cost-Visualization--How-to-Visualize-and-Present-Your-Cost-Model-Simulation-Data-and-Results.html) — LOW confidence (single commercial source)
- Line chart for cost-over-time recommendation: [WebDataRocks — Charts for Comparison Over Time](https://www.webdatarocks.com/blog/dataviz-project-part-3-charts-for-comparisons-over-time/) — LOW confidence (single source, verified by general Plotly documentation patterns)

---

*Feature research for: Interactive wind-powered desalination comparison dashboard (academic, Python/Dash/Plotly)*
*Researched: 2026-02-20*
