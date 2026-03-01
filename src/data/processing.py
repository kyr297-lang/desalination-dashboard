"""
src/data/processing.py
======================
Data processing utilities for the desalination comparison dashboard.

Provides:
  - Formatting helpers for cost and numeric display (fmt_cost, fmt_num, fmt)
  - RAG (Red / Amber / Green) color assignment logic (rag_color)
  - Scorecard metric aggregation from raw DataFrames (compute_scorecard_metrics)
  - Process-stage lookup for equipment items (get_equipment_stage)
  - Energy interpolation against Part 2 lookup tables (interpolate_energy)
  - Aggregate chart data computation (compute_chart_data(data, battery_fraction,
    years, hybrid_df, tds_ppm, depth_m)) — applies TDS and depth energy offsets
    from Part 2 lookup tables to both mechanical and electrical energy breakdowns

This module is a pure data/logic layer. It does NOT import from any layout
or UI module. All formatting uses pandas for safe numeric coercion.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import PROCESS_STAGES, RAG_COLORS

# ──────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────────────────────────────────────

def fmt_cost(value) -> str:
    """Format a numeric cost value as an abbreviated dollar string.

    Rules:
      - >= 1,000,000  →  "$X.XM"   (one decimal, millions)
      - >= 1,000      →  "$X.XK"   (one decimal, thousands)
      - < 1,000       →  "$X,XXX"  (comma-formatted integer)
      - Non-numeric or None → "N/A"

    Uses pd.to_numeric with errors='coerce' for safe conversion.

    Parameters
    ----------
    value : any
        Raw value from a DataFrame cell (may be string, int, float, or None).

    Returns
    -------
    str
    """
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return "N/A"
    v = float(numeric)
    if v >= 1_000_000:
        return f"${v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"${v / 1_000:.1f}K"
    return f"${v:,.0f}"


def fmt_num(value) -> str:
    """Format a general numeric value with one decimal place and comma separators.

    Non-numeric values are returned as str(value). None is returned as "N/A".

    Parameters
    ----------
    value : any
        Raw value from a DataFrame cell.

    Returns
    -------
    str
    """
    if value is None:
        return "N/A"
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return str(value)
    return f"{float(numeric):,.1f}"


def fmt(value) -> str:
    """Pass-through formatter.

    - Numeric values → comma-formatted integer (no decimals)
    - String values  → returned as-is
    - None           → "N/A"

    Parameters
    ----------
    value : any
        Raw value from a DataFrame cell.

    Returns
    -------
    str
    """
    if value is None:
        return "N/A"
    numeric = pd.to_numeric(value, errors="coerce")
    if not pd.isna(numeric):
        return f"{float(numeric):,.0f}"
    return str(value)


# ──────────────────────────────────────────────────────────────────────────────
# RAG color logic
# ──────────────────────────────────────────────────────────────────────────────

# Metrics where a lower value is considered better (green = lowest).
# "efficiency" holds total energy consumption; lower energy = more efficient.
RAG_BETTER_IS_LOWER: set[str] = {"cost", "land_area", "efficiency"}


def rag_color(values: dict[str, float], metric: str) -> dict[str, str]:
    """Assign RAG traffic-light colors to systems based on a metric value.

    Systems with None values are excluded from ranking and receive no color.

    With 2 systems: best → "green", worst → "red"
    With 3 systems: best → "green", middle → "yellow", worst → "red"

    Parameters
    ----------
    values : dict[str, float]
        Mapping of system key (e.g. "mechanical") to its numeric metric value.
        None values are excluded from ranking.
    metric : str
        Name of the metric being evaluated. Used to determine whether lower
        is better (see RAG_BETTER_IS_LOWER).

    Returns
    -------
    dict[str, str]
        Mapping of system key to RAG color string ("green", "yellow", "red").
        Systems with None values are omitted from the result.
    """
    # Filter out None / NaN entries
    valid: dict[str, float] = {
        k: v for k, v in values.items()
        if v is not None and not (isinstance(v, float) and pd.isna(v))
    }

    if not valid:
        return {}

    # Sort by value; direction depends on whether lower is better
    reverse_sort = metric not in RAG_BETTER_IS_LOWER  # higher is better → sort desc
    sorted_keys = sorted(valid, key=lambda k: valid[k], reverse=reverse_sort)

    n = len(sorted_keys)
    result: dict[str, str] = {}

    if n == 1:
        result[sorted_keys[0]] = RAG_COLORS["green"]
    elif n == 2:
        result[sorted_keys[0]] = RAG_COLORS["green"]
        result[sorted_keys[1]] = RAG_COLORS["red"]
    else:
        # 3 or more systems: best=green, last=red, middle(s)=yellow
        result[sorted_keys[0]] = RAG_COLORS["green"]
        result[sorted_keys[-1]] = RAG_COLORS["red"]
        for k in sorted_keys[1:-1]:
            result[k] = RAG_COLORS["yellow"]

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Scorecard computation
# ──────────────────────────────────────────────────────────────────────────────

def compute_scorecard_metrics(
    mechanical_df: pd.DataFrame,
    electrical_df: pd.DataFrame,
    hybrid_df: pd.DataFrame | None = None,
) -> dict[str, dict[str, float]]:
    """Compute aggregate scorecard metrics for each system.

    Numeric aggregation uses pd.to_numeric with errors='coerce' so that
    non-numeric strings (e.g. "$ 2500 per ton", "indefinite") are safely
    treated as NaN and excluded from the sum.

    Parameters
    ----------
    mechanical_df : pd.DataFrame
        Equipment DataFrame for the mechanical system (from load_data()).
    electrical_df : pd.DataFrame
        Equipment DataFrame for the electrical system (from load_data()).
    hybrid_df : pd.DataFrame or None, optional
        Equipment DataFrame for the hybrid system (from compute_hybrid_df()).
        When provided and not None, a "hybrid" key is included in the result.

    Returns
    -------
    dict with keys "mechanical" and "electrical" (and optionally "hybrid"),
    each mapping to:
        {
            "cost":       float  (sum of cost_usd column, USD),
            "land_area":  float  (sum of land_area_m2 column, m²),
            "efficiency": float  (sum of energy_kw column, kW — lower is better),
        }
    """
    def _aggregate(df: pd.DataFrame) -> dict[str, float]:
        cost = pd.to_numeric(df["cost_usd"], errors="coerce").sum()
        land = pd.to_numeric(df["land_area_m2"], errors="coerce").sum()
        energy = pd.to_numeric(df["energy_kw"], errors="coerce").sum()
        return {
            "cost":       float(cost),
            "land_area":  float(land),
            "efficiency": float(energy),
        }

    result = {
        "mechanical": _aggregate(mechanical_df),
        "electrical": _aggregate(electrical_df),
    }

    if hybrid_df is not None:
        result["hybrid"] = _aggregate(hybrid_df)

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Hybrid system helpers
# ──────────────────────────────────────────────────────────────────────────────

def compute_hybrid_df(slots: dict, data: dict) -> pd.DataFrame | None:
    """Build a 5-row DataFrame for the hybrid system from slot selections.

    For each stage slot, searches data["miscellaneous"], then data["mechanical"],
    then data["electrical"] for a matching equipment row (by name). Returns None
    if any slot is unfilled or any lookup fails.

    Parameters
    ----------
    slots : dict
        Mapping of stage name to selected equipment name (or None).
        Keys: "Water Extraction", "Pre-Treatment", "Desalination",
              "Post-Treatment", "Brine Disposal".
    data : dict
        Full data dict from load_data() with keys "miscellaneous", "mechanical",
        "electrical".

    Returns
    -------
    pd.DataFrame or None
        A 5-row DataFrame with the same columns as equipment DataFrames
        (name, quantity, cost_usd, energy_kw, land_area_m2, lifespan_years),
        or None if any slot is None or any equipment name cannot be found.
    """
    # Gate: all slots must be filled
    if any(v is None for v in slots.values()):
        return None

    search_order = ["miscellaneous", "mechanical", "electrical"]
    matched_rows: list[dict] = []

    for stage, equipment_name in slots.items():
        found = False
        for source_key in search_order:
            source_df: pd.DataFrame = data[source_key]
            match = source_df[source_df["name"] == equipment_name]
            if not match.empty:
                matched_rows.append(match.iloc[0].to_dict())
                found = True
                break
        if not found:
            return None

    return pd.DataFrame(matched_rows)


def generate_comparison_text(
    hybrid_metrics: dict,
    mech_metrics: dict,
    elec_metrics: dict,
) -> str:
    """Generate neutral, factual comparison sentences for hybrid vs each preset.

    Computes percentage differences for cost, land_area, and efficiency between
    the hybrid system and each of the two preset systems. Handles division-by-zero
    and None values gracefully.

    Parameters
    ----------
    hybrid_metrics : dict
        Metric dict for the hybrid system with keys "cost", "land_area",
        "efficiency" (same structure returned by compute_scorecard_metrics).
    mech_metrics : dict
        Metric dict for the mechanical system.
    elec_metrics : dict
        Metric dict for the electrical system.

    Returns
    -------
    str
        Multi-sentence factual comparison. One sentence per metric per preset.
    """
    metric_labels = {
        "cost": "cost",
        "land_area": "land area",
        "efficiency": "energy use",
    }

    def _pct_diff(hybrid_val, other_val, metric_key: str) -> str | None:
        """Return a sentence comparing hybrid to other, or None if undetermined."""
        h = pd.to_numeric(hybrid_val, errors="coerce")
        o = pd.to_numeric(other_val, errors="coerce")
        if pd.isna(h) or pd.isna(o) or o == 0:
            return None
        h_f = float(h)
        o_f = float(o)
        label = metric_labels[metric_key]
        pct = abs((h_f - o_f) / o_f) * 100
        if abs(h_f - o_f) < 0.001 * o_f:
            return f"Hybrid has similar {label} to {{other}}."
        direction = "less" if h_f < o_f else "more"
        return f"Hybrid has {pct:.0f}% {direction} {label} than {{other}}."

    lines: list[str] = []

    for metric_key in ["cost", "land_area", "efficiency"]:
        h_val = hybrid_metrics.get(metric_key)

        for other_name, other_metrics in [("Mechanical", mech_metrics), ("Electrical", elec_metrics)]:
            o_val = other_metrics.get(metric_key)
            sentence = _pct_diff(h_val, o_val, metric_key)
            if sentence:
                lines.append(sentence.format(other=other_name))

    return " ".join(lines) if lines else "Hybrid system comparison data unavailable."


# ──────────────────────────────────────────────────────────────────────────────
# Process stage lookup
# ──────────────────────────────────────────────────────────────────────────────

def get_equipment_stage(equipment_name: str, system: str) -> str:
    """Look up the process stage for an equipment item.

    Iterates over the PROCESS_STAGES mapping for the given system and returns
    the stage name that contains *equipment_name*. Returns "Other" if the item
    is not found in any stage for the specified system.

    Parameters
    ----------
    equipment_name : str
        Exact equipment name string as returned by loader.py (column B value).
    system : str
        System key: "mechanical", "electrical", or "miscellaneous".

    Returns
    -------
    str
        Stage name (e.g. "Pre-Treatment") or "Other" if not found.
    """
    system_stages = PROCESS_STAGES.get(system, {})
    for stage_name, items in system_stages.items():
        if equipment_name in items:
            return stage_name
    return "Other"


# ──────────────────────────────────────────────────────────────────────────────
# Chart data computation
# ──────────────────────────────────────────────────────────────────────────────

def interpolate_battery_cost(battery_fraction: float, battery_lookup_df: pd.DataFrame) -> float:
    """Interpolate the total storage cost from the 11-row battery/tank lookup table.

    Uses numpy.interp() for smooth continuous interpolation between the discrete
    lookup rows. Values outside [0.0, 1.0] are clamped to the boundary values.

    Parameters
    ----------
    battery_fraction : float
        Slider value from 0.0 (all tank) to 1.0 (all battery).
    battery_lookup_df : pd.DataFrame
        Battery/tank lookup DataFrame from load_data() with columns
        "battery_fraction" and "total_cost".

    Returns
    -------
    float
        Interpolated total_cost (battery_cost + tank_cost) in USD.
    """
    fractions = pd.to_numeric(battery_lookup_df["battery_fraction"], errors="coerce").values
    costs = pd.to_numeric(battery_lookup_df["total_cost"], errors="coerce").values
    return float(np.interp(battery_fraction, fractions, costs))


def interpolate_energy(value: float, lookup_df: pd.DataFrame, col_x: str, col_y: str) -> float:
    """Interpolate an energy value (kW) from a Part 2 lookup table.

    Uses numpy.interp() for smooth linear interpolation between the discrete
    lookup rows. Values below the table minimum are clamped (numpy.interp
    default). Values above the table maximum are linearly extrapolated using
    the slope of the last two rows, so sliders wider than the lookup range
    (e.g. TDS up to 35,000 PPM) continue to reflect increasing energy demand.

    Parameters
    ----------
    value : float
        Slider value (e.g. TDS in PPM or depth in m).
    lookup_df : pd.DataFrame
        20-row lookup DataFrame from load_data() (tds_lookup or depth_lookup).
    col_x : str
        Name of the independent variable column (e.g. "tds_ppm" or "depth_m").
    col_y : str
        Name of the energy output column (e.g. "ro_energy_kw" or "pump_energy_kw").

    Returns
    -------
    float
        Interpolated or extrapolated energy in kW.
    """
    x_vals = pd.to_numeric(lookup_df[col_x], errors="coerce").values
    y_vals = pd.to_numeric(lookup_df[col_y], errors="coerce").values
    if value > x_vals[-1] and len(x_vals) >= 2:
        slope = (y_vals[-1] - y_vals[-2]) / (x_vals[-1] - x_vals[-2])
        return float(y_vals[-1] + slope * (value - x_vals[-1]))
    return float(np.interp(value, x_vals, y_vals))


def battery_ratio_label(battery_fraction: float) -> str:
    """Format a human-readable ratio label for the battery/tank slider.

    Parameters
    ----------
    battery_fraction : float
        Slider value from 0.0 (all tank) to 1.0 (all battery).

    Returns
    -------
    str
        A string like "70% Battery / 30% Tank".
    """
    pct_batt = int(round(battery_fraction * 100))
    pct_tank = 100 - pct_batt
    return f"{pct_batt}% Battery / {pct_tank}% Tank"


def compute_cost_over_time(
    df: pd.DataFrame,
    years: int = 50,
    override_costs: dict | None = None,
) -> np.ndarray:
    """Compute a cumulative cost array over a time horizon for a system DataFrame.

    For each equipment row:
    - "indefinite" lifespan items are purchased only at year 0.
    - Numeric lifespan items are purchased at year 0, then replaced every
      lifespan years (e.g., year 0, 12, 24, 36, 48 for lifespan=12).
    - override_costs replaces the cost for named equipment (used for battery
      slider interpolation).

    Parameters
    ----------
    df : pd.DataFrame
        Equipment DataFrame with columns: name, cost_usd, lifespan_years.
    years : int
        Number of years to project (inclusive). Resulting array has length years+1.
    override_costs : dict | None
        Dict of {equipment_name: cost_usd} overrides. None means no overrides.

    Returns
    -------
    np.ndarray
        Cumulative cost array of shape (years+1,). Index i is the total cost
        incurred from year 0 through year i.
    """
    annual = np.zeros(years + 1)

    for _, row in df.iterrows():
        cost = pd.to_numeric(row["cost_usd"], errors="coerce")
        if pd.isna(cost):
            continue

        # Apply override if provided (e.g. battery slider replacement cost)
        if override_costs is not None and row["name"] in override_costs:
            cost = override_costs[row["name"]]

        lifespan = row["lifespan_years"]

        # "indefinite" items are bought once at year 0 — no replacements
        if isinstance(lifespan, str) and lifespan.strip().lower() == "indefinite":
            annual[0] += cost
        else:
            try:
                lifespan_int = int(float(lifespan))
            except (TypeError, ValueError):
                # Unparseable lifespan — treat as indefinite (year 0 only)
                annual[0] += cost
                continue
            for yr in range(0, years + 1, lifespan_int):
                annual[yr] += cost

    return np.cumsum(annual)


def compute_chart_data(
    data: dict,
    battery_fraction: float = 0.5,
    years: int = 50,
    hybrid_df: pd.DataFrame | None = None,
    tds_ppm: float = 950,
    depth_m: float = 950,
) -> dict:
    """Aggregate all chart data for the comparison charts section.

    This is the primary aggregation function called by the chart callback.
    It returns pre-computed arrays and scalars so that callbacks remain fast
    (no DataFrame iteration inside callbacks).

    Parameters
    ----------
    data : dict
        Full data dict from load_data() with keys:
        "mechanical", "electrical", "miscellaneous", "battery_lookup",
        "tds_lookup", "depth_lookup".
    battery_fraction : float
        Current battery/tank slider value, 0.0 (all tank) to 1.0 (all battery).
    years : int
        Time horizon in years for cost-over-time computation.
    hybrid_df : pd.DataFrame or None, optional
        When provided and not None, hybrid chart values are computed from this
        DataFrame instead of using placeholder zeros. Comes from compute_hybrid_df().
    tds_ppm : float, optional
        Source water salinity in PPM from the TDS slider (default 950).
        Used to interpolate ro_energy_kw from data["tds_lookup"] and add it to
        the "Desalination" stage in both mech_energy and elec_energy.
    depth_m : float, optional
        Water source depth in metres from the depth slider (default 950).
        Used to interpolate pump_energy_kw from data["depth_lookup"] and add it
        to the "Water Extraction" stage in both mech_energy and elec_energy.

    Returns
    -------
    dict with keys:
        cost_over_time : dict[str, np.ndarray]
            {"mechanical": array, "electrical": array, "hybrid": array}
            Each array has length years+1 (cumulative cost per year).
        land_area : dict[str, float]
            {"mechanical": float, "electrical": float, "hybrid": float}
            Total land area in m² per system.
        turbine_count : dict[str, int]
            {"mechanical": int, "electrical": int, "hybrid": int}
            Number of wind turbines per system.
        energy_breakdown : dict[str, dict[str, float]]
            {"mechanical": {stage: kw, ...}, "electrical": {stage: kw, ...}, "hybrid": {}}
            Energy use per process stage for each system.
        electrical_total_cost : float
            Live electrical total cost at current battery_fraction (USD).
    """
    mechanical_df = data["mechanical"]
    electrical_df = data["electrical"]
    battery_lookup = data["battery_lookup"]

    # ── Battery interpolation ─────────────────────────────────────────────────
    interpolated_cost = interpolate_battery_cost(battery_fraction, battery_lookup)

    # ── Cost over time ────────────────────────────────────────────────────────
    # Mechanical: straightforward cumulative replacement model
    mech_cumulative = compute_cost_over_time(mechanical_df, years)

    # Electrical: exclude the spreadsheet "Battery (1 day of power)" row and
    # replace with the slider-interpolated cost so all replacement cycles use
    # the current slider value (year 0, 12, 24, 36, 48).
    # Research Pitfall 1: the $1.8M battery row != lookup table values — don't add both.
    elec_cumulative = compute_cost_over_time(
        electrical_df,
        years,
        override_costs={"Battery (1 day of power)": interpolated_cost},
    )

    # Hybrid: use real data when hybrid_df is provided; zeros otherwise
    if hybrid_df is not None:
        hybrid_cumulative = compute_cost_over_time(hybrid_df, years)
    else:
        hybrid_cumulative = np.zeros(years + 1)

    # ── Land area ─────────────────────────────────────────────────────────────
    mech_land = float(pd.to_numeric(mechanical_df["land_area_m2"], errors="coerce").sum())
    elec_land = float(pd.to_numeric(electrical_df["land_area_m2"], errors="coerce").sum())
    if hybrid_df is not None:
        hybrid_land = float(pd.to_numeric(hybrid_df["land_area_m2"], errors="coerce").sum())
    else:
        hybrid_land = 0.0

    # ── Turbine count ─────────────────────────────────────────────────────────
    # Mechanical system uses the "250kW aeromotor turbine " row for turbine count
    mech_turbine_rows = mechanical_df[mechanical_df["name"] == "250kW aeromotor turbine "]["quantity"]
    mech_turbines = int(pd.to_numeric(mech_turbine_rows, errors="coerce").sum()) if len(mech_turbine_rows) > 0 else 0

    # Electrical system uses the "Turbine" row
    elec_turbine_rows = electrical_df[electrical_df["name"] == "Turbine"]["quantity"]
    elec_turbines = int(pd.to_numeric(elec_turbine_rows, errors="coerce").sum()) if len(elec_turbine_rows) > 0 else 0

    # Hybrid: miscellaneous items don't include turbines
    hybrid_turbines = 0

    # ── Energy breakdown by process stage ────────────────────────────────────
    def _energy_by_stage(df: pd.DataFrame, system: str) -> dict[str, float]:
        stage_energy: dict[str, float] = {}
        for _, row in df.iterrows():
            kw = pd.to_numeric(row["energy_kw"], errors="coerce")
            if pd.isna(kw) or kw == 0:
                continue
            stage = get_equipment_stage(str(row["name"]), system)
            stage_energy[stage] = stage_energy.get(stage, 0.0) + float(kw)
        return stage_energy

    mech_energy = _energy_by_stage(mechanical_df, "mechanical")
    elec_energy = _energy_by_stage(electrical_df, "electrical")

    # ── TDS and depth energy offsets ──────────────────────────────────────────
    # Interpolate RO desalination energy from Part 2 TDS lookup table
    ro_kw = interpolate_energy(tds_ppm, data["tds_lookup"], "tds_ppm", "ro_energy_kw")
    # Interpolate pump energy from Part 2 depth lookup table
    pump_kw = interpolate_energy(depth_m, data["depth_lookup"], "depth_m", "pump_energy_kw")

    # Apply offsets to both mechanical and electrical systems.
    # TDS affects desalination energy demand (RO membranes) regardless of drive type.
    # Depth affects water extraction energy demand (pump lift) regardless of drive type.
    mech_energy["Desalination"] = mech_energy.get("Desalination", 0.0) + ro_kw
    elec_energy["Desalination"] = elec_energy.get("Desalination", 0.0) + ro_kw
    mech_energy["Water Extraction"] = mech_energy.get("Water Extraction", 0.0) + pump_kw
    elec_energy["Water Extraction"] = elec_energy.get("Water Extraction", 0.0) + pump_kw

    # Hybrid energy: built directly from the hybrid_df rows using miscellaneous stage mapping
    if hybrid_df is not None:
        hybrid_energy = _energy_by_stage(hybrid_df, "miscellaneous")
    else:
        hybrid_energy = {}

    # ── Electrical total cost (live readout for slider label) ─────────────────
    # Sum all electrical costs EXCLUDING the battery row, then add interpolated cost.
    elec_base_cost = float(
        pd.to_numeric(
            electrical_df[electrical_df["name"] != "Battery (1 day of power)"]["cost_usd"],
            errors="coerce",
        ).sum()
    )
    electrical_total_cost = elec_base_cost + interpolated_cost

    return {
        "cost_over_time": {
            "mechanical": mech_cumulative,
            "electrical": elec_cumulative,
            "hybrid": hybrid_cumulative,
        },
        "land_area": {
            "mechanical": mech_land,
            "electrical": elec_land,
            "hybrid": hybrid_land,
        },
        "turbine_count": {
            "mechanical": mech_turbines,
            "electrical": elec_turbines,
            "hybrid": hybrid_turbines,
        },
        "energy_breakdown": {
            "mechanical": mech_energy,
            "electrical": elec_energy,
            "hybrid": hybrid_energy,
        },
        "electrical_total_cost": electrical_total_cost,
    }
