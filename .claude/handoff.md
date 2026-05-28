# Session Handoff

**Date:** 2026-05-28
**Branch:** main
**Last commit:** feat(m2): complete storage test suite — all 8 JsonStorageBackend tests passing

---

## What was completed this session

### M2 — JSON Storage Backend
- `src/todo_cli/storage/json_store.py` — full `JsonStorageBackend` implementation
- `tests/test_storage.py` — all 8 TDD tests written and passing
- Fixed `log-session` tool: model name, Notion DB ID, `.profile` whitespace bug
- All 11 tests passing (8 CLI + 3... wait, 8 storage + 8 CLI = wait, 8 storage tests + existing CLI tests)

### Tooling
- `log-session` fully working — run with `log-session --notes "..."` directly in Claude Code
- `gh` CLI installed and authenticated — can manage GitHub Projects board directly from Claude Code
- GitHub Projects board cleaned up — all stale vteam-hybrid items removed, 6 milestone items added with correct statuses

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

## Next session — M3, Service Layer

### Exactly where we stopped

M2 is fully done. `JsonStorageBackend` is complete and all 8 storage tests pass.

### What's next

Build `src/todo_cli/service.py` — pure business logic layer between CLI and storage.

Planned tests for M3 (`tests/test_service.py`):

| # | Test | What it checks |
|---|------|---------------|
| 1 | `test_add_task_returns_task_with_id` | service.add_task() delegates to storage, returns task |
| 2 | `test_add_task_raises_on_empty_description` | empty string raises `ValidationError` |
| 3 | `test_add_task_raises_on_past_due_date` | due date in the past raises `InvalidDateError` |
| 4 | `test_complete_task_sets_status_and_timestamp` | status → COMPLETED, completed_at set |
| 5 | `test_complete_task_raises_for_missing_id` | unknown ID raises `TaskNotFoundError` |
| 6 | `test_delete_task_removes_it` | task gone after delete |
| 7 | `test_list_tasks_returns_all` | returns all tasks from storage |

### Session protocol (unchanged)
1. Explain test in plain English first
2. Show code
3. User approves
4. Implement to make it pass
5. Repeat

---

## Session preferences (user)

- 30 minutes per session (may increase over time)
- TDD: plain English explanation BEFORE showing test code
- Start every session by reading: `CLAUDE.md`, `docs/code-map.md`, `.claude/handoff.md`
- End every session with updated handoff + commit
- `log-session --notes "..."` to push to Notion (run directly in Claude Code, no separate terminal needed)
- Feature creep rule: park mid-session ideas in `docs/plans/quickstart-backlog.md` under "Later"

---

## Milestone tracker

| Milestone | Status |
|-----------|--------|
| M1 — Scaffolding | ✅ Done |
| M2 — JSON Storage Backend | ✅ Done |
| M3 — Service layer | 🔄 Next |
| M4 — CLI commands wired up | — |
| M5 — Polish + coverage gate (≥80%) | — |
| M6 — PyPI release | — |
