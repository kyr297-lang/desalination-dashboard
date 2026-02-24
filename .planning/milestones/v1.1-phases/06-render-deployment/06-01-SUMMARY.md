---
phase: 06-render-deployment
plan: 01
subsystem: infra
tags: [gunicorn, render, wsgi, dash, flask, deployment]

# Dependency graph
requires:
  - phase: 05-hybrid-builder
    provides: completed Dash app (app.py) with all features working locally
provides:
  - WSGI server entry point (server = app.server) in app.py
  - Procfile declaring gunicorn web process for Render
  - gunicorn==25.1.0 pinned in requirements.txt
  - .python-version pinning 3.14 for Render runtime
  - .gitignore excluding __pycache__, ~$*, .venv, IDE files
  - data.xlsx tracked in git for deployment
affects: [06-render-deployment plan 02 - GitHub push and Render service creation]

# Tech tracking
tech-stack:
  added: [gunicorn==25.1.0]
  patterns: [WSGI entry point pattern via server = app.server at module level]

key-files:
  created: [Procfile, .python-version, .gitignore]
  modified: [app.py, requirements.txt, data.xlsx (git-tracked)]

key-decisions:
  - "Expose Flask server via server = app.server at module level (not inside if __name__ block) so gunicorn can import it"
  - "Pin gunicorn==25.1.0 in requirements.txt — stable release supporting Python 3.14"
  - "Use --workers 2 for Render free tier 512MB RAM safety"
  - "Use --timeout 120 as conservative safety margin for initial data load"
  - "Pin .python-version as 3.14 (major.minor only, not 3.14.3)"
  - "Track data.xlsx in git per user decision — data must be in repo for Render to serve it"
  - "Do not gitignore data.xlsx or .planning/ — both must remain in repo"

patterns-established:
  - "WSGI pattern: server = app.server immediately after app creation, before any config"
  - "Procfile format: web: gunicorn <module>:<callable> --workers N --timeout N"
  - "Python version pin: major.minor only in .python-version"

requirements-completed: [DEPLOY-01, DEPLOY-02, DEPLOY-03, DEPLOY-04]

# Metrics
duration: 5min
completed: 2026-02-23
---

# Phase 6 Plan 01: Render Deployment Prep Summary

**Dash app made Render-deployable via gunicorn WSGI entry point, Procfile, pinned Python 3.14, and data.xlsx committed to git**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-02-23T20:54:02Z
- **Completed:** 2026-02-23T20:59:00Z
- **Tasks:** 2
- **Files modified:** 5 (app.py, requirements.txt, Procfile, .python-version, .gitignore) + 1 tracked (data.xlsx)

## Accomplishments
- Added `server = app.server` at module level in app.py — gunicorn WSGI entry point established
- Added gunicorn==25.1.0 to requirements.txt in correct alphabetical position
- Created Procfile with `web: gunicorn app:server --workers 2 --timeout 120`
- Created .python-version pinning 3.14 for Render runtime selection
- Created .gitignore excluding Python cache, Excel lock files, and IDE files while keeping data.xlsx and .planning/
- Confirmed data.xlsx is now git-tracked and pathlib path resolves correctly
- Verified full import chain: `from app import server, DATA` loads Flask server + parsed DataFrame successfully

## Task Commits

Each task was committed atomically:

1. **Task 1: Add WSGI entry point, Procfile, gunicorn dep, and deployment config files** - `49124c6` (feat)
2. **Task 2: Verify data path and test gunicorn starts locally** - `42c8691` (feat)

**Plan metadata:** *(pending docs commit)*

## Files Created/Modified
- `app.py` - Added `server = app.server` at module level after app.title, before suppress_callback_exceptions
- `requirements.txt` - Added gunicorn==25.1.0 between dash-bootstrap-components and openpyxl
- `Procfile` - New file: `web: gunicorn app:server --workers 2 --timeout 120`
- `.python-version` - New file: `3.14`
- `.gitignore` - New file: excludes __pycache__, ~$*, .venv, .DS_Store, IDE dirs
- `data.xlsx` - Added to git tracking (was previously untracked)

## Decisions Made
- Placed `server = app.server` immediately after `app.title` and before `app.config.suppress_callback_exceptions` — keeps WSGI entry point close to app creation, clearly visible at module level
- Used `--workers 2` for Render free tier (512MB RAM) — safe for a lightweight Dash app
- Used `--timeout 120` as conservative safety for initial Excel data load on cold start
- Tracked data.xlsx in git (not using external storage) — simplest approach for a static dataset used in this educational project

## Deviations from Plan

### Auto-fixed Issues

None - plan executed exactly as written.

Note: data.xlsx was untracked (expected — the plan included a step to check and add it if missing). This was handled per plan instructions in Task 2, not a deviation.

## Issues Encountered

None. All verifications passed on first attempt.

- `python -c "import app; print(hasattr(app, 'server'))"` returned `True`
- `grep "gunicorn" requirements.txt` showed `gunicorn==25.1.0`
- `cat Procfile` showed `web: gunicorn app:server --workers 2 --timeout 120`
- `cat .python-version` showed `3.14`
- `git ls-files data.xlsx` showed `data.xlsx`
- `grep "__pycache__" .gitignore` and `grep '~\$\*' .gitignore` both matched

## User Setup Required

None for this plan — all changes are local file modifications. The next plan (06-02) will require manual GitHub push and Render service creation.

## Next Phase Readiness

- All deployment-ready files are in place and committed
- Repo is ready to push to GitHub
- Once pushed, Render can be connected via dashboard
- Plan 06-02 covers: GitHub push, Render service creation, environment verification

---
*Phase: 06-render-deployment*
*Completed: 2026-02-23*
