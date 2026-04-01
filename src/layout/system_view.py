"""
src/layout/system_view.py
=========================
System tab view: breadcrumb, tab bar, scorecard, and equipment grid assembly.

Exports
-------
create_system_view_layout(active_system, data)
    Returns the full system view component tree for the given active system.

All three systems (mechanical, electrical, hybrid) render identically:
- Static equipment table grouped by process stage
- 3-column scorecard from BOM data immediately on page load
- No gate overlay, slot dropdowns, or slot counter
"""

from dash import html
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS
from src.layout.scorecard import make_scorecard_table
from src.layout.equipment_grid import make_equipment_section
from src.layout.charts import make_chart_section
from src.data.processing import compute_scorecard_metrics, generate_comparison_text


# ──────────────────────────────────────────────────────────────────────────────
# System display metadata
# ──────────────────────────────────────────────────────────────────────────────

_SYSTEMS = [
    {"key": "mechanical",  "label": "Mechanical"},
    {"key": "electrical",  "label": "Electrical"},
    {"key": "hybrid",      "label": "Hybrid"},
]

_DIAGRAM_FILES = {
    "mechanical": "/assets/mechanical-layout.png",
    "electrical": "/assets/electrical-layout.png",
    "hybrid": "/assets/hybrid-layout.png",
}

_DIAGRAM_CARD_CLASSES = {
    "mechanical": "shadow-sm mb-3 system-card-mechanical",
    "electrical": "shadow-sm mb-3 system-card-electrical",
    "hybrid": "shadow-sm mb-3",
}


# ──────────────────────────────────────────────────────────────────────────────
# Layout factory
# ──────────────────────────────────────────────────────────────────────────────

def create_system_view_layout(active_system: str, data: dict) -> html.Div:
    """Build the system tab view component tree.

    Assembles:
    1. "Back to Overview" breadcrumb link
    2. Tab bar with Mechanical / Electrical / Hybrid tabs
    3. Scorecard container — always 3-column from BOM data, no gating
    4. Equipment section for the active system (static, same pattern for all systems)
    5. Chart section (no gate overlay)

    The tab bar is rendered as a static component with active_tab set each time
    the layout is re-rendered — this avoids the circular callback dependency
    that would arise from using a tab active_tab Output.

    Per user decision: tabs are the system selector; the sidebar is separate.
    Active tab label uses borderBottom highlight instead of backgroundColor
    (avoids a known Bootstrap + Dash tab styling bug).

    All three systems render equipment identically via make_equipment_section.
    The hybrid system is a pre-defined configuration loaded from data.xlsx —
    not user-assembled.

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
    breadcrumb = html.Button(
        "\u2190 Overview",
        id="back-to-overview",
        className="btn btn-link text-muted small mb-2 p-0 no-print",
        style={"textDecoration": "none", "verticalAlign": "baseline"},
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

    # ── Diagram card ────────────────────────────────────────────────────────
    diagram_src = _DIAGRAM_FILES.get(active_system, "")
    diagram_card = dbc.Card(
        dbc.CardBody(
            html.Img(
                src=diagram_src,
                style={"width": "100%", "maxWidth": "820px", "height": "auto", "margin": "0 auto"},
                className="d-block",
                alt=f"{active_system.capitalize()} system layout diagram",
            )
        ),
        className=_DIAGRAM_CARD_CLASSES.get(active_system, "shadow-sm mb-3"),
    )

    # ── 3. Scorecard — always 3-column from BOM data ──────────────────────────
    # All three DataFrames are available from load_data(); no gating required.
    initial_scorecard = make_scorecard_table(
        data["mechanical"], data["electrical"], data.get("hybrid")
    )
    scorecard_container = html.Div(
        initial_scorecard,
        id="scorecard-container",
    )

    # ── 4. Comparison text — generated from BOM metrics at render time ────────
    metrics = compute_scorecard_metrics(
        data["mechanical"], data["electrical"], data.get("hybrid")
    )
    if "hybrid" in metrics:
        comparison_str = generate_comparison_text(
            metrics["hybrid"], metrics["mechanical"], metrics["electrical"]
        )
        comparison_content = html.P(
            comparison_str,
            className="text-muted small mt-2",
            style={"fontStyle": "italic"},
        )
    else:
        comparison_content = None
    comparison_text_div = html.Div(comparison_content, id="comparison-text")

    # ── Export / Print button (hidden in print via no-print class) ────────────
    export_btn = dbc.Button(
        "Export / Print",
        id="export-btn",
        color="secondary",
        outline=True,
        size="sm",
        className="mb-2 no-print",
    )

    # ── 5. Equipment section — same pattern for all three systems ─────────────
    system_df = data.get(active_system, data.get("mechanical"))
    equipment = make_equipment_section(system_df, active_system, data)

    # ── 6. Chart section (no gate overlay) ───────────────────────────────────
    chart_wrapper = make_chart_section()

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

    equipment_card = dbc.Card(
        dbc.CardBody(equipment),
        className="shadow-sm mb-3",
    )

    main_content_children = [
        diagram_card,
        scorecard_card,
        equipment_card,
    ]

    # ── 3b. System badge (inserted after tab_bar, visible in print) ──────────
    label = active_system.capitalize()
    color = SYSTEM_COLORS.get(label, "#6c757d")
    system_badge = html.Div(
        dbc.Badge(
            label,
            pill=True,
            style={"backgroundColor": color, "fontSize": "0.85rem"},
        ),
        className="mt-2 mb-1",
        # NOTE: do NOT add no-print class — badge must appear in PDF export
    )

    top_level_children = [
        breadcrumb,
        tab_bar,
        system_badge,
        html.Div(main_content_children, className="mt-3"),
        chart_wrapper,
    ]

    return html.Div(top_level_children)
