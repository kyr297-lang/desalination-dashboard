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
    3. Scorecard table (Mechanical vs Electrical, Hybrid deferred)
    4. Equipment section for the active system

    The tab bar is rendered as a static component with active_tab set each time
    the layout is re-rendered — this avoids the circular callback dependency
    that would arise from using a tab active_tab Output.

    Per user decision: tabs are the system selector; the sidebar is separate.
    Active tab label uses borderBottom highlight instead of backgroundColor
    (avoids a known Bootstrap + Dash tab styling bug).

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

    # ── 3. Scorecard table ────────────────────────────────────────────────────
    scorecard = make_scorecard_table(data["mechanical"], data["electrical"])

    # ── 4. Equipment section ──────────────────────────────────────────────────
    system_df = data.get(active_system, data.get("mechanical"))
    equipment = make_equipment_section(system_df, active_system, data)

    return html.Div([
        breadcrumb,
        tab_bar,
        html.Div(
            [
                scorecard,
                html.Hr(className="my-3"),
                equipment,
            ],
            className="mt-3",
        ),
    ])
