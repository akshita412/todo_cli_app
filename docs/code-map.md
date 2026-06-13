---
agent-notes:
  ctx: "codebase structural overview for humans and agents"
  deps: []
  state: active
  last: "claude@2026-06-13"
---
# Code Map

Read this at the start of every session to orient before touching code.

## Architecture at a Glance

```
CLI (cli.py)  ← DONE (M4) — all 6 commands wired, Rich table output
  │  Click commands, output rendering, exit codes
  │  depends on ↓
Service (service.py)  ← DONE (M3 + edit)
  │  Pure business logic, validation, status transitions
  │  depends on ↓
Storage (storage/)
  │  Abstract interface + JSON backend
  └── json_store.py  ← DONE (M2)
  └── sqlite_store.py  ← DEFERRED post-MVP (opt-in)

Models (models.py)  ← used by all three layers
Exceptions (exceptions.py)  ← used by all three layers
Factory (factory.py)  ← build_service() — env-driven wiring (M4)
```

## Package Summary

### `src/todo_cli/`

| Module | Status | Purpose |
|--------|--------|---------|
| `cli.py` | Done | Click entry point. All 6 commands wired to the service; `handle_errors` maps domain errors → stderr + exit 1/2; Rich table for `list`. |
| `factory.py` | Done | `build_service()` — reads `TODO_BACKEND` (json default) + `TODO_DATA_PATH`; returns a `TaskService`. Unknown backend → `ValueError`. |
| `models.py` | Done | `Task` dataclass + `Status` enum. `is_overdue` property. Timezone-aware UTC timestamps. |
| `exceptions.py` | Done | 6 domain exceptions: `ValidationError`, `InvalidDateError`, `TaskNotFoundError`, `StorageCorruptError`, `StorageAccessError` (last two not yet raised — see M5 Wave B). |
| `service.py` | Done | `TaskService`: `add_task`, `complete_task`, `delete_task`, `list_tasks`, `get_task`, `update_description` — validation + status rules. |
| `storage/base.py` | Done | Abstract `StorageBackend` interface: `add`, `get`, `list`, `update`, `delete`. |
| `storage/json_store.py` | Done | JSON backend — full CRUD, persists to `~/.todo/tasks.json` (M2). |
| `storage/sqlite_store.py` | Deferred | SQLite backend — opt-in alternative, deferred post-MVP. |

## CLI Commands (top-level — CRUD complete)

| Command | Syntax | Status |
|---------|--------|--------|
| add | `todo add "<desc>" [--due YYYY-MM-DD]` | Done |
| list | `todo list [--status pending\|completed\|all]` | Done (Rich table + footer) |
| show | `todo show <id>` | Done |
| edit | `todo edit <id> "<desc>"` | Done (CRUD update) |
| complete | `todo complete <id>` | Done (one-way) |
| delete | `todo delete <id> [--force]` | Done |

Exit codes: `0` success · `1` input error · `2` resource not found. Data → stdout, errors → stderr.

## Task Model Fields

`id` · `description` · `due_date` · `status` · `created_at` · `completed_at`
No `duration` field — dropped from PRD.

## Test Inventory (57 total)

| File | Tests | Focus |
|------|-------|-------|
| `tests/test_cli.py` | 28 | CLI behavior — all commands, errors, exit codes, Rich table |
| `tests/test_service.py` | 18 | Service layer logic + validation incl. `get_task`, `update_description` |
| `tests/test_storage.py` | 8 | JSON backend operations (M2) |
| `tests/test_factory.py` | 3 | Env-driven `build_service()` |

## Storage Path (runtime)

- JSON default: `~/.todo/tasks.json`
- Override: set `TODO_DATA_PATH` env var to point at any directory
- SQLite (`TODO_BACKEND=sqlite`): deferred post-MVP

## Key External Dependencies

| Package | Purpose |
|---------|---------|
| `click>=8.1` | CLI framework |
| `rich>=13.0` | Table rendering, overdue highlighting |
| `pytest + pytest-cov` | Test runner + coverage |
| `uv` | Build and package management |
