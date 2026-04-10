---
phase: 18-comparison-table-overhaul-slider-explanation
reviewed: 2026-04-10T00:00:00Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - src/layout/equipment_grid.py
  - src/layout/system_view.py
  - src/config.py
  - assets/custom.css
  - src/layout/charts.py
findings:
  critical: 0
  warning: 4
  info: 5
  total: 9
status: issues_found
---

# Phase 18: Code Review Report

**Reviewed:** 2026-04-10
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

Five files covering the comparison table overhaul and slider explanation work were reviewed at standard depth. No security or data-loss issues were found. The main concerns are: a missing `dcc.Store` ID (`store-banner-dismissed`) that the `dismiss_banner` callback writes to, a docstring mismatch in `update_charts`, an `active_label_style` that is applied to every tab regardless of active state, and a CSS selector that may fail on certain Plotly builds. Several smaller informational items are noted below.

---

## Warnings

### WR-01: Missing `store-banner-dismissed` component — callback will crash on load

**File:** `src/layout/charts.py:735-770`

**Issue:** The `dismiss_banner` callback declares `Output("store-banner-dismissed", "data")` and reads `State("store-banner-dismissed", "data")`, but `make_chart_section()` never creates a `dcc.Store(id="store-banner-dismissed", ...)` component. Dash raises a `NonExistentIdException` at startup when it encounters an Output or State whose ID is not present in the layout. The banner itself (`id="banner-guidance"`) is present, but the companion store is missing.

**Fix:** Add the store to `make_chart_section()` immediately alongside `legend_store`:
```python
banner_store = dcc.Store(
    id="store-banner-dismissed",
    data={"dismissed": False},
    storage_type="session",   # persist across tab switches, clear on new session
)
```
Then include `banner_store` in the returned `html.Div` children list (e.g., after `legend_store`).

---

### WR-02: `active_label_style` applied to every tab, not only the active one

**File:** `src/layout/system_view.py:176`

**Issue:** The `active_label_style` kwarg is intended to be set only on the `dbc.Tab` that is currently active; Dash Bootstrap Components applies it when the tab's `tab_id` matches `active_tab`. However, the current code sets it conditionally only when `is_active` is `True` — if `is_active` is `False` it falls through to `{"color": "#6c757d"}`. That fallback value is assigned to `active_label_style`, meaning every non-active tab also receives an explicit `active_label_style` override (grey). This is benign most of the time but overrides the DBC default active styling if the active tab is later programmatically changed without a full re-render. The intent (only highlight the current system color) would be cleaner and more reliable by only passing `active_label_style` on the active tab:

```python
tab_kwargs = dict(
    label=label,
    tab_id=key,
    label_style={"color": "#6c757d"},
)
if is_active:
    tab_kwargs["active_label_style"] = {
        "color": system_color,
        "fontWeight": "bold",
        "borderBottom": f"3px solid {system_color}",
    }
tab = dbc.Tab(**tab_kwargs)
```

---

### WR-03: `update_charts` docstring lists stale TDS range (0–35000), actual slider max is 10,000

**File:** `src/layout/charts.py:572`

**Issue:** The docstring for `update_charts` states `tds_ppm : float — Source water salinity in PPM from the TDS slider (0-35000, default 950)`. The actual `slider-tds` component (line 401–413) has `max=10000`, matching the project memory note that TDS is capped at 10,000 PPM for West Texas brackish water. Any future developer reading the docstring may assume a wider valid range and pass out-of-range values without triggering a guard.

**Fix:** Update the docstring parameter line:
```python
tds_ppm : float
    Source water salinity in PPM from the TDS slider (0–10000, default 950).
```

---

### WR-04: CSS selector `js-plotly-plot .plotly .xtick text` targets internal Plotly SVG structure — may break silently on Plotly version changes

**File:** `assets/custom.css:89`

**Issue:** The mobile media query uses `.js-plotly-plot .plotly .xtick text` to reduce x-axis label font size. This selector drills into Plotly's internal SVG class structure (`.plotly`, `.xtick`). Plotly may rename or restructure these classes across minor versions, silently losing the mobile fix without a CSS parse error. The `!important` flag won't help if the selector simply stops matching.

**Fix:** Either document the specific Plotly version this was tested against as a comment, or switch to a container-level font-size override that affects all Plotly text in the chart card:
```css
@media (max-width: 575px) {
    /* Reduce all Plotly chart text on narrow viewports.
       Tested against plotly.js 2.x — re-verify on Plotly upgrades. */
    .js-plotly-plot text {
        font-size: 10px !important;
    }
}
```

---

## Info

### IN-01: `EQUIPMENT_DESCRIPTIONS` has two entries for `"Calcite bed contactors"` with different text

**File:** `src/config.py:157` and `src/config.py:231`

**Issue:** The key `"Calcite bed contactors"` appears twice in the `EQUIPMENT_DESCRIPTIONS` dict (lines 157–160 and 231–235). In Python, the second definition silently overwrites the first. This means the mechanical system's description (remineralizes RO permeate, raising pH) is discarded and the electrical system's description (restores minerals, raises alkalinity, prevents corrosion) is used for any equipment item keyed as `"Calcite bed contactors"`. If the mechanical system's xlsx column B contains exactly `"Calcite bed contactors"`, it will receive the electrical-oriented description.

**Fix:** Remove the duplicate; consolidate into one entry, or use two distinct keys if the mechanical and electrical descriptions should differ.

---

### IN-02: `"Other"` stage bucket in `make_equipment_section` is built with `setdefault` but never iterated

**File:** `src/layout/equipment_grid.py:217-218`

**Issue:** When `get_equipment_stage` returns a stage name not in `_STAGE_ORDER`, the code appends the item to an `"Other"` bucket via `stage_groups.setdefault("Other", [])`. However, the downstream iteration at line 223 only iterates `_STAGE_ORDER` which does not include `"Other"`. Any equipment assigned to `"Other"` is silently dropped from the rendered output. This is currently harmless only if `get_equipment_stage` always returns a known stage, but the code structure implies `"Other"` was intended to be displayed.

**Fix:** Either append `"Other"` to `_STAGE_ORDER`, or add it as a final fallback iteration after the main loop:
```python
for stage in _STAGE_ORDER + (["Other"] if stage_groups.get("Other") else []):
    ...
```

---

### IN-03: `_make_comparison_table` uses `active_system.capitalize()` — fails for multi-word future system names

**File:** `src/layout/system_view.py:67`

**Issue:** `active_system.capitalize()` converts the first character to upper-case and lowercases the rest. For the current keys (`"mechanical"`, `"electrical"`, `"hybrid"`) this produces the correct label strings. However `SYSTEM_COLORS` uses title-case keys (`"Mechanical"`) and `capitalize()` would silently produce wrong results for any future system key that is multi-word (e.g., `"solar_hybrid"` → `"Solar_hybrid"`, which would not match any `SYSTEM_COLORS` key, falling back to `#6c757d` grey). The pattern `.title()` is not meaningfully better; the safest fix is an explicit mapping.

**Fix:** Use the existing `_SYSTEMS` list as the canonical key→label mapping, or simply do `active_label = active_system.capitalize()` with a `SYSTEM_COLORS.get(active_label, "#6c757d")` already present as the fallback — which is correct. The real risk is the header cell lookup `SYSTEM_COLORS[sys_label]` at line 77 (no `.get`), which would raise `KeyError` if a new system label is added to `_make_comparison_table`'s `systems` list but not to `SYSTEM_COLORS`.

**Specific fix for line 77:**
```python
"backgroundColor": SYSTEM_COLORS.get(sys_label, "#6c757d") if is_active else "#f8f9fa",
```

---

### IN-04: `Banner` `dismissable=False` means the `×` close button is absent — only slider interaction dismisses it

**File:** `src/layout/charts.py:295-303`

**Issue:** The banner is created with `dismissable=False`, which removes the built-in close button. Dismissal only happens through the `dismiss_banner` callback (any slider drag). This is the documented intent ("Drag any slider to dismiss this tip") but the banner text does not make the absence of a close button obvious to users who do not read it carefully. This is a minor UX issue, not a bug — noted for awareness.

**Fix (optional):** Either set `dismissable=True` (adds the `×` button, dismiss_banner callback still works), or leave as-is if intentional. No code change required unless UX is updated.

---

### IN-05: `DISPLAY_NAMES` is missing the hybrid gearbox variant used in `PROCESS_STAGES`

**File:** `src/config.py:380` and `src/config.py:432-444`

**Issue:** `PROCESS_STAGES["hybrid"]["Power & Drive"]` includes `"Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft"` (line 122). This raw name has a double-space like the mechanical variant. `DISPLAY_NAMES` maps the mechanical double-space variant (`"Gearbox (Winergy  PEAB series)"`) to a clean single-space display name, but does not include the hybrid variant with the trailing description. When the equipment grid renders the hybrid gearbox, it will display the raw xlsx string (with double-space and the full ordering note) rather than a clean name.

**Fix:** Add the hybrid gearbox key to `DISPLAY_NAMES`:
```python
"Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft":
    "Gearbox (Winergy PEAB series) — Second Output Shaft",
```

---

_Reviewed: 2026-04-10_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
