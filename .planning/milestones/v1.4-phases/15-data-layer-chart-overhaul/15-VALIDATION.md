---
phase: 15
slug: data-layer-chart-overhaul
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-28
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none (default discovery) |
| **Quick run command** | `python -m pytest tests/ -x -q` |
| **Full suite command** | `python -m pytest tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 15-01-01 | 01 | 1 | DATA-01 | smoke | `python -c "from src.data.loader import load_data; load_data()"` | ❌ W0 | ⬜ pending |
| 15-01-02 | 01 | 1 | DATA-02 | unit | `python -m pytest tests/test_loader_columns.py -x` | ❌ W0 | ⬜ pending |
| 15-01-03 | 01 | 1 | DATA-03 | unit | `python -m pytest tests/test_cost_over_time.py -x` | ❌ W0 | ⬜ pending |
| 15-01-04 | 01 | 1 | DATA-04 | unit | `python -m pytest tests/test_subsystem_power.py -x` | ❌ W0 | ⬜ pending |
| 15-02-01 | 02 | 2 | CHART-01 | smoke | `python -c "from src.layout.charts import make_chart_section; s=make_chart_section(); assert 'chart-land' not in str(s)"` | ❌ W0 | ⬜ pending |
| 15-02-02 | 02 | 2 | CHART-02 | smoke | `python -c "from src.layout.charts import make_chart_section; s=make_chart_section(); assert 'chart-turbine' not in str(s)"` | ❌ W0 | ⬜ pending |
| 15-02-03 | 02 | 2 | CHART-03 | unit | `python -m pytest tests/test_energy_bar_chart.py -x` | ❌ W0 | ⬜ pending |
| 15-02-04 | 02 | 2 | CHART-04 | unit | `python -m pytest tests/test_compute_chart_data_sliders.py -x` | ✅ needs update | ⬜ pending |
| 15-02-05 | 02 | 2 | CHART-05 | unit | `python -m pytest tests/test_compute_chart_data_sliders.py -x` | ✅ needs update | ⬜ pending |
| 15-02-06 | 02 | 2 | CHART-06 | manual | Run app, drag each slider, verify all 4 labels update | manual-only | ⬜ pending |
| 15-02-07 | 02 | 2 | CHART-07 | smoke | `python -c "import subprocess; r=subprocess.run(['grep','-r','chart-pie','src/'],capture_output=True); assert r.returncode==1, 'chart-pie still exists'"` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_loader_columns.py` — new tests for DATA-01, DATA-02, DATA-03
- [ ] `tests/test_subsystem_power.py` — new tests for DATA-04 subsystem power constants
- [ ] `tests/test_energy_bar_chart.py` — new tests for CHART-03 3-subsystem power breakdown
- [ ] Update `tests/test_compute_chart_data_sliders.py` — update battery name and stage key references for CHART-04/05
- [ ] Update `tests/test_interpolate_energy.py` — verify still passes after processing.py changes

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Slider labels update on drag | CHART-06 | Requires running Dash app interactively | Run `python app.py`, open browser, drag each of the 4 sliders, verify label-years, label-battery-ratio, label-tds, label-depth all update |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
