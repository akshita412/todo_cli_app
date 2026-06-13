---
agent-notes:
  ctx: "codebase structural overview for humans and agents"
  deps: []
  state: active
  last: "sato@2026-06-04"
---
# Code Map

Read this at the start of every session to orient before touching code.

## Architecture at a Glance

```
CLI (cli.py)
  │  Click commands, output rendering, exit codes
  │  depends on ↓
Service (service.py)  ← DONE (M3)
  │  Pure business logic, validation, status transitions
  │  depends on ↓
Storage (storage/)
  │  Abstract interface + JSON and SQLite backends
  └── json_store.py  ← NOT YET BUILT (M2)
  └── sqlite_store.py  ← NOT YET BUILT (M2)

Models (models.py)  ← used by all three layers
Exceptions (exceptions.py)  ← used by all three layers
```

## Package Summary

### `src/todo_cli/`

| Module | Status | Purpose |
|--------|--------|---------|
| `cli.py` | Stub | Click entry point. All 5 commands defined but print placeholder output — not wired to service layer yet (M4). |
| `models.py` | Done | `Task` dataclass + `Status` enum. `is_overdue` property. Timezone-aware UTC timestamps. |
| `exceptions.py` | Done | 6 domain exceptions: `ValidationError`, `InvalidDateError`, `TaskNotFoundError`, `StorageCorruptError`, `StorageAccessError`. |
| `service.py` | Done | `TaskService`: `add_task`, `complete_task`, `delete_task`, `list_tasks` with validation + status rules (M3). |
| `storage/base.py` | Done | Abstract `StorageBackend` interface: `add`, `get`, `list`, `update`, `delete`. |
| `storage/json_store.py` | Done | JSON backend — full CRUD, persists to `~/.todo/tasks.json` (M2). |
| `storage/sqlite_store.py` | Not started | SQLite backend — opt-in alternative (M5). |

## CLI Commands (top-level, all stubbed)

| Command | Syntax | Status |
|---------|--------|--------|
| add | `todo add "<desc>" [--due YYYY-MM-DD]` | Stub |
| list | `todo list [--status pending\|completed\|all]` | Stub |
| complete | `todo complete <id>` | Stub |
| delete | `todo delete <id> [--force]` | Stub |
| show | `todo show <id>` | Stub |

## Task Model Fields

`id` · `description` · `due_date` · `status` · `created_at` · `completed_at`
No `duration` field — dropped from PRD.

## Test Inventory

| File | Tests | Focus |
|------|-------|-------|
| `tests/test_cli.py` | 8 | CLI smoke tests — happy path per command |
| `tests/test_storage.py` | 8 | JSON backend operations (M2) |
| `tests/test_service.py` | 13 | Service layer logic + validation (M3) |

## Storage Path (runtime)

- JSON default: `~/.todo/tasks.json`
- SQLite opt-in: `~/.todo/tasks.db` (set `TODO_BACKEND=sqlite`)
- Override: set `TODO_DATA_PATH` env var to point at any directory

## Key External Dependencies

| Package | Purpose |
|---------|---------|
| `click>=8.1` | CLI framework |
| `rich>=13.0` | Table rendering, overdue highlighting |
| `pytest + pytest-cov` | Test runner + coverage |
| `uv` | Build and package management |
