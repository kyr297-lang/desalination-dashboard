"""
src/layout/shell.py
===================
App shell layout: top header bar, collapsible sidebar, and content area.

create_layout(data) returns the full Dash component tree.  The sidebar toggle
callback is registered here via the @callback decorator (Dash 4.0 style).
"""

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

from src.config import SYSTEM_COLORS  # available for future use by child components

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

SIDEBAR_WIDTH_EXPANDED = "220px"
SIDEBAR_WIDTH_COLLAPSED = "0px"

_SIDEBAR_STYLE_BASE = {
    "overflow": "hidden",
    "backgroundColor": "#f8f9fa",
    "padding": "1rem 0",
    "transition": "width 0.2s ease",
    "flexShrink": "0",
}


# ──────────────────────────────────────────────────────────────────────────────
# Layout factory
# ──────────────────────────────────────────────────────────────────────────────

def create_layout(data: dict) -> html.Div:
    """
    Build and return the full app shell component tree.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().  Passed in for future use by child
        components (charts, tables) that will be embedded in the content area.

    Returns
    -------
    html.Div  — top-level Dash component containing the entire page.
    """
    return html.Div([
        # Persist sidebar collapsed/expanded state across callbacks
        dcc.Store(id="sidebar-collapsed", data=False),

        # ── Top header bar ─────────────────────────────────────────────────
        dbc.Navbar(
            dbc.Container([
                # Hamburger toggle button
                html.Button(
                    "\u2630",  # Unicode hamburger / trigram character
                    id="sidebar-toggle",
                    className="sidebar-toggle-btn",
                    n_clicks=0,
                ),
                # Brand / title
                dbc.NavbarBrand(
                    "Wind-Powered Desalination Dashboard",
                    className="ms-2",
                ),
            ], fluid=True),
            color="primary",
            dark=True,
        ),

        # ── Flex container: sidebar + content ──────────────────────────────
        html.Div([

            # Sidebar
            html.Div(
                id="sidebar",
                style={**_SIDEBAR_STYLE_BASE, "width": SIDEBAR_WIDTH_EXPANDED},
                children=[
                    dbc.Nav(
                        [
                            dbc.NavLink("Overview", href="/", active="exact"),
                            # Future phases add nav items here
                        ],
                        vertical=True,
                        pills=True,
                        className="px-2",
                    )
                ],
            ),

            # Main content area
            html.Div(
                id="page-content",
                style={"flex": "1", "padding": "1.5rem"},
                children=[
                    html.P(
                        "Dashboard content will appear here as features are built."
                    )
                ],
            ),

        ], style={"display": "flex", "flex": "1"}),

    ])


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar toggle callback
# ──────────────────────────────────────────────────────────────────────────────

@callback(
    Output("sidebar", "style"),
    Output("sidebar-collapsed", "data"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-collapsed", "data"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, is_collapsed):
    """
    Flip sidebar between expanded (220px) and collapsed (0px).

    Parameters
    ----------
    n_clicks : int
        Number of times the toggle button has been clicked.
    is_collapsed : bool
        Current collapsed state stored in dcc.Store.

    Returns
    -------
    tuple[dict, bool]
        Updated sidebar style dict and new collapsed boolean.
    """
    new_collapsed = not is_collapsed
    width = SIDEBAR_WIDTH_COLLAPSED if new_collapsed else SIDEBAR_WIDTH_EXPANDED
    new_style = {**_SIDEBAR_STYLE_BASE, "width": width}
    return new_style, new_collapsed
