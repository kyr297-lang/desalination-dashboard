"""
src/layout/overview.py
======================
Landing overview layout with three system selection cards.

Exports
-------
create_overview_layout()
    Returns the landing page Dash component tree with one card per system
    (Mechanical, Electrical, Hybrid).  Clicking "Explore" on a card sets the
    active-system dcc.Store, triggering navigation to the system tab view.
"""

from dash import html
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS

# ──────────────────────────────────────────────────────────────────────────────
# System card content definitions
# ──────────────────────────────────────────────────────────────────────────────

_SYSTEM_CARDS = [
    {
        "label": "Mechanical",
        "key": "mechanical",
        "description": (
            "Uses wind-driven mechanical pumps to directly pressurize seawater "
            "through reverse osmosis membranes. Requires multiple large turbines "
            "but avoids electrical conversion losses."
        ),
    },
    {
        "label": "Electrical",
        "key": "electrical",
        "description": (
            "Converts wind energy to electricity to power pumps, with battery or "
            "tank storage options for continuous operation. More flexible but adds "
            "conversion and storage costs."
        ),
    },
    {
        "label": "Hybrid",
        "key": "hybrid",
        "description": (
            "Combine components from both systems to create a custom desalination "
            "solution tailored to specific site conditions."
        ),
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Layout factory
# ──────────────────────────────────────────────────────────────────────────────

def create_overview_layout() -> html.Div:
    """Return the landing overview component tree.

    Builds three system cards arranged in equal-width columns.  Each card has a
    coloured header matching the system's SYSTEM_COLORS entry, a short
    description, and an "Explore" button that triggers navigation via the
    active-system dcc.Store.

    Returns
    -------
    html.Div
        Top-level container holding the intro text and card row.
    """
    cards = []
    for system in _SYSTEM_CARDS:
        card = dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        system["label"],
                        style={
                            "backgroundColor": SYSTEM_COLORS[system["label"]],
                            "color": "white",
                            "fontWeight": "600",
                        },
                    ),
                    dbc.CardBody(
                        [
                            html.P(system["description"], className="text-muted small"),
                            dbc.Button(
                                "Explore",
                                id={"type": "system-card-btn", "index": system["key"]},
                                color="secondary",
                                outline=True,
                                size="sm",
                                className="mt-auto",
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                className="h-100 shadow-sm",
            ),
            width=4,
        )
        cards.append(card)

    return html.Div(
        [
            html.P(
                "Select a desalination system to explore its equipment and performance.",
                className="text-muted mb-3",
            ),
            dbc.Row(cards, className="g-3"),
        ]
    )
