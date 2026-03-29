# Deferred Items — Phase 15

## Pre-existing Test Failures (out of scope for 15-01)

### test_compute_chart_data_sliders.py

**Status:** Failing BEFORE Plan 15-01 changes (verified via git stash)
**Root cause:** Test fixture uses old 6-column schema (`energy_kw`, `land_area_m2`) and synthetic_data dict is missing `hybrid` key. Test also references `land_area`/`turbine_count` as compute_chart_data return keys — these are removed in Plans 15-02/15-03.
**When to fix:** Plan 15-03 (after processing.py and charts.py overhaul completes)
**Research doc note:** Listed under "Wave 0 Gaps" in 15-RESEARCH.md
