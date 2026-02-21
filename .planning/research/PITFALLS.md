# Pitfalls Research

**Domain:** Interactive engineering comparison dashboard (Dash/Plotly, Python, Excel data source)
**Researched:** 2026-02-20
**Confidence:** HIGH (critical pitfalls verified against official Dash documentation and GitHub issues; UX pitfalls MEDIUM from multiple community sources)

---

## Critical Pitfalls

### Pitfall 1: Modifying Global Variables in Callbacks

**What goes wrong:**
Developers store mutable application state — such as the currently selected hybrid equipment, the battery/tank slider position, or loaded DataFrame — in Python module-level variables and modify them inside callback functions. The app appears to work during solo development but silently corrupts state when any second user connects, or when the app is later deployed with multiple workers on Render/Railway.

**Why it happens:**
Dash runs on Flask under the hood. When you write `df = pd.read_excel(...)` at module level and then mutate `df` inside a callback, it feels exactly like normal Python programming. The multi-user/multi-worker implications are invisible during local `python app.py` testing with a single developer.

**How to avoid:**
- Load `data.xlsx` at module startup into an **immutable** module-level dict or DataFrame. Never mutate it after initial load.
- Store user-specific state (selected hybrid slots, slider position, active tab) only in `dcc.Store` components with `storage_type='session'`.
- Never write to module-level variables inside any `@app.callback` function body.
- The official Dash rule: "Dash Callbacks must never modify variables outside of their scope."

**Warning signs:**
- Any line inside a callback that assigns to a variable defined outside that callback (e.g., `global df` or bare `state_dict[key] = value`).
- Tests pass consistently alone but produce wrong results when two browser tabs are open simultaneously.
- Slider state "bleeds" between page refreshes in ways that seem random.

**Phase to address:** Foundation / Data Layer — establish the module-level immutable data loading pattern before any callbacks are written.

---

### Pitfall 2: One Callback Output Can Only Have One Owning Callback (Pre-Dash 2.9)

**What goes wrong:**
When building the hybrid slot system (5 functional slots driving multiple downstream outputs) and the comparison graphs, developers naturally write separate callbacks for separate concerns. If two callbacks both attempt to update the same component property — e.g., a summary scorecard `div` updated from both the hybrid slot completion callback AND the system selector callback — Dash raises a `DuplicateCallbackOutput` error and the app breaks at startup.

**Why it happens:**
Dash's reactive model enforces that each `(component_id, property)` pair has exactly one owning callback. Developers coming from other frameworks expect event-driven multiple-handler patterns that Dash does not support by default.

**How to avoid:**
- In Dash 2.9+, use `Output(..., allow_duplicate=True)` where truly needed, but be aware update ordering is not guaranteed when two callbacks fire simultaneously.
- Preferred approach: consolidate related outputs into one callback that uses `dash.callback_context.triggered_id` to branch on which input fired.
- Design callback ownership as a graph during architecture phase — each output gets exactly one callback.

**Warning signs:**
- `dash.exceptions.DuplicateCallbackOutput` error on app startup.
- The temptation to write a new callback for "just this one case" when an existing callback already owns the output.

**Phase to address:** Core Interactivity — design callback ownership map before implementing the hybrid builder and comparison views.

---

### Pitfall 3: Loading Excel File Inside Callbacks Instead of at Startup

**What goes wrong:**
`pd.read_excel('data.xlsx', engine='openpyxl')` is placed inside a callback rather than at module startup. Every user interaction — clicking a system selector, moving the battery slider — reads the Excel file from disk again. On Render's free tier with limited I/O, this causes noticeable latency (200-800ms per interaction) and may hit file-read limits under concurrent use.

**Why it happens:**
Developers prototype the data loading in the callback where data is first needed, then never move it out. The penalty is invisible locally because the file is small and on an SSD.

**How to avoid:**
- Call `pd.read_excel(...)` exactly **once** at module startup, outside all callbacks.
- Store the resulting DataFrames in module-level constants (named in UPPER_CASE to signal immutability).
- Use `pathlib.Path(__file__).parent / 'data.xlsx'` — not a relative path string — to guarantee the file resolves correctly both locally and in deployment environments.
- Set `engine='openpyxl'` explicitly; never rely on the default engine, which may resolve to `xlrd` (which no longer supports `.xlsx` files and will raise `XLRDError`).

**Warning signs:**
- `pd.read_excel(...)` call found inside any function decorated with `@app.callback`.
- The path string `'data.xlsx'` used without `pathlib` — will fail when working directory differs from script directory (common in deployment).
- `xlrd.biffh.XLRDError: Excel xlsx file; not supported` — means xlrd was picked as engine instead of openpyxl.

**Phase to address:** Foundation / Data Layer — the very first task before any layout or callbacks.

---

### Pitfall 4: Hybrid Slot State Stored in DOM Instead of dcc.Store

**What goes wrong:**
The hybrid "build your own" system requires tracking which equipment item was assigned to each of the 5 functional slots (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal). Developers sometimes use component visibility (`display: none/block`) or dynamically injected `data-*` attributes to track this state rather than a proper `dcc.Store`. This makes the state invisible to callbacks, breaks the completion gate logic, and causes the comparison graphs to render stale or incorrect data.

**Why it happens:**
Building drag-and-drop or slot-filling UI in Dash feels like it should be HTML/DOM-first. But Dash callbacks cannot read DOM state directly — they can only read component properties that are declared as `Input` or `State`.

**How to avoid:**
- Maintain hybrid slot assignments in a single `dcc.Store(id='hybrid-slots', storage_type='session', data={})` component.
- Every slot selection updates this Store via a callback.
- The completion gate callback reads from the Store to check if all 5 slots are filled before enabling the comparison view.
- Never attempt to read HTML element state that isn't wired into the Dash component tree.

**Warning signs:**
- Callbacks that attempt to infer state from layout properties like `children`, `style`, or `className` instead of a dedicated Store.
- The completion gate intermittently allows access before all slots are filled.

**Phase to address:** Core Interactivity / Hybrid Builder — design the Store schema before building slot UI.

---

### Pitfall 5: suppress_callback_exceptions=True Used as a Crutch

**What goes wrong:**
When Dash reports `dash.exceptions.CallbackException` because a callback references a component ID not present in the initial layout, developers add `app.config.suppress_callback_exceptions = True` globally and move on. This silences the error but masks real architectural problems — components that are supposed to be present aren't, or callback dependencies are miswired. Actual runtime errors then surface as blank panels with no traceback.

**Why it happens:**
The error message is cryptic and the suppression flag is the first result in community searches. It solves the immediate symptom without diagnosing the cause.

**How to avoid:**
- Use `suppress_callback_exceptions=True` **only** when components are genuinely dynamically generated by other callbacks and cannot be in the initial layout (a legitimate pattern).
- For this project, if a component is conditionally shown (e.g., equipment detail panel), initialize it in the layout with `style={'display': 'none'}` rather than generating it dynamically — this keeps the ID visible at startup without suppression.
- When suppression IS needed, add a code comment explaining exactly which dynamic component requires it.

**Warning signs:**
- `suppress_callback_exceptions=True` set in `app = Dash(...)` at initialization without a comment explaining why.
- Panels that show nothing with no error in the terminal — the error is being swallowed.

**Phase to address:** Foundation / App Initialization — set the policy before any callbacks are written.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Relative path `'data.xlsx'` instead of `pathlib` | Slightly shorter code | Breaks on deployment where working directory differs from script | Never — always use `pathlib` |
| Hardcoding system comparison values instead of reading from DataFrame | Faster to prototype | Any data change in Excel breaks the app silently | Never for data-sourced values |
| Single monolithic callback handling all graph updates | Avoids callback ownership planning | Undebuggable 200-line function, impossible to test incrementally | Never — split by concern |
| Storing computed results in module globals | Avoids dcc.Store serialization complexity | Breaks with multiple workers or users | Never inside callbacks |
| Omitting `engine='openpyxl'` from `pd.read_excel` | Fewer characters | `XLRDError` on .xlsx files in environments with older pandas defaults | Never — always specify engine |
| Using `Dash(suppress_callback_exceptions=True)` globally from the start | Silences startup errors | Masks real wiring bugs, debugging becomes very hard | Only with explicit comment explaining the legitimate dynamic component |

---

## Integration Gotchas

Common mistakes when connecting to the Excel data source and deployment targets.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| `data.xlsx` loading | `pd.read_excel('data.xlsx')` — path relative to process CWD, not script location | `pd.read_excel(Path(__file__).parent / 'data.xlsx', engine='openpyxl', sheet_name=None)` |
| `data.xlsx` multi-sheet | Reading sheets individually in separate `pd.read_excel` calls | Pass `sheet_name=None` to get all sheets in one I/O operation, then index by name |
| Excel merged cells | pandas silently drops data from merged cells (only first cell gets value) | Pre-process merged cells in openpyxl before converting to DataFrame, or restructure the Excel file to avoid merges |
| Render deployment | Missing `server = app.server` in `app.py` | Add `server = app.server` and reference it in `Procfile: web: gunicorn app:server` |
| Render deployment | Missing `gunicorn` in `requirements.txt` | Add `gunicorn` explicitly; Render will not install it automatically |
| Render deployment | `data.xlsx` not committed to repo | Excel file must be in repository root or Render build will fail to find it |
| Battery/tank slider | Continuous `dcc.Slider` with `updatemode='drag'` fires callbacks on every pixel move | Use `updatemode='mouseup'` to fire only on release, preventing callback storm |

---

## Performance Traps

Patterns that work locally but degrade in deployment.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Reading `data.xlsx` inside callbacks | 200-800ms lag per interaction, noticeable on free-tier hosting | Load once at module startup | From the first deployment |
| Returning full Plotly `figure` dict when only one trace changed | Unnecessary full re-render, flickering on slow connections | Use `Patch()` for incremental updates (Dash 2.9+) | At any scale — wastes bandwidth |
| No `prevent_initial_call` on callbacks that fire expensively at startup | App takes 3-5 seconds to become interactive as all callbacks fire | Add `prevent_initial_call=True` to callbacks where no default selection exists | On every page load |
| Too many `dcc.Graph` components rendering simultaneously | Slow initial render, layout jitter | Use tab-based or conditional display to render only visible graphs | With 4+ graphs on one page |
| Pattern-matching callbacks with large dynamic component sets | Callback gathers all matching components before firing — slow with 50+ elements | This project has only 5 hybrid slots — safe; avoid scaling this pattern beyond ~20 elements | Above ~50 dynamic components |

---

## UX Pitfalls

Common user experience mistakes specific to engineering comparison dashboards for students.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Using inconsistent colors across graphs for the same system | Students cannot track "mechanical = blue" across charts — must re-read legends every time | Assign a fixed color per system (mechanical, electrical, hybrid) and apply it identically across every chart and scorecard element |
| Red/green-only ranking without colorblind-safe alternatives | ~8% of male students cannot distinguish red from green; ranking system becomes inaccessible | Use red/yellow/green AND add text labels or patterns — never rely on color alone to convey ranking |
| Showing all graphs visible simultaneously on one long scroll | Students lose context — the graph they're analyzing is far from the controls that affect it | Group related controls and their graphs together; use tabs or sections with the control panel adjacent to its chart |
| No indication of what happens when hybrid slots are incomplete | Students click "compare" or see empty graphs with no guidance | Implement the completion gate visually: show which slots are empty, disable comparison outputs with a clear label like "Fill all 5 slots to compare" |
| Overloading the scorecard with too many metrics | Students cannot extract the key insight; everything looks equally important | Scorecard should show exactly 3 dimensions (cost, land, efficiency) with the red/yellow/green ranking — resist adding more |
| Graph Y-axis not starting at 0 for bar/cost charts | Makes differences appear much larger than they are — misleads students about magnitude | Always start cost and land area axes at 0 for fair visual comparison |
| Hover tooltips with raw unformatted numbers | Students see `1234567.8923` instead of `$1.2M` | Format all Plotly hovertemplate values: currency with `$` and `,` separators, land in `m²` with commas, energy in `kW` |
| Time horizon slider with no default meaningful range | Students leave at default and miss long-term economics insight | Default to 20 years (reasonable infrastructure lifecycle); label endpoints clearly (e.g., "1 yr" to "50 yr") |

---

## "Looks Done But Isn't" Checklist

Things that appear complete during development but are missing critical pieces.

- [ ] **Hybrid completion gate:** Confirm the gate actually PREVENTS comparison graph rendering (not just shows a warning) when fewer than 5 slots are filled — verify callbacks return `no_update` or `dash.no_update`, not empty figures.
- [ ] **Battery/tank tradeoff slider:** Confirm slider values map correctly to the 11-row tradeoff table in the Electrical sheet (0%, 10%, 20% ... 100%) — off-by-one indexing is a common bug.
- [ ] **Cost over time graph:** Confirm the time horizon calculation correctly aggregates all cost components (capital + operational per year × lifespan) — spot-check against manual calculation for one system.
- [ ] **Data path on deployment:** Test that `data.xlsx` loads successfully when the app runs from a different working directory (simulate with `python -c "import app"` from a parent directory).
- [ ] **Excel engine:** Confirm `openpyxl` is in `requirements.txt` — `pd.read_excel` will silently fall back to xlrd and fail on .xlsx files in some environments.
- [ ] **Gunicorn in requirements.txt:** Deployment to Render/Railway fails silently without it — verify before first deploy.
- [ ] **`server = app.server` present:** Required for Procfile to expose the Flask server; often forgotten when the developer only tests with `python app.py`.
- [ ] **Color consistency:** Open all graphs simultaneously and verify that "mechanical" is the same color in every graph — it is easy for Plotly to auto-assign different colors per chart.
- [ ] **Scorecard ranking correctness:** For a system with the lowest cost, confirm it shows green (not red); ranking direction bugs are common (ascending vs descending confusion).
- [ ] **NaN handling from Excel:** Confirm that missing cells in `data.xlsx` (which pandas reads as `NaN`) do not silently propagate into graph data, producing invisible traces or broken calculations.

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Global variable mutation found mid-project | MEDIUM | Identify all globals mutated in callbacks; wrap in `dcc.Store`; refactor callbacks to read from Store `State`; test with two browser tabs |
| `DuplicateCallbackOutput` errors at startup | LOW | Map all callback outputs; identify conflicts; consolidate conflicting callbacks using `callback_context.triggered_id` branching |
| `XLRDError` in production | LOW | Add `engine='openpyxl'` to the `pd.read_excel` call; add `openpyxl` to `requirements.txt`; redeploy |
| Deployment fails — `server = app.server` missing | LOW | Add `server = app.server` after app initialization; verify Procfile reads `gunicorn app:server`; redeploy |
| Hybrid slot state lost on page refresh | MEDIUM | Migrate slot state from `storage_type='memory'` to `storage_type='session'` in the `dcc.Store`; verify callbacks read from `State` not `Input` where appropriate |
| Cost over time graph showing wrong values | HIGH | Audit the calculation formula in the callback; compare cell-by-cell against the Excel source data; add unit tests for the calculation function before it is used in the callback |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Global variable mutation in callbacks | Phase 1 (Foundation / Data Layer) | Code review: grep for any assignment to module-level names inside callback functions |
| Duplicate callback output conflicts | Phase 2 (Core Interactivity) | App starts without `DuplicateCallbackOutput` errors; callback ownership diagram created before coding |
| Excel loaded inside callbacks | Phase 1 (Foundation / Data Layer) | `pd.read_excel` appears exactly once, outside all callbacks; confirmed with grep |
| Hybrid slot state in DOM instead of Store | Phase 3 (Hybrid Builder) | All 5 slots and completion status readable as Store values; completion gate tested by partially filling slots |
| suppress_callback_exceptions misuse | Phase 1 (Foundation / App Init) | Flag only set if a comment explains the specific dynamic component requiring it |
| Missing `openpyxl` engine specification | Phase 1 (Foundation / Data Layer) | `engine='openpyxl'` explicit in `read_excel` call; `openpyxl` in requirements.txt |
| Deployment missing `server` and `gunicorn` | Phase 5 (Deployment) | Smoke test deployment checklist before first Render push |
| Color inconsistency across graphs | Phase 4 (Visualization) | Define `SYSTEM_COLORS = {'mechanical': ..., 'electrical': ..., 'hybrid': ...}` constant used by all graph callbacks |
| Completion gate not blocking rendering | Phase 3 (Hybrid Builder) | Integration test: with 4/5 slots filled, comparison graphs return `no_update` |
| Battery/tank slider index mismatch | Phase 2 or 3 (Electrical System) | Unit test: slider at 0% returns row 0 data, slider at 100% returns row 10 data, slider at 50% returns row 5 data |

---

## Sources

- [Dash Official Docs — Sharing Data Between Callbacks](https://dash.plotly.com/sharing-data-between-callbacks) (HIGH confidence — official documentation)
- [Dash Official Docs — Performance](https://dash.plotly.com/performance) (HIGH confidence — official documentation)
- [Dash Official Docs — Advanced Callbacks](https://dash.plotly.com/advanced-callbacks) (HIGH confidence — official documentation)
- [Dash Official Docs — Duplicate Callback Outputs](https://dash.plotly.com/duplicate-callback-outputs) (HIGH confidence — official documentation)
- [Dash Official Docs — Partial Property Updates](https://dash.plotly.com/partial-properties) (HIGH confidence — official documentation)
- [Dash GitHub Issues — Pattern-matching callback performance with many elements](https://github.com/plotly/dash/issues/3008) (HIGH confidence — official issue tracker)
- [Dash GitHub Issues — Global Variables](https://github.com/plotly/dash/issues/121) (HIGH confidence — official issue tracker)
- [Plotly Community Forum — Hot Reload with Excel File](https://community.plotly.com/t/hot-reload-watch-excel-file-for-changes/30604) (MEDIUM confidence — community discussion)
- [Render Community — Deploying Dash on Render](https://community.render.com/t/deploying-dash-by-plotly-app-on-render/3475) (MEDIUM confidence — community discussion, cross-referenced with official deployment docs)
- [xlrd GitHub — xlrd now supports .xls only](https://github.com/python-excel/xlrd) (HIGH confidence — official repository)
- [pandas docs — read_excel engine parameter](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) (HIGH confidence — official documentation)
- [DeepWiki — Dash Sample Apps Best Practices](https://deepwiki.com/plotly/dash-sample-apps/9-best-practices-and-common-patterns) (MEDIUM confidence — aggregated from official sample apps)
- [dash-resources.com — Callbacks Best Practices](https://dash-resources.com/dash-callbacks-best-practices-with-examples/) (MEDIUM confidence — community-verified patterns)

---
*Pitfalls research for: Wind-Powered Desalination Engineering Dashboard (Dash/Plotly)*
*Researched: 2026-02-20*
