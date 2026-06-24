---
agent-notes:
  ctx: "codebase structural overview for humans and agents"
  deps: []
  state: active
  last: "sato@2026-06-24"
---
# Code Map

Read this at the start of every session to orient before touching code.

**Status:** MVP complete — M1–M6 all shipped. CLI is fully wired end-to-end and
installable from GitHub (`uv tool install git+https://github.com/akshita412/todo_cli_app`).

## Architecture at a Glance

```
CLI (cli.py)
  │  Click commands, Rich table rendering, exit codes, friendly errors
  │  builds its service via ↓
factory.py (build_service)
  │  env-driven wiring: TODO_BACKEND, TODO_DATA_PATH
  │  depends on ↓
Service (service.py)
  │  Pure business logic, validation, status transitions
  │  depends on ↓
Storage (storage/)
  │  Abstract interface + JSON backend
  └── base.py        StorageBackend (abstract)
  └── json_store.py  JSON backend — atomic writes to ~/.todo/tasks.json

Models (models.py)       ← used by all layers
Exceptions (exceptions.py) ← used by all layers
```

> SQLite was scoped in the PRD but **deferred** — there is no `sqlite_store.py`.
> JSON is the only backend. The `StorageBackend` interface keeps it swappable later.

## Package Summary

### `src/todo_cli/`

| Module | Purpose |
|--------|---------|
| `cli.py` | Click entry point (`cli`). 6 commands, fully wired to the service. Rich table for `list` with overdue highlighting + summary footer. Errors → stderr + non-zero exit. |
| `factory.py` | `build_service()` — constructs a `TaskService` from env config (`TODO_BACKEND` default `json`, `TODO_DATA_PATH` default `~/.todo`). |
| `models.py` | `Task` dataclass + `Status` enum. `is_overdue` property. Timezone-aware UTC timestamps. |
| `exceptions.py` | `TodoError` (base) + `ValidationError`, `InvalidDateError` (subclass of `ValidationError`), `TaskNotFoundError`, `StorageCorruptError`, `StorageAccessError`. |
| `service.py` | `TaskService`: `add_task`, `complete_task`, `delete_task`, `get_task`, `update_description`, `list_tasks`. Validation + status rules. |
| `storage/base.py` | Abstract `StorageBackend` interface: `add`, `get`, `list`, `update`, `delete`. |
| `storage/json_store.py` | JSON backend — full CRUD, atomic writes (temp file + `fsync` + `os.replace`), friendly errors on corrupt/unreadable files. Persists to `~/.todo/tasks.json`. |

## CLI Commands (all wired end-to-end)

| Command | Syntax | Notes |
|---------|--------|-------|
| add | `todo add "<desc>" [--due YYYY-MM-DD]` | Prints the new task id. |
| list | `todo list [--status pending\|completed\|all]` | Rich table; overdue rows highlighted; summary footer. |
| show | `todo show <id>` | All fields for one task. Unknown id → exit 2. |
| complete | `todo complete <id>` | Marks complete (stamps `completed_at`). |
| edit | `todo edit <id> "<desc>"` | Updates a task's description. |
| delete | `todo delete <id> [--force]` | Confirms unless `--force`. |

## Task Model Fields

`id` · `description` · `due_date` · `status` · `created_at` · `completed_at`
No `duration` field — dropped from PRD.

## Test Inventory (72 tests, coverage ~99%, gate ≥95%)

| File | Tests | Focus |
|------|-------|-------|
| `tests/test_cli.py` | 29 | CLI behavior per command — output, flags, exit codes, error paths |
| `tests/test_service.py` | 19 | Service layer logic + validation |
| `tests/test_storage.py` | 21 | JSON backend CRUD, corruption handling, atomic writes |
| `tests/test_factory.py` | 3 | Env-driven backend wiring |

Use Click's `CliRunner` for CLI tests, not subprocess.

## Storage Path (runtime)

- JSON (only backend): `~/.todo/tasks.json`
- Override: set `TODO_DATA_PATH` to point at any directory
- `TODO_BACKEND` defaults to `json` (no other backend implemented)

## Key External Dependencies

| Package | Purpose |
|---------|---------|
| `click>=8.1` | CLI framework |
| `rich>=13.0` | Table rendering, overdue highlighting |
| `pytest + pytest-cov` | Test runner + coverage (gate ≥95% in `pyproject.toml`) |
| `uv` | Build and package management |
