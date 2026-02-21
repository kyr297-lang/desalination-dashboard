"""
Project configuration: constants, color maps, and file paths.
"""

from pathlib import Path

# Path to the Excel data file, relative to the project root
DATA_FILE = Path(__file__).parent.parent / "data.xlsx"

# Academic muted triad palette for the three system types.
# Colors are desaturated (muted) for an academic paper aesthetic and are
# distinguishable by most forms of colorblindness (blue / orange / green
# is a well-known accessible triad). Do not use these for RAG indicators.
SYSTEM_COLORS = {
    "Mechanical": "#5B8DB8",   # muted steel blue
    "Electrical": "#D4854A",   # muted terra cotta / burnt orange
    "Hybrid":     "#6BAA75",   # muted sage green
}

# RAG (Red / Amber / Green) traffic-light colors for the scorecard.
# These are standard Bootstrap alert colors, kept separate from SYSTEM_COLORS
# so neither set is confused with the other.
RAG_COLORS = {
    "red":    "#DC3545",
    "yellow": "#FFC107",
    "green":  "#28A745",
}
