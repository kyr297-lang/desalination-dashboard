"""
src/layout/system_view.py
=========================
System tab view: breadcrumb, tab bar, scorecard, and equipment grid assembly.

Exports
-------
create_system_view_layout(active_system, data)
    Returns the full system view component tree for the given active system.
"""

from dash import html
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS
from src.layout.scorecard import make_scorecard_table
from src.layout.equipment_grid import make_equipment_section
from src.layout.charts import make_chart_section
from src.layout.hybrid_builder import make_hybrid_builder


# ──────────────────────────────────────────────────────────────────────────────
# System display metadata
# ──────────────────────────────────────────────────────────────────────────────

_SYSTEMS = [
    {"key": "mechanical",  "label": "Mechanical"},
    {"key": "electrical",  "label": "Electrical"},
    {"key": "hybrid",      "label": "Hybrid"},
]


# ──────────────────────────────────────────────────────────────────────────────
# Layout factory
# ──────────────────────────────────────────────────────────────────────────────

def create_system_view_layout(active_system: str, data: dict) -> html.Div:
    """Build the system tab view component tree.

    Assembles:
    1. "Back to Overview" breadcrumb link
    2. Tab bar with Mechanical / Electrical / Hybrid tabs
    3. Scorecard container (dynamic — updated via callback when hybrid slot store changes)
    4. Equipment section for the active system
    5. Chart section (with gate overlay when viewing hybrid tab)

    The tab bar is rendered as a static component with active_tab set each time
    the layout is re-rendered — this avoids the circular callback dependency
    that would arise from using a tab active_tab Output.

    Per user decision: tabs are the system selector; the sidebar is separate.
    Active tab label uses borderBottom highlight instead of backgroundColor
    (avoids a known Bootstrap + Dash tab styling bug).

    For the Hybrid tab: the hybrid builder pipeline is rendered above the chart
    section. The chart section is wrapped with a gate overlay container that
    shows a semi-transparent message until all 5 slots are filled.

    Parameters
    ----------
    active_system : str
        Currently selected system key ("mechanical", "electrical", "hybrid").
    data : dict
        Full data dictionary from load_data().

    Returns
    -------
    html.Div
        Full system view component tree.
    """
    # ── 1. Breadcrumb ─────────────────────────────────────────────────────────
    breadcrumb = html.A(
        "\u2190 Overview",
        id="back-to-overview",
        href="#",
        className="text-muted small mb-2 d-inline-block",
        style={"cursor": "pointer", "textDecoration": "none"},
    )

    # ── 2. Tab bar ────────────────────────────────────────────────────────────
    tabs = []
    for sys in _SYSTEMS:
        key = sys["key"]
        label = sys["label"]
        system_color = SYSTEM_COLORS.get(label, "#6c757d")
        is_active = (key == active_system)

        tab = dbc.Tab(
            label=label,
            tab_id=key,
            label_style={"color": "#6c757d"},
            active_label_style={
                "color": system_color,
                "fontWeight": "bold",
                "borderBottom": f"3px solid {system_color}",
            } if is_active else {"color": "#6c757d"},
        )
        tabs.append(tab)

    tab_bar = dbc.Tabs(
        tabs,
        id="system-tabs",
        active_tab=active_system,
    )

    # ── 3. Hybrid builder (hybrid tab only) ───────────────────────────────────
    hybrid_builder_section = None
    if active_system == "hybrid":
        hybrid_builder_section = make_hybrid_builder(data)

    # ── 4. Scorecard container (dynamic via callback) ─────────────────────────
    # The initial render shows the 2-system scorecard. The scorecard callback
    # updates scorecard-container when store-hybrid-slots changes.
    # The export button is a sibling ABOVE scorecard-container inside the
    # CardBody so it is NOT destroyed when the scorecard callback re-renders
    # the scorecard-container children.
    initial_scorecard = make_scorecard_table(data["mechanical"], data["electrical"])
    scorecard_container = html.Div(
        initial_scorecard,
        id="scorecard-container",
    )

    # ── 5. Comparison text (populated by callback when gate is open) ──────────
    comparison_text_div = html.Div(id="comparison-text")

    # ── Export / Print button (hidden in print via no-print class) ────────────
    export_btn = dbc.Button(
        "Export / Print",
        id="export-btn",
        color="secondary",
        outline=True,
        size="sm",
        className="mb-2 no-print",
    )

    # ── 6. Equipment section ──────────────────────────────────────────────────
    if active_system == "hybrid":
        # Hybrid equipment is callback-driven (updates when slots change)
        equipment = html.Div(id="hybrid-equipment-container")
    else:
        system_df = data.get(active_system, data.get("mechanical"))
        equipment = make_equipment_section(system_df, active_system, data)

    # ── 7. Chart section (with gate overlay for hybrid tab) ───────────────────
    chart_section = make_chart_section()

    if active_system == "hybrid":
        # Gate overlay: shown when slots are incomplete; hidden via callback
        gate_overlay = html.Div(
            html.Div(
                [
                    html.Span(
                        "\u26a0",  # warning symbol
                        style={"fontSize": "2rem", "marginBottom": "0.5rem"},
                    ),
                    html.P(
                        "Fill all 5 slots to see hybrid results",
                        className="fw-bold mb-1",
                        style={"fontSize": "1.1rem"},
                    ),
                    html.P(
                        "Use the dropdowns above to select equipment for each stage.",
                        className="text-muted small",
                    ),
                ],
                style={
                    "textAlign": "center",
                    "padding": "2rem",
                },
            ),
            id="hybrid-gate-overlay",
            style={
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
            },
        )
        chart_wrapper = html.Div(
            [gate_overlay, chart_section],
            style={"position": "relative"},
        )
    else:
        chart_wrapper = chart_section

    # ── Assemble layout ───────────────────────────────────────────────────────
    # Scorecard section wrapped in a Card. The export button is inside the
    # CardBody ABOVE scorecard-container so the callback that re-renders
    # scorecard-container children does not destroy the button.
    scorecard_card = dbc.Card(
        dbc.CardBody([
            export_btn,
            scorecard_container,
            comparison_text_div,
        ]),
        className="shadow-sm mb-3",
    )

    main_content_children = [
        scorecard_card,
        html.Hr(className="my-3"),
        equipment,
    ]

    top_level_children = [
        breadcrumb,
        tab_bar,
    ]

    if hybrid_builder_section is not None:
        top_level_children.append(
            html.Div(hybrid_builder_section, className="mt-3")
        )

    top_level_children.append(
        html.Div(main_content_children, className="mt-3")
    )
    top_level_children.append(chart_wrapper)

    return html.Div(top_level_children)
