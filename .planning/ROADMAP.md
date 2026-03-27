# Roadmap: Wind-Powered Desalination Dashboard

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 (shipped 2026-02-23)
- ✅ **v1.1 Sharing & Analysis** — Phase 6 (shipped 2026-02-24)
- ✅ **v1.2 Parameter Exploration & Presentation** — Phases 7-11 (shipped 2026-03-01)
- 🚧 **v1.3 Systems Overhaul & UX Redesign** — Phases 12-15 (in progress)

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

### 🚧 v1.3 Systems Overhaul & UX Redesign (In Progress)

**Milestone Goal:** Reflect the redesigned hydraulic mechanical system and fixed hybrid preset, embed system diagrams, overhaul UI/UX for clarity and system distinctiveness, and push updated dashboard to GitHub.

**Phase Numbering:**
- Integer phases (12, 13, 14, 15): Planned milestone work
- Decimal phases (12.1, 12.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 12: Data Layer & Hybrid Builder Removal** - Fix loader crash, update BOMs for hydraulic mechanical and fixed hybrid, parse Energy sheet, remove hybrid builder entirely (completed 2026-03-27)
- [x] **Phase 13: System Layout Images & Creative Differentiation** - Embed PNG diagrams on all three system pages and create distinct layout identities for mechanical vs electrical (completed 2026-03-27)
- [ ] **Phase 14: UX Quality & Content Rewrite** - Slider fixes, loading spinners, first-visit guidance, landing page rewrite, and mechanical content update
- [ ] **Phase 15: Polish & GitHub Push** - Fix broken links, heading hierarchy, error messages, verify print export, push to GitHub

## Phase Details

### Phase 12: Data Layer & Hybrid Builder Removal
**Goal**: The app loads and displays correct data for all three systems with the hydraulic mechanical BOM, fixed hybrid preset, and Energy sheet values — and the hybrid builder is fully removed
**Depends on**: Phase 11 (v1.2 complete)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, CONTENT-03
**Success Criteria** (what must be TRUE):
  1. Running `python app.py` starts the dashboard without errors — no loader crash from missing sections or mismatched headers
  2. Mechanical equipment table shows hydraulic components (HPU, manifold, hydraulic motors, vertical turbine pump, plunger pump) with correct names, costs, and quantities
  3. Hybrid page displays a fixed preset configuration — no builder dropdowns, no slot selection UI, no "build your own" interaction
  4. Energy/power data from the Energy sheet appears correctly in the dashboard for all three systems
  5. Scorecard renders all three system columns on initial page load without requiring any user interaction
**Plans:** 3/3 plans complete

Plans:
- [x] 12-01-PLAN.md — Fix loader SECTION_HEADERS, rename miscellaneous to hybrid, parse Energy sheet
- [x] 12-02-PLAN.md — Delete hybrid builder, remove all references, wire static hybrid equipment table and ungated scorecard
- [x] 12-03-PLAN.md — Wire Energy sheet data into power breakdown and turbine count charts

### Phase 13: System Layout Images & Creative Differentiation
**Goal**: Each system page features its architecture diagram prominently and the mechanical and electrical pages have visually distinct layouts that reflect each system's character
**Depends on**: Phase 12
**Requirements**: VISUAL-01, VISUAL-02, VISUAL-03, VISUAL-04
**Success Criteria** (what must be TRUE):
  1. Mechanical system page displays the mechanical layout PNG as a prominent diagram (not a thumbnail or footnote)
  2. Electrical system page displays the electrical layout PNG as a prominent diagram
  3. Hybrid system page displays the hybrid layout PNG as a prominent diagram
  4. Mechanical and electrical pages are visually distinguishable beyond just color — different section emphasis, component presentation, or information hierarchy reflects each system's engineering character
**Plans:** 2/2 plans complete

Plans:
- [x] 13-01-PLAN.md — Copy PNGs to assets, insert diagram cards before scorecard, add differentiation CSS classes
- [x] 13-02-PLAN.md — Apply stage heading accents to equipment sections, visual verification checkpoint

### Phase 14: UX Quality & Content Rewrite
**Goal**: Sliders behave correctly without flicker, charts show loading feedback, first-time users get guidance, and all written content reflects the current system designs
**Depends on**: Phase 13
**Requirements**: UX-01, UX-02, UX-03, UX-04, UX-05, CONTENT-01, CONTENT-02
**Success Criteria** (what must be TRUE):
  1. Dragging the TDS or depth slider does NOT cause per-pixel chart recalculations — charts update only on mouse release
  2. A loading spinner appears during any chart recalculation — no blank white boxes visible during callback execution
  3. Battery/tank slider shows clear "100% Tank", "50/50", "100% Battery" endpoint labels and tooltip is visible during drag
  4. No text input boxes appear next to any slider (all four sliders have direct input suppressed)
  5. First-time visitors see a dismissable guidance banner explaining how to use the sliders; it disappears after interaction and does not reappear
  6. Landing page intro clearly explains wind-powered desalination, the three systems, and what students should explore — with no references to AI or automated tools
  7. Mechanical system descriptions and process stages reflect the hydraulic drive architecture (HPU, manifold, hydraulic motors driving pumps)
**Plans**: TBD
**UI hint**: yes

### Phase 15: Polish & GitHub Push
**Goal**: All rough edges resolved, print export verified after the overhaul, and the updated dashboard is pushed to GitHub
**Depends on**: Phase 14
**Requirements**: POLISH-01, POLISH-02, POLISH-03, POLISH-04
**Success Criteria** (what must be TRUE):
  1. The "System Explorer" sidebar link either navigates to a valid target or is removed — no broken navigation
  2. Scorecard, charts, and equipment sections have visually distinct heading levels — not three co-equal headings at the same size
  3. If data fails to load, the user sees a plain-English error message — no developer stack traces or raw sheet name errors
  4. Browser print-to-PDF produces clean output after hybrid builder removal and layout changes — no broken layouts, missing sections, or overlapping elements
  5. All changes are committed and pushed to the GitHub repository (https://github.com/kyr297-lang/desalination-dashboard)
**Plans**: TBD

## Deferred Features

The following were planned for v1.1 but deferred to a future milestone:

- NPV Lifecycle Cost Analysis — lifecycle economics with adjustable discount rate
- Equipment Comparison Table — side-by-side specs across all 3 systems
- Chart PNG Export — download charts as PNG for lab reports

## Progress

**Execution Order:**
Phases execute in numeric order: 12 → 13 → 14 → 15

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
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
| 12. Data Layer & Hybrid Builder Removal | v1.3 | 3/3 | Complete    | 2026-03-27 |
| 13. System Layout Images & Creative Differentiation | v1.3 | 2/2 | Complete    | 2026-03-27 |
| 14. UX Quality & Content Rewrite | v1.3 | 0/0 | Not started | - |
| 15. Polish & GitHub Push | v1.3 | 0/0 | Not started | - |
