# Requirements: Wind-Powered Desalination Dashboard

**Defined:** 2026-02-21
**Core Value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs

## v1 Requirements

### Data & Infrastructure

- [x] **DATA-01**: App loads and parses data.xlsx at startup (Electrical, Mechanical, Miscellaneous sheets)
- [x] **DATA-02**: Data validation ensures all three sheets parse correctly before rendering UI
- [x] **DATA-03**: Consistent color mapping per system (Mechanical/Electrical/Hybrid) across all charts and components

### System Selection

- [x] **SEL-01**: User can select between Mechanical, Electrical, or Hybrid system from a clear selector interface
- [x] **SEL-02**: Selecting Mechanical or Electrical shows equipment list with quantity, cost, energy, land area, and lifespan
- [x] **SEL-03**: User can click/select individual equipment for detailed description and data

### Hybrid Builder

- [ ] **HYB-01**: User sees 5 functional slots: Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal
- [ ] **HYB-02**: Each slot presents a dropdown of valid equipment from the Miscellaneous sheet
- [ ] **HYB-03**: User cannot see comparison results or detailed output until all 5 slots are filled (completion gate)
- [ ] **HYB-04**: After completion, user can select hybrid equipment for detailed data view

### Scorecard & Ranking

- [x] **SCORE-01**: Dashboard displays cost, land area, and efficiency scorecard for all systems
- [x] **SCORE-02**: Each metric has red/yellow/green (RAG) ranking relative to the three systems
- [ ] **SCORE-03**: Hybrid system shows comparison description text against the two preset systems

### Comparison Charts

- [ ] **CHART-01**: Cost over time line chart comparing all three systems side-by-side
- [ ] **CHART-02**: User can select time horizon for cost-over-time chart (slider or input)
- [ ] **CHART-03**: Land area grouped bar chart comparing all three systems
- [ ] **CHART-04**: Wind turbine count grouped bar chart comparing all three systems
- [ ] **CHART-05**: Pie chart showing energy percentage by action (water extraction, desalination) per system

### Interactive Controls

- [ ] **CTRL-01**: Battery/tank tradeoff slider for electrical system maps to 11-row lookup table from data.xlsx
- [ ] **CTRL-02**: Slider updates electrical system cost and all related charts in real-time

### Visual Design

- [x] **VIS-01**: Academic styling — clean, professional, muted colors (FLATLY Bootstrap theme or similar)
- [x] **VIS-02**: Easy to navigate for students unfamiliar with the tool
- [ ] **VIS-03**: All charts have labeled axes with units, hover tooltips with formatted values

### Export

- [ ] **EXP-01**: User can export or print the scorecard summary for lab reports

### Deployment

- [x] **DEP-01**: App runs locally via `python app.py` with no external service dependencies

## v2 Requirements

### Deployment

- **DEP-02**: App deployable to Render/Railway free tier for sharing with classmates

### Advanced Analysis

- **ADV-01**: Lifecycle cost (NPV) view with discount rate input
- **ADV-02**: Side-by-side equipment comparison table across systems

### Export

- **EXP-02**: Export charts as PNG/PDF for reports

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real-time wind data API | Maintenance burden, out of scope for static academic tool |
| User accounts / saved configurations | Adds auth and database complexity; unnecessary for academic use |
| 3D visualization | Obscures data; 2D charts are clearer for comparison |
| AI/LLM explanations | Breaks deterministic academic tool contract |
| Mobile-optimized layout | Desktop-first academic tool |
| Solar/gravity-fed configurations | Not covered by current data.xlsx |
| Cloud deployment (v1) | Local-only for v1; cloud deploy is v2 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Complete |
| DATA-02 | Phase 1 | Complete |
| DATA-03 | Phase 1 | Complete |
| DEP-01 | Phase 1 | Complete |
| SEL-01 | Phase 2 | Complete |
| SEL-02 | Phase 2 | Complete |
| SEL-03 | Phase 2 | Complete |
| SCORE-01 | Phase 2 | Complete |
| SCORE-02 | Phase 2 | Complete |
| VIS-01 | Phase 2 | Complete |
| VIS-02 | Phase 2 | Complete |
| CHART-01 | Phase 3 | Pending |
| CHART-02 | Phase 3 | Pending |
| CHART-03 | Phase 3 | Pending |
| CHART-04 | Phase 3 | Pending |
| CHART-05 | Phase 3 | Pending |
| CTRL-01 | Phase 3 | Pending |
| CTRL-02 | Phase 3 | Pending |
| VIS-03 | Phase 3 | Pending |
| HYB-01 | Phase 4 | Pending |
| HYB-02 | Phase 4 | Pending |
| HYB-03 | Phase 4 | Pending |
| HYB-04 | Phase 4 | Pending |
| SCORE-03 | Phase 4 | Pending |
| EXP-01 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 25 total
- Mapped to phases: 25
- Unmapped: 0

---
*Requirements defined: 2026-02-21*
*Last updated: 2026-02-21 after roadmap creation — traceability complete*
