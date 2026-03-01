# Phase 10: Landing Page - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Add a project introduction section above the existing system selection cards in the Overview tab. The section displays contributor names and course context so students know who built this and why before interacting with system cards. No new navigation, no new pages — just content added to the existing overview layout.

</domain>

<decisions>
## Implementation Decisions

### Section design
- Use a `dbc.Card` to frame the intro section — matches existing card-based layout
- Full width to align with the system card row below
- Card styling details (header accent color, shadow) at Claude's discretion — should complement, not compete with, the system-colored cards below

### Content & tone
- Include contributor names and course context (Fall 2025–Spring 2026 senior design class)
- Exact wording, tone, length, and whether to reference the dashboard name or university — at Claude's discretion
- Keep it concise enough that system cards remain visible without scrolling on a typical screen

### Contributor display
- Display all four names: Amogh Herle, Sofia Ijazi, Kevin Ren, Kyler Sanders
- Names only — no roles, links, or avatars
- Presentation format (inline sentence vs list), name order, and styling at Claude's discretion

### Placement & spacing
- Intro section appears above the system selection cards
- Should be compact enough that system cards are visible without scrolling
- What to do with the existing instruction text ("Start by clicking Explore...") — at Claude's discretion (absorb, keep, or remove)
- Spacing and heading presence at Claude's discretion

### Claude's Discretion
- Card header accent color (or no header)
- Shadow style (match system cards or differentiate)
- Intro text tone (academic vs conversational) and exact wording
- Contributor name order and inline formatting
- Whether to include a heading like "About This Project"
- Handling of existing instruction text
- Vertical spacing between intro and system cards

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches. The user gave Claude broad latitude on design and content decisions. The key constraints are: card-based, full-width, compact, names + course context included.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `dbc.Card`, `dbc.CardHeader`, `dbc.CardBody` — used throughout for system cards, can reuse same patterns
- `SYSTEM_COLORS` from `src/config` — available if accent color needed
- Bootstrap utility classes (`text-muted`, `small`, `shadow-sm`, `mb-3`) — established styling pattern

### Established Patterns
- Overview layout built in `src/layout/overview.py` via `create_overview_layout()`
- Returns `html.Div` containing intro text + `dbc.Row` of cards
- System cards use `dbc.Col(width=4)` in a `dbc.Row(className="g-3")`

### Integration Points
- `create_overview_layout()` in `src/layout/overview.py` — add intro card above existing content
- Called from `render_content()` in `src/layout/shell.py` when `active_system is None`
- No callback changes needed — purely layout addition

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 10-landing-page*
*Context gathered: 2026-03-01*
