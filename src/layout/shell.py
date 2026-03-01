"""
src/layout/shell.py
===================
App shell layout: top header bar, collapsible sidebar, and content area.

create_layout(data) returns the full Dash component tree.  The sidebar toggle
callback and navigation callbacks are registered here via the @callback
decorator (Dash 4.0 style).

Navigation state is managed via a dcc.Store("active-system"):
  - None          → landing overview
  - "mechanical"  → mechanical system tab view
  - "electrical"  → electrical system tab view
  - "hybrid"      → hybrid system tab view (empty state until Phase 4)
"""

import dash
from dash import html, dcc, callback, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc

from src.layout.hybrid_builder import SLOT_STAGES

from src.config import SYSTEM_COLORS  # available for future use by child components

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert a CSS hex color string to an rgba() string."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


_BASE_CONTENT_STYLE = {"flex": "1", "padding": "1.5rem"}

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

# Module-level data reference — avoids circular imports.
# Populated by set_data() called from app.py after data is loaded.
_data = None


def set_data(data: dict) -> None:
    """Store the loaded data dict for use in the render_content callback.

    Called once from app.py after DATA is loaded, before any callbacks fire.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().
    """
    global _data
    _data = data


# ──────────────────────────────────────────────────────────────────────────────
# Layout factory
# ──────────────────────────────────────────────────────────────────────────────

def create_layout(data: dict) -> html.Div:
    """
    Build and return the full app shell component tree.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().  Stored via set_data() for use in
        the render_content callback.

    Returns
    -------
    html.Div  — top-level Dash component containing the entire page.
    """
    return html.Div([
        # Persist sidebar collapsed/expanded state across callbacks
        dcc.Store(id="sidebar-collapsed", data=False),

        # Active system store — None = landing overview, string = system key
        dcc.Store(id="active-system", data=None),

        # Hybrid slot store — always in the DOM so chart/scorecard callbacks
        # can use it as an Input regardless of which tab is active.
        # Written by the hybrid builder callbacks when the Hybrid tab is open.
        dcc.Store(
            id="store-hybrid-slots",
            data={stage: None for stage in SLOT_STAGES},
        ),


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
                            dbc.NavLink(
                                "System Explorer",
                                href="#",
                                id="nav-system-explorer",
                            ),
                        ],
                        vertical=True,
                        pills=True,
                        className="px-2",
                    )
                ],
            ),

            # Main content area — populated by render_content callback
            html.Div(
                id="page-content",
                style={"flex": "1", "padding": "1.5rem"},
                children=[],
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


# ──────────────────────────────────────────────────────────────────────────────
# Navigation callbacks
# ──────────────────────────────────────────────────────────────────────────────

@callback(
    Output("active-system", "data"),
    Input({"type": "system-card-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def select_system_from_card(card_clicks):
    """Set active system when a landing page card is clicked."""
    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and triggered.get("type") == "system-card-btn":
        return triggered["index"]
    return dash.no_update


@callback(
    Output("active-system", "data", allow_duplicate=True),
    Input("system-tabs", "active_tab"),
    prevent_initial_call=True,
)
def select_system_from_tab(active_tab):
    """Set active system when a tab is clicked."""
    if active_tab is not None:
        return active_tab
    return dash.no_update


@callback(
    Output("active-system", "data", allow_duplicate=True),
    Input("back-to-overview", "n_clicks"),
    prevent_initial_call=True,
)
def back_to_overview(n_clicks):
    """Reset to landing page when back link is clicked."""
    return None


@callback(
    Output("page-content", "children"),
    Output("page-content", "style"),
    Input("active-system", "data"),
)
def render_content(active_system):
    """Render the main page content based on the active-system store.

    - None → landing overview (create_overview_layout), no tint
    - string → system tab view (create_system_view_layout) with system-color tint

    Imports are deferred inside this function to avoid circular imports at
    module load time.

    Parameters
    ----------
    active_system : str or None
        Current value of the active-system store.

    Returns
    -------
    tuple[list, dict]
        Dash component(s) to render in the page-content area, and the
        inline style dict to apply to #page-content (tint or transparent).
    """
    # Deferred imports — layout modules import from shell.py's module scope
    # so top-level imports would create circular dependencies.
    from src.layout.overview import create_overview_layout
    from src.layout.system_view import create_system_view_layout

    if active_system is None:
        no_tint = {**_BASE_CONTENT_STYLE, "backgroundColor": "transparent"}
        return create_overview_layout(), no_tint

    label = active_system.capitalize()
    hex_color = SYSTEM_COLORS.get(label, "#6c757d")
    tint_style = {**_BASE_CONTENT_STYLE, "backgroundColor": _hex_to_rgba(hex_color, 0.18)}
    return create_system_view_layout(active_system, _data), tint_style
