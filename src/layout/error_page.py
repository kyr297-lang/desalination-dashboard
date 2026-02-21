"""
src/layout/error_page.py
========================
Full-page error component displayed when data.xlsx cannot be loaded.

create_error_page(error, details) returns a Dash component tree that fills
the viewport with a human-readable error message and an expandable technical
details section.
"""

from dash import html
import dash_bootstrap_components as dbc


def create_error_page(error: str, details: str = "") -> html.Div:
    """
    Build a full-page error display for data-loading failures.

    Parameters
    ----------
    error : str
        High-level error message (e.g. "data.xlsx not found").
    details : str, optional
        Full traceback or technical context.  Shown in a collapsed accordion
        section so non-technical users are not overwhelmed.

    Returns
    -------
    html.Div  — full-viewport centered error page.
    """
    accordion_items = []
    if details:
        accordion_items.append(
            dbc.AccordionItem(
                html.Pre(details, style={"whiteSpace": "pre-wrap", "fontSize": "0.8rem"}),
                title="Details (for technical users)",
            )
        )

    return html.Div(
        style={"minHeight": "100vh", "paddingTop": "2rem"},
        children=[
            dbc.Container([
                dbc.Row(
                    dbc.Col([
                        html.H2(
                            "Unable to Load Dashboard",
                            className="text-danger mt-5",
                        ),
                        html.P(
                            "The dashboard could not start because the data file "
                            "could not be read."
                        ),
                        dbc.Alert(error, color="danger"),
                        dbc.Accordion(
                            accordion_items,
                            start_collapsed=True,
                        ) if accordion_items else html.Div(),
                    ], width=8),
                    justify="center",
                )
            ])
        ],
    )
