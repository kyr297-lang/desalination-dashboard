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
    "Groundwater Extraction": "#4AACB0",   # muted teal
    "Pressure Boost":         "#7B68A8",   # muted purple
    "RO Desalination":        "#D4A739",   # muted amber
    "Brine Reinjection":      "#C46E5A",   # muted brick red
    "Other":                  "#999999",   # medium grey (fallback)
}

# Per-system subsystem INPUT power (kW) — what the turbine shaft must supply.
# Source: FDR Tables 2–4, P_input column. Design conditions:
#   Q_feed = 0.0548 m³/s, depth = 275 m, ED = 1.5 kWh/m³, P_inject = 550 psi.
# Shaft process loads (P_subsystem) are identical across systems: 641.0 kW total.
# P_input differs because each system routes subsystems through different drivetrain
# paths (hydraulic vs. electrical), each with distinct efficiency losses.
# Hybrid: Groundwater Extraction uses the hydraulic path; all other subsystems
#         use the electrical path.
SUBSYSTEM_POWER_INPUT = {
    "mechanical": {
        "Groundwater Extraction": 241.9,
        "Pressure Boost":          80.4,
        "RO Desalination":        405.5,
        "Brine Reinjection":      106.6,
    },
    "electrical": {
        "Groundwater Extraction": 203.7,
        "Pressure Boost":          67.8,
        "RO Desalination":        341.6,
        "Brine Reinjection":       89.8,
    },
    "hybrid": {
        "Groundwater Extraction": 241.9,   # hydraulic drivetrain path
        "Pressure Boost":          67.8,   # electrical drivetrain path
        "RO Desalination":        341.6,   # electrical drivetrain path
        "Brine Reinjection":       89.8,   # electrical drivetrain path
    },
}

# Conversion factors: shaft power delta → input power delta per subsystem/system.
# factor = P_input / P_subsystem from FDR. Applied when TDS/depth sliders change
# the shaft load — the input power change is scaled by the drivetrain factor.
SUBSYSTEM_DRIVETRAIN_FACTOR = {
    "mechanical": {
        "Groundwater Extraction": 241.9 / 185.8,
        "Pressure Boost":          80.4 / 61.8,
        "RO Desalination":        405.5 / 311.5,
        "Brine Reinjection":      106.6 / 81.9,
    },
    "electrical": {
        "Groundwater Extraction": 203.7 / 185.8,
        "Pressure Boost":          67.8 / 61.8,
        "RO Desalination":        341.6 / 311.5,
        "Brine Reinjection":       89.8 / 81.9,
    },
    "hybrid": {
        "Groundwater Extraction": 241.9 / 185.8,   # hydraulic path
        "Pressure Boost":          67.8 / 61.8,    # electrical path
        "RO Desalination":        341.6 / 311.5,   # electrical path
        "Brine Reinjection":       89.8 / 81.9,    # electrical path
    },
}

# Shared shaft process loads (P_subsystem, kW) — kept for reference / legacy use.
# These are the same for all three systems. Use SUBSYSTEM_POWER_INPUT for the
# energy chart, which shows turbine input power (P_input).
SUBSYSTEM_POWER = {
    "Groundwater Extraction": 185.8,
    "Pressure Boost":         61.8,
    "RO Desalination":        311.5,
    "Brine Reinjection":      81.9,
}

# Default equipment lifespans (years) used when xlsx has no lifespan column.
# "indefinite" means the item is purchased once and never replaced.
# Keys must match exact equipment name strings from data.xlsx column B.
LIFESPAN_DEFAULTS = {
    # Electrical system
    "Battery (Tesla Megapack 3.9MWh unit)": 12,
    "RO Membrane Trains": 7,
    # Mechanical system
    "Reverse osmosis train": 7,
    # Hybrid system
    "Battery (Tesla Megapack 3.9 MWh)": 12,
    "Reverse Osmosis Trains": 7,
    # Default: everything else is indefinite (no replacement)
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
        "Power & Drive": [
            "1 MW Aeromotor Turbine",
            "Wind turbine rotor lock",
            "Gearbox (Winergy  PEAB series)",
            "Variable-Displacement Hydraulic Power Unit (HPU)",
            "300 Bar Hydraulic Manifold (Custom Ductile Iron Block)",
            "Hydraulic Motor (225 kW rating) (Haaglund CA 50)",
            "Hydraulic Motor (225 kW rating) (Haaglund CA 70)",
        ],
        "Water Extraction": [
            "Vertical Turbine Pump (PSI Prolew Flowserve VTP)",
        ],
        "Desalination": [
            "Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)",
            "High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)",
            "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post treatment)",
        ],
        "Brine & Storage": [
            "Extra storage tank (100,000 gallons)",
            "Brine Disposal Well",
        ],
        "Support": [
            "Gate valve",
            "Pipes (total)",
        ],
    },
    "electrical": {
        "Power & Drive": [
            "1.5\u202fMW Turbine (GE Vernova 1.5sle)",
            "Battery (Tesla Megapack 3.9MWh unit)",
        ],
        "Water Extraction": [
            "Submersible Pumps (WDM (Nidec) NHE Series high-head submersible)",
        ],
        "Desalination": [
            "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post treatment)",
            "Booster Pumps (Grundfos CR 10-10 K)",
        ],
        "Brine & Storage": [
            "Brine Disposal Well",
        ],
        "Support": [
            "PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)",
            "Piping (total)",
        ],
    },
    "hybrid": {
        "Power & Drive": [
            "1 MW Aeromotor Turbine",
            "Wind turbine rotor lock",
            "Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft",
            "Variable-Displacement Hydraulic Power Unit (HPU)",
            "Hydraulic Motor (225 kW rating) (Haaglund CA 70)",
            "Battery (Tesla Megapack 3.9MWh unit)",
            "HCI544E 3-Phase - Stamford | 600 kW ",
            "Rectifier/Inverter Package",
        ],
        "Water Extraction": [
            "Vertical Turbine Pump (PSI Prolew Flowserve VTP)",
        ],
        "Desalination": [
            "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post treatment)",
            "High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)",
        ],
        "Brine & Storage": [
            "Extra storage tank (100,000 gallons)",
            "Brine Disposal Well",
        ],
        "Support": [
            "PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)",
            "Pipes (total)",
        ],
    },
}

# EQUIPMENT_DESCRIPTIONS provides a 1-2 sentence technical description for
# each equipment item in the mechanical, electrical, and hybrid systems.
# Audience: engineering students. Keys match column B strings exactly.
EQUIPMENT_DESCRIPTIONS = {
    # ── Mechanical system ──────────────────────────────────────────────────────
    "Wind turbine rotor lock": (
        "A mechanical brake and locking mechanism that immobilizes the wind "
        "turbine rotor for safe maintenance, high-wind shutdown, or emergency "
        "stop conditions."
    ),
    "Gate valve": (
        "A full-bore isolation valve used to start, stop, or throttle flow "
        "within the piping system. Gate valves provide low pressure drop when "
        "fully open and are standard in water treatment infrastructure."
    ),
    "Calcite bed contactors": (
        "A post-treatment vessel packed with calcite (calcium carbonate) media "
        "that remineralizes RO permeate by dissolving into the low-TDS product "
        "water, raising pH and hardness to potable standards."
    ),
    "Gearbox (Winergy  PEAB series)": (
        "A multi-stage planetary gearbox from the Winergy PEAB series that steps "
        "up turbine shaft speed to the operating speed required by the hydraulic "
        "power unit, transmitting mechanical power with high efficiency."
    ),
    "Variable-Displacement Hydraulic Power Unit (HPU)": (
        "A variable-displacement hydraulic power unit that converts mechanical "
        "shaft input into high-pressure hydraulic flow, enabling continuous "
        "output control regardless of wind speed fluctuations."
    ),
    "Hydraulic Motor (225 kW rating) (Haaglund CA 50)": (
        "A Haaglund CA 50 low-speed high-torque hydraulic motor rated at 225 kW "
        "that converts hydraulic pressure into mechanical rotation to drive "
        "high-pressure pumps directly."
    ),
    "Hydraulic Motor (225 kW rating) (Haaglund CA 70)": (
        "A Haaglund CA 70 low-speed high-torque hydraulic motor rated at 225 kW, "
        "used alongside the CA 50 to distribute hydraulic power across multiple "
        "pump loads in the mechanical drivetrain."
    ),
    "Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)": (
        "A triplex plunger pump that delivers high-pressure feedwater to the "
        "reverse osmosis membranes through positive-displacement action, "
        "driven by the hydraulic motor drivetrain."
    ),
    "High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)": (
        "A Danfoss APP axial piston pump that pressurizes feedwater to the "
        "operating point required for reverse osmosis membrane separation."
    ),
    "Reverse osmosis train": (
        "A reverse osmosis membrane train that rejects dissolved salts from "
        "pressurized feedwater, producing low-TDS permeate for post-treatment "
        "and distribution."
    ),
    "Extra storage tank (100,000 gallons)": (
        "A 100,000-gallon buffer tank that stores product water or brine "
        "concentrate, providing operational flexibility during variable "
        "wind conditions."
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
    # ── New electrical names (Phase 15 xlsx update) ───────────────────────────
    "1.5\u202fMW Turbine (GE Vernova 1.5sle)": (
        "A GE Vernova 1.5sle wind turbine rated at 1.5 MW that converts wind "
        "energy into electricity to power the desalination system's pumps, "
        "controls, and ancillary loads."
    ),
    "PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)": (
        "A Siemens SIMATIC S7-1200 programmable logic controller that automates "
        "sequencing, monitoring, and control of the desalination system, including "
        "pump scheduling, pressure regulation, and alarm management."
    ),
    "Submersible Pumps (WDM (Nidec) NHE Series high-head submersible)": (
        "Nidec NHE Series high-head submersible pumps installed below the water "
        "surface to extract raw groundwater and deliver it to the pre-treatment "
        "stage at the required flow and pressure."
    ),
    "Battery (Tesla Megapack 3.9MWh unit)": (
        "A Tesla Megapack utility-scale battery module with 3.9 MWh capacity "
        "that stores electrical energy generated by the wind turbine, ensuring "
        "continuous 24/7 desalination output during low-wind periods."
    ),
    "Booster Pumps (Grundfos CR 10-10 K)": (
        "Grundfos CR 10-10 K multi-stage centrifugal booster pumps that elevate "
        "feedwater pressure to the operating point of the RO membranes."
    ),
    "RO Membrane Trains": (
        "Multiple reverse osmosis membrane trains arranged in parallel to increase "
        "system capacity while sharing the high-pressure feed, each rejecting "
        "dissolved salts to produce low-TDS permeate."
    ),
    "Multi-Media Filtration System (Pure Aqua MF-500 Series FRP Filter Skid)": (
        "A Pure Aqua MF-500 series multi-media filtration skid that removes "
        "suspended solids and turbidity from feedwater using layered sand, "
        "anthracite, and garnet media prior to the RO membranes."
    ),
    "Piping (total)": (
        "The complete piping network, including suction, feed, high-pressure, "
        "permeate, and brine lines, that interconnects all process equipment "
        "throughout the desalination system."
    ),
    # ── Hybrid system ─────────────────────────────────────────────────────────
    "1 MW Aeromotor Turbine": (
        "A large-format wind turbine rated at 1 MW that provides primary mechanical "
        "energy to the hydraulic drivetrain; the same turbine platform as the "
        "mechanical system, enabling shared component sourcing."
    ),
    "Gearbox (Winergy PEAB series)": (
        "A multi-stage planetary gearbox from the Winergy PEAB series that steps "
        "up turbine shaft speed to the operating speed required by the hydraulic "
        "power unit, transmitting mechanical power with high efficiency."
    ),
    "Variable-Displacement HPU": (
        "A variable-displacement hydraulic power unit that converts mechanical "
        "shaft input from the gearbox into high-pressure hydraulic flow, allowing "
        "continuous output control regardless of wind speed fluctuations."
    ),
    "300 Bar Hydraulic Manifold (Custom Ductile Iron Block)": (
        "A custom-machined ductile iron hydraulic manifold rated to 300 bar that "
        "distributes high-pressure hydraulic fluid to multiple actuators, "
        "minimizing piping connections and pressure losses in the drivetrain."
    ),
    "Hydraulic Motor (225 kW, Haaglund CA 50)": (
        "A Haaglund CA 50 low-speed high-torque hydraulic motor rated at 225 kW "
        "that converts hydraulic pressure into mechanical rotation to drive the "
        "high-pressure RO feed pump directly."
    ),
    "High Pressure Pump (Danfoss APP 78/1500 180B7808)": (
        "A Danfoss APP axial piston pump rated for high-pressure RO feed "
        "pressurization, delivering up to 1500 L/min at the pressure required "
        "for membrane separation in the reverse osmosis train."
    ),
    "Battery (Tesla Megapack 3.9 MWh)": (
        "A Tesla Megapack utility-scale battery module with 3.9 MWh capacity "
        "that stores electrical energy generated by the turbine generator, "
        "supplying the electrical subsystem loads (VTP, brine pump, PLC) "
        "for continuous 24/7 operation."
    ),
    "Vertical Turbine Pump (PSI Prolew Flowserve VTP)": (
        "A Flowserve vertical turbine pump used for groundwater extraction, "
        "electrically driven from the battery bank in the hybrid system to "
        "decouple extraction from the hydraulic drivetrain."
    ),
    "Booster Pump (Grundfos CR 10-10 K)": (
        "A Grundfos CR series multi-stage centrifugal booster pump that raises "
        "feedwater pressure ahead of the RO membranes, electrically driven "
        "from the battery supply in the hybrid configuration."
    ),
    "PLC (Siemens SIMATIC S7-1200 CPU1215C-1)": (
        "A Siemens SIMATIC S7-1200 programmable logic controller that provides "
        "automated sequencing, pressure monitoring, and fault management for "
        "the hybrid system's mixed hydraulic and electrical subsystems."
    ),
    "Multi-Media Filtration System (Pure Aqua MF-500 Series)": (
        "A Pure Aqua MF-500 series multi-media filtration skid that removes "
        "suspended solids and turbidity from feedwater using layered sand, "
        "anthracite, and garnet media prior to the RO membranes."
    ),
    "Reverse Osmosis Trains": (
        "Parallel reverse osmosis membrane trains that reject dissolved salts "
        "from pressurized feedwater, producing low-TDS permeate for post-treatment "
        "and distribution."
    ),
    "Calcite Bed Contactor (DrinTec FRP Calcite Contactor)": (
        "A DrinTec fiberglass-reinforced calcite contactor that remineralizes "
        "RO permeate by dissolving calcium carbonate media, restoring pH, "
        "hardness, and alkalinity to potable water standards."
    ),
    "Brine Disposal Well": (
        "Note: this is not a discrete equipment item but an entire engineered "
        "system — a permitted subsurface injection well with casing, wellhead "
        "assembly, and injection pumping infrastructure for safe disposal of RO "
        "brine concentrate. It is non-COTS and requires site-specific geological "
        "assessment, regulatory permitting, and custom civil/drilling works; no "
        "standard product lifespan applies."
    ),
    "Extra Storage Tank (100,000 gallons)": (
        "A 100,000-gallon product water or brine buffer tank that decouples "
        "the production rate from demand, providing operational flexibility "
        "during variable wind conditions."
    ),
    "Piping (total)": (
        "The complete piping network for the hybrid system, encompassing "
        "hydraulic lines, process water feed, RO permeate, brine reject, "
        "and chemical dosing connections between all process stages."
    ),
    # ── Shared across systems ─────────────────────────────────────────────────
    "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post treatment)": (
        "An integrated skid combining multi-media pre-treatment filtration, reverse "
        "osmosis membrane trains, and post-treatment remineralization into a single "
        "packaged system, rejecting dissolved salts and producing potable-quality permeate."
    ),
    "Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft": (
        "A Winergy PEAB series planetary gearbox configured with a second output shaft "
        "to simultaneously drive both the hydraulic power unit and an AC alternator, "
        "splitting mechanical power between the hydraulic and electrical subsystems."
    ),
    "HCI544E 3-Phase - Stamford | 600 kW ": (
        "A Stamford HCI544E synchronous AC alternator rated at 600 kW that converts "
        "mechanical drivetrain power from the gearbox second shaft into three-phase AC "
        "electricity for battery charging and electrical pump loads."
    ),
    "Rectifier/Inverter Package": (
        "A power electronics package that rectifies three-phase AC output from the "
        "alternator into DC for battery charging, and inverts stored DC back to AC "
        "to supply variable-frequency motor drives and system loads."
    ),
    # ── Shared chemical treatment ──────────────────────────────────────────────
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

# Clean display names for equipment items shown in the UI.
# Keys are exact data.xlsx column B strings (with unicode); values are
# the human-readable versions.  Items not in this dict display as-is.
# Usage: DISPLAY_NAMES.get(raw_name, raw_name)
DISPLAY_NAMES: dict[str, str] = {
    # Electrical — narrow no-break space U+202F before "MW"
    "1.5\u202fMW Turbine (GE Vernova 1.5sle)": "1.5 MW Turbine (GE Vernova 1.5sle)",
    # Electrical — non-breaking space U+00A0 before "CPU"
    "PLC (Siemens SIMATIC S7-1200\xa0CPU1215C-1)": "PLC (Siemens SIMATIC S7-1200 CPU1215C-1)",
    # Mechanical / Hybrid — double space in Winergy name; fix lowercase "series"
    "Gearbox (Winergy  PEAB series)": "Gearbox (Winergy PEAB Series)",
    # Hybrid — double space + non-standard second-shaft config
    "Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft": (
        "Gearbox (Winergy PEAB Series) — Must Be Ordered with Second Output Shaft"
    ),
    # Mechanical — en-dash U+2013
    "Plunger Pump (Triplex Plunger Pump K 13000 \u2013 3G)": "Plunger Pump (Triplex Plunger Pump K 13000 - 3G)",
    # Mechanical / Hybrid — missing closing paren
    "High Pressure Pump (Danfoss APP 78/1500 180B7808 (1300 L/min)": "High Pressure Pump (Danfoss APP 78/1500 180B7808, 1300 L/min)",
    # Capitalisation fixes — items below display as-is but have lowercase words
    "Wind turbine rotor lock": "Wind Turbine Rotor Lock",
    "Gate valve": "Gate Valve",
    "Pipes (total)": "Pipes (Total)",
    "Piping (total)": "Piping (Total)",
    "Extra storage tank (100,000 gallons)": "Extra Storage Tank (100,000 gallons)",
    "Hydraulic Motor (225 kW rating) (Haaglund CA 50)": "Hydraulic Motor (225 kW Rating) (Haaglund CA 50)",
    "Hydraulic Motor (225 kW rating) (Haaglund CA 70)": "Hydraulic Motor (225 kW Rating) (Haaglund CA 70)",
    "Battery (Tesla Megapack 3.9MWh unit)": "Battery (Tesla Megapack 3.9 MWh Unit)",
    "Submersible Pumps (WDM (Nidec) NHE Series high-head submersible)": (
        "Submersible Pumps (WDM (Nidec) NHE Series High-Head Submersible)"
    ),
    "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post treatment)": (
        "Pure Aqua Large Reverse Osmosis System RO-600 (Includes Pre and Post Treatment)"
    ),
    # Hybrid alternator — trailing space in xlsx string
    "HCI544E 3-Phase - Stamford | 600 kW ": "HCI544E 3-Phase - Stamford | 600 kW",
}

# Raw xlsx component names that are NOT commercial off-the-shelf products.
# Used by equipment_grid.py to add an asterisk marker and render a legend.
NON_COTS_COMPONENTS: frozenset[str] = frozenset({
    "300 Bar Hydraulic Manifold (Custom Ductile Iron Block)",
    "Hydraulic Motor (225 kW rating) (Haaglund CA 50)",
    "Gearbox (Winergy  PEAB series) - Must be ordered with second output shaft",
    "Rectifier/Inverter Package",
    "Brine Disposal Well",
})

# Drivetrain efficiency constants (turbine shaft output → RO pump shaft input).
# Derived from FDR report Tables 2–4: η = P_subsystem_total / P_input_total.
# Mechanical:  641.0 kW / 834.4 kW = 76.8%
# Electrical:  641.0 kW / 702.9 kW = 91.2%
# Hybrid:      641.0 kW / 741.1 kW = 86.5%
DRIVETRAIN_EFFICIENCY = {
    "mechanical": 0.768,
    "electrical": 0.912,
    "hybrid":     0.865,
}

# LCOW denominator: cumulative potable water production over 20-year project life.
# Q_potable = 157.7 m³/hr × 0.30 wind capacity factor × 0.95 plant availability × 8760 hr/yr × 20 yr
#           = 7,874,276 m³
# Converted: 7,874,276 m³ × 264.172 gal/m³ / 1000 = 2,080,163 thousand US gallons
# Usage: LCOW ($/kgal) = total_capex_usd / LCOW_DENOMINATOR_KGAL
LCOW_DENOMINATOR_KGAL = 2_080_163.0

# Static comparison table content for the consolidated 3-system comparison.
# Each row maps to a dict of {system_label: cell_text}.
# Rendered by system_view.py below the equipment accordion.
COMPARISON_TABLE_DATA = {
    "Drive mechanism": {
        "Mechanical": "Hydraulic drivetrain (gearbox, HPU, hydraulic motors)",
        "Electrical": "Electric motors powered by grid-tied wind turbine",
        "Hybrid": "Hydraulic drivetrain for RO; electric motors for extraction and brine",
    },
    "Energy storage": {
        "Mechanical": "Pressurized hydraulic accumulators and water tanks",
        "Electrical": "Tesla Megapack 3.9 MWh lithium-ion battery bank",
        "Hybrid": "Battery bank (electrical loads) + hydraulic accumulator (RO loads)",
    },
    "Key advantage": {
        "Mechanical": "No battery degradation; simple, robust drivetrain components",
        "Electrical": "Highest drivetrain efficiency (91%); precise electronic control",
        "Hybrid": "87% drivetrain efficiency; balances resilience and reduced losses",
    },
    "Key limitation": {
        "Mechanical": "Lowest drivetrain efficiency (77%); limited speed control flexibility",
        "Electrical": "Battery replacement every 12 years adds significant lifecycle cost",
        "Hybrid": "Most complex system; requires both hydraulic and electrical maintenance",
    },
    "Best suited for": {
        "Mechanical": "Remote sites prioritizing long-term simplicity over efficiency",
        "Electrical": "Sites with stable wind and access to battery supply chains",
        "Hybrid": "Sites needing operational resilience with moderate efficiency",
    },
}
