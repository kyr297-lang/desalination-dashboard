"""
app.py
======
Entry point for the Wind-Powered Desalination Dashboard.

Responsibilities:
  1. Load data.xlsx at module level (fail fast — never inside a callback).
  2. Create the Dash application with the FLATLY Bootstrap theme.
  3. Conditionally set the layout: shell on success, error page on failure.
  4. Auto-open a browser tab when run directly (python app.py).

Usage
-----
  python app.py
"""

import sys
import traceback

import dash
import dash_bootstrap_components as dbc

from src.data.loader import load_data
from src.layout.shell import create_layout
from src.layout.error_page import create_error_page

# ──────────────────────────────────────────────────────────────────────────────
# 1. Load data at module level
# ──────────────────────────────────────────────────────────────────────────────

DATA = None
_error_msg = ""
_detail_str = ""

try:
    DATA = load_data()
    print("[OK] data.xlsx loaded — all sections parsed successfully")
except FileNotFoundError as exc:
    _error_msg = str(exc)
    _detail_str = traceback.format_exc()
    print(f"[ERROR] {exc}", file=sys.stderr)
except ValueError as exc:
    _error_msg = str(exc)
    _detail_str = traceback.format_exc()
    print(f"[ERROR] {exc}", file=sys.stderr)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Create Dash app
# ──────────────────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
)
app.title = "Wind-Powered Desalination Dashboard"

# Allow callbacks that reference IDs not yet in the layout (needed when
# multi-page content is added in future phases).
app.config.suppress_callback_exceptions = True

# ──────────────────────────────────────────────────────────────────────────────
# 3. Set layout conditionally
# ──────────────────────────────────────────────────────────────────────────────

if DATA is not None:
    app.layout = create_layout(DATA)
else:
    app.layout = create_error_page(error=_error_msg, details=_detail_str)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Main block — run server with auto-open browser
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import threading
    import webbrowser

    PORT = 8050

    # Schedule browser open 1 second after server starts.
    # debug=False prevents Flask reloader from spawning a second process
    # (which would open a second browser tab).
    threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()

    app.run(debug=False, port=PORT)
