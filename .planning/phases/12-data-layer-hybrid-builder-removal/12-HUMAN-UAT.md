---
status: partial
phase: 12-data-layer-hybrid-builder-removal
source: [12-VERIFICATION.md]
started: 2026-03-27T00:45:00.000Z
updated: 2026-03-27T00:45:00.000Z
---

## Current Test

[awaiting human testing]

## Tests

### 1. Hybrid Tab Visual Consistency

**Test:** Open the app and navigate to the Hybrid system tab. Compare the equipment accordion layout with the Mechanical and Electrical tabs.
expected: All three tabs show equipment grouped by process stage with identical card structure, badge rows (quantity/cost/power/land/lifespan), and expandable detail views
result: [pending]

### 2. Scorecard Initial Render (3 columns, no blank state)

**Test:** Navigate between all three system tabs and confirm the 3-column scorecard (Mechanical, Electrical, Hybrid) appears immediately on each tab switch with no blank state.
expected: Scorecard always present, 3 columns, RAG dots visible on first render without any user interaction
result: [pending]

### 3. TDS/Depth Sliders Update Power Breakdown Chart

**Test:** Adjust the TDS and depth sliders and confirm the Power Breakdown chart updates for all three systems.
expected: Water Extraction and Desalination bars change for all three systems as sliders move
result: [pending]

## Summary

total: 3
passed: 0
issues: 0
pending: 3
skipped: 0
blocked: 0

## Gaps
