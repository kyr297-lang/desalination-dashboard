"""
src/layout/scorecard.py
=======================
RAG scorecard comparison table for the system overview view.

Exports
-------
make_scorecard_table(mechanical_df, electrical_df)
    Returns an html.Div containing the formatted comparison table with RAG
    traffic-light dots for Mechanical vs Electrical systems.  Hybrid is omitted
    until Phase 4.
"""

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from src.config import RAG_COLORS
from src.data.processing import compute_scorecard_metrics, rag_color, fmt_cost


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
            "width": "12px",
            "height": "12px",
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
) -> html.Div:
    """Build the RAG scorecard comparison table.

    Computes aggregate cost, land area, and energy metrics for Mechanical and
    Electrical systems, assigns RAG colors (green = best, red = worst), and
    renders a bordered Bootstrap table with colored dot indicators.

    An overall summary row counts which system has more green dots and declares
    the best overall system.  Hybrid is excluded until Phase 4.

    Parameters
    ----------
    mechanical_df : pd.DataFrame
        Equipment DataFrame for the mechanical system.
    electrical_df : pd.DataFrame
        Equipment DataFrame for the electrical system.

    Returns
    -------
    html.Div
        Container holding the title, legend note, table, and summary row.
    """
    # ── 1. Compute aggregate metrics ─────────────────────────────────────────
    metrics = compute_scorecard_metrics(mechanical_df, electrical_df)
    mech = metrics["mechanical"]
    elec = metrics["electrical"]

    # ── 2. Assign RAG colors per metric ──────────────────────────────────────
    cost_colors = rag_color(
        {"mechanical": mech["cost"], "electrical": elec["cost"]},
        metric="cost",
    )
    land_colors = rag_color(
        {"mechanical": mech["land_area"], "electrical": elec["land_area"]},
        metric="land_area",
    )
    energy_colors = rag_color(
        {"mechanical": mech["efficiency"], "electrical": elec["efficiency"]},
        metric="efficiency",
    )

    # ── 3. Count green dots per system ───────────────────────────────────────
    green_hex = RAG_COLORS["green"]
    mech_greens = sum(
        1 for colors in [cost_colors, land_colors, energy_colors]
        if colors.get("mechanical") == green_hex
    )
    elec_greens = sum(
        1 for colors in [cost_colors, land_colors, energy_colors]
        if colors.get("electrical") == green_hex
    )

    if mech_greens > elec_greens:
        best_overall = "Mechanical"
    elif elec_greens > mech_greens:
        best_overall = "Electrical"
    else:
        best_overall = "Tied"

    # ── 4. Build table rows ───────────────────────────────────────────────────
    def _value_cell(value_str: str, color_hex: str) -> html.Td:
        return html.Td(
            [_make_rag_dot(color_hex), value_str],
            style={"textAlign": "center"},
        )

    rows = [
        html.Tr([
            html.Th("Total Cost"),
            _value_cell(fmt_cost(mech["cost"]), cost_colors.get("mechanical", "")),
            _value_cell(fmt_cost(elec["cost"]), cost_colors.get("electrical", "")),
        ]),
        html.Tr([
            html.Th("Total Land Area"),
            _value_cell(
                f"{mech['land_area']:.1f} m\u00b2",
                land_colors.get("mechanical", ""),
            ),
            _value_cell(
                f"{elec['land_area']:.1f} m\u00b2",
                land_colors.get("electrical", ""),
            ),
        ]),
        html.Tr([
            html.Th("Total Energy (kW)"),
            _value_cell(
                f"{mech['efficiency']:,.0f} kW",
                energy_colors.get("mechanical", ""),
            ),
            _value_cell(
                f"{elec['efficiency']:,.0f} kW",
                energy_colors.get("electrical", ""),
            ),
        ]),
    ]

    # ── 5. Best overall summary row ───────────────────────────────────────────
    summary_row = html.Tr(
        html.Td(
            f"Best Overall: {best_overall}",
            colSpan=3,
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
            html.Thead(
                html.Tr([
                    html.Th("Metric"),
                    html.Th("Mechanical", style={"textAlign": "center"}),
                    html.Th("Electrical", style={"textAlign": "center"}),
                ])
            ),
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
            "Green = best of the compared systems, Red = worst. "
            "Lower cost, less land, and less energy are better.",
            className="text-muted small",
        ),
        table,
    ])
