"""
src/layout/charts.py
====================
Plotly figure builders and chart section layout for the System Comparison panel.

Provides four pure figure-building functions (no callbacks) and one layout
factory. All callbacks that wire sliders and legend toggles to these figures
are defined in Plan 02 (03-02-PLAN.md).

Exports
-------
build_cost_chart(years, mech_cumulative, elec_cumulative, hybrid_cumulative, visibility) -> go.Figure
build_land_chart(mech_land, elec_land, hybrid_land, visibility) -> go.Figure
build_turbine_chart(mech_count, elec_count, hybrid_count, visibility) -> go.Figure
build_pie_chart(mech_energy, elec_energy, hybrid_energy, visibility) -> go.Figure
make_chart_section() -> html.Div
"""

import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS


# ──────────────────────────────────────────────────────────────────────────────
# Shared layout constants
# ──────────────────────────────────────────────────────────────────────────────

_TRANSITION = {"duration": 300, "easing": "cubic-in-out"}
_MARGIN = dict(l=60, r=20, t=10, b=40)


def _visibility(visibility: dict, key: str):
    """Return True or 'legendonly' based on the visibility store dict."""
    return True if visibility.get(key, True) else "legendonly"


# ──────────────────────────────────────────────────────────────────────────────
# Figure builders
# ──────────────────────────────────────────────────────────────────────────────

def build_cost_chart(
    years: int,
    mech_cumulative,
    elec_cumulative,
    hybrid_cumulative,
    visibility: dict,
) -> go.Figure:
    """Build the cumulative cost-over-time line chart.

    Displays three smooth lines (one per system) showing cumulative capital
    cost from year 0 to the selected time horizon. No data point markers.
    Hover shows dollar amount and year. External shared legend controls
    visibility; in-chart legend is hidden.

    Parameters
    ----------
    years : int
        Number of years to display (x-axis 0 to years inclusive).
    mech_cumulative : array-like
        Cumulative cost array for mechanical system, length years+1.
    elec_cumulative : array-like
        Cumulative cost array for electrical system, length years+1.
    hybrid_cumulative : array-like
        Cumulative cost array for hybrid system, length years+1.
    visibility : dict
        Store dict {"mechanical": bool, "electrical": bool, "hybrid": bool}.

    Returns
    -------
    go.Figure
    """
    x = list(range(0, years + 1))

    systems = [
        ("Mechanical", mech_cumulative,  SYSTEM_COLORS["Mechanical"]),
        ("Electrical", elec_cumulative,  SYSTEM_COLORS["Electrical"]),
        ("Hybrid",     hybrid_cumulative, SYSTEM_COLORS["Hybrid"]),
    ]

    fig = go.Figure()
    for name, cumulative, color in systems:
        key = name.lower()
        fig.add_trace(go.Scatter(
            x=x,
            y=list(cumulative[: years + 1]),
            mode="lines",
            name=name,
            line=dict(color=color, width=2.5),
            visible=_visibility(visibility, key),
            hovertemplate=f"{name}: %{{y:$,.0f}} at Year %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Cost (USD)",
        showlegend=False,
        uirevision="static",
        transition=_TRANSITION,
        margin=_MARGIN,
        hovermode="x unified",
    )
    return fig


def build_land_chart(
    mech_land: float,
    elec_land: float,
    hybrid_land: float,
    visibility: dict,
) -> go.Figure:
    """Build the land area grouped bar chart.

    Compares total physical footprint (m²) across all three systems.
    Values shown on hover only — no bar labels. Hybrid shows 0 in Phase 3.

    Parameters
    ----------
    mech_land : float
        Mechanical system land area in m².
    elec_land : float
        Electrical system land area in m².
    hybrid_land : float
        Hybrid system land area in m² (0 placeholder in Phase 3).
    visibility : dict
        Store dict {"mechanical": bool, "electrical": bool, "hybrid": bool}.

    Returns
    -------
    go.Figure
    """
    systems = [
        ("Mechanical", mech_land,  SYSTEM_COLORS["Mechanical"]),
        ("Electrical", elec_land,  SYSTEM_COLORS["Electrical"]),
        ("Hybrid",     hybrid_land, SYSTEM_COLORS["Hybrid"]),
    ]

    fig = go.Figure()
    for name, value, color in systems:
        key = name.lower()
        fig.add_trace(go.Bar(
            x=["Land Area"],
            y=[value],
            name=name,
            marker_color=color,
            visible=_visibility(visibility, key),
            hovertemplate=f"{name}: %{{y:,.0f}} m<sup>2</sup><extra></extra>",
            text=None,
        ))

    fig.update_layout(
        barmode="group",
        yaxis_title="Area (m\u00b2)",
        showlegend=False,
        uirevision="static",
        transition=_TRANSITION,
        margin=_MARGIN,
    )
    return fig


def build_turbine_chart(
    mech_count: int,
    elec_count: int,
    hybrid_count: int,
    visibility: dict,
) -> go.Figure:
    """Build the wind turbine count grouped bar chart.

    Compares the number of wind turbines per system. Integer y-axis.
    Hybrid shows 0 in Phase 3.

    Parameters
    ----------
    mech_count : int
        Number of wind turbines in the mechanical system.
    elec_count : int
        Number of wind turbines in the electrical system.
    hybrid_count : int
        Number of wind turbines in the hybrid system (0 in Phase 3).
    visibility : dict
        Store dict {"mechanical": bool, "electrical": bool, "hybrid": bool}.

    Returns
    -------
    go.Figure
    """
    systems = [
        ("Mechanical", mech_count,  SYSTEM_COLORS["Mechanical"]),
        ("Electrical", elec_count,  SYSTEM_COLORS["Electrical"]),
        ("Hybrid",     hybrid_count, SYSTEM_COLORS["Hybrid"]),
    ]

    fig = go.Figure()
    for name, count, color in systems:
        key = name.lower()
        fig.add_trace(go.Bar(
            x=["Wind Turbines"],
            y=[count],
            name=name,
            marker_color=color,
            visible=_visibility(visibility, key),
            hovertemplate=f"{name}: %{{y}} turbines<extra></extra>",
            text=None,
        ))

    fig.update_layout(
        barmode="group",
        yaxis_title="Count",
        yaxis=dict(dtick=1),
        showlegend=False,
        uirevision="static",
        transition=_TRANSITION,
        margin=_MARGIN,
    )
    return fig


def build_pie_chart(
    mech_energy: dict,
    elec_energy: dict,
    hybrid_energy: dict,
    visibility: dict,
) -> go.Figure:
    """Build three side-by-side pie charts showing energy breakdown by process stage.

    One pie per system, arranged horizontally using domain positioning. No slice
    labels — percentages shown on hover only. Empty energy dicts (Hybrid in
    Phase 3) render as a single grey "No data" slice to avoid go.Pie errors
    with empty values. Each pie has a system name annotation below it.

    Parameters
    ----------
    mech_energy : dict[str, float]
        Stage -> kW dict for mechanical system.
    elec_energy : dict[str, float]
        Stage -> kW dict for electrical system.
    hybrid_energy : dict[str, float]
        Stage -> kW dict for hybrid system (empty in Phase 3).
    visibility : dict
        Store dict {"mechanical": bool, "electrical": bool, "hybrid": bool}.

    Returns
    -------
    go.Figure
    """
    fig = go.Figure()

    spacing = 0.05
    width = (1.0 - 2 * spacing) / 3

    systems = [
        ("Mechanical", mech_energy,  0),
        ("Electrical", elec_energy,  1),
        ("Hybrid",     hybrid_energy, 2),
    ]

    annotations = []
    for label, energy_dict, index in systems:
        key = label.lower()
        x_start = index * (width + spacing)
        x_end = x_start + width
        midpoint = x_start + width / 2

        # Phase 3: Hybrid has no energy data — use a grey "No data" placeholder
        if not energy_dict:
            labels_list = ["No data"]
            values_list = [1]
            marker = dict(colors=["#e0e0e0"])
        else:
            labels_list = list(energy_dict.keys())
            values_list = list(energy_dict.values())
            marker = dict()

        fig.add_trace(go.Pie(
            labels=labels_list,
            values=values_list,
            name=label,
            domain=dict(x=[x_start, x_end], y=[0.15, 1.0]),
            textinfo="none",
            hovertemplate="%{label}: %{percent}<extra></extra>",
            showlegend=False,
            visible=_visibility(visibility, key),
            marker=marker,
        ))

        annotations.append(dict(
            text=label,
            x=midpoint,
            y=0.05,
            showarrow=False,
            font=dict(size=12),
        ))

    fig.update_layout(
        annotations=annotations,
        uirevision="static",
        transition=_TRANSITION,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# Chart section layout factory
# ──────────────────────────────────────────────────────────────────────────────

def make_chart_section() -> html.Div:
    """Build the full System Comparison chart section layout.

    Returns the complete component tree including:
    - Section heading
    - Control panel card with both sliders (time horizon and battery/tank)
    - Shared legend row with clickable system badges
    - dcc.Store for legend visibility state
    - 2x2 responsive chart grid

    No callbacks are defined in this function — they are registered in Plan 02
    (03-02-PLAN.md). All IDs defined here are referenced by those callbacks.

    Returns
    -------
    html.Div
        Full chart section layout ready to embed in system_view.py.
    """

    def _chart_card(title: str, description: str, graph_id: str) -> dbc.Col:
        """Helper: returns a dbc.Col wrapping a titled chart card."""
        return dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Strong(title),
                    html.P(description, className="text-muted small mb-1"),
                    dcc.Graph(
                        id=graph_id,
                        config={"displayModeBar": False},
                    ),
                ]),
                className="shadow-sm h-100",
            ),
            lg=6,
            xs=12,
        )

    # ── Control panel ─────────────────────────────────────────────────────────
    control_panel = dbc.Card(
        dbc.CardBody(
            dbc.Row([
                # Left column: Time Horizon slider
                dbc.Col(
                    [
                        html.Div([
                            html.Strong("Time Horizon"),
                            html.Small(
                                " \u2014 Adjust the projection period",
                                className="text-muted ms-1",
                            ),
                        ], className="mb-1"),
                        dcc.Slider(
                            id="slider-time-horizon",
                            min=1,
                            max=50,
                            step=1,
                            value=50,
                            marks={1: "1yr", 25: "25yr", 50: "50yr"},
                            tooltip={"always_visible": True, "placement": "bottom"},
                            updatemode="drag",
                        ),
                        html.Span(
                            id="label-years",
                            children="50 years",
                            className="fw-bold ms-2",
                        ),
                    ],
                    width=6,
                ),
                # Right column: Battery / Tank slider
                dbc.Col(
                    [
                        html.Div([
                            html.Strong("Battery / Tank Tradeoff"),
                            html.Small(
                                " \u2014 Adjust electrical system storage mix",
                                className="text-muted ms-1",
                            ),
                        ], className="mb-1"),
                        dcc.Slider(
                            id="slider-battery",
                            min=0,
                            max=1,
                            step=0.001,
                            value=0.5,
                            marks={},
                            tooltip={"always_visible": False},
                            updatemode="drag",
                        ),
                        html.Span(
                            id="label-battery-ratio",
                            children="50% Battery / 50% Tank",
                            className="fw-bold ms-2",
                        ),
                        html.Span(
                            id="label-elec-cost",
                            children="",
                            className="text-muted ms-2",
                        ),
                    ],
                    width=6,
                ),
            ])
        ),
        className="shadow-sm mb-3",
        style={"backgroundColor": "#f8f9fa"},
    )

    # ── Shared legend badges ──────────────────────────────────────────────────
    legend_row = html.Div(
        [
            html.Strong("Systems: ", className="me-2"),
            dbc.Badge(
                "Mechanical",
                id="legend-btn-mechanical",
                style={
                    "cursor": "pointer",
                    "backgroundColor": SYSTEM_COLORS["Mechanical"],
                    "fontSize": "0.9rem",
                },
                className="me-2 p-2",
                pill=True,
            ),
            dbc.Badge(
                "Electrical",
                id="legend-btn-electrical",
                style={
                    "cursor": "pointer",
                    "backgroundColor": SYSTEM_COLORS["Electrical"],
                    "fontSize": "0.9rem",
                },
                className="me-2 p-2",
                pill=True,
            ),
            dbc.Badge(
                "Hybrid",
                id="legend-btn-hybrid",
                style={
                    "cursor": "pointer",
                    "backgroundColor": SYSTEM_COLORS["Hybrid"],
                    "fontSize": "0.9rem",
                },
                className="me-2 p-2",
                pill=True,
            ),
        ],
        className="mb-3 d-flex align-items-center",
    )

    # ── Legend visibility store ───────────────────────────────────────────────
    legend_store = dcc.Store(
        id="store-legend-visibility",
        data={"mechanical": True, "electrical": True, "hybrid": True},
    )

    # ── 2x2 chart grid ────────────────────────────────────────────────────────
    row1 = dbc.Row(
        [
            _chart_card(
                "Cost Over Time",
                "Cumulative capital cost per year",
                "chart-cost",
            ),
            _chart_card(
                "Land Area",
                "Total footprint per system (m\u00b2)",
                "chart-land",
            ),
        ],
        className="mb-3",
    )

    row2 = dbc.Row(
        [
            _chart_card(
                "Wind Turbine Count",
                "Number of turbines per system",
                "chart-turbine",
            ),
            _chart_card(
                "Energy Breakdown",
                "Energy use by process stage (kW)",
                "chart-pie",
            ),
        ],
        className="mb-3",
    )

    return html.Div([
        html.H4("System Comparison", className="mt-4 mb-3"),
        legend_store,
        control_panel,
        legend_row,
        row1,
        row2,
    ])
