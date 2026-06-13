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

### M3 — Service layer ✅ (merged, PR #1)
- `service.py` — `TaskService`, the business logic between CLI and storage
- Validates descriptions (rejects empty → `ValidationError`)
- Validates due dates (rejects past dates → `InvalidDateError`)
- `complete`/`delete` raise `TaskNotFoundError` on unknown IDs; complete stamps a UTC timestamp
- 13 tests, written first (TDD), all passing
- Merged into `main` as PR #1
- Cleanup: switched off the deprecated `datetime.utcnow()` to timezone-aware UTC across models/service/tests — suite now runs warning-free

**Test count: 29 tests, all passing (0 warnings).**

## Tooling set up
- `log-session` — logs each session summary to Notion. Now push-only: Claude Code writes the entry on the Pro subscription and the tool pushes it (`NOTION_TOKEN` only, no Anthropic API key needed)
- `gh` CLI — installed and authenticated, manages the GitHub Projects board
- GitHub Projects board — synced with milestone progress (github.com/akshita412/todo_cli_app → Projects → Todo CLI)

---

## What's left

### M4 — Wire up the CLI (next, planned)
Connect the CLI commands to the service layer.
Right now `todo add` just prints a placeholder. After M4 it will actually save a task.

**Contract (from PRD):** data → stdout, errors → stderr (never a stack trace),
exit codes `0` success / `1` input error / `2` not found. `todo list` renders a
Rich table with overdue highlighting and a summary footer.

**Plan decided 2026-06-04:**
- Add a small service/backend factory driven by `TODO_BACKEND` + `TODO_DATA_PATH`
- Parse `--due` in the CLI; map domain exceptions to exit codes + stderr messages
- Add `TaskService.get_task(id)` for `show` / filtered `list`
- **`complete` is one-way** (marks done; no un-complete/toggle in the MVP)

**Wave plan (one per ~30-min session):**
1. Factory + `add` + `list` (functional, plain text)
2. `show`, `complete`, `delete` + not-found exit codes
3. Rich table polish (formatting, overdue highlight, summary footer)

### M5 — Polish
- SQLite backend (optional, for users who prefer it)
- Test coverage ≥ 80%
- Clean error messages (no stack traces ever shown to users)

### M6 — Share it (install from GitHub)
- No PyPI release. Distribute straight from the GitHub repo.
- Anyone interested installs with one command:
  ```bash
  uv tool install git+https://github.com/akshita412/todo_cli_app
  # or: pipx install git+https://github.com/akshita412/todo_cli_app
  ```
- README with install + usage instructions for these users.
- Keep `pyproject.toml` tidy so a PyPI publish stays a one-step option later if it's ever wanted.

---

## File map (what matters day-to-day)

| File | Purpose |
|------|---------|
| `src/todo_cli/models.py` | Task data structure |
| `src/todo_cli/exceptions.py` | Error types |
| `src/todo_cli/cli.py` | CLI entry point |
| `src/todo_cli/service.py` | Business logic (validation, status rules) |
| `src/todo_cli/storage/json_store.py` | JSON storage backend |
| `tests/test_cli.py` | CLI tests |
| `tests/test_storage.py` | Storage tests |
| `tests/test_service.py` | Service layer tests |
| `pyproject.toml` | Dependencies and build config |

---

## How to run it

```bash
uv sync --dev          # install dependencies
uv run pytest          # run all tests
uv run todo --help     # try the CLI
```

---

*Last updated: 2026-06-13 — M3 cleanup merged (PR #2); PyPI dropped from scope (M6 is now "install from GitHub"); M4 (wire up the CLI) is next.*
