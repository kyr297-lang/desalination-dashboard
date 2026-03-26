# Phase 12: Data Layer & Hybrid Builder Removal - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-26
**Phase:** 12-data-layer-hybrid-builder-removal
**Areas discussed:** Energy sheet wiring, Hybrid preset display, Builder removal depth

---

## Energy Sheet Wiring

**Q: What should the dashboard use from the Energy sheet?**
- Options: Key summary values only / Full subsystem breakdown / Just parse it don't wire yet
- **Selected:** Full subsystem breakdown — parse all rows (GW extraction, RO feed, brine) per system and show per-subsystem power in the breakdown chart

**Q: Should per-subsystem values replace existing hardcoded/calculated values in the power breakdown chart?**
- Options: Yes, drive chart from Energy sheet / Keep calculated, Energy sheet is reference
- **Selected:** Yes, drive chart from Energy sheet — chart becomes the source of truth from data.xlsx

**Q: Should selected turbine size from the Energy sheet drive the turbine count chart?**
- Options: Yes, use Energy sheet turbine size / No, turbine size stays hardcoded
- **Selected:** Yes, use Energy sheet turbine size — turbine count = total load ÷ selected turbine size, both from Energy sheet

**Q: Should the loader expose all columns or just numeric values?**
- Options: All columns / Numeric values only
- **Selected:** All columns — full DataFrame from Energy sheet stored in data dict; charts pick what they need, future phases can use the rest

---

## Hybrid Preset Display

**Q: What should the hybrid page show in place of the 5-slot builder?**
- Options: Static table only / Table + preset label / Table + short explanation
- **Selected:** Static table only — equipment table showing hybrid BOM, same style as mechanical/electrical

**Q: Should the scorecard render immediately on page load?**
- Options: Yes, render immediately / Keep some gate
- **Selected:** Yes, render immediately — all 3 system columns load at startup, consistent with mechanical and electrical

---

## Builder Removal Depth

**Q: Should hybrid_builder.py be deleted or just imports removed?**
- Options: Delete the file / Remove imports only
- **Selected:** Delete the file — full removal, no dead modules

**Q: What about dcc.Store, gate overlay, and hybrid-equipment-container?**
- Options: Remove all of it / Remove gate only / Remove store + gate
- **Selected:** Remove all of it — clean slate removal of all builder-related artifacts
