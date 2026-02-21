# Wind-Powered Desalination Dashboard

## What This Is

An interactive 2D dashboard built with Python (Dash/Plotly) that lets users explore and compare three wind-powered desalination system configurations — mechanical, electrical, and hybrid — for a municipality of ~10,000 people. Designed as an academic tool for engineering students to understand design tradeoffs in wind-powered desalination.

## Core Value

Students can visually compare mechanical, electrical, and custom hybrid desalination systems side-by-side to understand cost, land, and efficiency tradeoffs — and build intuition for real engineering decisions.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Three-system selection interface (mechanical, electrical, hybrid)
- [ ] Equipment detail view showing parts, data, and descriptions for mechanical and electrical systems
- [ ] Hybrid "build your own" interface with 5 functional slots (Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal)
- [ ] Hybrid system completion gate — user must fill all functional slots before seeing details
- [ ] Equipment selection shows detailed data and description per part
- [ ] Cost/land/efficiency scorecard with red/yellow/green ranking
- [ ] Comparison description of hybrid system vs. the other two preset systems
- [ ] Cost over time graph with user-selectable time horizon
- [ ] Land area comparison graph across all three systems
- [ ] Wind turbine count per system graph
- [ ] Pie chart showing energy percentage by action (water extraction, desalination)
- [ ] All graphs compare mechanical, electrical, and hybrid side-by-side
- [ ] Electrical system battery/tank tradeoff slider (bigger storage tank vs. smaller battery)
- [ ] Academic visual design — clean, professional, not tacky or high-tech
- [ ] Data sourced from `data.xlsx` Excel file in project directory
- [ ] Runs locally via `python app.py`
- [ ] Optionally deployable to a hosted service (Render, Railway, etc.)

### Out of Scope

- 3D visualization — 2D dashboard only
- Real-time wind data integration — static/calculated data from spreadsheet
- Mobile-optimized layout — desktop-first academic tool
- User accounts or saving configurations — stateless dashboard

## Context

- Data lives in `data.xlsx` with three sections: Electrical Components, Mechanical Components, Miscellaneous (hybrid parts)
- Electrical sheet includes battery fraction vs. tank fraction tradeoff table (11 rows, 0% to 100% battery)
- Mechanical system uses 4x 250kW aeromotor turbines; electrical uses 1 turbine + battery/PLC
- Miscellaneous parts include green blend addition, activated carbon, evaporation pond, piston pump, antiscalant
- Equipment data includes: quantity, cost (USD), energy (kW), land area (m²), lifespan (years)
- Target: potable water for ~10,000 people (~1 million gal/day)
- Hybrid functional categories: Water Extraction, Pre-Treatment, Desalination, Post-Treatment, Brine Disposal
- Dashboard will be used by future engineering students — clarity and learnability are paramount

## Constraints

- **Tech stack**: Python with Dash/Plotly — academic standard, students likely familiar
- **Data source**: Must read from existing `data.xlsx` — single source of truth
- **Audience**: Engineering students — academic tone, no flashy UI
- **Deployment**: Must work locally (`python app.py`) and be deployable to free hosting

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dash/Plotly for dashboard | Academic standard, good data viz, Python ecosystem | — Pending |
| 5 hybrid functional slots | Maps to real desalination process stages | — Pending |
| User-selectable time horizon for cost graph | Allows exploration of short vs. long-term economics | — Pending |
| Red/yellow/green ranking system | Intuitive at-a-glance comparison for students | — Pending |

---
*Last updated: 2026-02-20 after initialization*
