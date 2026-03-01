# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.2 — Parameter Exploration & Presentation

**Shipped:** 2026-03-01
**Phases:** 5 | **Plans:** 7 | **Commits:** 37

### What Was Built
- Part 2 data layer with TDS and depth lookup table parsing
- Interactive TDS/depth sliders with live np.interp-driven chart updates
- System page visual differentiation (colored top border + pill badge)
- Project landing section with contributors and course context
- Power terminology correction, grouped bar chart, 2-sig-fig formatting

### What Worked
- Parallel phase execution: Phases 9 and 10 ran independently after Phase 7, cutting elapsed time
- Reusable interpolation pattern: interpolate_energy() mirrors interpolate_battery_cost(), making Phase 8 implementation fast
- Human checkpoint model: user-directed pivots (tint→border, slider range) caught early without rework
- Audit-first completion: running `/gsd:audit-milestone` before completion confirmed 15/15 requirements with zero gaps

### What Was Inefficient
- Phase 8 had two plans (08-01, 08-02) when the work was tightly coupled — could have been a single plan
- Phase 9 plan described "background tint" but user directed border at checkpoint — plan text became misleading mid-execution
- SLDR-01 success criteria said 0-1900 PPM but correct range was 0-35,000 PPM — requirements spec was wrong, caught during implementation

### Patterns Established
- `fmt_sig2()` pattern for consistent numeric display — reuse in future formatting needs
- `STAGE_COLORS` dict for deterministic chart color assignment — prevents color drift on data changes
- render_content 2-tuple return (children, style) for system-aware page rendering
- Neutral card header pattern for project-wide content above system-specific cards

### Key Lessons
1. Success criteria should be validated against real data ranges before phase planning — the TDS slider range was wrong in the spec
2. When a design pivot happens at checkpoint, update the plan description to match — prevents confusion in audit
3. Single-plan phases (9, 10, 11) executed faster and cleaner than multi-plan phases (7, 8) for this project's scope

### Cost Observations
- Model mix: predominantly opus for execution, haiku for verification agents
- Sessions: ~5 across 2 days
- Notable: 5 phases in 2 days with parallel execution of independent phases

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Commits | Phases | Key Change |
|-----------|---------|--------|------------|
| v1.0 | 50 | 5 | Foundation — established all patterns |
| v1.1 | 6 | 1 | Deployment — single-phase milestone |
| v1.2 | 37 | 5 | Parallel phases, audit-first completion |

### Top Lessons (Verified Across Milestones)

1. Module-level `set_data()` pattern scales well — used successfully across all 3 milestones without circular import issues
2. Human checkpoints during execution catch design mismatches early — confirmed in v1.0 (hybrid builder), v1.1 (Python version), v1.2 (border vs tint, slider range)
3. Single-plan phases are faster and cleaner for focused feature work — v1.2 phases 9/10/11 vs multi-plan phases
