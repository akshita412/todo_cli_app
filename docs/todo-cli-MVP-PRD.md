# Product Requirements Document
## CLI To-Do List Application — MVP

**Version:** 1.0 · Draft
**Date:** April 2026
**Language:** Python 3.10+

---

## 1. Executive Summary

This document defines the complete product and engineering requirements for `todo-cli`, a command-line task management tool built in Python. The MVP delivers a fast, persistent, zero-friction to-do manager for terminal-native users — developers, data professionals, and engineers who live in their shell and do not want to context-switch into a GUI application to manage daily work.

The product is scoped deliberately narrow: no accounts, no cloud sync, no notifications. Every design decision in this MVP prioritizes speed of adoption (install and be productive in under two minutes) and engineering correctness (clean architecture that makes post-MVP extensions non-breaking). The codebase produced from this PRD is the full implementation — not a prototype.

---

## 2. Problem Statement

Existing task management tools fail terminal-native users in one of two ways: they are too heavyweight (Notion, Linear, Jira require browser context-switching and account management) or too ephemeral (plain text files, ad hoc `echo` commands, and sticky notes carry no structure and do not surface overdue items). There is no widely-adopted, installable Python CLI tool that is structured, persistent, overdue-aware, and composable with shell pipelines.

`todo-cli` closes this gap with a single installable Python package that stores tasks locally, renders a clean table, and flags overdue items — all without leaving the terminal.

---

## 3. Goals and Non-Goals

### 3.1 MVP Goals

- Users can add, list, complete, and delete tasks from a single CLI entry point (`todo`).
- Tasks persist across sessions via a local storage backend (JSON default, SQLite opt-in).
- Due dates are validated, stored, and surfaced visually with overdue flagging.
- The tool installs in one command (`uv tool install git+https://github.com/akshita412/todo_cli_app`, or the equivalent `pipx` command) and requires zero configuration.
- Output is composable: errors go to stderr, data goes to stdout, exit codes are standard.
- The codebase is layered (CLI → Service → Storage) so any layer is replaceable post-MVP.

### 3.2 Explicit Non-Goals (MVP)

- No cloud sync or remote backend.
- No task priorities, tags, or labels.
- No recurring tasks or reminders/notifications.
- No search or keyword filter.
- No multi-user or shared task lists.
- No GUI, TUI, or web frontend.
- No import/export (CSV, JSON dump).

---

## 4. User Stories

_(See PRD source document for full user story table)_

---

## 5. Technical Architecture

The application follows a strict three-layer architecture. No layer may import from a higher layer. The CLI layer is the only layer permitted to perform I/O outside of storage operations.

### 5.1 Layer Overview

```
CLI (cli.py)          ← Click commands, output rendering, exit codes
     ↓
Service (service.py)  ← Pure business logic, validation, status transitions
     ↓
Storage (storage/)    ← Abstract interface + JSON and SQLite backends
```

### 5.2 Package Structure

```
todo-cli/
├── todo_cli/
│   ├── __init__.py
│   ├── cli.py           # Click entry point
│   ├── service.py       # Pure business logic — no I/O
│   ├── models.py        # Task dataclass
│   ├── exceptions.py    # Domain-specific exceptions
│   └── storage/
│       ├── __init__.py
│       ├── base.py      # Abstract StorageBackend interface
│       ├── json_store.py
│       └── sqlite_store.py
├── tests/
│   ├── test_cli.py
│   ├── test_service.py
│   └── test_storage.py
├── pyproject.toml
└── README.md
```

### 5.3 Technology Decisions

_(See PRD source document for full table)_

### 5.4 Storage Path Resolution

Priority order (highest to lowest):

1. `TODO_DATA_PATH` env var if set (enables pointing at any directory).
2. Default: `~/.todo/tasks.json` (JSON) or `~/.todo/tasks.db` (SQLite). Directory created on first run.

---

## 6. Data Schema

### 6.1 Task Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Auto-assigned, never reused |
| `description` | str | 1–255 characters |
| `due_date` | date \| None | ISO 8601, optional |
| `status` | enum | `pending` \| `completed` |
| `created_at` | datetime | Set on creation |
| `completed_at` | datetime \| None | Set when completed |

### 6.2 JSON Canonical Representation

```json
{
  "id": 4,
  "description": "Buy milk",
  "due_date": "2026-04-01",
  "status": "pending",
  "created_at": "2026-03-28T10:45:00Z",
  "completed_at": null
}
```

### 6.3 SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  description  TEXT    NOT NULL CHECK(length(description) BETWEEN 1 AND 255),
  due_date     TEXT    DEFAULT NULL,
  status       TEXT    NOT NULL DEFAULT 'pending'
                       CHECK(status IN ('pending', 'completed')),
  created_at   TEXT    NOT NULL,
  completed_at TEXT    DEFAULT NULL
);
```

### 6.4 Python Task Model

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class Status(str, Enum):
    PENDING   = "pending"
    COMPLETED = "completed"

@dataclass
class Task:
    description:  str
    id:           int               = field(default=0)
    due_date:     Optional[date]    = field(default=None)
    status:       Status            = field(default=Status.PENDING)
    created_at:   datetime          = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = field(default=None)

    @property
    def is_overdue(self) -> bool:
        return (
            self.due_date is not None
            and self.status == Status.PENDING
            and self.due_date < date.today()
        )
```

---

## 7. CLI Command Reference

All commands are accessed via the `todo` entry point. Errors go to stderr, data to stdout. Exit codes: `0` = success, `1` = input error, `2` = resource not found.

### 7.1 Output — `todo list`

```
┌────┬─────────────────────────┬────────────┬───────────┐
│ ID │ Description             │ Due Date   │ Status    │
├────┼─────────────────────────┼────────────┼───────────┤
│  1 │ Draft Q2 roadmap        │ 2026-03-25 │ ! OVERDUE │
│  2 │ Review PRs              │ 2026-03-28 │ PENDING   │
│  3 │ Update dependencies     │ 2026-04-05 │ PENDING   │
│  4 │ Buy milk                │ 2026-04-01 │ ✓ DONE    │
│  5 │ Write unit tests        │ —          │ PENDING   │
└────┴─────────────────────────┴────────────┴───────────┘
5 tasks  ·  1 completed  ·  3 pending  ·  1 overdue
```

---

## 8. Error Handling Contract

All error messages go to stderr. The CLI catches domain exceptions from the service layer and formats them as human-readable messages. Stack traces must never be visible to the user in normal operation.

---

## 9. Testing Strategy

Coverage must reach **≥ 80%** before MVP is shippable.

### 9.1 Unit Tests — Service Layer
Pure functions, no mocking required. Covers: valid creation, description boundaries, invalid dates, status transitions, overdue detection.

### 9.2 Integration Tests — CLI Layer
Use Click's `CliRunner`. Inject temp-file storage. Verify stdout, stderr, and exit codes for happy paths and all error scenarios.

### 9.3 Storage Tests
Same suite against both JSON and SQLite backends via `pytest.mark.parametrize`. Covers: write-read round trips, ID uniqueness after deletion.

### 9.4 Test Infrastructure
- **Framework:** pytest + pytest-cov
- **CI:** GitHub Actions — ubuntu-latest, Python 3.10 + 3.12
- **Coverage gate:** PRs below 80% are blocked

---

## 10. Delivery Milestones

| Milestone | Scope |
|-----------|-------|
| M1 | Scaffold — models, exceptions, storage interface, CI |
| M2 | Storage backends — JSON (default), SQLite (opt-in) |
| M3 | Service layer — business logic, validation |
| M4 | CLI commands wired up end-to-end |
| M5 | Polish + coverage gate (≥ 95%) |
| M6 | Distribution — GitHub install (`uv tool` / `pipx`) + README |

> **Distribution note:** M6 ships via direct GitHub install rather than a PyPI release.
> JSON-only local storage is plenty for sharing with a handful of users, and GitHub install
> avoids the overhead of a published package. `pyproject.toml` metadata is kept complete so a
> PyPI publish remains a one-step, post-MVP option if it's ever wanted.

---

## 11. Out of Scope — MVP

All items in section 3.2. Not to be implemented in the MVP branch even if they appear trivial.

---

## 12. Acceptance Criteria

- `uv tool install git+https://github.com/akshita412/todo_cli_app` (or the `pipx` equivalent) installs a working `todo` on a clean Python 3.10+ environment (macOS, Ubuntu 22.04, WSL2).
- A user can add five tasks, list them, complete two, delete one — in under two minutes — using only `--help`.
- `todo list` renders a correctly formatted table with overdue highlighting and summary footer.
- All commands return correct exit codes for success and error scenarios.
- `pytest --cov` reports ≥ 95% coverage across the full package.
- No stack traces visible to the user under normal operation.
- Tasks persist across terminal restarts on both JSON and SQLite backends.
- CI passes on Python 3.10 and 3.12.

---

_End of Document · todo-cli MVP PRD v1.0_
