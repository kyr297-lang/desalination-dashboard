# Roadmap: Wind-Powered Desalination Dashboard

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 (shipped 2026-02-23)
- ✅ **v1.1 Sharing & Analysis** — Phase 6 (shipped 2026-02-24)
- ✅ **v1.2 Parameter Exploration & Presentation** — Phases 7-11 (shipped 2026-03-01)
- ✅ **v1.3 Systems Overhaul & UX Redesign** — Phases 12-14 (shipped 2026-03-27) — [archive](.planning/milestones/v1.3-ROADMAP.md)

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

<details>
<summary>✅ v1.2 Parameter Exploration & Presentation (Phases 7-11) — SHIPPED 2026-03-01</summary>

- [x] Phase 7: Data Layer (2/2 plans) — completed 2026-02-28
- [x] Phase 8: Parameter Sliders (2/2 plans) — completed 2026-03-01
- [x] Phase 9: System Page Differentiation (1/1 plan) — completed 2026-03-01
- [x] Phase 10: Landing Page (1/1 plan) — completed 2026-03-01
- [x] Phase 11: Terminology and Display Polish (1/1 plan) — completed 2026-03-01

</details>

<details>
<summary>✅ v1.3 Systems Overhaul & UX Redesign (Phases 12-14) — SHIPPED 2026-03-27</summary>

- [x] Phase 12: Data Layer & Hybrid Builder Removal (3/3 plans) — completed 2026-03-27
- [x] Phase 13: System Layout Images & Creative Differentiation (2/2 plans) — completed 2026-03-27
- [x] Phase 14: UX Quality & Content Rewrite (3/3 plans) — completed 2026-03-27

</details>

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1. Foundation | v1.0 | 2/2 | Complete | 2026-02-21 |
| 2. System Selection and Scorecard | v1.0 | 2/2 | Complete | 2026-02-21 |
| 3. Comparison Charts and Electrical Slider | v1.0 | 2/2 | Complete | 2026-02-22 |
| 4. Hybrid Builder | v1.0 | 2/2 | Complete | 2026-02-22 |
| 5. Polish and Deployment | v1.0 | 2/2 | Complete | 2026-02-23 |
| 6. Render Deployment | v1.1 | 2/2 | Complete | 2026-02-24 |
| 7. Data Layer | v1.2 | 2/2 | Complete | 2026-02-28 |
| 8. Parameter Sliders | v1.2 | 2/2 | Complete | 2026-03-01 |
| 9. System Page Differentiation | v1.2 | 1/1 | Complete | 2026-03-01 |
| 10. Landing Page | v1.2 | 1/1 | Complete | 2026-03-01 |
| 11. Terminology and Display Polish | v1.2 | 1/1 | Complete | 2026-03-01 |
| 12. Data Layer & Hybrid Builder Removal | v1.3 | 3/3 | Complete | 2026-03-27 |
| 13. System Layout Images & Creative Differentiation | v1.3 | 2/2 | Complete | 2026-03-27 |
| 14. UX Quality & Content Rewrite | v1.3 | 3/3 | Complete | 2026-03-27 |

---

## v1.4 Data & Display Overhaul

### Phase 15: data-layer-chart-overhaul
**Goal:** Fix loader for new xlsx; remove land/turbine charts; power breakdown uses 3 subsystems; all sliders work.
**Requirements:** DATA-01–04, CHART-01–07
**Files:** loader.py, processing.py, charts.py, config.py

### Phase 16: display-polish-content
**Goal:** Photos, equipment names/grouping, scorecard, descriptions, hybrid accent.
**Requirements:** DISP-01–11
**Files:** assets/*.png, config.py, equipment_grid.py, scorecard.py, overview.py, custom.css
