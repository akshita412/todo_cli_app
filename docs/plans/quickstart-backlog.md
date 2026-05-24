# Backlog

## Sprint 1

- [ ] #1: `todo add "<description>" [--due YYYY-MM-DD] [--duration <minutes>]` — creates a new task
- [ ] #2: `todo list [--status pending|completed|all]` — renders Rich table with overdue flagging
- [ ] #3: `todo complete <id>` — toggles task status pending↔completed
- [ ] #4: `todo delete <id> [--force]` — permanently removes a task
- [ ] #5: `todo show <id>` — displays all fields for a single task
- [ ] #6: `todo update <id>` — edits title, due date, or duration
- [ ] #7: `todo status <id> <status>` — explicitly sets task status

## Tech Stack

- Python 3.10+, Click 8.x, Rich
- Storage: JSON default (`~/.todo/tasks.json`), SQLite opt-in via `TODO_BACKEND=sqlite`

## Architecture (non-negotiable 3-layer)

| Layer | File | Responsibility |
|-------|------|---------------|
| CLI | `cli.py` | Click commands, output rendering only |
| Service | `service.py` | Pure business logic, zero I/O |
| Storage | `storage/` | Abstract interface with JSON and SQLite backends |

## Task Model Fields

`id`, `description`, `due_date`, `status`, `duration`, `created_at`, `completed_at`

## Later

- [ ] Filter/search tasks by due date range
- [ ] Export tasks to CSV
- [ ] Recurring tasks
