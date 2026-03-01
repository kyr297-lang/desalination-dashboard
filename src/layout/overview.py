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
            "Click Explore to view cost, land area, and energy data for the "
            "mechanical system. Uses wind-driven pumps to pressurize seawater "
            "through reverse osmosis membranes — no electrical conversion losses."
        ),
    },
    {
        "label": "Electrical",
        "key": "electrical",
        "description": (
            "Click Explore to view cost, land area, and energy data for the "
            "electrical system. Converts wind to electricity with adjustable "
            "battery/tank storage — use the slider to compare storage options."
        ),
    },
    {
        "label": "Hybrid",
        "key": "hybrid",
        "description": (
            "Click Explore to build a custom system. Select one piece of equipment "
            "for each process stage to see its combined cost, land, and energy "
            "performance compared with the two standard systems."
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

    intro_card = dbc.Card(
        [
            dbc.CardHeader(
                "About This Project",
                style={"fontWeight": "600"},
            ),
            dbc.CardBody(
                [
                    html.P(
                        "This dashboard was built as part of a Fall 2025\u2013Spring 2026 "
                        "senior design class to help students compare wind-powered "
                        "desalination system configurations. Start by clicking Explore "
                        "on any system card below to compare costs, land use, and "
                        "energy requirements.",
                        className="mb-2 small",
                    ),
                    html.P(
                        [
                            html.Span("Contributors: ", className="fw-semibold"),
                            "Amogh Herle, Sofia Ijazi, Kevin Ren, Kyler Sanders",
                        ],
                        className="mb-0 small text-muted",
                    ),
                ]
            ),
        ],
        className="mb-3 shadow-sm",
    )

    return html.Div(
        [
            intro_card,
            dbc.Row(cards, className="g-3"),
        ]
    )
