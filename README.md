# Wind-Powered Desalination Dashboard

Interactive engineering dashboard for comparing three desalination system architectures — **Mechanical**, **Electrical**, and **Hybrid** — powered by wind energy.

Built with Python, Dash, and Plotly. Deployed on [Render](https://render.com).

---

## Features

- **System Overview** — side-by-side comparison cards for Mechanical, Electrical, and Hybrid systems
- **Detailed System Views** — per-system equipment specs, power breakdowns, and cost analysis
- **Interactive Charts** — slider-driven parameter exploration (wind speed, recovery ratio, etc.)
- **RAG Scorecard** — Red/Amber/Green comparison table across key metrics
- **Hybrid Builder** — drag-and-drop 5-stage pipeline builder for custom hybrid configurations
- **Equipment Grid** — detailed cards showing specs for every piece of equipment

---

## Quick Start

```bash
# 1. Install Python 3.11+
# 2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
python app.py
```

Opens at **http://localhost:8050**.

---

## Project Structure

```
desalination-dashboard/
│
├── app.py                  # Entry point — starts the Dash server
├── data.xlsx               # Source data (equipment specs, costs, parameters)
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── .python-version         # Python version pin (3.11)
│
├── src/                    # Application source code
│   ├── config.py           # Colors, equipment metadata, stage mappings
│   ├── data/               # Data layer
│   │   ├── loader.py       #   Parses data.xlsx into DataFrames
│   │   └── processing.py   #   Calculations, formatting, RAG scoring
│   └── layout/             # UI components
│       ├── shell.py        #   App shell, sidebar, navigation
│       ├── overview.py     #   Landing page with system cards
│       ├── system_view.py  #   System detail view with tabs
│       ├── charts.py       #   Plotly chart builders & callbacks
│       ├── scorecard.py    #   RAG comparison table
│       ├── hybrid_builder.py   # 5-stage hybrid pipeline builder
│       ├── equipment_grid.py   # Equipment detail cards
│       └── error_page.py       # Data load error display
│
├── assets/
│   └── custom.css          # Custom styling
│
└── tests/                  # Unit tests
    ├── test_interpolate_energy.py
    └── test_compute_chart_data_sliders.py
```

---

## Making Changes

### Updating Data
Edit `data.xlsx` directly — the dashboard reads it on startup, no code changes needed.

### Modifying the UI
| What to change | Where to look |
|---|---|
| Colors & metadata | `src/config.py` |
| Charts & sliders | `src/layout/charts.py` |
| Scorecard table | `src/layout/scorecard.py` |
| Hybrid builder | `src/layout/hybrid_builder.py` |
| Styling | `assets/custom.css` |

### Adding New Equipment
1. Add the row in `data.xlsx` under the correct section
2. Add the equipment-to-stage mapping in `src/config.py` → `PROCESS_STAGES`
3. Optionally add a description in `src/config.py` → `EQUIPMENT_DESCRIPTIONS`

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| dash | 4.0.0 | Web framework (includes Plotly) |
| dash-bootstrap-components | 2.0.4 | Bootstrap 5 UI components |
| pandas | 2.2.3 | Data manipulation |
| openpyxl | 3.1.5 | Excel file parsing |
| gunicorn | 23.0.0 | Production WSGI server |

---

## Deployment

Deployed on [Render](https://render.com) as a Web Service. The `Procfile` configures gunicorn as the production server.

To deploy your own instance:
1. Fork this repo
2. Create a new Web Service on Render, connected to your fork
3. Render auto-detects the Procfile and deploys
