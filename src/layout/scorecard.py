"""
src/layout/scorecard.py
=======================
RAG scorecard comparison table for the system overview view.

Exports
-------
set_data(data) -> None
make_scorecard_table(mechanical_df, electrical_df, hybrid_df=None)
    Returns an html.Div containing the formatted comparison table with RAG
    traffic-light dots. Accepts an optional hybrid_df for 3-column display.

Callbacks registered here
--------------------------
update_scorecard  -- Output("scorecard-container", "children"),
                     Output("comparison-text", "children")
                     triggered by Input("store-hybrid-slots", "data")
update_gate_overlay -- Output("hybrid-gate-overlay", "style")
                       triggered by Input("store-hybrid-slots", "data")
"""

import pandas as pd
from dash import html, callback, clientside_callback, Input, Output
import dash_bootstrap_components as dbc

from src.config import RAG_COLORS
from src.data.processing import (
    compute_scorecard_metrics,
    compute_hybrid_df,
    generate_comparison_text,
    rag_color,
    fmt_cost,
    fmt_sig2,
)
from src.layout.equipment_grid import make_equipment_section


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
        Equipment DataFrame for the hybrid system (from compute_hybrid_df()).
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
        land_values = {"mechanical": mech["land_area"], "electrical": elec["land_area"], "hybrid": hyb["land_area"]}
        energy_values = {"mechanical": mech["efficiency"], "electrical": elec["efficiency"], "hybrid": hyb["efficiency"]}
    else:
        cost_values = {"mechanical": mech["cost"], "electrical": elec["cost"]}
        land_values = {"mechanical": mech["land_area"], "electrical": elec["land_area"]}
        energy_values = {"mechanical": mech["efficiency"], "electrical": elec["efficiency"]}

    cost_colors = rag_color(cost_values, metric="cost")
    land_colors = rag_color(land_values, metric="land_area")
    energy_colors = rag_color(energy_values, metric="efficiency")

    # ── 3. Count green dots per system ───────────────────────────────────────
    green_hex = RAG_COLORS["green"]
    all_color_maps = [cost_colors, land_colors, energy_colors]

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
            html.Tr([
                html.Th("Total Land Area"),
                _value_cell(
                    f"{fmt_sig2(mech['land_area'])} m\u00b2",
                    land_colors.get("mechanical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(elec['land_area'])} m\u00b2",
                    land_colors.get("electrical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(hyb['land_area'])} m\u00b2",
                    land_colors.get("hybrid", ""),
                ),
            ]),
            html.Tr([
                html.Th("Total Power (kW)"),
                _value_cell(
                    f"{fmt_sig2(mech['efficiency'])} kW",
                    energy_colors.get("mechanical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(elec['efficiency'])} kW",
                    energy_colors.get("electrical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(hyb['efficiency'])} kW",
                    energy_colors.get("hybrid", ""),
                ),
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
            html.Tr([
                html.Th("Total Land Area"),
                _value_cell(
                    f"{fmt_sig2(mech['land_area'])} m\u00b2",
                    land_colors.get("mechanical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(elec['land_area'])} m\u00b2",
                    land_colors.get("electrical", ""),
                ),
            ]),
            html.Tr([
                html.Th("Total Power (kW)"),
                _value_cell(
                    f"{fmt_sig2(mech['efficiency'])} kW",
                    energy_colors.get("mechanical", ""),
                ),
                _value_cell(
                    f"{fmt_sig2(elec['efficiency'])} kW",
                    energy_colors.get("electrical", ""),
                ),
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
            "Green = best of the compared systems, Red = worst. "
            "Lower cost, less land, and less energy are better.",
            className="text-muted small",
        ),
        table,
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────

@callback(
    Output("scorecard-container", "children"),
    Output("comparison-text", "children"),
    Input("store-hybrid-slots", "data"),
)
def update_scorecard(slots):
    """Update the scorecard table and comparison text when hybrid slots change.

    When all 5 slots are filled (gate open): builds hybrid_df, renders a
    3-column scorecard with hybrid RAG indicators, and generates comparison text.

    When any slot is None (gate closed): renders the 2-system scorecard and
    returns no comparison text.

    Parameters
    ----------
    slots : dict or None
        Current hybrid slot store data mapping stage names to equipment names.

    Returns
    -------
    tuple
        (scorecard_children, comparison_text_children)
    """
    if _data is None:
        return [], None

    mech_df = _data["mechanical"]
    elec_df = _data["electrical"]

    # Check if gate is open (all 5 slots filled)
    gate_open = (
        slots is not None
        and all(v is not None for v in slots.values())
    )

    if gate_open:
        hybrid_df = compute_hybrid_df(slots, _data)
        if hybrid_df is not None:
            # Build 3-column scorecard
            scorecard = make_scorecard_table(mech_df, elec_df, hybrid_df)

            # Build comparison text
            metrics = compute_scorecard_metrics(mech_df, elec_df, hybrid_df)
            comparison_str = generate_comparison_text(
                metrics["hybrid"],
                metrics["mechanical"],
                metrics["electrical"],
            )
            comparison_content = html.P(
                comparison_str,
                className="text-muted small mt-2",
                style={"fontStyle": "italic"},
            )
            return scorecard, comparison_content

    # Gate closed or hybrid_df failed — 2-system scorecard, no comparison text
    scorecard = make_scorecard_table(mech_df, elec_df)
    return scorecard, None


@callback(
    Output("hybrid-gate-overlay", "style"),
    Input("store-hybrid-slots", "data"),
)
def update_gate_overlay(slots):
    """Show or hide the hybrid gate overlay based on slot completion.

    Returns a complete style dict (never partial) to ensure consistent
    overlay behavior. The overlay is hidden when all 5 slots are filled;
    visible otherwise.

    Parameters
    ----------
    slots : dict or None
        Current hybrid slot store data.

    Returns
    -------
    dict
        Complete CSS style dict for the overlay div.
    """
    gate_open = (
        slots is not None
        and all(v is not None for v in slots.values())
    )

    if gate_open:
        return {"display": "none"}

    return {
        "display": "flex",
        "position": "absolute",
        "top": "0",
        "left": "0",
        "right": "0",
        "bottom": "0",
        "backgroundColor": "rgba(255,255,255,0.85)",
        "zIndex": "10",
        "alignItems": "center",
        "justifyContent": "center",
        "borderRadius": "4px",
    }


@callback(
    Output("hybrid-equipment-container", "children"),
    Input("store-hybrid-slots", "data"),
)
def update_hybrid_equipment(slots):
    """Update the hybrid equipment detail section when slots change.

    When all 5 slots are filled: builds hybrid_df and renders equipment
    accordion items. When any slot is empty: shows gate message.

    Parameters
    ----------
    slots : dict or None
        Current hybrid slot store data.

    Returns
    -------
    dash component
        Equipment section or gate message.
    """
    if _data is None:
        return []

    gate_open = (
        slots is not None
        and all(v is not None for v in slots.values())
    )

    if gate_open:
        hybrid_df = compute_hybrid_df(slots, _data)
        if hybrid_df is not None:
            data_with_hybrid = {**_data, "hybrid_selected": hybrid_df}
            return make_equipment_section(hybrid_df, "hybrid", data_with_hybrid)

    return make_equipment_section(None, "hybrid", _data)
