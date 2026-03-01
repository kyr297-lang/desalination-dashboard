# Roadmap: Wind-Powered Desalination Dashboard

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 (shipped 2026-02-23)
- ✅ **v1.1 Sharing & Analysis** — Phase 6 (shipped 2026-02-24)
- 🚧 **v1.2 Parameter Exploration & Presentation** — Phases 7-11 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-5) — SHIPPED 2026-02-23</summary>

- [x] Phase 1: Foundation (2/2 plans) — completed 2026-02-21
- [x] Phase 2: System Selection and Scorecard (2/2 plans) — completed 2026-02-21
- [x] Phase 3: Comparison Charts and Electrical Slider (2/2 plans) — completed 2026-02-22
- [x] Phase 4: Hybrid Builder (2/2 plans) — completed 2026-02-22
- [x] Phase 5: Polish and Deployment (2/2 plans) — completed 2026-02-23

</details>

<details>
<summary>✅ v1.1 Sharing & Analysis (Phase 6) — SHIPPED 2026-02-24</summary>

- [x] Phase 6: Render Deployment (2/2 plans) — completed 2026-02-24

</details>

### 🚧 v1.2 Parameter Exploration & Presentation (In Progress)

**Milestone Goal:** Add salinity/depth energy tradeoff sliders from Part 2 data, differentiate system page designs, add a project landing section, and correct terminology and chart type throughout.

- [x] **Phase 7: Data Layer** — Update sheet loader and ingest Part 2 lookup tables (completed 2026-02-28)
- [~] **Phase 8: Parameter Sliders** — Salinity (TDS) and depth sliders wired to power breakdown chart (checkpoint awaiting human verification)
- [x] **Phase 9: System Page Differentiation** — Distinct visual treatment for Mechanical vs Electrical pages (completed 2026-03-01)
- [x] **Phase 10: Landing Page** — Project introduction section with contributors and course context (completed 2026-03-01)
- [x] **Phase 11: Terminology and Display Polish** — Power labels, pie-to-bar chart, 2 significant figures (completed 2026-03-01)

## Phase Details

### Phase 7: Data Layer
**Goal**: App correctly reads all data it needs for v1.2 features — equipment from the renamed sheet and both Part 2 lookup tables for energy interpolation
**Depends on**: Phase 6 (working deployed app)
**Requirements**: DATA-01, DATA-02, DATA-03
**Success Criteria** (what must be TRUE):
  1. App launches without errors after the sheet rename from "Sheet1" to "Part 1"
  2. Equipment data (Electrical, Mechanical, Miscellaneous) loads correctly from "Part 1"
  3. Salinity (TDS) vs RO-energy lookup table is accessible in memory for use by the slider callback
  4. Depth vs pump-energy lookup table is accessible in memory for use by the slider callback
**Plans**: TBD

### Phase 8: Parameter Sliders
**Goal**: Students can explore how source water salinity and depth affect energy requirements by moving sliders and seeing the power breakdown chart update live
**Depends on**: Phase 7
**Requirements**: SLDR-01, SLDR-02, SLDR-03
**Success Criteria** (what must be TRUE):
  1. A salinity (TDS) slider with range 0–1900 PPM is visible on the relevant chart or panel
  2. A water source depth slider with range 0–1900 m is visible on the relevant chart or panel
  3. Moving either slider updates the power breakdown chart without a full page reload
  4. The power breakdown chart values reflect the interpolated energy values from the Part 2 lookup tables at the selected slider positions
**Plans**: TBD

### Phase 9: System Page Differentiation
**Goal**: Students can immediately tell whether they are looking at the Mechanical or Electrical system page from its visual styling alone, without reading the header
**Depends on**: Phase 7
**Requirements**: DIFF-01, DIFF-02
**Success Criteria** (what must be TRUE):
  1. The Mechanical system page has a distinct color accent, section styling, or descriptive callout not present on the Electrical page
  2. The Electrical system page has a distinct color accent, section styling, or descriptive callout not present on the Mechanical page
  3. Both pages remain readable and consistent with the FLATLY academic theme
**Plans**: 1 plan

Plans:
- [ ] 09-01-PLAN.md — System badge + page-wide background tint for Mechanical and Electrical tabs

### Phase 10: Landing Page
**Goal**: The Overview tab opens with a project introduction section that tells students who built this and why before they interact with any system cards
**Depends on**: Phase 7
**Requirements**: LAND-01, LAND-02, LAND-03
**Success Criteria** (what must be TRUE):
  1. A project introduction section appears above the system selection cards in the Overview tab
  2. The section displays all four contributor names: Amogh Herle, Sofia Ijazi, Kevin Ren, Kyler Sanders
  3. The section identifies the course context as a Fall 2025–Spring 2026 senior design class
**Plans**: TBD

### Phase 11: Terminology and Display Polish
**Goal**: Every power-related label in the dashboard uses "Power" not "Energy", the power breakdown chart is a grouped bar chart, and all numeric values display at consistent 2 significant figures
**Depends on**: Phase 8
**Requirements**: POLISH-01, POLISH-02, POLISH-03, POLISH-04
**Success Criteria** (what must be TRUE):
  1. The scorecard row that previously read "Total Energy (kW)" now reads "Total Power (kW)"
  2. The equipment accordion badge that previously read "Energy" now reads "Power"
  3. The power breakdown chart is a grouped bar chart, not a pie chart
  4. Numeric values in the equipment grid and scorecard display at consistent 2 significant figures (e.g., 1200 → 1200, 1234.5 → 1200, 0.00456 → 0.0046)
**Plans**: 1 plan

Plans:
- [ ] 11-01-PLAN.md — Rename Energy->Power labels, switch to grouped bar chart, add 2-sig-fig formatting

## Deferred Features

The following were planned for v1.1 but deferred to a future milestone:

- NPV Lifecycle Cost Analysis — lifecycle economics with adjustable discount rate
- Equipment Comparison Table — side-by-side specs across all 3 systems
- Chart PNG Export — download charts as PNG for lab reports

Use `/gsd:new-milestone` to start a new milestone incorporating any of these.

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation | v1.0 | 2/2 | Complete | 2026-02-21 |
| 2. System Selection and Scorecard | v1.0 | 2/2 | Complete | 2026-02-21 |
| 3. Comparison Charts and Electrical Slider | v1.0 | 2/2 | Complete | 2026-02-22 |
| 4. Hybrid Builder | v1.0 | 2/2 | Complete | 2026-02-22 |
| 5. Polish and Deployment | v1.0 | 2/2 | Complete | 2026-02-23 |
| 6. Render Deployment | v1.1 | 2/2 | Complete | 2026-02-24 |
| 7. Data Layer | v1.2 | 2/2 | Complete | 2026-02-28 |
| 8. Parameter Sliders | v1.2 | 2/2 | Checkpoint (human-verify) | - |
| 9. System Page Differentiation | 1/1 | Complete   | 2026-03-01 | - |
| 10. Landing Page | 1/1 | Complete    | 2026-03-01 | - |
| 11. Terminology and Display Polish | 1/1 | Complete   | 2026-03-01 | - |
