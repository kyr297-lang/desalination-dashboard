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
