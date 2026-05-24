---
agent-notes: { ctx: "human model for product decisions and proxy mode", deps: [docs/tracking/2026-04-16-todo-cli-discovery.md], state: active, last: "pat@2026-04-16" }
---

# Product Context — todo-cli

## Decision Style

Present options for architectural or irreversible decisions — the user wants to choose consciously and understand the tradeoff. For routine implementation choices (naming, formatting, minor structure), pick and move with a one-line explanation. The learning happens at the architectural layer, not in boilerplate.

## Quality vs. Speed

Clean, always. A rough edge not understood is worse than a 2-hour delay. The 3-layer architecture separation is non-negotiable even when it slows delivery. 4 hours understood beats 2 hours opaque.

## Scope Appetite

Flag and park. Interesting mid-build ideas go to the backlog under "Later" — never explored in-session. Feature creep was named as a failure mode in discovery. Hold the line even if the user gets excited in the moment.

## TDD Involvement

User reviews and approves failing tests before implementation starts. Does not write tests from scratch (still learning), but reads each assertion, understands what it checks, and consciously approves before green phase begins. This is the primary mechanism for building understanding vs. just watching output.

## Non-Negotiable

**3-layer architecture.** CLI layer touches only Click and rendering. Service layer is pure logic with zero I/O. Storage layer owns all persistence behind an abstract interface. If CLI reaches into storage directly, or service layer does I/O, the codebase is to be scrapped and rebuilt. The separation is the learning artifact — it must be correct or it teaches the wrong thing.

## Proxy Rules (when user is unavailable)

- Approve scope additions only if they fit within a named "Later" backlog item already parked.
- Never approve architectural shortcuts — always block and wait.
- Default to "flag and park" for anything ambiguous.
- Never sacrifice layer separation for delivery speed.

## Project Goals (from discovery)

- Primary: hands-on learning of Claude Code, GitHub CLI, terminal-native development
- Secondary: fix fragmented task tracking (Slack/tabs/notes)
- Long-term: reusable reference codebase + baseline template for future AI engineering projects, including sprint management via CLI in future iterations
