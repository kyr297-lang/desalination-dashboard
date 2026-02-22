# Roadmap: Wind-Powered Desalination Dashboard

## Overview

This roadmap builds the dashboard in strict dependency order: data layer first (nothing else works without it), then static layouts and the scorecard (validating component structure), then the four comparison charts with the electrical slider (the main visual payoff), then the most complex feature — the Hybrid 5-slot builder with its completion gate — and finally polish, the comparison description text, and local deployment readiness. Each phase delivers a verifiable capability before the next begins.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation** - Data layer, app shell, and project scaffolding — everything else depends on this (completed 2026-02-21)
- [x] **Phase 2: System Selection and Scorecard** - Static layouts, equipment detail views, and RAG scorecard (completed 2026-02-21)
- [x] **Phase 3: Comparison Charts and Electrical Slider** - All four comparison charts with real data and the battery/tank tradeoff control (completed 2026-02-22)
- [ ] **Phase 4: Hybrid Builder** - 5-slot equipment builder, completion gate, and hybrid data flowing into all charts
- [ ] **Phase 5: Polish and Deployment** - Comparison description text, visual audit, export, and local deployment readiness

## Phase Details

### Phase 1: Foundation
**Goal**: The app launches, reads data.xlsx correctly, and provides the structural shell all features build on
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, DEP-01
**Success Criteria** (what must be TRUE):
  1. Running `python app.py` starts the app with no errors and opens in a browser
  2. All three Excel sheets (Electrical, Mechanical, Miscellaneous) load and parse without crashing
  3. A startup validation message or error clearly tells the user if any sheet fails to parse
  4. A consistent color is visibly assigned to each system (Mechanical, Electrical, Hybrid) that will persist across all future charts
**Plans:** 2/2 plans complete
Plans:
- [ ] 01-01-PLAN.md — Data layer: Excel parser, config, system colors, requirements.txt
- [ ] 01-02-PLAN.md — App shell: Dash entry point, collapsible sidebar, error page, browser auto-open

### Phase 2: System Selection and Scorecard
**Goal**: Students can select a system, browse its equipment list, and see an at-a-glance RAG scorecard comparing all three systems
**Depends on**: Phase 1
**Requirements**: SEL-01, SEL-02, SEL-03, SCORE-01, SCORE-02, VIS-01, VIS-02
**Success Criteria** (what must be TRUE):
  1. User can click Mechanical, Electrical, or Hybrid and see the correct equipment list appear
  2. Equipment list shows quantity, cost, energy, land area, and lifespan for each component
  3. User can click an individual piece of equipment and see its detailed description and data
  4. Scorecard displays cost, land area, and efficiency values for all three systems
  5. Each scorecard metric has a clearly visible red, yellow, or green indicator relative to the other systems
**Plans:** 2/2 plans complete
Plans:
- [ ] 02-01-PLAN.md — Data processing helpers, config domain data (process stages, equipment descriptions, RAG logic, scorecard computation)
- [ ] 02-02-PLAN.md — Landing overview, tab navigation, RAG scorecard table, equipment card grid with accordion detail and cross-system comparison

### Phase 3: Comparison Charts and Electrical Slider
**Goal**: Students can explore side-by-side charts for all three systems and adjust the electrical battery/tank tradeoff to see its effect in real time
**Depends on**: Phase 2
**Requirements**: CHART-01, CHART-02, CHART-03, CHART-04, CHART-05, CTRL-01, CTRL-02, VIS-03
**Success Criteria** (what must be TRUE):
  1. Cost over time line chart shows all three systems plotted side-by-side with labeled axes and hover tooltips
  2. User can move a time horizon slider and the cost chart updates to reflect the selected number of years
  3. Land area grouped bar chart and wind turbine count grouped bar chart both display all three systems side-by-side
  4. Pie chart shows energy breakdown by process action (water extraction, desalination) for each system
  5. Moving the electrical battery/tank slider updates the electrical system values across all relevant charts in real time
**Plans:** 2/2 plans complete
Plans:
- [x] 03-01-PLAN.md — Data computation functions (cost-over-time, battery interpolation, chart data aggregation) and chart figure builders with layout
- [ ] 03-02-PLAN.md — Callback wiring, legend toggle, slider integration, and chart section into system view

### Phase 4: Hybrid Builder
**Goal**: Students can assemble a custom hybrid system by selecting equipment for each process stage, and the dashboard blocks results until all five slots are filled
**Depends on**: Phase 3
**Requirements**: HYB-01, HYB-02, HYB-03, HYB-04, SCORE-03
**Success Criteria** (what must be TRUE):
  1. User sees five labeled slots (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal) each with a dropdown of valid equipment options
  2. With fewer than five slots filled, the comparison charts and scorecard do not update for the hybrid system (gate is enforced)
  3. After all five slots are filled, the hybrid system appears in all comparison charts and the scorecard alongside the two preset systems
  4. User can click a hybrid equipment item to see its detailed data view
  5. A description text compares the hybrid system's scorecard ranking against the Mechanical and Electrical presets
**Plans:** 1/2 plans executed
Plans:
- [ ] 04-01-PLAN.md — Config fix, hybrid processing helpers, and pipeline builder UI with slot store and callbacks
- [ ] 04-02-PLAN.md — Integration: gate overlay, chart/scorecard/equipment wiring, comparison text, human verification

### Phase 5: Polish and Deployment
**Goal**: The dashboard is visually polished, easy for unfamiliar students to navigate, supports export for lab reports, and runs cleanly from a single command
**Depends on**: Phase 4
**Requirements**: VIS-02, EXP-01, DEP-01
**Success Criteria** (what must be TRUE):
  1. A student who has never used the tool can identify what to do first within 30 seconds of opening it
  2. All chart axes have labeled units, all hover tooltips show formatted values (dollar signs, units), and colors are consistent across every chart
  3. User can export or print the scorecard summary suitable for inclusion in a lab report
  4. Running `python app.py` on a clean machine with dependencies installed starts the app with no configuration beyond the command
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 2/2 | Complete    | 2026-02-21 |
| 2. System Selection and Scorecard | 2/2 | Complete    | 2026-02-22 |
| 3. Comparison Charts and Electrical Slider | 2/2 | Complete    | 2026-02-22 |
| 4. Hybrid Builder | 1/2 | In Progress|  |
| 5. Polish and Deployment | 0/TBD | Not started | - |
