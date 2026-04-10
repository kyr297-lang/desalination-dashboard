# POLISH-04 Print Output Verification (D-06, D-07, D-08)

## Test method
Verified @media print CSS rules in assets/custom.css (lines 154-200) against expected checklist.

## Expected visible in print
- ✅ RAG scorecard table — `.scorecard-print-section` has `page-break-inside: avoid`, scorecard NOT in hidden list — PASS
- ✅ Cost Over Time chart with Plotly in-chart legend — `showlegend=True` confirmed in build_cost_chart; charts/graphs NOT hidden — PASS
- ✅ Power Breakdown chart — `.dcc-graph, .js-plotly-plot` kept full-width — PASS
- ✅ System badge — not in any display:none rule — PASS
- ✅ System accent top border — stage-heading accent classes have `print-color-adjust: exact` — PASS

## Expected hidden in print
- ❌ Sidebar NOT visible — `#sidebar { display: none !important }` at line 157 — PASS
- ❌ Navbar NOT visible — `.navbar { display: none !important }` at line 156 — PASS
- ❌ System tabs NOT visible — `#system-tabs { display: none !important }` at line 162 — PASS
- ❌ Back-to-overview link NOT visible — `#back-to-overview { display: none !important }` at line 163 — PASS
- ❌ Chart control panel sliders NOT visible — `.chart-controls { display: none !important }` at line 171 — PASS
- ❌ Badge pill legend row NOT visible (Phase 17 NEW) — `.legend-badge-row { display: none !important }` at line 168 — PASS
- ❌ Export/Print button NOT visible — `.no-print { display: none !important }` at line 165 covers export button — PASS
- ✅ Page layout dropdown available — `@page` rule at top level (not inside @media print) present — PASS

## Result: PASS
All print whitelist/blacklist items verified via CSS inspection. Phase 17 badge pill row hide is confirmed in place.
