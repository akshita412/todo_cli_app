# Project Status

A plain English overview of what this project is, what's been built, and what's left.
Updated at the end of each working session.

---

## What are we building?

A command-line to-do app in Python called `todo-cli`.

You install it once and use it entirely from your terminal:
```bash
todo add "Write tests" --due 2026-06-01
todo list
todo complete 1
todo delete 2
```

Tasks are saved locally to `~/.todo/tasks.json`. No accounts, no browser, no cloud.

Target users: developers and engineers who live in the terminal and don't want to switch to Notion or Jira to manage daily tasks.

Full requirements: `docs/todo-cli-MVP-PRD.md`

---

## Architecture (3 layers)

```
CLI  →  Service  →  Storage
```

- **CLI** — what you type (`todo add`, `todo list`, etc.)
- **Service** — business logic (validation, status rules)
- **Storage** — reads and writes tasks to disk

Each layer is independent. You can swap the storage backend (JSON → SQLite) without touching the CLI.

---

## What's been built

### M1 — Foundation ✅
- `models.py` — Task data structure and Status enum
- `exceptions.py` — Error types (ValidationError, TaskNotFoundError, etc.)
- `storage/base.py` — Abstract storage interface
- `cli.py` — All 5 commands defined (stubs, not wired up yet)
- CI — GitHub Actions runs tests on every push

### M2 — Storage ✅
- `storage/json_store.py` — Full JSON backend implementation
- Saves tasks to `~/.todo/tasks.json`
- Auto-assigns IDs, never reuses deleted IDs
- Data survives restart (reads from disk on every call)
- 8 tests covering all storage operations

**Test count: 16 tests, all passing.**

## Tooling set up
- `log-session` — logs each session summary to Notion automatically (`log-session --notes "..."`)
- `gh` CLI — installed and authenticated, manages the GitHub Projects board
- GitHub Projects board — synced with milestone progress (github.com/akshita412/todo_cli_app → Projects → Todo CLI)

---

## What's left

### M3 — Service layer (next)
`service.py` — the business logic between CLI and storage.
- Validate descriptions (not empty, max 255 chars)
- Validate due dates (can't be in the past)
- Handle complete/delete with proper error messages

### M4 — Wire up the CLI
Connect the CLI commands to the service layer.
Right now `todo add` just prints a placeholder. After M4 it will actually save a task.

### M5 — Polish
- SQLite backend (optional, for users who prefer it)
- Test coverage ≥ 80%
- Clean error messages (no stack traces ever shown to users)

### M6 — PyPI release
- Publish to PyPI so anyone can `pip install todo-cli`
- Final README for public users

---

## File map (what matters day-to-day)

| File | Purpose |
|------|---------|
| `src/todo_cli/models.py` | Task data structure |
| `src/todo_cli/exceptions.py` | Error types |
| `src/todo_cli/cli.py` | CLI entry point |
| `src/todo_cli/service.py` | Business logic (not built yet) |
| `src/todo_cli/storage/json_store.py` | JSON storage backend |
| `tests/test_cli.py` | CLI tests |
| `tests/test_storage.py` | Storage tests |
| `pyproject.toml` | Dependencies and build config |

---

## How to run it

```bash
uv sync --dev          # install dependencies
uv run pytest          # run all tests
uv run todo --help     # try the CLI
```

---

*Last updated: 2026-05-28 — M2 complete, starting M3 next session.*
