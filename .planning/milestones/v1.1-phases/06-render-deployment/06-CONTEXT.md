# Phase 6: Render Deployment - Context

**Gathered:** 2026-02-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Deploy the existing Dash desalination dashboard to Render free tier so classmates can access it via a public URL. All dashboard features (charts, scorecard, hybrid builder) must work identically to the local version. No new features — deployment only.

</domain>

<decisions>
## Implementation Decisions

### URL & access
- Render subdomain: desalination-dashboard.onrender.com (or closest available)
- Fully public — no authentication or password protection
- Direct to dashboard — no landing page, URL loads straight into the app
- No custom domain needed

### Cold start handling
- Accept Render free tier sleep behavior (~30-60s cold start after 15min inactivity)
- No keep-alive pings or loading indicators needed
- Rely on Render's built-in logs for monitoring — no custom health endpoint

### Data bundling
- Bundle data.xlsx directly in the repo — committed to version control
- No sensitive data in the file — safe for public repo
- Data will be updated frequently — push updated data.xlsx to GitHub, Render auto-redeploys
- Use pathlib-based paths so data.xlsx loads correctly in both local and deployed environments

### Deploy workflow
- Create a public GitHub repo for the project
- Connect GitHub repo to Render with auto-deploy on push to main branch
- Every push to main triggers automatic redeploy (~1 min)
- Data updates flow: update data.xlsx locally → git push → Render auto-redeploys

### Claude's Discretion
- Gunicorn worker count and configuration
- Procfile specifics
- requirements.txt generation method (pip freeze vs manual curation)
- .gitignore contents
- Render service configuration details (region, plan settings)
- Build command and start command specifics

</decisions>

<specifics>
## Specific Ideas

- App name on Render: "desalination-dashboard"
- Data will be updated frequently, so the push-and-redeploy workflow needs to be smooth
- This is a class project — simplicity over sophistication

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 06-render-deployment*
*Context gathered: 2026-02-23*
