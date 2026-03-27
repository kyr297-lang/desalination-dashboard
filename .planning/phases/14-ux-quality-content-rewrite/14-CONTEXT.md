# Phase 14: UX Quality & Content Rewrite - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix slider behavior (mouseup updatemode, no direct-input boxes, battery endpoint labels), add dcc.Loading spinners around chart outputs, add a session-scoped first-visit guidance banner above the control panel, fully rewrite the landing page intro, and update all mechanical content in config.py to reflect the hydraulic drive architecture (HPU, manifold, hydraulic motors, VTP, plunger pump).

</domain>

<decisions>
## Implementation Decisions

### Slider Fixes (UX-02, UX-03, UX-04)
- **D-01:** Change `slider-tds` `updatemode` from `"drag"` → `"mouseup"` — prevents per-pixel chart recalculations during drag
- **D-02:** Change `slider-depth` `updatemode` from `"drag"` → `"mouseup"` — same reason; `slider-time-horizon` and `slider-battery` already have `"mouseup"` (no change needed)
- **D-03:** Add `allow_direct_input=False` to all four sliders (`slider-time-horizon`, `slider-battery`, `slider-tds`, `slider-depth`) — suppresses Dash 4.0 text input boxes
- **D-04:** Battery slider (`slider-battery`) marks: `{0: "100% Tank", 0.5: "50/50", 1: "100% Battery"}` — replace current empty `marks={}`. Tooltip: `{"always_visible": True, "placement": "bottom"}` — replace current `{"always_visible": False}`

### Loading Spinners (UX-01)
- **D-05:** One `dcc.Loading` wrapper around the entire chart output area (all four charts together) — not individual per-chart wrappers. Simpler, consistent with the academic clean aesthetic.
- **D-06:** Spinner type: default circle (`type="default"`)

### First-Visit Guidance Banner (UX-05)
- **D-07:** Placement: immediately above the control panel card (the card containing the sliders), as a separate component inserted before it in the layout
- **D-08:** Trigger for dismiss: first slider interaction — any drag or click on any of the four sliders fires a callback that sets a dcc.Store flag to hide the banner
- **D-09:** Persistence: session-only via `dcc.Store` — banner reappears on fresh page reload; no localStorage required
- **D-10:** Banner text (exact): "Use the sliders below to adjust salinity, depth, and storage mix — charts update on mouse release. Drag any slider to dismiss this tip."
- **D-11:** Use `dbc.Alert` with `color="info"` and `is_open` controlled by the dcc.Store flag. `dismissable=False` — closing is handled by slider interaction, not an X button. Compact/small styling consistent with academic tone.

### Landing Page Rewrite (CONTENT-01)
- **D-12:** Full rewrite of intro card body — replace the current 2-sentence paragraph with a complete rewrite
- **D-13:** Card title: keep "About This Project" unchanged
- **D-14:** Content focus: explain what wind-powered desalination is, describe the senior design context (10,000-person municipality scenario), describe what the three systems represent technically (mechanical = hydraulic drive, electrical = battery/tank storage, hybrid = combined preset), and state what the project is trying to accomplish — no data source mentions
- **D-15:** Hybrid system card description: remove "build a custom system" and "select one piece of equipment for each process stage" (stale after Phase 12 builder removal) — update to reflect that hybrid is a fixed preset combining hydraulic mechanical and electrical approaches
- **D-16:** Mechanical system card description: remove "wind-driven pumps" — update to reflect hydraulic drive architecture (HPU driving VTP and plunger pump via manifold and hydraulic motors)

### Mechanical Content Update (CONTENT-02)
- **D-17:** Update `PROCESS_STAGES["mechanical"]` in `src/config.py` to match the Phase 12 BOM exactly — researcher reads the Mechanical section of `data.xlsx` Part 1 to derive the correct component names and stage assignments (names must match column B strings exactly for the equipment table to render)
- **D-18:** Write new `EQUIPMENT_DESCRIPTIONS` entries for all new hydraulic components (HPU, gearbox, manifold, hydraulic motors, VTP, plunger pump) — 1-2 sentences per component, same technical depth and student-accessible tone as existing entries in `config.py`
- **D-19:** Stale mechanical descriptions (old aeromotor turbine, wind turbine rotor lock, gear and booster pump) may be removed from `EQUIPMENT_DESCRIPTIONS` if they are no longer referenced by `PROCESS_STAGES` — planner should verify no other code references them before deleting

### Claude's Discretion
- Exact `dcc.Store` ID name for the banner dismissed-state flag
- Whether banner store is added to `shell.py` alongside other stores, or initialized in the charts/controls layout
- CSS styling details for the banner (size, padding) within the `dbc.Alert` component
- Exact paragraph structure and sentence order in the landing page rewrite (user chose "project purpose + technical context" direction; Claude writes to fit the card's existing small-text style)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Slider & Chart Code
- `src/layout/charts.py` — All four slider definitions (lines ~403–511) and chart output IDs; the chart output div that needs the dcc.Loading wrapper; callback inputs that reference slider IDs

### Landing Page
- `src/layout/overview.py` — Intro card body and `_SYSTEM_CARDS` descriptions for all three systems; full rewrite targets this file

### Content & Configuration
- `src/config.py` — `PROCESS_STAGES["mechanical"]` (old component names to replace) and `EQUIPMENT_DESCRIPTIONS` (stale mechanical entries to update/replace with hydraulic component descriptions)
- `data.xlsx` — Mechanical section of Part 1: researcher must read the exact column B component names and their row groupings to correctly map to PROCESS_STAGES stage buckets

### Shell / Store Layer
- `src/layout/shell.py` — Existing `dcc.Store` definitions; new banner store must be added here alongside `sidebar-collapsed` and `active-system` stores

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dcc.Slider` pattern: all four sliders in `charts.py` follow the same structure — `id`, `min`, `max`, `step`, `value`, `marks`, `tooltip`, `updatemode`. `allow_direct_input` just needs to be added as a new kwarg.
- `dbc.Alert` with `is_open` prop: standard Dash Bootstrap pattern for controlled show/hide; pairs well with a dcc.Store callback trigger
- `dcc.Store` already in use in `shell.py` for `sidebar-collapsed` and `active-system` — banner state store fits this pattern

### Established Patterns
- Data flow: `dcc.Store` → callback `Input` → `Output("component", "style")` or `is_open` — banner dismiss follows this pattern
- Card pattern: `dbc.Card(dbc.CardBody(...), className="shadow-sm mb-3")` — banner should NOT use this pattern; `dbc.Alert` is more appropriate
- `EQUIPMENT_DESCRIPTIONS` keys must match column B strings from `data.xlsx` exactly (including trailing spaces if present) — critical for the equipment table lookup

### Integration Points
- The banner needs a callback with `Input` on each of the four slider IDs (any of `"value"` property changing fires it) — same IDs already used by the main chart callback
- `dcc.Loading` wraps the chart *output* div, not the callback function — researcher should identify the output `html.Div` ID that holds all chart figures
- Overview layout is a pure layout function (`create_overview_layout()` in `overview.py`) — no callbacks to modify; only the component tree and text strings change

### Known Constraints
- `suppress_callback_exceptions=True` in `app.py` — new store IDs must be initialized in `shell.py` layout before any callback references them
- Academic tone throughout — banner and landing copy should be plain, informative, not marketing-style
- Desktop-first — no mobile/responsive considerations for banner placement

</code_context>

<specifics>
## Specific User Inputs

- Banner text (exact): "Use the sliders below to adjust salinity, depth, and storage mix — charts update on mouse release. Drag any slider to dismiss this tip."
- Banner dismiss trigger: explicitly worded in the banner itself; users know what to do
- Landing page focus: project purpose + senior design context + 10,000-person municipality scenario + three-system technical overview; NO data source mentions
- Mechanical PROCESS_STAGES: derive from data.xlsx Part 1 Mechanical rows — do not guess component names; they must match exactly
- Equipment descriptions: 1-2 sentences each, same depth as existing entries (see `config.py` ~line 126 for style reference)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 14-ux-quality-content-rewrite*
*Context gathered: 2026-03-27*
