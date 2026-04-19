"""
src/layout/equipment_grid.py
============================
Equipment card grid with accordion detail expansion.

Exports
-------
make_equipment_section(df, system, all_data)
    Returns an html.Div grouping equipment accordion items by process stage,
    with full detail in the expanded view.
"""

from __future__ import annotations

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from src.config import EQUIPMENT_DESCRIPTIONS, PROCESS_STAGES, DISPLAY_NAMES, LIFESPAN_DEFAULTS, NON_COTS_COMPONENTS
from src.data.processing import fmt_cost, fmt_num, fmt, fmt_sig2, get_equipment_stage


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

# Canonical stage order for display.  Equipment that does not match any stage
# is placed under "Other".
_STAGE_ORDER = [
    "Power & Drive",
    "Water Extraction",
    "Desalination",
    "Brine & Storage",
    "Support",
]


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _fmt_lifespan(value, name: str = "") -> str:
    """Format lifespan value, applying LIFESPAN_DEFAULTS when xlsx has no data."""
    if value is None:
        value = LIFESPAN_DEFAULTS.get(name, "indefinite")
    if isinstance(value, str) and value.strip().lower() == "indefinite":
        return "Indefinite"
    n = pd.to_numeric(value, errors="coerce")
    if pd.isna(n):
        return str(value)
    return f"{float(n):.0f} years"


def _make_summary_badges(row: pd.Series) -> dbc.Row:
    """Build a row of metric badges for the collapsed accordion header summary.

    Parameters
    ----------
    row : pd.Series
        Equipment row from the system DataFrame.

    Returns
    -------
    dbc.Row
        Three small badge columns: Qty, Cost, Lifespan.
    """
    badges = [
        ("Qty", fmt_sig2(row.get("quantity"))),
        ("Cost", fmt_cost(row.get("cost_usd"))),
        ("Lifespan", _fmt_lifespan(row.get("lifespan_years"), row.get("name", ""))),
    ]
    cols = []
    for label, value in badges:
        cols.append(
            dbc.Col(
                dbc.Badge(
                    [html.Small(label, className="text-muted me-1"), value],
                    color="light",
                    text_color="dark",
                    className="border me-1",
                    style={"fontSize": "0.75rem"},
                ),
                width="auto",
            )
        )
    return dbc.Row(cols, className="g-1 mt-1")


def _make_detail_table(row: pd.Series) -> dbc.Table:
    """Build the full detail table for an expanded equipment accordion item.

    Parameters
    ----------
    row : pd.Series
        Equipment row from the system DataFrame.

    Returns
    -------
    dbc.Table
        Two-column table with label (Th) and value (Td) for Name, Qty, Cost, Lifespan.
    """
    name = row.get("name", "")
    display_name = DISPLAY_NAMES.get(name, name)
    fields = [
        ("Name", fmt(display_name)),
        ("Quantity", fmt_sig2(row.get("quantity"))),
        ("Cost", fmt_cost(row.get("cost_usd"))),
        ("Lifespan", _fmt_lifespan(row.get("lifespan_years"), name)),
    ]
    table_rows = [
        html.Tr([html.Th(label, style={"width": "35%"}), html.Td(value)])
        for label, value in fields
    ]
    return dbc.Table(
        html.Tbody(table_rows),
        bordered=True,
        size="sm",
        className="mt-2",
    )


def _make_accordion_item(
    row: pd.Series,
    system: str,
    idx: int,
) -> dbc.AccordionItem:
    """Build a single accordion item for one equipment row.

    Parameters
    ----------
    row : pd.Series
        Equipment row from the system DataFrame.
    system : str
        System key ("mechanical", "electrical", or "hybrid").
    idx : int
        Row index (used for unique item IDs).

    Returns
    -------
    dbc.AccordionItem
    """
    name = str(row.get("name", "Unknown"))
    display_name = DISPLAY_NAMES.get(name, name)
    is_non_cots = name in NON_COTS_COMPONENTS
    cost_display = fmt_cost(row.get("cost_usd"))

    # Collapsed header: display name + optional non-COTS marker + cost
    header_parts: list = [html.Strong(display_name)]
    if is_non_cots:
        header_parts.append(
            html.Sup("*", style={"color": "#C0392B", "marginLeft": "2px"})
        )
    header_parts.append(
        html.Span(
            f" — {cost_display}",
            className="text-muted ms-1",
            style={"fontSize": "0.85rem"},
        )
    )
    title = html.Span(header_parts)

    # Description uses original name since EQUIPMENT_DESCRIPTIONS keys match raw xlsx strings
    description_text = EQUIPMENT_DESCRIPTIONS.get(name, "No description available.")
    description = html.P(
        description_text,
        className="fst-italic text-muted small",
    )

    # Detail content
    detail_table = _make_detail_table(row)

    content = html.Div([
        description,
        _make_summary_badges(row),
        detail_table,
    ])

    return dbc.AccordionItem(
        content,
        title=title,
        item_id=f"item-{system}-{idx}",
    )


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def make_equipment_section(
    df: pd.DataFrame,
    system: str,
    all_data: dict,
) -> html.Div:
    """Build the equipment grid for a given system.

    Groups equipment by process stage, renders each stage with a header and a
    dbc.Accordion.  Each accordion item shows collapsed summary (name + cost)
    and expanded detail (description, badges, data table).

    Parameters
    ----------
    df : pd.DataFrame
        Equipment DataFrame for the system being displayed.
    system : str
        System key: "mechanical", "electrical", or "hybrid".
    all_data : dict
        Full data dictionary from load_data() (retained for API compatibility).

    Returns
    -------
    html.Div
        Equipment grid component tree.
    """
    # ── Group equipment by process stage ──────────────────────────────────────
    stage_groups: dict[str, list[tuple[int, pd.Series]]] = {
        stage: [] for stage in _STAGE_ORDER
    }

    for idx, row in df.iterrows():
        name = str(row.get("name", ""))
        stage = get_equipment_stage(name, system)
        if stage not in stage_groups:
            stage_groups.setdefault("Other", [])
            stage = "Other"
        stage_groups[stage].append((idx, row))

    # ── Build stage sections ──────────────────────────────────────────────────
    sections = []
    for stage in _STAGE_ORDER:
        items_in_stage = stage_groups.get(stage, [])
        if not items_in_stage:
            continue

        accordion_items = [
            _make_accordion_item(row, system, idx)
            for idx, row in items_in_stage
        ]

        stage_class = "section-heading"
        if system == "mechanical":
            stage_class += " stage-heading-mechanical"
        elif system == "electrical":
            stage_class += " stage-heading-electrical"
        elif system == "hybrid":
            stage_class += " stage-heading-hybrid"

        sections.append(
            html.Div([
                html.H5(stage, className=stage_class),
                dbc.Accordion(
                    accordion_items,
                    always_open=False,
                    active_item=None,
                    className="shadow-sm",
                ),
            ])
        )

    if not sections:
        return html.Div(
            html.P(
                "No equipment data available for this system.",
                className="text-muted fst-italic",
            )
        )

    has_non_cots = any(
        str(row.get("name", "")) in NON_COTS_COMPONENTS
        for _, row in df.iterrows()
    )
    children: list = sections
    if has_non_cots:
        children = sections + [
            html.Div(
                html.Small([
                    html.Sup("*", style={"color": "#C0392B", "marginRight": "3px"}),
                    "Non-COTS: custom-fabricated or specially ordered component; "
                    "not available as a standard commercial off-the-shelf product.",
                ], className="text-muted fst-italic"),
                className="mt-3 px-1",
            )
        ]
    return html.Div(children)
