# Requirements: Wind-Powered Desalination Dashboard

**Defined:** 2026-02-28
**Core Value:** Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs

## v1.2 Requirements

Requirements for milestone v1.2. Each maps to roadmap phases.

### Data Layer

- [x] **DATA-01**: App reads equipment data from the "Part 1" sheet (loader updated from "Sheet1")
- [x] **DATA-02**: App loads Part 2 salinity (TDS) vs RO-energy lookup table from "Part 2" sheet
- [x] **DATA-03**: App loads Part 2 depth vs pump-energy lookup table from "Part 2" sheet

### Sliders

- [ ] **SLDR-01**: User can adjust salinity (TDS, 0–1900 PPM) with a slider to see how it affects RO desalination energy requirement
- [ ] **SLDR-02**: User can adjust water source depth (0–1900 m) with a slider to see how it affects pump energy requirement
- [ ] **SLDR-03**: Salinity and depth slider values are reflected live in the power breakdown chart

### System Page Differentiation

- [ ] **DIFF-01**: Mechanical system page has a distinct visual treatment (color accent, section styling, or descriptive callout) that distinguishes it from the Electrical page
- [ ] **DIFF-02**: Electrical system page has a distinct visual treatment that distinguishes it from the Mechanical page

### Landing Page

- [ ] **LAND-01**: Overview tab shows a project introduction section above the system selection cards
- [ ] **LAND-02**: Landing section displays the four contributor names (Amogh Herle, Sofia Ijazi, Kevin Ren, Kyler Sanders)
- [ ] **LAND-03**: Landing section identifies the course context (Fall 2025–Spring 2026 senior design class)

### Terminology & Display Polish

- [ ] **POLISH-01**: Label "Energy" changed to "Power" in the scorecard row header (currently "Total Energy (kW)")
- [ ] **POLISH-02**: Label "Energy" changed to "Power" in the equipment accordion badge (currently shows "Energy" badge)
- [ ] **POLISH-03**: Power breakdown chart changed from pie chart to grouped bar chart
- [ ] **POLISH-04**: Numeric values in equipment grid and scorecard display at consistent 2 significant figures

## Future Requirements

Deferred from v1.1, not in this milestone scope.

### Analytics

- **NPV-01**: User can view lifecycle cost (NPV) with adjustable discount rate
- **EXPORT-01**: User can export individual charts as PNG/PDF files

### Equipment

- **EQUIP-01**: Side-by-side equipment comparison table across systems

## Out of Scope

| Feature | Reason |
|---------|--------|
| NPV/lifecycle cost view | Deferred from v1.1 — separate milestone |
| Chart PNG export | Deferred from v1.1 — separate milestone |
| Equipment comparison table | Deferred from v1.1 — separate milestone |
| Mobile layout | Desktop-first academic tool |
| Real-time wind data | Static data only; maintenance burden |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 7 | Complete |
| DATA-02 | Phase 7 | Complete |
| DATA-03 | Phase 7 | Complete |
| SLDR-01 | Phase 8 | Pending |
| SLDR-02 | Phase 8 | Pending |
| SLDR-03 | Phase 8 | Pending |
| DIFF-01 | Phase 9 | Pending |
| DIFF-02 | Phase 9 | Pending |
| LAND-01 | Phase 10 | Pending |
| LAND-02 | Phase 10 | Pending |
| LAND-03 | Phase 10 | Pending |
| POLISH-01 | Phase 11 | Pending |
| POLISH-02 | Phase 11 | Pending |
| POLISH-03 | Phase 11 | Pending |
| POLISH-04 | Phase 11 | Pending |

**Coverage:**
- v1.2 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-28*
*Last updated: 2026-02-28 after initial definition*
