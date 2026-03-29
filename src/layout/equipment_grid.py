"""
src/layout/equipment_grid.py
============================
Equipment card grid with accordion detail expansion and cross-system comparison.

Exports
-------
make_equipment_section(df, system, all_data)
    Returns an html.Div grouping equipment accordion items by process stage,
    with full detail and cross-system comparison in the expanded view.
"""

from __future__ import annotations

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from src.config import EQUIPMENT_DESCRIPTIONS, PROCESS_STAGES, DISPLAY_NAMES, LIFESPAN_DEFAULTS
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


def _make_cross_system_comparison(
    equipment_name: str,
    system: str,
    all_data: dict,
) -> html.Div:
    """Build a cross-system comparison table for equipment in the same process stage.

    Finds equipment items from other systems that share the same process stage as
    the given equipment item, then renders a small comparison table highlighting
    the best value per numeric metric column.

    Parameters
    ----------
    equipment_name : str
        Name of the equipment item being expanded.
    system : str
        System key ("mechanical" or "electrical").
    all_data : dict
        Full data dictionary from load_data().

    Returns
    -------
    html.Div
        Container with heading and comparison table, or a note if no equivalents.
    """
    # Determine the stage for the current equipment
    this_stage = get_equipment_stage(equipment_name, system)

    # Collect equivalents from other systems (same process stage)
    other_systems = [s for s in ("mechanical", "electrical") if s != system]

    comparison_rows: list[dict] = []
    # Include current item
    this_df = all_data.get(system, pd.DataFrame())
    this_row_df = this_df[this_df["name"] == equipment_name]
    if not this_row_df.empty:
        r = this_row_df.iloc[0]
        raw_name = str(r.get("name", "N/A"))
        raw_ls = r.get("lifespan_years")
        comparison_rows.append({
            "System": system.capitalize(),
            "Name": DISPLAY_NAMES.get(raw_name, raw_name),
            "Cost": r.get("cost_usd"),
            "Lifespan": raw_ls if raw_ls is not None else LIFESPAN_DEFAULTS.get(raw_name, "indefinite"),
        })

    for other_sys in other_systems:
        other_df = all_data.get(other_sys, pd.DataFrame())
        if other_df.empty:
            continue
        # Find items in the same process stage
        for _, other_row in other_df.iterrows():
            other_stage = get_equipment_stage(str(other_row.get("name", "")), other_sys)
            if other_stage == this_stage:
                other_name = str(other_row.get("name", "N/A"))
                raw_ls = other_row.get("lifespan_years")
                comparison_rows.append({
                    "System": other_sys.capitalize(),
                    "Name": DISPLAY_NAMES.get(other_name, other_name),
                    "Cost": other_row.get("cost_usd"),
                    "Lifespan": raw_ls if raw_ls is not None else LIFESPAN_DEFAULTS.get(other_name, "indefinite"),
                })

    if len(comparison_rows) <= 1:
        return html.Div(
            html.P(
                "No equivalent equipment found in other systems for this process stage.",
                className="text-muted small fst-italic",
            ),
            className="mt-2",
        )

    # Best values: lowest cost, highest lifespan
    best_cost = None
    best_lifespan = None
    for r in comparison_rows:
        c = pd.to_numeric(r["Cost"], errors="coerce")
        if not pd.isna(c):
            best_cost = min(best_cost, c) if best_cost is not None else c
        ls = pd.to_numeric(r["Lifespan"], errors="coerce")
        if not pd.isna(ls):
            best_lifespan = max(best_lifespan, ls) if best_lifespan is not None else ls

    # Build table rows
    header = html.Thead(
        html.Tr([
            html.Th("System"),
            html.Th("Name"),
            html.Th("Cost"),
            html.Th("Lifespan"),
        ])
    )
    body_rows = []
    for comp_row in comparison_rows:
        cost_raw = comp_row["Cost"]
        cost_numeric = pd.to_numeric(cost_raw, errors="coerce")
        cost_is_best = (
            best_cost is not None
            and not pd.isna(cost_numeric)
            and float(cost_numeric) == best_cost
        )

        ls_raw = comp_row["Lifespan"]
        ls_numeric = pd.to_numeric(ls_raw, errors="coerce")
        ls_is_best = (
            best_lifespan is not None
            and not pd.isna(ls_numeric)
            and float(ls_numeric) == best_lifespan
        )

        best_style = {"color": "#28A745", "fontWeight": "bold"}
        cells = [
            html.Td(comp_row["System"], style={"fontWeight": "600"}),
            html.Td(comp_row["Name"], style={"fontSize": "0.85rem"}),
            html.Td(fmt_cost(cost_raw), style=best_style if cost_is_best else {}),
            html.Td(_fmt_lifespan(ls_raw), style=best_style if ls_is_best else {}),
        ]
        body_rows.append(html.Tr(cells))

    table = dbc.Table(
        [header, html.Tbody(body_rows)],
        bordered=True,
        size="sm",
        responsive=True,
    )

    return html.Div(
        [
            html.H6("Cross-System Comparison", className="mt-3 text-muted"),
            html.P(
                f"Equipment in the same process stage ({this_stage}) across systems. "
                "Green = best value (lowest cost, longest lifespan).",
                className="small text-muted",
            ),
            table,
        ]
    )


def _make_accordion_item(
    row: pd.Series,
    system: str,
    idx: int,
    all_data: dict,
) -> dbc.AccordionItem:
    """Build a single accordion item for one equipment row.

    Parameters
    ----------
    row : pd.Series
        Equipment row from the system DataFrame.
    system : str
        System key ("mechanical" or "electrical").
    idx : int
        Row index (used for unique item IDs).
    all_data : dict
        Full data dictionary for cross-system comparison.

    Returns
    -------
    dbc.AccordionItem
    """
    name = str(row.get("name", "Unknown"))
    display_name = DISPLAY_NAMES.get(name, name)
    cost_display = fmt_cost(row.get("cost_usd"))

    # Collapsed header: display name + cost
    title = html.Span([
        html.Strong(display_name),
        html.Span(
            f" — {cost_display}",
            className="text-muted ms-1",
            style={"fontSize": "0.85rem"},
        ),
    ])

    # Description uses original name since EQUIPMENT_DESCRIPTIONS keys match raw xlsx strings
    description_text = EQUIPMENT_DESCRIPTIONS.get(name, "No description available.")
    description = html.P(
        description_text,
        className="fst-italic text-muted small",
    )

    # Detail content
    detail_table = _make_detail_table(row)
    cross_comparison = _make_cross_system_comparison(name, system, all_data)

    content = html.Div([
        description,
        _make_summary_badges(row),
        detail_table,
        cross_comparison,
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
    and expanded detail (description, badges, data table, cross-system comparison).

    For the Hybrid system: when hybrid equipment is available (via
    all_data["hybrid_selected"]), renders 5 accordion items for the selected
    equipment. When hybrid data is unavailable, returns a gate message prompting
    the user to fill all 5 slots.

    Parameters
    ----------
    df : pd.DataFrame
        Equipment DataFrame for the system being displayed.
    system : str
        System key: "mechanical", "electrical", or "hybrid".
    all_data : dict
        Full data dictionary from load_data() — passed to cross-system comparison.
        For hybrid, all_data may contain "hybrid_selected" key with the hybrid_df.

    Returns
    -------
    html.Div
        Equipment grid component tree.
    """
    # Hybrid: check if gate is open (hybrid_df provided in all_data)
    if system == "hybrid":
        hybrid_df = all_data.get("hybrid_selected")
        if hybrid_df is None:
            # Gate closed — show placeholder message
            return html.Div([
                html.H5("Hybrid System Equipment"),
                html.P(
                    "Fill all 5 slots to see equipment details.",
                    className="text-muted fst-italic",
                ),
            ])

        # Gate open — render accordion items for each selected equipment row
        accordion_items = []
        for idx, row in hybrid_df.iterrows():
            accordion_items.append(
                _make_accordion_item(row, "miscellaneous", idx, all_data)
            )

        return html.Div([
            html.H5("Hybrid System Equipment", className="mt-2 mb-2"),
            dbc.Accordion(
                accordion_items,
                always_open=False,
                active_item=None,
                className="shadow-sm",
            ),
        ])

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
            _make_accordion_item(row, system, idx, all_data)
            for idx, row in items_in_stage
        ]

        stage_class = "mt-4 mb-2"
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

    return html.Div(sections)
