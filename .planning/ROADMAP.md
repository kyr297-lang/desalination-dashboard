# Roadmap: Wind-Powered Desalination Dashboard

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 (shipped 2026-02-23)
- ✅ **v1.1 Sharing & Analysis** — Phase 6 (shipped 2026-02-24)
- ✅ **v1.2 Parameter Exploration & Presentation** — Phases 7-11 (shipped 2026-03-01)
- ✅ **v1.3 Systems Overhaul & UX Redesign** — Phases 12-14 (shipped 2026-03-27) — [archive](milestones/v1.3-ROADMAP.md)
- ✅ **v1.4 Data & Display Overhaul** — Phases 15-16 (shipped 2026-03-29) — [archive](milestones/v1.4-ROADMAP.md)
- 🚧 **v1.5 Polish & Comparison Overhaul** — Phases 17-18 (in progress)

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

<details>
<summary>✅ v1.4 Data & Display Overhaul (Phases 15-16) — SHIPPED 2026-03-29</summary>

- [x] Phase 15: Data Layer & Chart Overhaul (3/3 plans) — completed 2026-03-28
- [x] Phase 16: Display Polish & Content (3/3 plans) — completed 2026-03-29

</details>

### v1.5 Polish & Comparison Overhaul (Phases 17-18)

- [ ] **Phase 17: UI Polish & Chart Legend** — Sidebar nav, heading hierarchy, error messages, print/export verification, and cost-over-time graph legend
- [x] **Phase 18: Comparison Table Overhaul & Slider Explanation** — Replace per-stage cross-system slots with a consolidated 3-system comparison table on each system tab, and add slider explanation paragraph (completed 2026-04-10)

## Phase Details

### Phase 17: UI Polish & Chart Legend
**Goal**: Users experience a consistent, well-polished dashboard where navigation works, headings are visually uniform, errors are informative, print/export produces clean output, and chart lines are identifiable
**Depends on**: Phase 16 (v1.4 display baseline)
**Requirements**: POLISH-01, POLISH-02, POLISH-03, POLISH-04, CHART-01
**Success Criteria** (what must be TRUE):
  1. User can click the sidebar navigation link and reach the expected destination without broken behavior
  2. User sees a visually consistent heading hierarchy across every page (landing, system tabs, equipment sections)
  3. User sees clear, informative error messages when data fails to load or an invalid state is reached
  4. User can print or export the scorecard and produce correct output suitable for a lab report
  5. User can identify which line on the cost-over-time graph represents each of the three systems via a visible legend
**Plans**: 2 plans
- [ ] 17-01-PLAN.md — Chart legend (Plotly in-chart + badge sync), badge no-print, heading hierarchy normalization
- [ ] 17-02-PLAN.md — Verification: sidebar nav round-trip, data-load error page, print/export output

**UI hint**: yes

### Phase 18: Comparison Table Overhaul & Slider Explanation
**Goal**: Users see a consolidated 3-system comparison (including hybrid) on each system tab with their current system highlighted, and understand what the TDS and depth sliders control before interacting with them
**Depends on**: Phase 17
**Requirements**: COMP-01, COMP-02, COMP-03, COMP-04, COMP-05, SLDR-01
**Success Criteria** (what must be TRUE):
  1. User no longer sees per-stage cross-system comparison slots inside the equipment accordion
  2. User sees a single consolidated 3-system comparison table (mechanical, electrical, hybrid) below the accordion on every system tab
  3. User sees comparison rows for drive mechanism, energy storage, key advantage, key limitation, and best suited for
  4. User sees the current system's column visually highlighted using that system's existing CSS identity
  5. User reads a brief explanatory paragraph above the TDS and depth sliders describing what each slider controls and why it matters
**Plans**: TBD
**UI hint**: yes

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
| 15. Data Layer & Chart Overhaul | v1.4 | 3/3 | Complete | 2026-03-28 |
| 16. Display Polish & Content | v1.4 | 3/3 | Complete | 2026-03-29 |
| 17. UI Polish & Chart Legend | v1.5 | 0/? | Not started | - |
| 18. Comparison Table Overhaul & Slider Explanation | v1.5 | 2/2 | Complete   | 2026-04-10 |
