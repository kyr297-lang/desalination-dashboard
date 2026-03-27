# Deferred Items — Phase 12

Discovered during 12-01 execution. Out-of-scope for 12-01 (data layer only).

## Remaining "miscellaneous" references in src/

These files still reference `data["miscellaneous"]`, `PROCESS_STAGES["miscellaneous"]`,
or related patterns. They will crash when the app runs because the loader no longer
provides a `"miscellaneous"` key.

| File | Line(s) | Issue | Planned Fix |
|------|---------|-------|-------------|
| `src/data/processing.py` | multiple | Uses `data["miscellaneous"]`, search_order includes `"miscellaneous"`, docstrings reference it | Plan 12-03 (processing/charts update) |
| `src/layout/equipment_grid.py` | line referencing `"miscellaneous"` | Passes `"miscellaneous"` as system key | Plan 12-02 or 12-03 |
| `src/layout/hybrid_builder.py` | multiple | Uses `PROCESS_STAGES["miscellaneous"]` | Plan 12-02 (hybrid_builder removal) |

These are tracked — do NOT fix in 12-01.
