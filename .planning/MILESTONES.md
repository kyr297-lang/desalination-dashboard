# Milestones

## v1.0 MVP (Shipped: 2026-02-23)

**Delivered:** Interactive wind-powered desalination comparison dashboard for engineering students — 3 systems, 4 charts, hybrid builder, and export.

**Stats:** 5 phases, 10 plans | 3,772 LOC Python | 50 commits | 3 days (2026-02-20 → 2026-02-23)
**Git range:** 19d6a75 → 710fb62

**Key accomplishments:**
1. Data layer parses 3-sheet data.xlsx into validated DataFrames with consistent system colors
2. System selection UI with landing overview, tab navigation, RAG scorecard, and accordion equipment grid (24 items)
3. Four comparison charts (cost-over-time, land area, turbine count, energy pie) with battery slider and real-time updates
4. 5-slot hybrid pipeline builder with completion gate, integrated into all charts, scorecard, and comparison text
5. Browser print-to-PDF export, chart axis formatting, and user-verified 30-second student comprehension

**Requirements:** 25/25 v1 requirements satisfied
**Tech debt:** 25 items (18 human verification, 4 orphaned imports, 2 doc, 1 architectural) — 0 critical

---


## v1.1 Sharing & Analysis (Shipped: 2026-02-24)

**Delivered:** Deployed the dashboard to Render free tier with auto-deploy from GitHub, making it accessible to classmates via public URL.

**Stats:** 1 phase, 2 plans | 6 commits | 1 day (2026-02-23 → 2026-02-24)

**Key accomplishments:**
1. WSGI entry point (`server = app.server`) and Procfile with gunicorn for Render deployment
2. Public GitHub repo at https://github.com/kyr297-lang/desalination-dashboard
3. Auto-deploy pipeline: push to main → Render rebuilds automatically
4. Fixed Python 3.14 → 3.11 compatibility (no pre-built wheels for pandas on 3.14)

**Requirements:** 4/14 v1.1 requirements satisfied (DEPLOY-01 through DEPLOY-04)
**Known gaps:** NPV analysis (Phase 7), Equipment comparison table (Phase 8), Chart PNG export (Phase 9) — deferred to future milestone

---

