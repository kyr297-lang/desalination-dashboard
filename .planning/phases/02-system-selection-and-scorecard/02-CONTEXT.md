# Phase 2: System Selection and Scorecard - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Students can select a system (Mechanical, Electrical, or Hybrid), browse its equipment list with key metrics, view individual equipment details with cross-system comparison, and see an at-a-glance RAG scorecard comparing all systems. Charts and the Hybrid builder are separate phases.

</domain>

<decisions>
## Implementation Decisions

### System selector & navigation
- Horizontal tab bar across the top of the main content area for switching between Mechanical, Electrical, and Hybrid
- Tabs use clean names only ("Mechanical", "Electrical", "Hybrid") — no metrics on the tab itself
- Active tab uses the system's assigned color (from Phase 1) for strong visual reinforcement
- Sidebar from Phase 1 stays separate — not involved in system selection
- Scorecard on top, equipment list below — vertical stack layout
- Same-page content swap when switching tabs — no page transitions

### Landing / Overview state
- On first load, show a landing overview (no system pre-selected)
- Landing has a brief intro line (e.g., "Select a desalination system to explore")
- Three cards in a horizontal row — one per system
- Each card: system name + brief 1-2 sentence description, text only (no icons/images)
- Cards have a colored header/top bar using the system's assigned color
- Clicking a card enters the tab view for that system
- "Back to Overview" breadcrumb/link (not a fourth tab) to return to the landing state

### Hybrid tab (before Phase 4)
- Empty state with message: "Build your hybrid system to see equipment here"
- Points students to the builder (which is Phase 4 work)

### Equipment list layout
- Card/tile format — each equipment item is a card, not a table row
- Cards arranged in a grid (2-3 cards per row)
- All five metrics visible on each card at a glance: quantity, cost, energy, land area, lifespan
- Cards grouped by process stage (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal) with section headers

### Equipment detail view
- Clicking a card expands it in place (accordion style) — other cards shift down
- Only one card expanded at a time — expanding a new card auto-collapses the previous
- Expanded view shows: full text description + all raw data fields from the spreadsheet
- Explicit close button (X or "Close") in the expanded area
- Cross-system comparison: small comparison table showing this equipment vs. equivalents from other systems for the same process stage
- Comparison table highlights the best value per metric (bold or green)
- Missing/empty data fields show "N/A"

### Data formatting
- Costs: abbreviated large numbers ($42.5K, $1.2M)
- Units inline with each value ("450 kWh", "$42.5K", "2.3 acres")

### Scorecard presentation
- Horizontal comparison table: systems as columns, metrics (cost, land area, efficiency) as rows
- RAG indicators: colored dots/circles next to each value
- Actual numeric values displayed alongside RAG dots
- RAG logic: relative ranking — green = best of systems, yellow = middle, red = worst
- With only 2 systems (Hybrid not built): green and red only, no yellow
- Hybrid column hidden until Hybrid system is fully assembled (Phase 4)
- Scorecard has a title + brief explanation of RAG meaning (green = best, red = worst)
- Includes an overall ranking/summary row showing which system "wins" overall

### Claude's Discretion
- Exact card spacing, padding, shadows, and typography
- Animation/transitions for card expand/collapse
- Exact wording of the landing page intro and empty state messages
- How the overall ranking row is calculated (equal weight, weighted, etc.)
- Loading states and error handling

</decisions>

<specifics>
## Specific Ideas

- Landing cards with colored header strips per system color — students see the color mapping immediately
- Equipment detail comparison table across all three systems (not just current) — helps students understand tradeoffs at the component level
- "Back to Overview" as a breadcrumb, not a tab — keeps the tab bar clean with just the three systems

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-system-selection-and-scorecard*
*Context gathered: 2026-02-21*
