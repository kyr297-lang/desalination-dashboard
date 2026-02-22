"""
src/layout/hybrid_builder.py
=============================
Pipeline builder UI for the Hybrid System tab.

Provides a horizontal 5-stage pipeline layout with labeled dropdowns,
a slot counter, a Clear All button, and a dcc.Store for the slot state.
Three callbacks handle slot store updates, clearing all slots, and
displaying the current slot count.

Follows the module-level _data / set_data() pattern used throughout this
project (shell.py, charts.py) to avoid circular imports and callback
data-loading anti-patterns.

Exports
-------
set_data(data) -> None
make_hybrid_builder(data) -> html.Div
SLOT_STAGES : list[str]
"""

from __future__ import annotations

from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from src.config import PROCESS_STAGES


# ──────────────────────────────────────────────────────────────────────────────
# Module-level data reference — mirrors set_data() pattern from shell.py.
# Populated by set_data() called from app.py after data is loaded.
# ──────────────────────────────────────────────────────────────────────────────

_data: dict | None = None


def set_data(data: dict) -> None:
    """Store the loaded data dict for use in dropdown option building.

    Called once from app.py after DATA is loaded, before layout is rendered.
    Mirrors the pattern used in shell.py and charts.py.

    Parameters
    ----------
    data : dict
        Data dict returned by load_data().
    """
    global _data
    _data = data


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

# Ordered list of process stages in the hybrid pipeline (left to right).
SLOT_STAGES: list[str] = [
    "Water Extraction",
    "Pre-Treatment",
    "Desalination",
    "Post-Treatment",
    "Brine Disposal",
]

# Dropdown ID for each stage — derived from stage name, snake_case.
_STAGE_TO_DD_ID: dict[str, str] = {
    "Water Extraction":  "slot-dd-water-extraction",
    "Pre-Treatment":     "slot-dd-pre-treatment",
    "Desalination":      "slot-dd-desalination",
    "Post-Treatment":    "slot-dd-post-treatment",
    "Brine Disposal":    "slot-dd-brine-disposal",
}


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_dropdown_options(stage: str, data: dict) -> list[dict]:
    """Build dropdown option dicts for a given pipeline stage.

    Looks up the item names defined in PROCESS_STAGES["miscellaneous"][stage],
    then verifies each name exists in at least one of the three DataFrames
    (miscellaneous, mechanical, electrical). Names that match no DataFrame row
    are excluded so the dropdown never shows a selection that cannot be looked up.

    Parameters
    ----------
    stage : str
        Stage name matching a key in PROCESS_STAGES["miscellaneous"].
    data : dict
        Full data dict from load_data() with keys "miscellaneous", "mechanical",
        "electrical".

    Returns
    -------
    list[dict]
        List of {"label": name, "value": name} option dicts, one per valid item.
    """
    item_names: list[str] = PROCESS_STAGES.get("miscellaneous", {}).get(stage, [])
    options: list[dict] = []

    for name in item_names:
        found_in_any = any(
            not data[source][data[source]["name"] == name].empty
            for source in ("miscellaneous", "mechanical", "electrical")
        )
        if found_in_any:
            options.append({"label": name, "value": name})

    return options


def _stage_dropdown(stage: str, data: dict) -> html.Div:
    """Build a single pipeline slot: a label above a dropdown.

    Parameters
    ----------
    stage : str
        Stage name (e.g. "Desalination").
    data : dict
        Full data dict for building dropdown options.

    Returns
    -------
    html.Div
        A vertically laid-out slot with a muted bold label and a dropdown.
    """
    dd_id = _STAGE_TO_DD_ID[stage]
    options = _build_dropdown_options(stage, data)

    return html.Div(
        [
            html.Label(
                stage,
                className="small fw-bold text-muted mb-1 d-block",
                style={"whiteSpace": "nowrap"},
            ),
            dcc.Dropdown(
                id=dd_id,
                options=options,
                value=None,
                clearable=True,
                placeholder="Select...",
                style={"minWidth": "160px"},
            ),
        ],
        style={"flex": "1 1 160px"},
    )


# ──────────────────────────────────────────────────────────────────────────────
# Public layout factory
# ──────────────────────────────────────────────────────────────────────────────

def make_hybrid_builder(data: dict) -> html.Div:
    """Build the pipeline builder layout with all 5 equipment slot dropdowns.

    Constructs a horizontal pipeline (flexbox with wrapping) where each stage
    is represented by a labeled dropdown. Arrows between stages reinforce the
    left-to-right process flow. A slot counter and Clear All button sit above
    the pipeline. A dcc.Store holds the current slot selections.

    Anti-patterns avoided:
    - Dropdown options are built at layout time (static data); no callback
      dynamically populates options.
    - Only update_slot_store writes to store-hybrid-slots.
    - This function does not call make_chart_section().

    Parameters
    ----------
    data : dict
        Full data dict from load_data(). Used to build dropdown options inline.

    Returns
    -------
    html.Div
        Complete pipeline builder section ready to embed in the Hybrid tab.
    """
    # ── Slot store ────────────────────────────────────────────────────────────
    slot_store = dcc.Store(
        id="store-hybrid-slots",
        data={stage: None for stage in SLOT_STAGES},
    )

    # ── Top bar: counter + Clear All button ──────────────────────────────────
    top_bar = html.Div(
        [
            html.Span(
                id="slot-counter",
                children="0/5 slots filled",
                className="text-muted small me-3 align-self-center",
            ),
            dbc.Button(
                "Clear All",
                id="btn-clear-all",
                size="sm",
                color="secondary",
                outline=True,
            ),
        ],
        className="d-flex align-items-center mb-3",
    )

    # ── Pipeline: dropdowns with arrows between ───────────────────────────────
    pipeline_children: list = []
    for i, stage in enumerate(SLOT_STAGES):
        pipeline_children.append(_stage_dropdown(stage, data))
        if i < len(SLOT_STAGES) - 1:
            pipeline_children.append(
                html.Span(
                    "\u2192",
                    className="text-muted align-self-center fs-4 mx-1",
                    style={"lineHeight": "1", "paddingTop": "1.4rem"},
                )
            )

    pipeline = html.Div(
        pipeline_children,
        className="d-flex flex-wrap align-items-start gap-2 mb-3",
    )

    return html.Div(
        [
            slot_store,
            html.H5("Hybrid System Builder", className="mb-3"),
            top_bar,
            pipeline,
        ]
    )


# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────

@callback(
    Output("store-hybrid-slots", "data"),
    Input(_STAGE_TO_DD_ID["Water Extraction"], "value"),
    Input(_STAGE_TO_DD_ID["Pre-Treatment"], "value"),
    Input(_STAGE_TO_DD_ID["Desalination"], "value"),
    Input(_STAGE_TO_DD_ID["Post-Treatment"], "value"),
    Input(_STAGE_TO_DD_ID["Brine Disposal"], "value"),
)
def update_slot_store(water, pretreat, desal, posttreat, brine):
    """Write all 5 dropdown values into the slot store.

    Fires on any dropdown change and always reflects the current state of all
    5 dropdowns. This is the sole writer to store-hybrid-slots.

    Parameters
    ----------
    water : str or None
        Selected equipment for Water Extraction stage.
    pretreat : str or None
        Selected equipment for Pre-Treatment stage.
    desal : str or None
        Selected equipment for Desalination stage.
    posttreat : str or None
        Selected equipment for Post-Treatment stage.
    brine : str or None
        Selected equipment for Brine Disposal stage.

    Returns
    -------
    dict
        Slot store data mapping each stage name to its selected equipment name.
    """
    return {
        "Water Extraction": water,
        "Pre-Treatment":    pretreat,
        "Desalination":     desal,
        "Post-Treatment":   posttreat,
        "Brine Disposal":   brine,
    }


@callback(
    Output(_STAGE_TO_DD_ID["Water Extraction"], "value"),
    Output(_STAGE_TO_DD_ID["Pre-Treatment"], "value"),
    Output(_STAGE_TO_DD_ID["Desalination"], "value"),
    Output(_STAGE_TO_DD_ID["Post-Treatment"], "value"),
    Output(_STAGE_TO_DD_ID["Brine Disposal"], "value"),
    Input("btn-clear-all", "n_clicks"),
    prevent_initial_call=True,
)
def clear_all_slots(n_clicks):
    """Reset all 5 dropdowns to None when Clear All is clicked.

    Does NOT write to the store directly — the cascade through
    update_slot_store handles that automatically when dropdown values change.

    Parameters
    ----------
    n_clicks : int or None
        Number of times the Clear All button was clicked.

    Returns
    -------
    tuple[None, None, None, None, None]
        None for each of the 5 dropdown value Outputs.
    """
    return None, None, None, None, None


@callback(
    Output("slot-counter", "children"),
    Input("store-hybrid-slots", "data"),
)
def update_slot_counter(slots: dict) -> str:
    """Update the slot counter label from the slot store.

    Parameters
    ----------
    slots : dict
        Current slot store data mapping stage names to equipment selections.

    Returns
    -------
    str
        A human-readable string like "3/5 slots filled".
    """
    if slots is None:
        return "0/5 slots filled"
    filled = sum(1 for v in slots.values() if v is not None)
    return f"{filled}/5 slots filled"
