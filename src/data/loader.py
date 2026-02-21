"""
src/data/loader.py
==================
Section-based Excel parser for data.xlsx.

data.xlsx uses a single sheet ("Part 1") with three logically separate
sections stacked vertically — NOT three separate Excel sheets.  Each section
begins with a named header row in column B:

  Row  1 – "Electrical Components"  (data rows 2-11, total row 12)
  Row 15 – "Mechanical Components"  (data rows 16-24, total row 25)
  Row 27 – "Miscalleneous"          (NOTE: deliberate typo in source file)

A battery/tank lookup table occupies columns J-P, rows 3-14 (header row 3,
data rows 4-14).

Non-numeric values ("indefinite", "~15 tons", "$ 2500 per ton", etc.) are
stored as-is.  No coercion is performed here; downstream modules handle it.
"""

from pathlib import Path

import openpyxl
import pandas as pd

from src.config import DATA_FILE

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

# Exact header strings as they appear in column B of Part 1.
# Key is the header text; value is the canonical dict key we expose.
# "Miscalleneous" is a typo in the actual file — match it exactly.
SECTION_HEADERS: dict[str, str] = {
    "Electrical Components": "electrical",
    "Mechanical Components": "mechanical",
    "Miscalleneous": "miscellaneous",
}

# Ordered column names for the equipment rows (columns B-G, positions 2-7).
EQUIPMENT_COLUMNS = [
    "name",
    "quantity",
    "cost_usd",
    "energy_kw",
    "land_area_m2",
    "lifespan_years",
]

# Column names for the battery/tank lookup table (columns J-P, positions 10-16).
BATTERY_COLUMNS = [
    "battery_fraction",
    "tank_fraction",
    "battery_kwh",
    "tank_gal",
    "battery_cost",
    "tank_cost",
    "total_cost",
]

# Column names for the Part 2 TDS and depth lookup tables.
TDS_LOOKUP_COLUMNS = ["tds_ppm", "ro_energy_kw"]
DEPTH_LOOKUP_COLUMNS = ["depth_m", "pump_energy_kw"]


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _parse_section(ws, header_row: int, stop_rows: set) -> list[dict]:
    """
    Parse equipment rows starting immediately after *header_row*.

    Iteration stops when:
      - The current row number is in *stop_rows* (start of next section), OR
      - Column B value is ``None`` (blank cell, including merged-cell spillover).

    Rows where column B value is ``"Total"`` are silently skipped (they are
    section summary rows, not equipment data).

    Parameters
    ----------
    ws : openpyxl.worksheet.worksheet.Worksheet
    header_row : int
        1-based row number of the section header ("Electrical Components", etc.)
    stop_rows : set[int]
        Row numbers that mark the start of the *next* section (or end boundary).

    Returns
    -------
    list[dict]
        One dict per equipment row, keys matching EQUIPMENT_COLUMNS.
    """
    rows = []
    for r in range(header_row + 1, ws.max_row + 1):
        if r in stop_rows:
            break
        name = ws.cell(r, 2).value
        # None means blank (or merged-cell note row) — stop scanning.
        if name is None:
            break
        # Skip section-total summary rows.
        if name == "Total":
            continue
        rows.append({
            "name":          name,
            "quantity":      ws.cell(r, 3).value,   # may be None or string
            "cost_usd":      ws.cell(r, 4).value,   # may be string e.g. "$ 2500 per ton"
            "energy_kw":     ws.cell(r, 5).value,
            "land_area_m2":  ws.cell(r, 6).value,
            "lifespan_years": ws.cell(r, 7).value,  # may be "indefinite"
        })
    return rows


def _parse_battery_lookup(ws) -> pd.DataFrame:
    """
    Parse the battery/tank lookup table from the fixed range J3:P14.

    Header labels are at row 3 (cols J-P); data occupies rows 4-14
    (11 rows: battery_fraction 0.0 to 1.0 in 0.1 steps).

    Returns
    -------
    pd.DataFrame  with columns matching BATTERY_COLUMNS
    """
    rows = []
    for r in range(4, 15):   # rows 4–14 inclusive
        rows.append({
            "battery_fraction": ws.cell(r, 10).value,
            "tank_fraction":    ws.cell(r, 11).value,
            "battery_kwh":      ws.cell(r, 12).value,
            "tank_gal":         ws.cell(r, 13).value,
            "battery_cost":     ws.cell(r, 14).value,
            "tank_cost":        ws.cell(r, 15).value,
            "total_cost":       ws.cell(r, 16).value,
        })
    return pd.DataFrame(rows, columns=BATTERY_COLUMNS)


def _parse_part2_lookups(wb) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse both lookup tables from the 'Part 2' sheet.

    Layout (confirmed from data.xlsx):
      Row 1: headers — col A="TDS", col B="kW required (RO Desalination)",
                       col D="Depth", col E="kW required (pump energy)"
      Rows 2-21: 20 data rows for each table (values 0-1900 in 100-unit steps)

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (tds_df, depth_df)
        tds_df columns:   ["tds_ppm", "ro_energy_kw"]
        depth_df columns: ["depth_m", "pump_energy_kw"]
    """
    if "Part 2" not in wb.sheetnames:
        raise ValueError(
            f"Expected sheet 'Part 2' not found. "
            f"Available sheets: {wb.sheetnames}"
        )
    ws2 = wb["Part 2"]

    tds_rows = []
    depth_rows = []
    for r in range(2, 22):   # rows 2-21 inclusive (20 data rows)
        tds_rows.append({
            "tds_ppm":      ws2.cell(r, 1).value,   # col A
            "ro_energy_kw": ws2.cell(r, 2).value,   # col B
        })
        depth_rows.append({
            "depth_m":        ws2.cell(r, 4).value, # col D
            "pump_energy_kw": ws2.cell(r, 5).value, # col E
        })

    tds_df   = pd.DataFrame(tds_rows,   columns=TDS_LOOKUP_COLUMNS)
    depth_df = pd.DataFrame(depth_rows, columns=DEPTH_LOOKUP_COLUMNS)

    print(f"  [loader] TDS lookup:   {len(tds_df)} rows parsed")
    print(f"  [loader] Depth lookup: {len(depth_df)} rows parsed")
    return tds_df, depth_df


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def load_data() -> dict[str, pd.DataFrame]:
    """
    Load and parse data.xlsx, returning six DataFrames.

    Sections are located by scanning column B of Part 1 for known header
    strings.  Values are stored as-is from the Excel cells — no numeric
    coercion is applied.

    Returns
    -------
    dict with keys:
        "electrical"    – pd.DataFrame (equipment rows for the electrical system)
        "mechanical"    – pd.DataFrame (equipment rows for the mechanical system)
        "miscellaneous" – pd.DataFrame (equipment rows for the miscellaneous/hybrid parts)
        "battery_lookup"– pd.DataFrame (battery fraction vs. tank fraction lookup)
        "tds_lookup"    – pd.DataFrame with columns ["tds_ppm", "ro_energy_kw"], 20 rows (TDS 0-1900 PPM)
        "depth_lookup"  – pd.DataFrame with columns ["depth_m", "pump_energy_kw"], 20 rows (Depth 0-1900 m)

    Raises
    ------
    FileNotFoundError
        If data.xlsx does not exist at the configured path.
    ValueError
        If one or more expected section headers are missing from 'Part 1',
        or if parsing otherwise fails.
    """
    # ── 1. File existence check ──────────────────────────────────────────────
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"data.xlsx not found at expected path: {DATA_FILE}\n"
            "Ensure the file is in the project root directory."
        )

    # ── 2. Open workbook ─────────────────────────────────────────────────────
    wb = openpyxl.load_workbook(DATA_FILE, data_only=True)

    # ── 2b. Parse Part 2 lookup tables ──────────────────────────────────────
    tds_df, depth_df = _parse_part2_lookups(wb)

    if "Part 1" not in wb.sheetnames:
        raise ValueError(
            f"Expected sheet 'Part 1' not found. "
            f"Available sheets: {wb.sheetnames}"
        )
    ws = wb["Part 1"]

    # ── 3. Scan for section header rows ──────────────────────────────────────
    section_row_map: dict[str, int] = {}
    for row in ws.iter_rows(min_col=2, max_col=2):
        cell = row[0]
        if cell.value in SECTION_HEADERS:
            canonical_key = SECTION_HEADERS[cell.value]
            section_row_map[canonical_key] = cell.row
            print(f"  [loader] Found section '{cell.value}' at row {cell.row}")

    # ── 4. Validate all sections present ─────────────────────────────────────
    required = {"electrical", "mechanical", "miscellaneous"}
    missing = required - set(section_row_map.keys())
    if missing:
        raise ValueError(
            f"Missing section(s) in 'Part 1': {sorted(missing)}. "
            f"Found: {sorted(section_row_map.keys())}. "
            "Check that data.xlsx has not been modified."
        )

    # ── 5. Parse equipment sections ──────────────────────────────────────────
    elec_start = section_row_map["electrical"]
    mech_start = section_row_map["mechanical"]
    misc_start = section_row_map["miscellaneous"]

    electrical_rows   = _parse_section(ws, elec_start,  stop_rows={mech_start})
    mechanical_rows   = _parse_section(ws, mech_start,  stop_rows={misc_start})
    miscellaneous_rows = _parse_section(ws, misc_start, stop_rows=set())

    print(f"  [loader] Electrical:    {len(electrical_rows)} equipment rows parsed")
    print(f"  [loader] Mechanical:    {len(mechanical_rows)} equipment rows parsed")
    print(f"  [loader] Miscellaneous: {len(miscellaneous_rows)} equipment rows parsed")

    # ── 6. Parse battery/tank lookup ─────────────────────────────────────────
    battery_df = _parse_battery_lookup(ws)
    print(f"  [loader] Battery lookup: {len(battery_df)} rows parsed")

    return {
        "electrical":    pd.DataFrame(electrical_rows,    columns=EQUIPMENT_COLUMNS),
        "mechanical":    pd.DataFrame(mechanical_rows,    columns=EQUIPMENT_COLUMNS),
        "miscellaneous": pd.DataFrame(miscellaneous_rows, columns=EQUIPMENT_COLUMNS),
        "battery_lookup": battery_df,
        "tds_lookup":    tds_df,
        "depth_lookup":  depth_df,
    }
