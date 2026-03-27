# Requirements — v1.3 Systems Overhaul & UX Redesign

## Milestone v1.3 Requirements

### Data Layer

- [x] **DATA-01**: App loads without crashing after data.xlsx schema change — loader SECTION_HEADERS updated to match new Part 1 layout (no 'miscellaneous' section, updated mechanical/hybrid headers)
- [x] **DATA-02**: Mechanical BOM reflects hydraulic system — components include HPU, manifold, hydraulic motors, vertical turbine pump, plunger pump with correct names, costs, and quantities from data.xlsx
- [x] **DATA-03**: Hybrid BOM reflects fixed preset — hybrid section reads the fixed component list from data.xlsx Part 1 (no user-assembled slots)
- [x] **DATA-04**: Energy sheet parsed — shaft power and turbine sizing values for all three systems read from data.xlsx Energy sheet and displayed correctly in the dashboard

### System Content

- [x] **CONTENT-01**: Landing page intro rewritten — clearly explains what wind-powered desalination is, what the three systems represent, and what students are meant to explore and compare; no references to AI or automated tools
- [x] **CONTENT-02**: Mechanical system process stages and equipment descriptions updated — reflect hydraulic drive architecture (HPU → manifold → hydraulic motors driving pumps)
- [x] **CONTENT-03**: Hybrid builder replaced with static preset display — hybrid system shown as a fixed configuration matching the preset BOM; builder dropdowns and slot selection removed entirely

### Visual Design

- [x] **VISUAL-01**: Mechanical system layout image displayed on mechanical page — PNG served from assets/, shown as a prominent diagram above or alongside the equipment section
- [x] **VISUAL-02**: Electrical system layout image displayed on electrical page — PNG served from assets/, shown as a prominent diagram
- [x] **VISUAL-03**: Hybrid system layout image displayed on hybrid page — PNG served from assets/
- [x] **VISUAL-04**: Mechanical and electrical pages have creatively distinct layouts — not just different colors; different section emphasis, component presentation, or information hierarchy that reflects each system's character

### UX Quality

- [x] **UX-01**: All chart outputs wrapped in dcc.Loading — no blank white boxes during callback updates; spinner appears during any chart recalculation
- [x] **UX-02**: Battery/tank slider has clear endpoint labels — marks show "100% Tank", "50/50", "100% Battery"; tooltip always visible during drag
- [x] **UX-03**: TDS and depth sliders use mouseup updatemode — callbacks fire on release only, preventing per-pixel callback spam
- [x] **UX-04**: allow_direct_input=False set on all four sliders — prevents Dash 4.0 text input boxes from appearing on sliders
- [x] **UX-05**: First-visit dismissable callout shown — a banner above the control panel guides first-time users on how to use the sliders; dismisses after first interaction and does not reappear

### Polish

- [ ] **POLISH-01**: Broken sidebar link resolved — "System Explorer" link in shell.py either wired to a valid navigation target or removed
- [ ] **POLISH-02**: Heading hierarchy improved on system tabs — scorecard, charts, and equipment sections have visually distinct heading levels; not three co-equal H5s
- [ ] **POLISH-03**: Student-friendly error messages — if data fails to load, user sees a clear plain-English explanation; no developer-facing stack traces or sheet name errors exposed
- [ ] **POLISH-04**: Print/export verified after changes — browser print-to-PDF produces a clean output after hybrid builder removal and layout overhaul

## Future Requirements (deferred)

- Collapsible/expandable system diagrams — diagrams can be toggled to save screen space
- Guided tour overlay — step-by-step walkthrough for new users (requires JS integration)
- NPV / net present value analysis — financial metric beyond cumulative cost
- Equipment comparison table — cross-system equipment spec grid
- Chart PNG export — download individual chart images

## Out of Scope

- 3D visualization — 2D dashboard only; clarity over flash
- Real-time wind data integration — static data from spreadsheet
- Mobile-optimized layout — desktop-first academic tool
- User accounts or saving configurations — stateless dashboard
- Solar/gravity-fed configurations — not covered by current data.xlsx
- Render deployment — GitHub push only for v1.3; Render update deferred

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 12 | Complete |
| DATA-02 | Phase 12 | Complete |
| DATA-03 | Phase 12 | Complete |
| DATA-04 | Phase 12 | Complete |
| CONTENT-01 | Phase 14 | Complete |
| CONTENT-02 | Phase 14 | Complete |
| CONTENT-03 | Phase 12 | Complete |
| VISUAL-01 | Phase 13 | Complete |
| VISUAL-02 | Phase 13 | Complete |
| VISUAL-03 | Phase 13 | Complete |
| VISUAL-04 | Phase 13 | Complete |
| UX-01 | Phase 14 | Complete |
| UX-02 | Phase 14 | Complete |
| UX-03 | Phase 14 | Complete |
| UX-04 | Phase 14 | Complete |
| UX-05 | Phase 14 | Complete |
| POLISH-01 | Phase 15 | Pending |
| POLISH-02 | Phase 15 | Pending |
| POLISH-03 | Phase 15 | Pending |
| POLISH-04 | Phase 15 | Pending |
