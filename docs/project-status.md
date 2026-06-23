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

### M4 — CLI fully wired ✅ (merged, PRs #6 / #8 / #9)
- **Wave 1** — `factory.build_service()` (env-driven); `todo add` saves + prints id; `todo list` reads back; `--due` parsing, `--status` filter, friendly errors (stderr + exit 1)
- **Wave 2** — `show` / `complete` / `delete` wired; `TaskService.get_task()`; unknown id → exit 2
- **Wave 3** — `todo list` is now a Rich table (ID · Description · Due Date · Status) with `✓ DONE` / `! OVERDUE` / `PENDING` labels, red overdue rows, and a summary footer
- The app is fully functional end-to-end (`uv run todo …`)

**Test count: 50 tests, all passing (0 warnings).**

### M5 — Polish ✅ (merged, PRs #13 / #17)
SQLite stayed **deferred** (JSON is plenty for sharing with a few people). Two waves:
- **Wave 1 — Coverage gate (#12)** — `--cov-fail-under=80` centralized in `pyproject.toml` so local `uv run pytest` and CI enforce one threshold. CI step simplified to plain `uv run pytest`.
- **Wave 2 — Storage hardening (#14)** — a corrupt/unreadable `tasks.json` no longer crashes with a traceback. `JsonStorageBackend` raises `StorageCorruptError` (unparseable JSON, wrong top-level shape, malformed task record) and `StorageAccessError` (read/write `OSError`), which the CLI renders as a friendly message + exit 1. Built TDD (Tara red → Sato green) and passed a three-lens review (Vik + Tara + Pierrot) that caught record-level corruption escaping `_deserialize`.

**Test count: 70 tests, all passing. Coverage 93% (gate ≥80%).**

**Deferred follow-ups (tracked):** atomic writes #15 · remove dead `commands/tasks.py` stub #16.

## Tooling set up
- `log-session` — logs each session summary to Notion. Now push-only: Claude Code writes the entry on the Pro subscription and the tool pushes it (`NOTION_TOKEN` only, no Anthropic API key needed)
- `gh` CLI — installed and authenticated, manages the GitHub Projects board
- GitHub Projects board — synced with milestone progress (github.com/akshita412/todo_cli_app → Projects → Todo CLI)

---

## What's left

### M6 — Share it (install from GitHub) ← next
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

*Last updated: 2026-06-23 — M5 complete (PRs #13/#17): coverage gate + storage hardening. 70 tests, 93% coverage. SQLite still deferred. M6 (install from GitHub) is next; follow-ups #15 (atomic writes) and #16 (dead-code cleanup) tracked.*
