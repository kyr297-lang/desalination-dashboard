"""
src/data/processing.py
======================
Data processing utilities for the desalination comparison dashboard.

Provides:
  - Formatting helpers for cost and numeric display (fmt_cost, fmt_num, fmt)
  - RAG (Red / Amber / Green) color assignment logic (rag_color)
  - Scorecard metric aggregation from raw DataFrames (compute_scorecard_metrics)
  - Process-stage lookup for equipment items (get_equipment_stage)

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

    Returns
    -------
    dict with keys "mechanical" and "electrical", each mapping to:
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

    return {
        "mechanical": _aggregate(mechanical_df),
        "electrical": _aggregate(electrical_df),
    }


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
) -> dict:
    """Aggregate all chart data for the comparison charts section.

    This is the primary aggregation function called by the chart callback.
    It returns pre-computed arrays and scalars so that callbacks remain fast
    (no DataFrame iteration inside callbacks).

    Parameters
    ----------
    data : dict
        Full data dict from load_data() with keys:
        "mechanical", "electrical", "miscellaneous", "battery_lookup".
    battery_fraction : float
        Current battery/tank slider value, 0.0 (all tank) to 1.0 (all battery).
    years : int
        Time horizon in years for cost-over-time computation.

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

    # Hybrid: placeholder zeros for Phase 3 — real data comes in Phase 4
    # TODO Phase 4: replace with actual hybrid system data
    hybrid_cumulative = np.zeros(years + 1)

    # ── Land area ─────────────────────────────────────────────────────────────
    mech_land = float(pd.to_numeric(mechanical_df["land_area_m2"], errors="coerce").sum())
    elec_land = float(pd.to_numeric(electrical_df["land_area_m2"], errors="coerce").sum())
    hybrid_land = 0.0  # TODO Phase 4

    # ── Turbine count ─────────────────────────────────────────────────────────
    # Mechanical system uses the "250kW aeromotor turbine " row for turbine count
    mech_turbine_rows = mechanical_df[mechanical_df["name"] == "250kW aeromotor turbine "]["quantity"]
    mech_turbines = int(pd.to_numeric(mech_turbine_rows, errors="coerce").sum()) if len(mech_turbine_rows) > 0 else 0

    # Electrical system uses the "Turbine" row
    elec_turbine_rows = electrical_df[electrical_df["name"] == "Turbine"]["quantity"]
    elec_turbines = int(pd.to_numeric(elec_turbine_rows, errors="coerce").sum()) if len(elec_turbine_rows) > 0 else 0

    hybrid_turbines = 0  # TODO Phase 4

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
    hybrid_energy: dict[str, float] = {}  # TODO Phase 4

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
