---
agent-notes: { ctx: "discovery tracking for todo-cli kickoff", deps: [docs/plans/quickstart-backlog.md, CLAUDE.md], state: active, last: "cam@2026-04-16" }
---

# Discovery: todo-cli

**Date:** 2026-04-16
**Lead:** Cam
**Status:** Complete
**Prior Phase:** None

## Key Decisions

- Chose CLI over REST API because target user lives in the shell — zero-friction adoption is the product
- Chose JSON default over SQLite default because human-readable, zero-setup, git-trackable for solo dev workflow
- Chose SQLite as opt-in via `TODO_BACKEND=sqlite` env var — clean upgrade path, not default burden
- Chose production-quality architecture over prototype because codebase is a reusable reference template
- Chose local-only storage (no sync) for MVP — intentional scope constraint, not an oversight

## Artifacts Produced

- `docs/plans/quickstart-backlog.md` — 7-command backlog with 3-layer architecture constraint

## Open Questions

- Which parts of the build does the user want to write themselves vs. approve? (Learning risk to monitor)
- Future iteration: sprint management via CLI — not in scope for MVP but shapes architecture choices

## Vision Summary

Solo dev learning project. Dual goal: fix fragmented task tracking (Slack/tabs/notes) AND build first end-to-end terminal project as engineering evidence. Success = 7 commands working + every layer understood by the builder. Failure = abandoned before M3 or Claude writes it all without the user understanding it. Codebase becomes baseline template for future AI engineering projects.

## Next Phase

- Phase 1b: Pat human model elicitation → `docs/product-context.md`
- Phase 2: Sacrificial concepts (Dani)
