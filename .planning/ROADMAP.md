# Roadmap: Wind-Powered Desalination Dashboard

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 (shipped 2026-02-23)
- 🔄 **v1.1 Sharing & Analysis** — Phases 6-9 (Phase 6 complete; Phases 7-9 pending)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-5) — SHIPPED 2026-02-23</summary>

- [x] Phase 1: Foundation (2/2 plans) — completed 2026-02-21
- [x] Phase 2: System Selection and Scorecard (2/2 plans) — completed 2026-02-21
- [x] Phase 3: Comparison Charts and Electrical Slider (2/2 plans) — completed 2026-02-22
- [x] Phase 4: Hybrid Builder (2/2 plans) — completed 2026-02-22
- [x] Phase 5: Polish and Deployment (2/2 plans) — completed 2026-02-23

</details>

### v1.1 Sharing & Analysis (Phases 6-9)

- [x] **Phase 6: Render Deployment** — App runs on Render free tier and is shareable via URL (completed 2026-02-23)
- [ ] **Phase 7: NPV Lifecycle Cost Analysis** — Students can explore lifecycle economics with adjustable discount rate
- [ ] **Phase 8: Equipment Comparison Table** — Students can compare equipment specs across all three systems in one table
- [ ] **Phase 9: Chart PNG Export** — Students can download any comparison chart as PNG for lab reports

## Phase Details

### Phase 6: Render Deployment
**Goal**: The app runs reliably on Render free tier and classmates can access it via a public URL
**Depends on**: Phase 5 (v1.0 shipped app)
**Requirements**: DEPLOY-01, DEPLOY-02, DEPLOY-03, DEPLOY-04
**Success Criteria** (what must be TRUE):
  1. User can access the dashboard from a public URL without running `python app.py` locally
  2. User visits the URL and all charts, scorecard, and hybrid builder load with correct data
  3. User who clones the repo can install all dependencies with a single `pip install -r requirements.txt` using pinned versions
  4. Deployed app reads `data.xlsx` correctly with no path-related errors in the Render logs
**Plans**: 2 plans
Plans:
- [x] 06-01-PLAN.md — Prepare codebase for Render (WSGI entry point, Procfile, gunicorn, .gitignore)
- [x] 06-02-PLAN.md — Push to GitHub and create Render Web Service

### Phase 7: NPV Lifecycle Cost Analysis
**Goal**: Students can view and explore net present value lifecycle costs for all three systems with a user-controlled discount rate
**Depends on**: Phase 6
**Requirements**: NPV-01, NPV-02, NPV-03, NPV-04
**Success Criteria** (what must be TRUE):
  1. User can see an NPV chart displaying lifecycle cost for all three systems (mechanical, electrical, hybrid)
  2. User can drag a discount rate slider from 1% to 10% and see the chart update without reloading the page
  3. User sets discount rate to 5% (default) and the displayed NPV values match manual calculation using capital cost, annual operating cost, and equipment lifespan from data.xlsx
  4. User changes the discount rate and the chart updates in real-time (no button press required)
**Plans**: TBD

### Phase 8: Equipment Comparison Table
**Goal**: Students can compare the key specs of all three systems side-by-side in a single table without switching tabs
**Depends on**: Phase 7
**Requirements**: COMP-01, COMP-02, COMP-03
**Success Criteria** (what must be TRUE):
  1. User can see a comparison table with mechanical, electrical, and hybrid as columns
  2. User can read cost, land area, energy, lifespan, and turbine count for each system in the same row
  3. User views the comparison table before completing the hybrid builder and sees only the mechanical and electrical columns populated; the hybrid column fills in after all 5 slots are selected
**Plans**: TBD

### Phase 9: Chart PNG Export
**Goal**: Students can download any comparison chart as a PNG image suitable for inclusion in lab reports
**Depends on**: Phase 8
**Requirements**: EXPORT-01, EXPORT-02, EXPORT-03
**Success Criteria** (what must be TRUE):
  1. User sees a download button on each comparison chart and clicking it saves a PNG file to their computer
  2. User opens the downloaded PNG and can read the chart title, axis labels with units, and legend clearly
  3. User on the deployed Render URL downloads a chart PNG and receives the same quality file as when running locally
**Plans**: TBD

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation | v1.0 | 2/2 | Complete | 2026-02-21 |
| 2. System Selection and Scorecard | v1.0 | 2/2 | Complete | 2026-02-21 |
| 3. Comparison Charts and Electrical Slider | v1.0 | 2/2 | Complete | 2026-02-22 |
| 4. Hybrid Builder | v1.0 | 2/2 | Complete | 2026-02-22 |
| 5. Polish and Deployment | v1.0 | 2/2 | Complete | 2026-02-23 |
| 6. Render Deployment | v1.1 | 2/2 | Complete | 2026-02-23 |
| 7. NPV Lifecycle Cost Analysis | v1.1 | 0/? | Not started | - |
| 8. Equipment Comparison Table | v1.1 | 0/? | Not started | - |
| 9. Chart PNG Export | v1.1 | 0/? | Not started | - |
