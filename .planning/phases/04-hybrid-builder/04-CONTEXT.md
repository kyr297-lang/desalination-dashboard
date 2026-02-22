# Phase 4: Hybrid Builder - Context

**Gathered:** 2026-02-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Students can assemble a custom hybrid desalination system by selecting equipment for each of 5 process stages (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal). The dashboard blocks hybrid results until all 5 slots are filled. Once complete, the hybrid system appears in all comparison charts and the scorecard alongside the two preset systems, with a factual comparison description text.

</domain>

<decisions>
## Implementation Decisions

### Builder layout & slots
- Horizontal pipeline layout: slots flow left-to-right representing the process flow
- Visual arrows (→) connect each stage to reinforce the pipeline concept
- Each slot is a labeled dropdown only — minimal, clean, no per-slot stats before gate opens
- Dropdown options show equipment names only (no inline stats)
- Builder sits at the top of the Hybrid tab, above charts/scorecard
- Include a "Clear All" / reset button to start over
- On small screens, pipeline wraps to multiple rows (not horizontal scroll)

### Completion gate UX
- Before all 5 slots are filled: charts area shows a centered message overlay (e.g., "Fill all 5 slots to see hybrid results") with empty/placeholder chart outlines behind it
- Simple counter displayed: "3/5 slots filled"
- When 5th slot is filled: charts and scorecard appear instantly (no animation)
- If a user clears a slot after gate was met: charts disappear immediately and message overlay returns (gate re-engages)

### Hybrid results integration
- Hybrid color: Claude's discretion — pick a color that complements existing Mechanical and Electrical colors
- Charts recalculate only when all 5 slots are filled — changing one slot hides results until all 5 are set again
- Hybrid row in scorecard uses same styling as preset systems (no special distinction)
- Clicking hybrid equipment opens the same detail view as preset equipment items
- Hybrid system appears as an equal third system in all comparison charts

### Comparison description text
- Neutral/factual tone: straightforward percentage comparisons (e.g., "Hybrid costs 15% less than Mechanical")
- Covers all scorecard metrics: cost, land area, and efficiency
- Appears below the scorecard table
- Updates dynamically whenever the hybrid configuration changes (and gate is met)

### Claude's Discretion
- Hybrid system color choice
- Exact arrow styling between pipeline slots
- Loading/placeholder chart outline design behind the gate message
- Responsive breakpoints for pipeline wrapping

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-hybrid-builder*
*Context gathered: 2026-02-22*
