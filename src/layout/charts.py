"""
src/layout/charts.py
====================
Plotly figure builders, chart section layout, and callbacks for the System
Comparison panel.

Provides four pure figure-building functions, one layout factory, and three
Dash callbacks that wire sliders and legend toggles to the chart figures.

Exports
-------
set_data(data) -> None
build_cost_chart(years, mech_cumulative, elec_cumulative, hybrid_cumulative, visibility) -> go.Figure
build_land_chart(mech_land, elec_land, hybrid_land, visibility) -> go.Figure
build_turbine_chart(mech_count, elec_count, hybrid_count, visibility) -> go.Figure
build_pie_chart(mech_energy, elec_energy, hybrid_energy, visibility) -> go.Figure
make_chart_section() -> html.Div
update_charts(years, battery_fraction, visibility, slots, tds_ppm, depth_m) -> tuple
toggle_legend(n_mech, n_elec, n_hybrid, visibility) -> dict
update_badge_styles(visibility) -> tuple
"""

import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS
from src.data.processing import compute_chart_data, compute_hybrid_df, interpolate_battery_cost, battery_ratio_label, fmt_cost


# ──────────────────────────────────────────────────────────────────────────────
# Module-level data reference — mirrors set_data() pattern from shell.py.
# Populated by set_data() called from app.py after data is loaded.
# ──────────────────────────────────────────────────────────────────────────────

_data = None


def set_data(data: dict) -> None:
    """Store the loaded data dict for use in the chart callbacks.

    Called once from app.py after DATA is loaded, before any callbacks fire.
    Mirrors the pattern used in shell.py to avoid circular imports and
    callback data loading.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().
    """
    global _data
    _data = data


# ──────────────────────────────────────────────────────────────────────────────
# Shared layout constants
# ──────────────────────────────────────────────────────────────────────────────

_TRANSITION = {"duration": 300, "easing": "cubic-in-out"}
_MARGIN = dict(l=75, r=20, t=10, b=40)


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
        yaxis=dict(
            tickprefix="$",
            tickformat="~s",
        ),
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
        yaxis_title="Wind Turbines",
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
        dbc.CardBody([
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
                            updatemode="mouseup",
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
                            updatemode="mouseup",
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
            ]),
            dbc.Row([
                # Left column: TDS slider
                dbc.Col(
                    [
                        html.Div([
                            html.Strong("Source Water Salinity"),
                            html.Small(
                                " \u2014 Adjust to model RO energy demand",
                                className="text-muted ms-1",
                            ),
                        ], className="mb-1"),
                        dcc.Slider(
                            id="slider-tds",
                            min=0,
                            max=1900,
                            step=1,
                            value=950,
                            marks={0: "0", 950: "950", 1900: "1900"},
                            tooltip={"always_visible": True, "placement": "bottom"},
                            updatemode="drag",
                        ),
                        html.Span(
                            id="label-tds",
                            children="950 PPM",
                            className="fw-bold ms-2",
                        ),
                    ],
                    width=6,
                ),
                # Right column: Depth slider
                dbc.Col(
                    [
                        html.Div([
                            html.Strong("Water Source Depth"),
                            html.Small(
                                " \u2014 Adjust to model pump energy demand",
                                className="text-muted ms-1",
                            ),
                        ], className="mb-1"),
                        dcc.Slider(
                            id="slider-depth",
                            min=0,
                            max=1900,
                            step=1,
                            value=950,
                            marks={0: "0", 950: "950", 1900: "1900"},
                            tooltip={"always_visible": True, "placement": "bottom"},
                            updatemode="drag",
                        ),
                        html.Span(
                            id="label-depth",
                            children="950 m",
                            className="fw-bold ms-2",
                        ),
                    ],
                    width=6,
                ),
            ], className="mt-3"),
        ]),
        className="shadow-sm mb-3 chart-controls",
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


# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────

@callback(
    Output("chart-cost", "figure"),
    Output("chart-land", "figure"),
    Output("chart-turbine", "figure"),
    Output("chart-pie", "figure"),
    Output("label-years", "children"),
    Output("label-battery-ratio", "children"),
    Output("label-elec-cost", "children"),
    Output("label-tds", "children"),
    Output("label-depth", "children"),
    Input("slider-time-horizon", "value"),
    Input("slider-battery", "value"),
    Input("store-legend-visibility", "data"),
    Input("store-hybrid-slots", "data"),
    Input("slider-tds", "value"),
    Input("slider-depth", "value"),
)
def update_charts(years, battery_fraction, visibility, slots, tds_ppm, depth_m):
    """Master chart update callback.

    Fires whenever the time horizon slider, battery/tank slider, TDS slider,
    depth slider, legend visibility store, or hybrid slot store changes.
    Computes all chart data in one call and returns four updated figures plus
    five live label strings.

    Parameters
    ----------
    years : int
        Time horizon from the time horizon slider (1-50).
    battery_fraction : float
        Battery/tank split from the battery slider (0.0-1.0).
    visibility : dict
        Legend visibility store {"mechanical": bool, "electrical": bool, "hybrid": bool}.
    slots : dict or None
        Hybrid slot store mapping stage names to selected equipment names.
        When all 5 slots are filled, hybrid data is computed and passed to
        compute_chart_data. When any slot is None, hybrid uses placeholder zeros.
    tds_ppm : float
        Source water salinity in PPM from the TDS slider (0-1900, default 950).
    depth_m : float
        Water source depth in metres from the depth slider (0-1900, default 950).

    Returns
    -------
    tuple
        (cost_fig, land_fig, turbine_fig, pie_fig, label_years, label_ratio,
         label_cost, label_tds, label_depth)
    """
    # Guard: if data not yet loaded, return empty figures and blank labels
    if _data is None:
        empty = go.Figure()
        return empty, empty, empty, empty, "", "", "", "", ""

    # Build hybrid_df if gate is open (all 5 slots filled)
    hybrid_df = None
    if slots is not None and all(v is not None for v in slots.values()):
        hybrid_df = compute_hybrid_df(slots, _data)

    cd = compute_chart_data(_data, battery_fraction, years, hybrid_df=hybrid_df, tds_ppm=tds_ppm, depth_m=depth_m)

    cost_fig = build_cost_chart(
        years,
        cd["cost_over_time"]["mechanical"],
        cd["cost_over_time"]["electrical"],
        cd["cost_over_time"]["hybrid"],
        visibility,
    )
    land_fig = build_land_chart(
        cd["land_area"]["mechanical"],
        cd["land_area"]["electrical"],
        cd["land_area"]["hybrid"],
        visibility,
    )
    turbine_fig = build_turbine_chart(
        cd["turbine_count"]["mechanical"],
        cd["turbine_count"]["electrical"],
        cd["turbine_count"]["hybrid"],
        visibility,
    )
    pie_fig = build_pie_chart(
        cd["energy_breakdown"]["mechanical"],
        cd["energy_breakdown"]["electrical"],
        cd["energy_breakdown"]["hybrid"],
        visibility,
    )

    label_years = f"{years} year{'s' if years != 1 else ''}"
    label_ratio = battery_ratio_label(battery_fraction)
    label_cost = f"Electrical total: {fmt_cost(cd['electrical_total_cost'])}"
    label_tds = f"{int(round(tds_ppm))} PPM"
    label_depth = f"{int(round(depth_m))} m"

    return cost_fig, land_fig, turbine_fig, pie_fig, label_years, label_ratio, label_cost, label_tds, label_depth


@callback(
    Output("store-legend-visibility", "data"),
    Input("legend-btn-mechanical", "n_clicks"),
    Input("legend-btn-electrical", "n_clicks"),
    Input("legend-btn-hybrid", "n_clicks"),
    State("store-legend-visibility", "data"),
    prevent_initial_call=True,
)
def toggle_legend(n_mech, n_elec, n_hybrid, visibility):
    """Toggle a system's visibility in the legend store.

    Uses ctx.triggered_id to identify which badge was clicked, then flips
    that system's boolean in the visibility dict.

    Parameters
    ----------
    n_mech : int or None
        Number of times Mechanical badge was clicked.
    n_elec : int or None
        Number of times Electrical badge was clicked.
    n_hybrid : int or None
        Number of times Hybrid badge was clicked.
    visibility : dict
        Current legend visibility store.

    Returns
    -------
    dict
        Updated visibility dict with one system's bool toggled.
    """
    _id_to_key = {
        "legend-btn-mechanical": "mechanical",
        "legend-btn-electrical": "electrical",
        "legend-btn-hybrid": "hybrid",
    }
    triggered = ctx.triggered_id
    key = _id_to_key.get(triggered)
    if key is None:
        return visibility

    updated = dict(visibility)
    updated[key] = not updated[key]
    return updated


@callback(
    Output("legend-btn-mechanical", "style"),
    Output("legend-btn-electrical", "style"),
    Output("legend-btn-hybrid", "style"),
    Input("store-legend-visibility", "data"),
)
def update_badge_styles(visibility):
    """Update legend badge opacity to reflect visibility state.

    Fully visible systems have opacity 1.0; hidden systems have opacity 0.4
    with a line-through text decoration to signal toggled-off state.

    Parameters
    ----------
    visibility : dict
        Legend visibility store {"mechanical": bool, "electrical": bool, "hybrid": bool}.

    Returns
    -------
    tuple[dict, dict, dict]
        Style dicts for Mechanical, Electrical, and Hybrid badges.
    """
    systems = [
        ("mechanical", "Mechanical"),
        ("electrical", "Electrical"),
        ("hybrid",     "Hybrid"),
    ]
    styles = []
    for key, label in systems:
        is_visible = visibility.get(key, True)
        style = {
            "cursor": "pointer",
            "backgroundColor": SYSTEM_COLORS[label],
            "fontSize": "0.9rem",
            "opacity": "1" if is_visible else "0.4",
        }
        if not is_visible:
            style["textDecoration"] = "line-through"
        styles.append(style)

    return styles[0], styles[1], styles[2]
