# Phase 6: Render Deployment - Research

**Researched:** 2026-02-23
**Domain:** Python WSGI deployment on Render free tier (Dash + gunicorn)
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**URL & access**
- Render subdomain: desalination-dashboard.onrender.com (or closest available)
- Fully public — no authentication or password protection
- Direct to dashboard — no landing page, URL loads straight into the app
- No custom domain needed

**Cold start handling**
- Accept Render free tier sleep behavior (~30-60s cold start after 15min inactivity)
- No keep-alive pings or loading indicators needed
- Rely on Render's built-in logs for monitoring — no custom health endpoint

**Data bundling**
- Bundle data.xlsx directly in the repo — committed to version control
- No sensitive data in the file — safe for public repo
- Data will be updated frequently — push updated data.xlsx to GitHub, Render auto-redeploys
- Use pathlib-based paths so data.xlsx loads correctly in both local and deployed environments

**Deploy workflow**
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

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DEPLOY-01 | App is deployable to Render free tier with gunicorn and Procfile | Procfile pattern `web: gunicorn app:server`, gunicorn must be in requirements.txt; currently missing from both |
| DEPLOY-02 | App exposes `server = app.server` for WSGI compatibility | Line must be added to app.py after `app = dash.Dash(...)` — currently absent from app.py |
| DEPLOY-03 | `requirements.txt` includes all dependencies with pinned versions | Current requirements.txt has 4 packages but lacks gunicorn; needs manual addition of gunicorn==25.1.0 |
| DEPLOY-04 | App loads `data.xlsx` correctly in deployed environment (pathlib-based paths) | `src/config.py` already uses `Path(__file__).parent.parent / "data.xlsx"` — correct pattern; data.xlsx must be committed to repo |
</phase_requirements>

---

## Summary

Deploying this Dash app to Render free tier requires four concrete changes to the codebase plus one-time Render service configuration. The changes are surgical: add `server = app.server` to `app.py`, add `gunicorn==25.1.0` to `requirements.txt`, create a `Procfile`, create a `.gitignore`, and commit `data.xlsx`. No architectural changes are needed — the existing pathlib-based data path in `src/config.py` already resolves correctly on Render.

The most error-prone step is DEPLOY-02: Render's gunicorn cannot find the WSGI callable without `server = app.server` exposed as a module-level name. The app currently omits this line entirely, so gunicorn would fail on first deploy with a "Failed to find application object 'server' in 'app'" error. Everything else is additive (new files, one new package), not a modification of existing logic.

The data workflow the user wants — edit `data.xlsx` locally, `git push`, Render auto-redeploys — works cleanly because Render builds from the repo root and gunicorn imports `app.py`, which calls `load_data()` at module level. Since `data.xlsx` is in the repo root and `DATA_FILE = Path(__file__).parent.parent / "data.xlsx"` resolves relative to `src/config.py` (two levels up = repo root), the path is correct in both local and deployed environments.

**Primary recommendation:** Make the four code/file changes, push to a public GitHub repo, create a Render Web Service pointing at that repo with build command `pip install -r requirements.txt` and start command `gunicorn app:server`.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| gunicorn | 25.1.0 | WSGI HTTP server for production | Industry standard for Python WSGI apps; required by Render; sync worker class is correct for a stateless, CPU-light Dash app |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Procfile | (text file) | Declares the process type and start command for Render | Required; Render reads this to know how to start the app |
| .python-version | (text file) | Pins Python version in the repo | Recommended; ensures Render uses the same Python version as local dev |
| .gitignore | (text file) | Excludes local artifacts from git | Required; prevents committing `__pycache__`, `.venv`, etc. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Procfile | Render dashboard start command only | Procfile is version-controlled; dashboard-only is not. Procfile is better practice. |
| Manual requirements.txt curation | `pip freeze > requirements.txt` | pip freeze bloats file with transitive deps and OS-specific packages. Manual curation with exact versions is cleaner for a project with only 5 direct deps. |
| `gunicorn app:server` | `gunicorn app:app` | Dash 4.x added WSGI compliance (PR #3131, merged June 2025) allowing `app:app`, but `app:server` is the battle-tested pattern; use `app:server` for maximum compatibility and clarity. |

**Installation (addition to existing requirements.txt):**
```bash
pip install gunicorn==25.1.0
# Then manually add to requirements.txt — do not re-run pip freeze
```

---

## Architecture Patterns

### Recommended Project Structure (additions only)

```
project-root/
├── app.py              # MODIFY: add server = app.server
├── Procfile            # CREATE: web: gunicorn app:server
├── .python-version     # CREATE: 3.14
├── .gitignore          # CREATE: standard Python gitignore
├── requirements.txt    # MODIFY: add gunicorn==25.1.0
├── data.xlsx           # ENSURE COMMITTED: must be in repo
└── src/
    └── config.py       # NO CHANGE NEEDED: pathlib path already correct
```

### Pattern 1: WSGI Exposure (DEPLOY-02)

**What:** Gunicorn needs a module-level name `server` in `app.py` that holds the WSGI callable (the underlying Flask app).
**When to use:** Always required for Render/gunicorn deployment.
**Placement:** Immediately after `app = dash.Dash(...)` creation, before any layout or callback registration.

```python
# Source: Plotly Dash deployment docs + render.com community confirmed
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
)
app.title = "Wind-Powered Desalination Dashboard"

# WSGI server entry point — required for gunicorn
server = app.server
```

The `server` variable must be a module-level name (not nested inside an if block) so gunicorn can import it with `app:server`.

### Pattern 2: Procfile

**What:** A plain text file named `Procfile` (no extension) in the repo root that tells Render how to start the app.
**Format:** `web: gunicorn app:server`

```
web: gunicorn app:server --workers 2 --timeout 120
```

Worker recommendation for Render free tier:
- Free tier has 512 MB RAM and a shared CPU
- `--workers 2` is safe; more workers risk OOM kills on free tier
- `--timeout 120` prevents gunicorn from killing workers during Dash's initial data load (data.xlsx parsing takes <1s, but 120s is a conservative safety margin)
- Sync worker class (default) is correct — this app is not I/O-bound per request

### Pattern 3: Pathlib Data Path (DEPLOY-04 — already implemented)

**What:** `DATA_FILE = Path(__file__).parent.parent / "data.xlsx"` in `src/config.py`
**Why it works on Render:** `__file__` is the absolute path to `config.py` on the Render filesystem. `.parent.parent` navigates up to the repo root. `data.xlsx` in the repo root is included in the git checkout, so the path resolves correctly.

```python
# src/config.py — current implementation (no change needed)
from pathlib import Path
DATA_FILE = Path(__file__).parent.parent / "data.xlsx"
```

This pattern is deployment-safe. Do NOT use `os.getcwd() / "data.xlsx"` — the working directory on Render is not guaranteed to be the repo root.

### Pattern 4: requirements.txt Manual Curation

**What:** Maintain requirements.txt with only direct dependencies, all pinned with `==`.
**Why:** `pip freeze` dumps all transitive dependencies (100+ packages for a Dash project) plus OS-specific packages that may not resolve on Render's Linux environment.

Current `requirements.txt`:
```
dash==4.0.0
dash-bootstrap-components==2.0.4
openpyxl==3.1.5
pandas==2.3.3
```

After this phase:
```
dash==4.0.0
dash-bootstrap-components==2.0.4
gunicorn==25.1.0
openpyxl==3.1.5
pandas==2.3.3
```

Note: The existing `requirements.txt` pins `pandas==2.3.3` but the previous STACK.md research cited `pandas==3.0.1`. Use the version currently installed (2.3.3) — do NOT upgrade pandas as part of this phase.

### Pattern 5: Render Service Configuration

**Build command:** `pip install -r requirements.txt`
**Start command:** `gunicorn app:server --workers 2 --timeout 120`
**Environment:** Python 3 (auto-detected)
**Plan:** Free
**Region:** Oregon (default) — adequate for a US academic project
**Branch:** `main`
**Auto-deploy:** Yes (default — triggers on every push to main)

### Anti-Patterns to Avoid

- **Nesting `server = app.server` inside `if __name__ == "__main__":`**: Gunicorn does not execute the `__main__` block. The server assignment must be at module level.
- **Using `app:app.server` as the gunicorn target**: The dotted attribute syntax (`app.server`) is not supported by gunicorn 20+. Use `server = app.server` + `app:server`.
- **Running `pip freeze > requirements.txt` on Windows and deploying to Render**: pip freeze on Windows includes `pywin32` and other Windows-only packages that will fail to install on Render's Linux environment.
- **Not committing `data.xlsx`**: Render's filesystem is ephemeral — files created after build are lost. Only files in the git checkout persist. `data.xlsx` must be in the repo.
- **Committing `__pycache__`, `.venv`, or `~$data.xlsx`**: The `~$data.xlsx` temp file (visible in the project root) must be gitignored; it is created by Excel when the file is open and will corrupt the deployed data load.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| WSGI serving | Custom Flask run loop | gunicorn | gunicorn handles concurrency, signal handling, worker recycling, graceful shutdown — all invisible complexity |
| Python version pinning | Nothing / rely on Render default | `.python-version` file | Render's default Python version changes over time; pin it to avoid surprise upgrades breaking the build |
| Process type declaration | Relying solely on Render dashboard config | `Procfile` | Procfile is version-controlled; config in the Render dashboard is not reproducible and can drift |

**Key insight:** For a Dash app this size, deployment is a configuration problem, not a code problem. The only code change needed is one line (`server = app.server`). Everything else is new files.

---

## Common Pitfalls

### Pitfall 1: Missing `server = app.server`
**What goes wrong:** Gunicorn exits immediately with: `Failed to find application object 'server' in 'app'`. The Render deploy log shows a build success but the service crashes on start.
**Why it happens:** Gunicorn imports the module and looks for a name `server` at module level. Dash does not auto-expose this.
**How to avoid:** Add `server = app.server` immediately after `app = dash.Dash(...)`.
**Warning signs:** Render logs show "Worker failed to boot" or "Failed to find application object".

### Pitfall 2: gunicorn Not in requirements.txt
**What goes wrong:** Render's build succeeds (`pip install -r requirements.txt` runs fine), but the start command `gunicorn app:server` fails with `command not found: gunicorn`.
**Why it happens:** Render does not pre-install gunicorn; it must be an explicit dependency.
**How to avoid:** Add `gunicorn==25.1.0` to `requirements.txt` before pushing.
**Warning signs:** "bash: gunicorn: command not found" in Render logs immediately after build.

### Pitfall 3: data.xlsx Not Committed
**What goes wrong:** App starts but immediately shows the error page ("data.xlsx not found at expected path").
**Why it happens:** Render's build installs packages but only checks out files that are in git. Untracked or gitignored files do not exist in the deployed environment.
**How to avoid:** `git add data.xlsx && git commit` before pushing to GitHub.
**Warning signs:** App loads but shows the error page with a FileNotFoundError; Render logs show "[ERROR] data.xlsx not found at expected path".

### Pitfall 4: `~$data.xlsx` Committed Accidentally
**What goes wrong:** The temp file Excel creates when `data.xlsx` is open gets committed, which may cause confusion and adds a binary blob that git LFS doesn't handle.
**Why it happens:** `git add .` or `git add data.xlsx` can accidentally pick up the lock file if Excel is open.
**How to avoid:** Add `~$*` to `.gitignore`.
**Warning signs:** `git status` shows `~$data.xlsx` as a new file.

### Pitfall 5: Cold Start Confusion
**What goes wrong:** User visits the URL, gets a blank page or timeout for 30-60 seconds, assumes deployment is broken.
**Why it happens:** Render free tier spins down after 15 minutes of inactivity. The first request after inactivity triggers a cold start.
**How to avoid:** This is expected behavior per the locked decisions — no action needed. Document in README that first visit may be slow.
**Warning signs:** Normal — not a sign of deployment failure.

### Pitfall 6: Port Binding (Render Requires PORT env var)
**What goes wrong:** App binds to a hardcoded port (e.g., 8050) and Render's load balancer cannot reach it.
**Why it happens:** Render assigns a dynamic port via the `PORT` environment variable and expects the app to bind to `0.0.0.0:$PORT`.
**How to avoid:** Gunicorn automatically uses `$PORT` when it is set. The Procfile `web: gunicorn app:server` works without specifying `--bind` because Render's gunicorn integration handles this. Do NOT hardcode `--bind 0.0.0.0:8050`.
**Warning signs:** App shows as deployed but URL returns "Service Unavailable" — gunicorn is listening on a different port than Render's load balancer.

### Pitfall 7: Python Version Mismatch
**What goes wrong:** Code works locally on Python 3.14.3 but Render deploys with a different version that has incompatible syntax or package behavior.
**Why it happens:** Render's default Python version depends on service creation date; as of 2026-02-11, default is 3.14.3 — but this can change.
**How to avoid:** Create a `.python-version` file containing `3.14` in the repo root to pin the major.minor version.
**Warning signs:** Build fails with syntax errors or import errors that don't reproduce locally.

---

## Code Examples

Verified patterns from official sources:

### DEPLOY-02: Adding server = app.server to app.py

The line goes immediately after `app = dash.Dash(...)` and before any other app configuration or layout assignment:

```python
# Source: Plotly Dash deployment docs (dash.plotly.com/deployment)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
)
app.title = "Wind-Powered Desalination Dashboard"

# WSGI entry point — exposes Flask server for gunicorn
# Must be module-level (NOT inside if __name__ == "__main__")
server = app.server

app.config.suppress_callback_exceptions = True
```

### DEPLOY-01: Procfile

```
web: gunicorn app:server --workers 2 --timeout 120
```

File must be named exactly `Procfile` (capital P, no extension), placed in the repo root.

### DEPLOY-03: Final requirements.txt

```
dash==4.0.0
dash-bootstrap-components==2.0.4
gunicorn==25.1.0
openpyxl==3.1.5
pandas==2.3.3
```

### .python-version

```
3.14
```

### .gitignore (minimal, project-appropriate)

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/

# Excel lock files
~$*

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Planning artifacts (optional — keep if desired)
# .planning/
```

### DEPLOY-04: Verifying the data path (already correct, no change needed)

```python
# src/config.py — resolves to repo root regardless of working directory
from pathlib import Path
DATA_FILE = Path(__file__).resolve().parent.parent / "data.xlsx"
```

Note: Adding `.resolve()` before `.parent.parent` is technically more robust (handles symlinks) but the existing `Path(__file__).parent.parent / "data.xlsx"` also works correctly on Render. Either form is acceptable.

### Render Service Setup (manual steps, not code)

1. Push repo to GitHub (public repository)
2. Log in to render.com → New + → Web Service
3. Connect GitHub repo
4. Configure:
   - **Name:** `desalination-dashboard`
   - **Environment:** Python 3
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server --workers 2 --timeout 120`
   - **Plan:** Free
5. Click "Create Web Service"
6. Wait ~3-5 minutes for initial build + deploy
7. URL: `https://desalination-dashboard.onrender.com` (or similar if name taken)

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `gunicorn app:app.server` | `server = app.server` then `gunicorn app:server` | gunicorn 20+ | Dotted attribute syntax no longer supported; must expose server as a top-level name |
| `pip freeze > requirements.txt` | Manual curation of direct deps only | Always best practice, increasingly recognized | Cleaner, more portable requirements file |
| Heroku (most Dash tutorials) | Render | Heroku removed free tier in 2022 | Render is now the standard free hosting target for Dash apps |
| `app.run_server()` | `app.run()` | Dash 2.0 | `run_server()` still works but `run()` is the current API |

**Deprecated/outdated:**
- Heroku free tier: Eliminated November 2022 — all tutorials referencing Heroku free tier are outdated
- `dash-core-components` as a separate package: Bundled into `dash` since v2.0
- `gunicorn app:app.server` syntax: Broken since gunicorn 20 — use `server = app.server` then `gunicorn app:server`

---

## Open Questions

1. **Exact Render URL availability**
   - What we know: The user wants `desalination-dashboard.onrender.com`
   - What's unclear: Whether that name is available at time of service creation
   - Recommendation: Attempt the exact name; if taken, Render will suggest alternatives or append a suffix. The plan should note this is a best-effort name.

2. **pandas version discrepancy**
   - What we know: `requirements.txt` pins `pandas==2.3.3` but STACK.md research cited `pandas==3.0.1`
   - What's unclear: Which version is actually installed in the local venv
   - Recommendation: Use whatever version is in the current `requirements.txt` (`pandas==2.3.3`). Do not upgrade pandas in this phase — that is a separate concern and could break existing data loading code.

3. **Dash 4.x WSGI compliance via `app:app`**
   - What we know: PR #3131 merged June 2025 added WSGI compliance to Dash, enabling `gunicorn app:app`
   - What's unclear: Whether `dash==4.0.0` (released Feb 2025) includes this change or if it landed after 4.0.0
   - Recommendation: Use the proven `server = app.server` + `gunicorn app:server` pattern. Do not rely on the new `app:app` feature until the version boundary is confirmed.

---

## Sources

### Primary (HIGH confidence)
- Render official docs `https://render.com/docs/free` — Free tier behavior: 15min sleep, 512MB RAM, 750 hrs/month, ephemeral filesystem confirmed
- Render official docs `https://render.com/docs/python-version` — Python version pinning via `PYTHON_VERSION` env var or `.python-version` file; default for services created 2026-02-11+ is 3.14.3
- Render official docs `https://render.com/docs/web-services` — Build/start command conventions, PORT env var (default 10000)
- open-resources.github.io Dash curriculum Chapter 5 — `gunicorn [filename]:server` pattern confirmed; `server = app.server` placement confirmed
- Project codebase `src/config.py` — `Path(__file__).parent.parent / "data.xlsx"` already in place; DEPLOY-04 is pre-satisfied
- Project codebase `app.py` — `server = app.server` is absent; DEPLOY-02 gap confirmed
- Project codebase `requirements.txt` — gunicorn absent; DEPLOY-01/03 gap confirmed

### Secondary (MEDIUM confidence)
- gunicorn PyPI page `https://pypi.org/project/gunicorn/` — gunicorn 25.1.0 confirmed as latest stable
- GitHub issue plotly/dash#3131 — WSGI compliance PR merged June 4, 2025; version where it landed not confirmed
- WebSearch: Render community forum on Dash deployment — Procfile + gunicorn pattern universally confirmed across multiple community posts

### Tertiary (LOW confidence)
- WebSearch: pip freeze vs manual curation best practices — Multiple sources agree on manual curation for small projects; no single authoritative source

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — gunicorn 25.1.0 on PyPI confirmed; Render free tier behavior from official docs
- Architecture: HIGH — pathlib path pattern verified against existing code; WSGI exposure from official Dash docs
- Pitfalls: HIGH for pitfalls 1-4 (directly confirmed against this codebase); MEDIUM for pitfalls 5-7 (from Render docs + community)

**Research date:** 2026-02-23
**Valid until:** 2026-09-23 (stable domain — Render free tier behavior and gunicorn patterns change slowly; re-verify if Render announces pricing changes)
