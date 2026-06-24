# Session Handoff

**Date:** 2026-06-24
**Branch:** `main` (all work merged; no open branches)
**Status:** 🎉 **MVP COMPLETE — M1 through M6 all shipped and merged.**

---

## Current state

The app is **done, installed, and in daily personal use.** `todo` is on PATH at
`~/.local/bin/todo` (installed via `uv tool install git+https://github.com/akshita412/todo_cli_app`).

| Layer | Status |
|-------|--------|
| Models + Exceptions | ✅ |
| Storage (JSON backend, atomic writes, corruption-hardened) | ✅ |
| Service layer | ✅ |
| CLI: 6 commands (`add`/`list`/`show`/`edit`/`complete`/`delete`) | ✅ |
| Packaging + GitHub-install distribution | ✅ |
| Docs (PRD, code-map, README, project-status) reconciled to reality | ✅ |

**72 tests passing, coverage ~99% (gate ≥95%).** Data lives in `~/.todo/tasks.json`
(override with `TODO_DATA_PATH`).

## Milestone tracker

| Milestone | Status |
|-----------|--------|
| M1 — Scaffolding | ✅ Done + merged |
| M2 — JSON Storage Backend | ✅ Done + merged |
| M3 — Service layer | ✅ Done + merged |
| M4 — CLI commands wired up | ✅ Done + merged |
| M5 — Polish (coverage gate + storage hardening; SQLite deferred) | ✅ Done + merged |
| M6 — Share it (GitHub install + README) | ✅ Done + merged (PRs #21–#24) |

Board: all six cards show **Done**.

---

## What this session did (2026-06-24)

- Atomic writes #15 (PR #20) — reviewed, merged; closed the last M5 follow-up.
- M6 in full: packaging metadata + MIT license, GitHub-install verification, README
  rewrite, sdist hardening (review caught it bundling the whole repo + a gitignored
  local file), PRD/code-map reconciliation, README expanded into a user guide.
- Installed the tool persistently for the user's daily use.
- Board updated (M1–M6 Done); Notion Session Log kept current.

---

## Next (optional — post-MVP, nothing blocking)

1. **Project/tag field** — *highest-value next feature.* The app is one flat list; the
   user wants to log tasks per project. Target: `todo add "…" --project X` +
   `todo list --project X`. Would be the first post-MVP milestone. Workaround documented
   in the README (separate lists via `TODO_DATA_PATH` aliases, or tag-in-description +
   `grep`). See [[mvp-status]] memory.
2. **CI install-smoke job** — cover the macOS/Ubuntu acceptance claim (only Linux/WSL2
   verifiable locally).
3. **`todo --version` flag** — small nicety for an installed CLI.

If pursuing #1, follow the Session Entry Protocol: create the work item, run the
Architecture Gate (a new `--project` field touches model + storage + service + CLI), then
Tara writes failing tests first.

---

## Locked decisions (do not revisit)

| Decision | Value |
|----------|-------|
| Package layout | `src/todo_cli/` |
| Data model | stdlib dataclass (no Pydantic) |
| Storage default | JSON (`~/.todo/tasks.json`) — only shipped backend |
| Storage alt | SQLite **deferred** post-MVP (opt-in via `TODO_BACKEND=sqlite` when built) |
| `duration` field | Dropped — not in PRD |
| CLI commands | Top-level, no subgroups; 6 commands incl. `edit` |
| `complete` behavior | One-way (mark done). No un-complete/toggle in MVP. |
| CI | GitHub Actions, Python 3.10 + 3.12 |
| Distribution | GitHub install (`uv tool install git+…`). No PyPI (kept publish-ready). |
| PRD source of truth | `docs/todo-cli-MVP-PRD.md` |

---

## Session preferences (user)

- TDD: plain-English explanation of each test BEFORE showing code; user approves before green.
- Start every session: read `CLAUDE.md`, `docs/code-map.md`, `.claude/handoff.md`.
- End every session: update this handoff + commit.
- Log sessions to Notion: just ask — Claude authors the entry and pushes it (Pro, no API key).
- User is now a **daily user** of the tool, not just its developer — weigh real-use ergonomics.
