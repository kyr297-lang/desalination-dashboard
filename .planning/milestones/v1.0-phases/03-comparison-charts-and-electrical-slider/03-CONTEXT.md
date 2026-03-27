# Phase 3: Comparison Charts and Electrical Slider - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Students can explore side-by-side charts for all three desalination systems (Mechanical, Electrical, Hybrid) and adjust the electrical battery/tank tradeoff to see its effect in real time. Four comparison charts: cost-over-time line chart, land area grouped bar chart, wind turbine count grouped bar chart, and energy breakdown pie chart. Plus a time horizon slider and battery/tank tradeoff slider.

</domain>

<decisions>
## Implementation Decisions

### Chart layout & arrangement
- 2x2 grid layout, all four charts visible at once
- All charts equal size in the grid
- Grid position: Cost over time (top-left), Land area (top-right), Wind turbines (bottom-left), Energy pie (bottom-right)
- Same page as scorecard, below it — no separate tab
- Section heading: "System Comparison" to separate charts from scorecard above
- Each chart has a bold title and a one-line description of what it shows
- Charts in card containers with white background, shadow/border — matching existing scorecard card style
- Clean dashboard aesthetic (modern, card-based containers with subtle borders)
- Responsive layout — reflows to single column on narrow screens
- Shared legend above the chart grid showing all system colors
- Clicking a system name in the shared legend toggles that system's visibility across all four charts

### Control panel
- Both sliders (time horizon + battery/tank) in a distinct control panel above the chart grid
- Control panel has light background or subtle border to visually group controls
- Both sliders arranged side by side within the control panel
- Both sliders have same visual style for consistency
- Each slider has a label AND short help text explaining what it does

### Battery/tank slider interaction
- Free movement with interpolation between the 11 lookup table rows (not snapping to discrete positions)
- Live ratio label showing percentages: "70% Battery / 30% Tank" — percentages only, no unit counts
- No endpoint labels — ratio label is sufficient
- Charts update instantly on drag (real-time)
- Default starting position: middle (50/50)
- No reset button — students drag back to middle themselves
- No visual highlight on affected charts — charts update silently
- Live total cost readout for the electrical system displayed next to the slider, updating in real time

### Time horizon slider
- Slider control (matching battery/tank slider style)
- Range: 1 to 50 years
- Default: 50 years
- 1-year step increments
- Live year label (e.g., "25 years") updating as user drags
- Cost-over-time chart X-axis adjusts to only show up to the selected horizon year
- Cost shown as cumulative (running total from year 1 to selected year)

### Chart detail & style
- Tooltips on cost-over-time: system name + dollar amount (e.g., "Mechanical: $45.2K at Year 5")
- Bar charts: values on hover only (no labels on bars)
- Energy breakdown: 3 pie charts side by side (one per system), not a single pie with selector
- Each pie has system name as subtitle below it
- Pie chart slices: hover only for percentage labels (no labels on slices)
- Smooth animation transitions when data updates (slider moves)
- Dollar values abbreviated for large numbers (e.g., "$45.2K")
- Cost-over-time lines: smooth lines without data point markers
- Cost-over-time shows cumulative cost per year

### Claude's Discretion
- Color strategy: system colors vs per-chart palette — Claude picks based on visual clarity
- Bar chart width/spacing — Claude picks appropriate sizing
- Exact animation duration and easing
- Chart padding and internal margins
- Tooltip positioning and styling details

</decisions>

<specifics>
## Specific Ideas

- Charts should feel like a clean analytics dashboard — modern card containers, not academic/textbook
- Battery/tank slider should feel smooth and responsive with real-time chart updates
- The shared legend toggling visibility across all charts is important for comparison workflows
- Students need to quickly see cost implications — live electrical cost readout next to the battery/tank slider

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-comparison-charts-and-electrical-slider*
*Context gathered: 2026-02-21*
