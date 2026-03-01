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

# Fixed per-stage colors for the energy breakdown bar chart.
# Muted academic palette — distinct from SYSTEM_COLORS and from each other.
# Fixed assignment prevents color shifting when stage values drop to 0.
STAGE_COLORS = {
    "Water Extraction": "#4AACB0",   # muted teal
    "Pre-Treatment":    "#9975B5",   # muted purple
    "Desalination":     "#D4A739",   # muted amber
    "Post-Treatment":   "#7DAA5A",   # muted olive green
    "Brine Disposal":   "#C46E5A",   # muted brick red
    "Control":          "#7A9FBF",   # muted slate blue
    "Other":            "#999999",   # medium grey
}

# RAG (Red / Amber / Green) traffic-light colors for the scorecard.
# These are standard Bootstrap alert colors, kept separate from SYSTEM_COLORS
# so neither set is confused with the other.
RAG_COLORS = {
    "red":    "#DC3545",
    "yellow": "#FFC107",
    "green":  "#28A745",
}

# PROCESS_STAGES maps each system's equipment items to their functional process
# stage in the desalination workflow. Equipment names must match exactly the
# strings returned by loader.py (from column B of data.xlsx).
PROCESS_STAGES = {
    "mechanical": {
        "Water Extraction": [
            "250kW aeromotor turbine ",
            "Submersible pump ",
            "Wind turbine rotor lock",
        ],
        "Pre-Treatment": [
            "Pipes",
            "Gate valve",
        ],
        "Desalination": [
            "2 RO membranes in parallel",
            "Gear and Booster Pump",
        ],
        "Post-Treatment": [
            "Calcite bed contactors",
        ],
        "Brine Disposal": [
            "Extra storage tank",
        ],
    },
    "electrical": {
        "Water Extraction": [
            "Turbine",
            "Submersible pump",
            "Battery (1 day of power)",
        ],
        "Pre-Treatment": [
            "Multi-Media Filtration",
            "Pipes (total)",
        ],
        "Desalination": [
            "RO membranes in parallel",
            "Booster Pump",
        ],
        "Post-Treatment": [
            "Calcite bed contactors",
        ],
        "Brine Disposal": [
            "Brine Well",
        ],
        "Control": [
            "PLC",
        ],
    },
    "miscellaneous": {
        "Water Extraction": [
            "Piston pump",
        ],
        "Pre-Treatment": [
            "Antiscalant (assuming 3g/L of antiscalant)",
        ],
        "Desalination": [
            "2 RO membranes in parallel",
            "RO membranes in parallel",
            "Gear and Booster Pump",
            "Booster Pump",
        ],
        "Post-Treatment": [
            "Green blend addition",
            "Activated carbon (annual)",
            "55 gallon container is 2500 USD, for 1 million gal/day lasts about 20 days",
        ],
        "Brine Disposal": [
            "Evaporation Pond",
        ],
    },
}

# EQUIPMENT_DESCRIPTIONS provides a 1-2 sentence technical description for
# each equipment item in the mechanical, electrical, and miscellaneous systems.
# Audience: engineering students. Keys match column B strings exactly.
EQUIPMENT_DESCRIPTIONS = {
    # ── Mechanical system ──────────────────────────────────────────────────────
    "250kW aeromotor turbine ": (
        "A large wind-driven turbine rated at 250 kW that provides mechanical "
        "energy to drive pumps and pressurize water for reverse osmosis. "
        "It directly couples wind energy to the desalination process without "
        "converting to electricity."
    ),
    "2 RO membranes in parallel": (
        "Two reverse osmosis membrane modules connected in parallel to increase "
        "throughput while maintaining operating pressure. Semi-permeable membranes "
        "reject dissolved salts as pressurized feedwater passes through."
    ),
    "Pipes": (
        "Network of pressurized piping that routes water between process stages "
        "including from the extraction point through pre-treatment, the RO unit, "
        "and post-treatment to the product water storage."
    ),
    "Submersible pump ": (
        "An electrically driven pump installed below the water surface in the "
        "source well or intake structure to lift raw water to the treatment "
        "system at the required flow rate."
    ),
    "Wind turbine rotor lock": (
        "A mechanical brake and locking mechanism that immobilizes the wind "
        "turbine rotor for safe maintenance, high-wind shutdown, or emergency "
        "stop conditions."
    ),
    "Extra storage tank": (
        "A buffer tank that stores treated product water or brine concentrate, "
        "decoupling production rate fluctuations from demand and providing "
        "capacity for brine disposal scheduling."
    ),
    "Gate valve": (
        "A full-bore isolation valve used to start, stop, or throttle flow "
        "within the piping system. Gate valves provide low pressure drop when "
        "fully open and are standard in water treatment infrastructure."
    ),
    "Gear and Booster Pump": (
        "A gear pump or centrifugal booster pump that raises feedwater pressure "
        "to the level required for effective reverse osmosis membrane operation, "
        "compensating for system head losses."
    ),
    "Calcite bed contactors": (
        "A post-treatment vessel packed with calcite (calcium carbonate) media "
        "that remineralizes RO permeate by dissolving into the low-TDS product "
        "water, raising pH and hardness to potable standards."
    ),
    # ── Electrical system ─────────────────────────────────────────────────────
    "Turbine": (
        "A wind or mechanical turbine that converts kinetic energy into "
        "electrical power to supply the desalination system's pumps, "
        "controls, and ancillary loads."
    ),
    "PLC": (
        "A Programmable Logic Controller that automates sequencing, monitoring, "
        "and control of the desalination system, including pump scheduling, "
        "pressure regulation, and alarm management."
    ),
    "Submersible pump": (
        "An electrically driven pump installed below the water surface to "
        "extract raw water from a well or intake and deliver it to the "
        "pre-treatment stage at the required flow and pressure."
    ),
    "Battery (1 day of power)": (
        "An electrochemical energy storage bank sized to provide one full day "
        "of system operation, ensuring continuous desalination output during "
        "periods of low wind or turbine maintenance."
    ),
    "Booster Pump": (
        "A high-pressure centrifugal pump that elevates feedwater pressure to "
        "the operating point of the RO membranes, typically 150-600 psi "
        "depending on feedwater salinity."
    ),
    "RO membranes in parallel": (
        "Multiple reverse osmosis membrane elements arranged in parallel to "
        "increase system capacity while sharing the high-pressure feed. "
        "Each membrane rejects dissolved salts, producing low-TDS permeate."
    ),
    "Calcite bed contactors": (
        "Post-treatment vessels filled with calcite media that dissolve into "
        "the RO permeate to restore minerals, raise alkalinity, and prevent "
        "corrosion in distribution piping."
    ),
    "Multi-Media Filtration": (
        "A multi-layer filtration vessel containing sand, anthracite, and "
        "garnet media that removes suspended solids, turbidity, and "
        "particulates from feedwater ahead of the RO membranes."
    ),
    "Brine Well": (
        "A dedicated injection or disposal well into which concentrated brine "
        "reject from the RO process is safely discharged to a suitable "
        "geological formation, preventing surface contamination."
    ),
    "Pipes (total)": (
        "The complete piping network, including suction, feed, high-pressure, "
        "permeate, and brine lines, that interconnects all process equipment "
        "throughout the electrical desalination system."
    ),
    # ── Miscellaneous / shared ────────────────────────────────────────────────
    "Green blend addition": (
        "Addition of a blend of minerals or pH-adjusting chemicals to the "
        "product water to meet regulatory requirements for taste, hardness, "
        "and corrosion inhibition before distribution."
    ),
    "Activated carbon (annual)": (
        "Granular or pelletized activated carbon used to adsorb chlorine, "
        "organic compounds, and taste/odor compounds from the product water; "
        "replaced on an annual maintenance cycle."
    ),
    "Evaporation Pond": (
        "A large, shallow lined pond where brine concentrate is discharged and "
        "water evaporates under solar radiation, leaving behind a dry salt "
        "residue for periodic removal or disposal."
    ),
    "Piston pump": (
        "A positive-displacement piston pump used to deliver precise, "
        "high-pressure flow of feedwater or chemical dosing solutions, "
        "suitable for variable-speed wind-driven operation."
    ),
    "Antiscalant (assuming 3g/L of antiscalant)": (
        "A chemical additive dosed at approximately 3 g/L into the RO feedwater "
        "to inhibit scale formation (calcium carbonate, sulfate) on membrane "
        "surfaces, extending membrane life and maintaining flux."
    ),
    "55 gallon container is 2500 USD, for 1 million gal/day lasts about 20 days": (
        "A standard 55-gallon drum of chemical reagent (antiscalant or "
        "treatment chemical) costing approximately $2,500 per drum; at a "
        "consumption rate supporting 1 million gallons per day, each drum "
        "lasts roughly 20 days."
    ),
}
