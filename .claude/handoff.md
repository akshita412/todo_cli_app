# Session Handoff

**Date:** 2026-05-24
**Branch:** main
**Last commit:** feat(m1): complete scaffold — models, exceptions, storage interface, CI

---

## What was completed this session

### Scaffold (`/scaffold-cli`)
- Created `src/todo_cli/` package with stub CLI commands
- `pyproject.toml` with Click, Rich, pytest, uv
- `.gitignore` for Python + uv + SQLite
- GitHub Actions CI (`.github/workflows/ci.yml`) — Python 3.10 + 3.12

### M1 — Foundations
- `src/todo_cli/models.py` — `Task` dataclass, `Status` enum, `is_overdue` property
- `src/todo_cli/exceptions.py` — 6 domain exceptions
- `src/todo_cli/storage/base.py` — abstract `StorageBackend` interface
- CLI commands flattened to top-level (`todo add`, `todo list`, `todo complete`, `todo delete`, `todo show`)
- `docs/adrs/0003-tech-stack.md` — locked stack decision
- PRD copied to `docs/todo-cli-MVP-PRD.docx` from Windows host

### Housekeeping
- `README.md` updated with real project info
- `docs/code-map.md` filled in with actual structure
- CLAUDE.md stale reference removed

**All 8 tests passing. Two commits pushed.**

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
| PRD source of truth | `docs/todo-cli-MVP-PRD.docx` |

---

## Next session — M2, JSON storage backend

### Exactly where we stopped

We were about to write the **first failing test** for `JsonStorageBackend` in `tests/test_storage.py`.

The session protocol is:
1. Explain the test in plain English first
2. Show the test code
3. User reads, asks questions, approves
4. Implement to make it pass
5. Repeat

### The 3 tests planned for next session (30 min)

| # | Test | What it checks |
|---|------|---------------|
| 1 | `test_add_returns_task_with_assigned_id` | `storage.add(task)` assigns auto-incremented ID starting at 1 |
| 2 | `test_get_returns_task_by_id` | `storage.get(1)` returns the task just added |
| 3 | `test_get_returns_none_for_missing_id` | `storage.get(999)` returns `None`, not a crash |

Full storage test list (across all sessions):
- [ ] test_add_returns_task_with_assigned_id
- [ ] test_get_returns_task_by_id
- [ ] test_get_returns_none_for_missing_id
- [ ] test_list_returns_all_tasks_sorted_by_created_at
- [ ] test_update_persists_changes
- [ ] test_delete_removes_task
- [ ] test_id_not_reused_after_deletion
- [ ] test_tasks_persist_across_reinitialisation (file survives reload)

### File to create next session
`src/todo_cli/storage/json_store.py` — implements `StorageBackend` using `~/.todo/tasks.json`

---

## Session preferences (user)

- 30 minutes per session (may increase over time)
- TDD: plain English explanation BEFORE showing test code
- Start every session by reading: `CLAUDE.md`, `docs/code-map.md`, `.claude/handoff.md`
- End every session with updated handoff + commit
- Feature creep rule: park any mid-session ideas in `docs/plans/quickstart-backlog.md` under "Later"

---

## Milestone tracker

| Milestone | Status |
|-----------|--------|
| M1 — Scaffolding | ✅ Done |
| M2 — Storage backends (JSON first, then SQLite) | 🔄 Next |
| M3 — Service layer | — |
| M4 — CLI commands wired up | — |
| M5 — Polish + coverage gate (≥80%) | — |
| M6 — PyPI release | — |
