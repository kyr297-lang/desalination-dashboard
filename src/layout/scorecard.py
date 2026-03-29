"""
src/layout/scorecard.py
=======================
RAG scorecard comparison table for the system overview view.

Exports
-------
set_data(data) -> None
make_scorecard_table(mechanical_df, electrical_df, hybrid_df=None)
    Returns an html.Div containing the formatted comparison table with RAG
    traffic-light dots. Always renders 3 columns when hybrid_df is provided.

Callbacks registered here
--------------------------
(export button only — no slot-based callbacks; scorecard is always 3-column)
"""

import pandas as pd
from dash import html, clientside_callback, Input, Output
import dash_bootstrap_components as dbc

from src.config import RAG_COLORS
from src.data.processing import (
    compute_scorecard_metrics,
    generate_comparison_text,
    rag_color,
    fmt_cost,
    fmt_sig2,
)


# ──────────────────────────────────────────────────────────────────────────────
# Export / Print clientside callback
# Fires window.print() when the export button is clicked.
# Uses module-level clientside_callback (not app.clientside_callback) to
# follow the project's existing callback registration pattern.
# ──────────────────────────────────────────────────────────────────────────────

clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        window.print();
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-btn", "n_clicks"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)


# ──────────────────────────────────────────────────────────────────────────────
# Module-level data reference — mirrors set_data() pattern from shell.py.
# ──────────────────────────────────────────────────────────────────────────────

_data: dict | None = None


def set_data(data: dict) -> None:
    """Store the loaded data dict for use in scorecard callbacks.

    Called once from app.py after DATA is loaded, before any callbacks fire.
    Mirrors the pattern used in shell.py and charts.py.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().
    """
    global _data
    _data = data


# ──────────────────────────────────────────────────────────────────────────────
# Helper: RAG dot
# ──────────────────────────────────────────────────────────────────────────────

def _make_rag_dot(color_hex: str) -> html.Span:
    """Create a small circular RAG indicator span.

    Parameters
    ----------
    color_hex : str
        Hex color string (e.g. "#28A745") from RAG_COLORS.

    Returns
    -------
    html.Span
        Inline circle element styled as a 12 px colored dot.
    """
    return html.Span(
        "",
        style={
            "display": "inline-block",
            "width": "14px",
            "height": "14px",
            "borderRadius": "50%",
            "backgroundColor": color_hex,
            "marginRight": "6px",
            "verticalAlign": "middle",
        },
    )


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def make_scorecard_table(
    mechanical_df: pd.DataFrame,
    electrical_df: pd.DataFrame,
    hybrid_df: pd.DataFrame | None = None,
) -> html.Div:
    """Build the RAG scorecard comparison table.

    Computes aggregate cost, land area, and energy metrics for Mechanical and
    Electrical systems, assigns RAG colors (green = best, red = worst), and
    renders a bordered Bootstrap table with colored dot indicators.

    An overall summary row counts which system has more green dots and declares
    the best overall system.

    When hybrid_df is provided, a third "Hybrid" column is added to the table
    and RAG colors are computed across all three systems.

    Parameters
    ----------
    mechanical_df : pd.DataFrame
        Equipment DataFrame for the mechanical system.
    electrical_df : pd.DataFrame
        Equipment DataFrame for the electrical system.
    hybrid_df : pd.DataFrame or None, optional
        Equipment DataFrame for the hybrid system (from data["hybrid"]).
        When provided, a Hybrid column is added with RAG indicators.

    Returns
    -------
    html.Div
        Container holding the title, legend note, table, and summary row.
    """
    # ── 1. Compute aggregate metrics ─────────────────────────────────────────
    metrics = compute_scorecard_metrics(mechanical_df, electrical_df, hybrid_df)
    mech = metrics["mechanical"]
    elec = metrics["electrical"]
    has_hybrid = hybrid_df is not None and "hybrid" in metrics
    hyb = metrics.get("hybrid") if has_hybrid else None

    # ── 2. Assign RAG colors per metric ──────────────────────────────────────
    if has_hybrid:
        cost_values = {"mechanical": mech["cost"], "electrical": elec["cost"], "hybrid": hyb["cost"]}
    else:
        cost_values = {"mechanical": mech["cost"], "electrical": elec["cost"]}

    cost_colors = rag_color(cost_values, metric="cost")

    # ── 3. Count green dots per system ───────────────────────────────────────
    green_hex = RAG_COLORS["green"]
    all_color_maps = [cost_colors]

    mech_greens = sum(1 for colors in all_color_maps if colors.get("mechanical") == green_hex)
    elec_greens = sum(1 for colors in all_color_maps if colors.get("electrical") == green_hex)
    hyb_greens = sum(1 for colors in all_color_maps if colors.get("hybrid") == green_hex) if has_hybrid else 0

    systems_greens = {"Mechanical": mech_greens, "Electrical": elec_greens}
    if has_hybrid:
        systems_greens["Hybrid"] = hyb_greens

    best_overall = max(systems_greens, key=lambda k: systems_greens[k])
    # Check for tie
    max_greens = systems_greens[best_overall]
    tied = [k for k, v in systems_greens.items() if v == max_greens]
    if len(tied) > 1:
        best_overall = "Tied"

    # ── 4. Build table rows ───────────────────────────────────────────────────
    def _value_cell(value_str: str, color_hex: str) -> html.Td:
        return html.Td(
            [_make_rag_dot(color_hex), value_str],
            style={"textAlign": "center"},
        )

    if has_hybrid:
        rows = [
            html.Tr([
                html.Th("Total Cost"),
                _value_cell(fmt_cost(mech["cost"]), cost_colors.get("mechanical", "")),
                _value_cell(fmt_cost(elec["cost"]), cost_colors.get("electrical", "")),
                _value_cell(fmt_cost(hyb["cost"]), cost_colors.get("hybrid", "")),
            ]),
        ]
        col_span = 4
        header_row = html.Tr([
            html.Th("Metric"),
            html.Th("Mechanical", style={"textAlign": "center"}),
            html.Th("Electrical", style={"textAlign": "center"}),
            html.Th("Hybrid", style={"textAlign": "center"}),
        ])
    else:
        rows = [
            html.Tr([
                html.Th("Total Cost"),
                _value_cell(fmt_cost(mech["cost"]), cost_colors.get("mechanical", "")),
                _value_cell(fmt_cost(elec["cost"]), cost_colors.get("electrical", "")),
            ]),
        ]
        col_span = 3
        header_row = html.Tr([
            html.Th("Metric"),
            html.Th("Mechanical", style={"textAlign": "center"}),
            html.Th("Electrical", style={"textAlign": "center"}),
        ])

    # ── 5. Best overall summary row ───────────────────────────────────────────
    summary_row = html.Tr(
        html.Td(
            f"Best Overall: {best_overall}",
            colSpan=col_span,
            style={
                "textAlign": "center",
                "fontWeight": "600",
                "fontStyle": "italic",
                "backgroundColor": "#f8f9fa",
            },
        )
    )

    table = dbc.Table(
        [
            html.Thead(header_row),
            html.Tbody(rows + [summary_row]),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )

    return html.Div([
        html.H5("System Scorecard", className="mt-3"),
        html.P(
            "Green = lowest cost, Red = highest cost.",
            className="text-muted small",
        ),
        table,
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────
# Note: scorecard and comparison text are rendered statically in system_view.py
# using BOM data from load_data(). No slot-based callbacks are needed.
