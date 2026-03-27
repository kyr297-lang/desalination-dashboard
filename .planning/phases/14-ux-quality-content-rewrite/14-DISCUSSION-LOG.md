# Phase 14: UX Quality & Content Rewrite - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-27
**Phase:** 14-ux-quality-content-rewrite
**Areas discussed:** First-visit banner, Loading spinner scope, Landing page rewrite, Mechanical content

---

## First-Visit Banner (UX-05)

### Banner placement

| Option | Description | Selected |
|--------|-------------|----------|
| Above the control panel | Directly above the slider card — most contextual | ✓ |
| Top of page content | Full-width at top of main area | |
| Inside control card header | Subtle info line in header | |

**User's choice:** Above the control panel

---

### Dismiss trigger

| Option | Description | Selected |
|--------|-------------|----------|
| First slider interaction | Disappears on first drag or click of any slider | ✓ |
| Explicit close button only | User must click X | |
| Any click anywhere | Disappears on any click | |

**User's choice:** First slider interaction
**Notes:** User specified the banner text itself should explicitly tell users to drag a slider to dismiss it

---

### Persistence

| Option | Description | Selected |
|--------|-------------|----------|
| Session-only via dcc.Store | Reappears on fresh reload | ✓ |
| Persisted via localStorage | Never reappears on same device | |

**User's choice:** Session-only via dcc.Store

---

### Banner text

| Option | Description | Selected |
|--------|-------------|----------|
| Slider-focused, short | One sentence, functional, drag-to-dismiss instruction | ✓ |
| Broader how-to-use | Navigation + sliders, two sentences | |
| User writes it | Custom wording | |

**User's choice:** Slider-focused, short
**Exact text:** "Use the sliders below to adjust salinity, depth, and storage mix — charts update on mouse release. Drag any slider to dismiss this tip."

---

## Loading Spinner Scope (UX-01)

### Wrapper scope

| Option | Description | Selected |
|--------|-------------|----------|
| One wrapper, all chart outputs | Single dcc.Loading for the entire chart area | ✓ |
| Individual per-chart | Four separate dcc.Loading wrappers | |

**User's choice:** One wrapper around all chart outputs

---

### Spinner type

| Option | Description | Selected |
|--------|-------------|----------|
| Default circle | Standard Bootstrap circle spinner | ✓ |
| Dot | Three-dot pulsing | |
| Cube | Animated cube | |

**User's choice:** Default circle

---

## Landing Page Rewrite (CONTENT-01)

### Intro depth

| Option | Description | Selected |
|--------|-------------|----------|
| Stay brief, fix stale content | 2-sentence format, fix stale descriptions | |
| Expand with more detail | 2-3 additional sentences | |
| Rewrite intro card completely | Full rewrite with clear structure | ✓ |

**User's choice:** Rewrite intro card completely

---

### Intro card title

| Option | Description | Selected |
|--------|-------------|----------|
| Keep "About This Project" | Neutral, familiar | ✓ |
| Change to "Wind-Powered Desalination" | More descriptive | |
| You decide | Claude picks | |

**User's choice:** Keep "About This Project"

---

### Content focus

| Option | Description | Selected |
|--------|-------------|----------|
| What the tool does + how to use it | Action-oriented, slider guidance | |
| Project purpose + technical context | Senior design context, municipal scenario, 3 systems | ✓ |
| User writes it | Custom content | |

**User's choice:** Project purpose + technical context
**Notes:** User wanted option 2 but without data source mentions, and with emphasis on what the project is trying to accomplish/the goal

---

## Mechanical Content (CONTENT-02)

### Component list source

| Option | Description | Selected |
|--------|-------------|----------|
| Match Phase 12 BOM exactly | Derive from data.xlsx Part 1 Mechanical rows | ✓ |
| User provides list | User specifies names | |
| Claude's discretion | Read data.xlsx and infer | |

**User's choice:** Match Phase 12 BOM exactly (researcher reads data.xlsx)

---

### Description depth

| Option | Description | Selected |
|--------|-------------|----------|
| Same depth as existing (1-2 sentences) | Match existing config.py style | ✓ |
| More detailed (3-4 sentences) | Include operating parameters | |
| Briefer (1 sentence) | Just identify what it does | |

**User's choice:** Same depth as existing descriptions

---

## Claude's Discretion

- Exact dcc.Store ID name for banner dismissed-state
- Whether banner store goes in shell.py or charts layout
- Banner CSS styling details
- Exact paragraph structure for landing page rewrite

## Deferred Ideas

None

---

*Logged: 2026-03-27*
