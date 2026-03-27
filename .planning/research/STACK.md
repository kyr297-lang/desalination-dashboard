# Technology Stack: v1.3 UI/UX Overhaul Additions

**Project:** Wind-Powered Desalination Dashboard
**Researched:** 2026-03-26
**Overall confidence:** HIGH -- all features use built-in Dash/DBC capabilities already in requirements.txt

## Executive Summary

No new packages are needed. Every feature in the v1.3 scope (static images, loading spinners, slider UX improvements) is handled by Dash 4.0.0 and dash-bootstrap-components 2.0.4 already pinned in `requirements.txt`. The research below documents the exact APIs to use, current slider patterns that need updating, and Dash 4.0 gotchas.

---

## 1. Serving Static PNG Images (System Layout Diagrams)

### How It Works

Dash automatically serves everything in the `assets/` folder at the `/assets/` URL path. The project already has `assets/custom.css` in place, so the static file server is active.

### What to Do

1. Move the three PNGs into `assets/`:
   - `Mechanical System Layout.png`
   - `Electrical System Layout.png`
   - `Hybrid System Layout.png`

2. Reference them with `html.Img`:
   ```python
   html.Img(
       src="/assets/Mechanical System Layout.png",
       style={"maxWidth": "100%", "height": "auto"},
       alt="Mechanical system layout diagram",
   )
   ```

### Key Details

| Detail | Value |
|--------|-------|
| Dash component | `html.Img` (from `dash import html`) |
| URL pattern | `/assets/<filename>` -- Dash serves automatically |
| Config needed | None -- `Dash(__name__)` uses `assets/` by default |
| Filename spaces | Spaces in filenames work but encode as `%20` in URLs; Dash handles this transparently |
| Confidence | HIGH -- tested pattern, official docs confirm |

### Gotcha: Filenames with Spaces

The PNGs have spaces in their names. This works fine with Dash's static server, but for cleanliness consider renaming to `mechanical-system-layout.png`, etc. Either approach works -- Dash URL-encodes automatically.

### Alternative: `app.get_asset_url()`

```python
html.Img(src=app.get_asset_url("Mechanical System Layout.png"))
```

This is the "official" helper but requires passing the `app` object. Since this project uses module-level layout builders (not app-scoped), the direct `/assets/` string is simpler and equally correct.

**Source:** [Dash External Resources docs](https://dash.plotly.com/external-resources)

---

## 2. Loading Spinners for Chart Updates

### Recommended Approach: `dcc.Loading`

Use `dcc.Loading` to wrap chart `dcc.Graph` components. The spinner displays automatically when a callback updates the wrapped component's children/figure.

### API

```python
from dash import dcc

dcc.Loading(
    id="loading-cost-chart",
    type="circle",                    # Options: default, graph, cube, circle, dot
    children=dcc.Graph(id="chart-cost", ...),
    delay_show=200,                   # ms before spinner appears (prevents flicker)
    delay_hide=0,                     # ms minimum display time
    overlay_style={
        "visibility": "visible",
        "filter": "blur(2px)",
        "opacity": 0.6,
    },
)
```

### Key Properties

| Property | Type | Purpose | Recommended Value |
|----------|------|---------|-------------------|
| `type` | string | Spinner visual style | `"circle"` -- clean, academic feel |
| `delay_show` | int (ms) | Delay before showing spinner | `200` -- prevents flicker on fast updates |
| `delay_hide` | int (ms) | Minimum spinner display | `0` -- dismiss immediately when done |
| `overlay_style` | dict | CSS for the overlay | See above -- keeps chart visible but blurred |
| `color` | string | Spinner color | `"var(--bs-primary)"` to match FLATLY theme |
| `target_components` | dict | Which prop updates trigger it | Not needed here; wrapping is sufficient |
| `show_initially` | bool | Show on page load | `True` (default) is fine |

### Alternative: `dbc.Spinner`

dash-bootstrap-components 2.0.4 provides `dbc.Spinner` with Bootstrap-styled spinners:

```python
import dash_bootstrap_components as dbc

dbc.Spinner(
    children=dcc.Graph(id="chart-cost", ...),
    color="primary",
    type="border",               # "border" or "grow"
    debounce=200,                # ms delay (DBC 2.0 feature)
    spinner_style={"width": "2rem", "height": "2rem"},
)
```

**DBC 2.0 breaking change:** The `style` and `class_name` props were renamed to `spinner_style` and `spinnerClassName`. If copying patterns from DBC 1.x examples, update accordingly.

### Recommendation

Use `dcc.Loading` with `type="circle"`. Reasons:
- Built into Dash core, no extra dependency concerns
- `delay_show` prevents visual noise on fast slider drags
- `overlay_style` with blur keeps the chart visible (better UX than replacing with spinner)
- Consistent with Plotly's design language

**Confidence:** HIGH
**Source:** [dcc.Loading docs](https://dash.plotly.com/dash-core-components/loading), [dbc.Spinner docs](https://www.dash-bootstrap-components.com/docs/components/spinner/)

---

## 3. Slider UX Improvements

### Current State

The project has four sliders in `src/layout/charts.py`:

| Slider | ID | Range | Current Marks | Tooltip |
|--------|----|-------|--------------|---------|
| Time Horizon | `slider-time-horizon` | 1--50 | `{1: "1yr", 25: "25yr", 50: "50yr"}` | always_visible, bottom |
| Battery/Tank | `slider-battery` | 0--1 | `{}` (empty) | not always_visible |
| TDS Salinity | `slider-tds` | 0--35000 | `{0: "0", 10000: "10k", 20000: "20k", 35000: "35k"}` | always_visible, bottom |
| Depth | `slider-depth` | 0--1900 | `{0: "0", 950: "950", 1900: "1900"}` | always_visible, bottom |

### Improvement Opportunities

#### A. Styled Marks with Units

Current marks are bare numbers. Add units and optional styling:

```python
marks={
    0: {"label": "0 m", "style": {"fontSize": "0.75rem"}},
    950: {"label": "950 m", "style": {"fontSize": "0.75rem"}},
    1900: {"label": "1,900 m", "style": {"fontSize": "0.75rem"}},
}
```

#### B. Tooltip Template (Dash 2.15+, available in Dash 4.0)

Use `tooltip.template` to format tooltip values without JavaScript:

```python
tooltip={
    "always_visible": True,
    "placement": "bottom",
    "template": "{value} PPM",
}
```

#### C. Tooltip Transform with JavaScript (for complex formatting)

For the TDS slider where you want comma-formatted numbers, use a JS transform function:

1. Create `assets/slider_transforms.js`:
   ```javascript
   window.dccFunctions = window.dccFunctions || {};
   window.dccFunctions.formatTDS = function(value) {
       return value.toLocaleString() + " PPM";
   };
   window.dccFunctions.formatDepth = function(value) {
       return value.toLocaleString() + " m";
   };
   ```

2. Reference in slider:
   ```python
   tooltip={
       "always_visible": True,
       "placement": "bottom",
       "transform": "formatTDS",
   }
   ```

#### D. Battery Slider: Add Marks for Clarity

The battery slider currently has empty marks `{}`. Add semantic anchors:

```python
marks={
    0: {"label": "All Tank", "style": {"fontSize": "0.7rem"}},
    0.5: {"label": "50/50", "style": {"fontSize": "0.7rem"}},
    1: {"label": "All Battery", "style": {"fontSize": "0.7rem"}},
}
```

#### E. Dash 4.0: `allow_direct_input` Property

New in Dash 4.0 -- sliders can show a direct text input field by default. Set `allow_direct_input=False` to disable this if the input box is not wanted:

```python
dcc.Slider(
    ...,
    allow_direct_input=False,   # Dash 4.0: hides text input box
)
```

If the text input is currently not showing, it may be because of existing CSS or the specific slider configuration. Check if `allow_direct_input` is causing unexpected input fields to appear in the current build.

### Recommended Slider Configuration Summary

```python
# TDS Slider -- improved
dcc.Slider(
    id="slider-tds",
    min=0, max=35000, step=100, value=950,
    marks={
        0: {"label": "0", "style": {"fontSize": "0.75rem"}},
        10000: {"label": "10k", "style": {"fontSize": "0.75rem"}},
        20000: {"label": "20k", "style": {"fontSize": "0.75rem"}},
        35000: {"label": "35k PPM", "style": {"fontSize": "0.75rem"}},
    },
    tooltip={
        "always_visible": True,
        "placement": "bottom",
        "template": "{value} PPM",
    },
    updatemode="drag",
    allow_direct_input=False,
)
```

**Confidence:** HIGH for marks/tooltip.template (official docs). MEDIUM for `allow_direct_input` (new Dash 4.0 prop, release notes confirm but limited examples).

**Source:** [dcc.Slider docs](https://dash.plotly.com/dash-core-components/slider)

---

## 4. Dash 4.0 Gotchas (vs. Dash 2.x)

### 4a. Redesigned Core Components CSS

Dash 4.0 shipped "redesigned dash core components." This means `dcc.Slider`, `dcc.Dropdown`, `dcc.Loading`, etc. have updated default styling. The visual appearance of sliders and other controls may differ from Dash 2.x.

**Impact:** Slider track/handle colors and sizing may not match your existing custom.css assumptions. Test visually after upgrading.

**Mitigation:** The project already uses `assets/custom.css`. Inspect the rendered slider elements and adjust CSS variables if needed.

### 4b. `allow_direct_input` Default is `True`

New Dash 4.0 sliders render a text input field by default. If this was not present in your Dash 2.x version, explicitly set `allow_direct_input=False` on all sliders to preserve the old behavior.

### 4c. DataTable Deprecation

Dash 4.0 deprecates `dash_table.DataTable` in favor of `dash-ag-grid`. This project does not use DataTable, so no impact. But avoid adding DataTable in v1.3.

### 4d. DBC 2.0 Prop Renames

dash-bootstrap-components 2.0.4 renamed several props. Relevant to this milestone:

| Old (DBC 1.x) | New (DBC 2.0) |
|----------------|---------------|
| `Spinner(style=...)` | `Spinner(spinner_style=...)` |
| `Spinner(class_name=...)` | `Spinner(spinnerClassName=...)` |

The project is already on DBC 2.0.4, so any new code should use the new names.

### 4e. CSS Variable Names

Dash 4.0 uses CSS custom properties like `--Dash-Fill-Interactive-Strong` for component colors. If you override spinner or slider colors, use these variables for consistency, or set explicit hex values.

### 4f. `set_props` Incompatibility with `dcc.Loading`

The official docs note: "Updating component properties with `set_props` in a callback does not update the loading state." This project uses standard `Output()` callbacks, not `set_props`, so no impact. But avoid `set_props` for any loading-wrapped components.

**Confidence:** MEDIUM -- release notes are sparse for Dash 4.0 specifics. The component redesign is confirmed but detailed breakage lists are not published. Recommend visual testing of all sliders and controls after any code changes.

**Sources:**
- [Dash GitHub Releases](https://github.com/plotly/dash/releases)
- [DBC Changelog](https://www.dash-bootstrap-components.com/changelog/)

---

## 5. Stack Summary: No New Packages Needed

| Current Package | Version | Sufficient for v1.3? | Notes |
|----------------|---------|-----------------------|-------|
| dash | 4.0.0 | YES | `html.Img`, `dcc.Loading`, `dcc.Slider` all built-in |
| dash-bootstrap-components | 2.0.4 | YES | `dbc.Spinner` available as alternative; already installed |
| pandas | 2.2.3 | YES | No data layer changes |
| openpyxl | 3.1.5 | YES | No data layer changes |
| gunicorn | 23.0.0 | YES | No deployment changes |

### New Files to Create (not packages)

| File | Purpose |
|------|---------|
| `assets/slider_transforms.js` | Optional -- JS functions for tooltip formatting if `template` is insufficient |
| Move PNGs to `assets/` | Static image serving for system layout diagrams |

### requirements.txt

**No changes needed.** The current `requirements.txt` is complete for v1.3.

---

## Sources

- [Dash External Resources / Static Assets](https://dash.plotly.com/external-resources) -- HIGH confidence
- [dcc.Loading docs](https://dash.plotly.com/dash-core-components/loading) -- HIGH confidence
- [Dash Loading States](https://dash.plotly.com/loading-states) -- HIGH confidence
- [dcc.Slider docs](https://dash.plotly.com/dash-core-components/slider) -- HIGH confidence
- [dbc.Spinner docs](https://www.dash-bootstrap-components.com/docs/components/spinner/) -- HIGH confidence
- [DBC Changelog](https://www.dash-bootstrap-components.com/changelog/) -- HIGH confidence
- [Dash GitHub Releases](https://github.com/plotly/dash/releases) -- MEDIUM confidence (sparse 4.0 details)

---

*Stack research for: Wind-Powered Desalination Dashboard v1.3 UI/UX Overhaul*
*Researched: 2026-03-26*
