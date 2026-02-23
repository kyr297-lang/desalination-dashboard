# Requirements: Wind-Powered Desalination Dashboard

**Defined:** 2026-02-23
**Core Value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs

## v1.1 Requirements

Requirements for Milestone v1.1: Sharing & Analysis. Each maps to roadmap phases.

### Deployment

- [ ] **DEPLOY-01**: App is deployable to Render free tier with gunicorn and Procfile
- [ ] **DEPLOY-02**: App exposes `server = app.server` for WSGI compatibility
- [ ] **DEPLOY-03**: `requirements.txt` includes all dependencies with pinned versions
- [ ] **DEPLOY-04**: App loads `data.xlsx` correctly in deployed environment (pathlib-based paths)

### NPV Analysis

- [ ] **NPV-01**: User can view Net Present Value lifecycle cost for all 3 systems
- [ ] **NPV-02**: User can adjust discount rate via slider (range 1-10%, default 5%)
- [ ] **NPV-03**: NPV chart updates in real-time as discount rate changes
- [ ] **NPV-04**: NPV calculation accounts for capital cost, annual operating cost, and equipment lifespan

### Equipment Comparison

- [ ] **COMP-01**: User can view side-by-side equipment comparison table across all 3 systems
- [ ] **COMP-02**: Table shows cost, land area, energy, lifespan, and turbine count per system
- [ ] **COMP-03**: Hybrid system column populates only when all 5 slots are filled (respects completion gate)

### Chart Export

- [ ] **EXPORT-01**: Each comparison chart has a PNG download button
- [ ] **EXPORT-02**: Downloaded PNG includes chart title, axis labels, and legend
- [ ] **EXPORT-03**: Export works both locally and in deployed environment

## Future Requirements

Deferred beyond v1.1.

### Reporting
- **RPT-01**: Export all charts as combined PDF for lab reports
- **RPT-02**: Export scorecard as standalone printable page

### Additional Systems
- **SYS-01**: Solar-powered desalination configuration
- **SYS-02**: Gravity-fed desalination configuration

## Out of Scope

| Feature | Reason |
|---------|--------|
| Railway deployment | Render is sufficient; Railway docs available if needed later |
| Real-time wind data API | Static data from spreadsheet; maintenance burden |
| User accounts / saved configurations | Stateless dashboard; unnecessary complexity |
| AI/LLM explanations | Breaks deterministic academic tool contract |
| Mobile-optimized layout | Desktop-first academic tool |
| Combined PDF export | Per-chart PNG is sufficient for v1.1; combined export deferred |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DEPLOY-01 | TBD | Pending |
| DEPLOY-02 | TBD | Pending |
| DEPLOY-03 | TBD | Pending |
| DEPLOY-04 | TBD | Pending |
| NPV-01 | TBD | Pending |
| NPV-02 | TBD | Pending |
| NPV-03 | TBD | Pending |
| NPV-04 | TBD | Pending |
| COMP-01 | TBD | Pending |
| COMP-02 | TBD | Pending |
| COMP-03 | TBD | Pending |
| EXPORT-01 | TBD | Pending |
| EXPORT-02 | TBD | Pending |
| EXPORT-03 | TBD | Pending |

**Coverage:**
- v1.1 requirements: 14 total
- Mapped to phases: 0
- Unmapped: 14 ⚠️

---
*Requirements defined: 2026-02-23*
*Last updated: 2026-02-23 after initial definition*
