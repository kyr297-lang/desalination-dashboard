# Phase 8: Parameter Sliders - Context

**Gathered:** 2026-02-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Add two interactive sliders — TDS (salinity) and depth — that feed into the power breakdown chart and all 4 comparison charts via linear interpolation against the Part 2 lookup tables. Students drag sliders and see chart values update live. Creating the lookup tables (Phase 7), changing the power chart from pie to bar (Phase 11), and system page styling (Phase 9) are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Slider placement
- Add a second row to the existing `chart-controls` card in `src/layout/charts.py`
- TDS slider on the left column, depth slider on the right column — mirrors the time-horizon / battery layout above it
- Tab visibility (all tabs vs. specific tabs): Claude's discretion — pick the most consistent approach given how the chart section is shared across Mechanical, Electrical, and Hybrid tabs

### Scope of impact
- Moving either slider triggers an update to all 4 charts (cost, land, turbine count, power breakdown)
- TDS and depth add additional energy demand on top of the base system energy; the turbine count chart is the most directly affected alongside the power breakdown chart

### Labels and feedback
- Match the existing time-horizon slider style: always-visible tooltip showing the current numeric value, plus a dynamic `html.Span` below showing the value with its unit (e.g., "950 PPM" / "950 m")
- TDS unit: PPM; depth unit: m

### Update responsiveness
- Continuous drag updates (`updatemode="drag"`) — Part 2 lookup tables are 20 rows each; interpolation is computationally trivial so there is no need to wait for mouseup

### Default values
- TDS slider defaults to 950 PPM (midpoint of 0–1900 range)
- Depth slider defaults to 950 m (midpoint of 0–1900 range)
- Students land on a "middle scenario" and can explore in both directions

### Claude's Discretion
- Whether to show/hide sliders on specific tabs (all tabs vs. Mechanical + Electrical only)
- Exact label wording and spacing
- Whether to add a small descriptive subtitle under each slider label (consistent with existing "— Adjust the projection period" style)

</decisions>

<specifics>
## Specific Ideas

No specific references — open to standard approaches consistent with the existing `chart-controls` card pattern.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dcc.Slider` component: already used as `slider-time-horizon` and `slider-battery` in `src/layout/charts.py:393` and `src/layout/charts.py:421` — same component, same props pattern
- `chart-controls` card: the `dbc.Card` at `src/layout/charts.py:380` — extend by adding a `dbc.Row` for the new sliders
- `html.Span` live labels: `label-years` and `label-battery-ratio` patterns at `src/layout/charts.py:403–435` — replicate for TDS and depth

### Established Patterns
- Slider callback: `update_charts()` at `src/layout/charts.py:557` — add `Input("slider-tds", "value")` and `Input("slider-depth", "value")` as new Inputs; callback already handles all 4 charts
- Interpolation: lookup tables are `pd.DataFrame` objects (`tds_lookup`, `depth_lookup`) accessible via `_data`; use `numpy.interp` or `pandas` interpolation against the 20-row table
- `updatemode="mouseup"` is the existing default — for these sliders, use `updatemode="drag"` instead

### Integration Points
- `src/data/processing.py` — `compute_chart_data()` function will need `tds_ppm` and `depth_m` parameters added; it currently receives `battery_fraction` and `years` from the callback
- `src/data/loader.py` — `tds_lookup` and `depth_lookup` DataFrames already returned from `load_data()` and accessible via `_data` in `charts.py`
- `app.py` — data is loaded once at startup and passed through; no changes needed there

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 08-parameter-sliders*
*Context gathered: 2026-02-28*
