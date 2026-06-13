# Session Handoff

**Date:** 2026-06-13
**Branch:** docs/wave1-handoff (off main)
**Last merged work:** PR #6 — feat(m4): wire add + list (Wave 1, MERGED into main)

---

## What was completed this session

### M4 Wave 1 — `add` + `list` wired (DONE + MERGED, PR #6)
- `src/todo_cli/factory.py` — `build_service()` reads `TODO_BACKEND` (json default) + `TODO_DATA_PATH`; unknown backend → `ValueError`
- `src/todo_cli/cli.py` — `add` (parse `--due`, persist, print new id) and `list` (`--status` filter, plain-text) wired to `TaskService`; `handle_errors` maps domain errors → stderr + exit 1
- `complete` docstring fixed "toggle" → "mark complete" (body still a stub)
- `tests/test_factory.py` (3) + rewritten `tests/test_cli.py` — **37 passing**
- 3-lens review: 0 Critical / 0 Important

### Repo housekeeping (all MERGED this session)
- M3 cleanup — timezone-aware UTC datetimes, warning-free suite (PR #2)
- **PyPI dropped** — M6 reframed as "install from GitHub" (PR #3)
- Removed template scaffolding: cloud research, enterprise stubs, 5 orphaned cloud commands (PRs #4, #5). Repo 111 → 96 files.

---

## Current state

| Layer | Status |
|-------|--------|
| Models + Exceptions | ✅ Done |
| Storage (JSON backend) | ✅ Done |
| Service layer | ✅ Done + merged |
| CLI: `add` + `list` | ✅ Done + merged (Wave 1) |
| CLI: `show` / `complete` / `delete` | ❌ Stubbed — Wave 2 |

`add` and `list` now persist/read real tasks. `show`, `complete`, `delete` still print placeholders and are NOT connected to `TaskService`.

---

## Next session — M4 Wave 2: `show`, `complete`, `delete`

**Status:** Wave 1 done + merged. Wave 2 is next.

### Goal
Wire the 3 remaining stubbed commands (`show`, `complete`, `delete`) to `TaskService`,
with `TaskNotFoundError` → **exit 2**. Extend the existing `handle_errors` wrapper in
`cli.py` to map not-found → 2 (it already maps other `TodoError` → 1).

### Wave 2 specifics
- **Add `TaskService.get_task(id)`** (raises `TaskNotFoundError`) — small M3-service extension `show` needs.
- `show <id>` → print all fields; unknown id → exit 2.
- `complete <id>` → `complete_task` (one-way); unknown id → exit 2. Replace stub "Toggled" message.
- `delete <id>` → `delete_task`; `--force` skips the confirm prompt; unknown id → exit 2.
- Tests first (TDD): not-found exit-2 paths, `--force` vs confirm, show output.

### Original M4 goal (for reference)
Wire the 5 stubbed Click commands in `src/todo_cli/cli.py` to `TaskService` so they
actually persist and read tasks. (Wave 1 did `add` + `list`.)

### Contract (from PRD §7–8)
- **Exit codes:** `0` success · `1` input error · `2` resource not found
- **Streams:** data → stdout, errors → stderr, **never** a stack trace
- **`todo list`:** Rich table — ID · Description · Due Date · Status — with
  `! OVERDUE` / `✓ DONE` / `PENDING`, plus summary footer
  (`N tasks · X completed · Y pending · Z overdue`)
- **Tests:** Click `CliRunner` with temp-file storage injected via `TODO_DATA_PATH`

### Design (decided this planning session)
1. **Service/backend factory** — a helper that reads `TODO_BACKEND` (json default;
   sqlite is M5) and `TODO_DATA_PATH`, returns a `TaskService`. Tests point
   `TODO_DATA_PATH` at a tmp dir. (Implements the already-locked env-var contract.)
2. **`--due` parsing** in the CLI: string → `date`; bad format → `InvalidDateError` → exit 1.
3. **Error → exit-code mapping:** `ValidationError`/`InvalidDateError` → 1,
   `TaskNotFoundError` → 2, storage errors → 1; all messages to stderr.
4. **Add `TaskService.get_task(id)`** (raises `TaskNotFoundError`) so `show` and
   `list --status` have a clean read path. Small extension to the M3 service.
5. **`complete` is ONE-WAY** — see locked decisions. The stub docstring still says
   "toggle"; fix it to "mark complete" during M4.

### Command mapping
| Command | Service call | Notes |
|---------|-------------|-------|
| `add` | `add_task` | parse `--due`; print new id |
| `list` | `list_tasks` | filter by `--status`; Rich table + footer + overdue highlight |
| `show` | `get_task` (new) | not-found → exit 2 |
| `complete` | `complete_task` | one-way; not-found → exit 2 |
| `delete` | `delete_task` | `--force` skips confirm; not-found → exit 2 |

### Wave plan (one wave per ~30-min session, TDD + approval each step)
- **Wave 1** ✅ — factory + `add` + `list` (functional output + `--status` filter, plain text). Done + merged (PR #6).
- **Wave 2** 🔄 — `show`, `complete`, `delete` + `TaskNotFoundError` → exit 2. **Next.**
- **Wave 3** — Rich table polish: formatting, overdue highlight, summary footer.

### Housekeeping before starting Wave 2
- Move the M4 board item's Wave 2 work to **In Progress** before coding.

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
| `complete` behavior | One-way (mark done). No un-complete/toggle in MVP. |
| CI | GitHub Actions, Python 3.10 + 3.12 |
| Distribution | Install from GitHub (`uv tool install git+…`). No PyPI. (Decided 2026-06-13.) |
| PRD source of truth | `docs/todo-cli-MVP-PRD.md` |

---

## Session preferences (user)

- 30 minutes per session (may grow over time)
- TDD: plain-English explanation of each test BEFORE showing code; user approves before green
- Start every session: read `CLAUDE.md`, `docs/code-map.md`, `.claude/handoff.md`
- End every session: update this handoff + commit
- Log sessions to Notion: just ask Claude — it authors the entry and runs `log-session` (Pro-only, no API key)
- Feature creep rule: park mid-session ideas in `docs/plans/quickstart-backlog.md` under "Later"

---

## Milestone tracker

| Milestone | Status |
|-----------|--------|
| M1 — Scaffolding | ✅ Done |
| M2 — JSON Storage Backend | ✅ Done |
| M3 — Service layer | ✅ Done + merged |
| M4 — CLI commands wired up | 🔄 In progress — Wave 1 done; Waves 2–3 left |
| M5 — Polish + coverage gate (≥80%) | — |
| M6 — Share it (install from GitHub) | — |
