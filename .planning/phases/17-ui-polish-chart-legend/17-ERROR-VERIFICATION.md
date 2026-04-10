# POLISH-03 Error Page Verification (D-04, D-05)

## Test method
- Renamed data.xlsx → data.xlsx.bak, started app, confirmed HTTP 200 response
- Verified `create_error_page` component structure programmatically
- Restored data.xlsx, confirmed normal startup

## Error page component structure (verified via Python)
- Root element: Div → Col (width=8)
- H2("Unable to Load Dashboard", className="text-danger mt-5") — PASS
- P("The dashboard could not start because the data file could not be read.") — PASS
- Alert(error_message, color="danger") — PASS
- Accordion with "Details (for technical users)" (start_collapsed=True) — PASS

## app.py wiring
- Line 36: `DATA = load_data()` in try block
- Line 77: `app.layout = create_error_page(error=_error_msg, details=_detail_str)` in else block
- App correctly falls through to error layout when data.xlsx missing — PASS

## Console output on missing file
```
[ERROR] data.xlsx not found at expected path: ...
Ensure the file is in the project root directory.
```

## Result: PASS
Error page renders with readable heading, error message, and detail accordion on data.xlsx failure.
