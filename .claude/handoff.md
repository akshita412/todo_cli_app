# Session Handoff

**Date:** 2026-06-04
**Branch:** chore/post-m3-cleanup (off main @ fffb7e0)
**Last merged work:** PR #1 — feat(m3): service layer (MERGED into main)

---

## What was completed this session

### M3 — Service layer (DONE + MERGED)
- `src/todo_cli/service.py` — `TaskService` with `add_task`, `complete_task`, `delete_task`, `list_tasks`
- Validation: empty desc → `ValidationError`, past due → `InvalidDateError`, unknown id → `TaskNotFoundError`
- `tests/test_service.py` — 13 TDD tests, all green
- **PR #1 merged into `main`** (`fffb7e0`). Local `main` fast-forwarded; feature branch deleted.

### Post-M3 cleanup (this branch — not yet committed)
- Killed the `datetime.utcnow()` deprecation: now timezone-aware `datetime.now(timezone.utc)` in `models.py`, `service.py`, and `tests/test_service.py`
- Full suite: **29 passing, 0 warnings** (was 29 passing / 24 deprecation warnings)
- Notion journal: removed duplicate M3 entry (one canonical entry remains)
- `log-session` tool refactored to push-only (no Anthropic API; runs on Pro via `NOTION_TOKEN`)

---

## Current state

| Layer | Status |
|-------|--------|
| Models + Exceptions | ✅ Done |
| Storage (JSON backend) | ✅ Done |
| Service layer | ✅ Done + merged |
| **CLI ↔ service wiring** | ❌ Stubbed — this is M4 |

CLI commands (`add`, `list`, `complete`, `delete`, `show`) still print placeholders and are NOT connected to `TaskService`.

---

## Next session — M4, Wire CLI to the service layer

Connect each Click command in `src/todo_cli/cli.py` to `TaskService`:
- Construct the storage backend (JSON default, SQLite via `TODO_BACKEND=sqlite`) and wrap in `TaskService`
- `add` → `add_task`; `list` → `list_tasks` (Rich table, overdue highlight); `complete` → `complete_task`; `delete` → `delete_task` (respect `--force`); `show` → fetch one
- Map domain exceptions to friendly CLI errors + non-zero exit codes
- TDD: extend `tests/test_cli.py` (Click `CliRunner`), tests first

### Open housekeeping before/at start of M4
- **Commit this cleanup branch** (`chore/post-m3-cleanup`) or fold it into the first M4 commit — currently uncommitted.
- Move the M4 board item to **In Progress** before coding.

---

## Locked decisions (do not revisit)

| Decision | Value |
|----------|-------|
| Package layout | `src/todo_cli/` |
| Data model | stdlib dataclass (no Pydantic) |
| Storage default | JSON (`~/.todo/tasks.json`) |
| Storage alt | SQLite opt-in via `TODO_BACKEND=sqlite` |
| `duration` field | Dropped — not in PRD |
| CLI commands | Top-level, no subgroups |
| CI | GitHub Actions, Python 3.10 + 3.12 |
| PyPI publish | Real goal — M6 |
| PRD source of truth | `docs/todo-cli-MVP-PRD.md` |

---

## Session preferences (user)

- 30 minutes per session (may grow over time)
- TDD: plain-English explanation of each test BEFORE showing code; user approves before green
- Start every session: read `CLAUDE.md`, `docs/code-map.md`, `.claude/handoff.md`
- End every session: update this handoff + commit
- Log sessions to Notion: just ask Claude — it authors the entry and runs `log-session` (Pro-only, no API key)
- Feature creep rule: park mid-session ideas in `docs/plans/quickstart-backlog.md` under "Later"

---

## Milestone tracker

| Milestone | Status |
|-----------|--------|
| M1 — Scaffolding | ✅ Done |
| M2 — JSON Storage Backend | ✅ Done |
| M3 — Service layer | ✅ Done + merged |
| M4 — CLI commands wired up | 🔄 Next |
| M5 — Polish + coverage gate (≥80%) | — |
| M6 — PyPI release | — |
