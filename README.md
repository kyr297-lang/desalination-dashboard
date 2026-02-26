# Wind-Powered Desalination Dashboard

Interactive engineering comparison tool for three desalination system architectures: **Mechanical**, **Electrical**, and **Hybrid**.

Built with Python, Dash, and Plotly. Deployed on Render.

---

## Quick Start (Local Development)

```bash
# 1. Install Python 3.11+ from https://www.python.org

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
python app.py
```

The dashboard opens automatically at **http://localhost:8050**.

---

## Project Structure

```
├── app.py                  # Entry point — starts the Dash server
├── data.xlsx               # Source data (equipment specs & costs)
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── .python-version         # Python version (3.11)
│
├── src/                    # Application code
│   ├── config.py           # Colors, equipment metadata, stage mappings
│   │
│   ├── data/               # Data layer
│   │   ├── loader.py       # Parses data.xlsx into DataFrames
│   │   └── processing.py   # Calculations, formatting, RAG scoring
│   │
│   └── layout/             # UI components
│       ├── shell.py        # App shell, sidebar, navigation
│       ├── overview.py     # Landing page with system cards
│       ├── system_view.py  # System detail view with tabs
│       ├── charts.py       # Plotly chart builders & callbacks
│       ├── scorecard.py    # RAG comparison table
│       ├── hybrid_builder.py   # 5-stage hybrid pipeline builder
│       ├── equipment_grid.py   # Equipment detail cards
│       └── error_page.py       # Data load error display
│
└── assets/
    └── custom.css          # Custom styling
```

---

## How to Make Changes

### Updating Equipment Data
Edit `data.xlsx` directly. The dashboard reads it on startup — no code changes needed.

### Modifying the UI
- **Colors & metadata** → `src/config.py`
- **Charts** → `src/layout/charts.py`
- **Scorecard / comparison table** → `src/layout/scorecard.py`
- **Hybrid builder dropdowns** → `src/layout/hybrid_builder.py`
- **Styling** → `assets/custom.css`

### Adding New Equipment
1. Add the row in `data.xlsx` under the correct section
2. Add the equipment-to-stage mapping in `src/config.py` → `PROCESS_STAGES`
3. Optionally add a description in `src/config.py` → `EQUIPMENT_DESCRIPTIONS`

---

## Deploying to Render

This project is configured for [Render](https://render.com) deployment:

1. Push this code to a GitHub repository
2. In Render, create a new **Web Service** and connect the GitHub repo
3. Render auto-detects the `Procfile` and deploys
4. Enable **Auto-Deploy** so any push to `main` triggers a redeploy

### Auto-Deploy Workflow
```
Edit code locally → git push → Render auto-redeploys → Live in ~1 minute
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| dash | 4.0.0 | Web framework (includes Plotly) |
| dash-bootstrap-components | 2.0.4 | Bootstrap 5 UI components |
| pandas | 2.2.3 | Data manipulation |
| openpyxl | 3.1.5 | Excel file parsing |
| gunicorn | 23.0.0 | Production WSGI server |
