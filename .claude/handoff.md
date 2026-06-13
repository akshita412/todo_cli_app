# Session Handoff

**Date:** 2026-06-04
**Branch:** chore/post-m3-cleanup (off main @ fffb7e0)
**Last merged work:** PR #1 — feat(m3): service layer (MERGED into main)

---

## What was completed this session

### M3 — Service layer (DONE + MERGED)
- `src/todo_cli/service.py` — `TaskService` with `add_task`, `complete_task`, `delete_task`, `list_tasks`
- Validation: empty desc → `ValidationError`, past due → `InvalidDateError`, unknown id → `TaskNotFoundError`
- `tests/test_service.py` — 13 TDD tests, all green
- **PR #1 merged into `main`** (`fffb7e0`). Local `main` fast-forwarded; feature branch deleted.

### Post-M3 cleanup (this branch — not yet committed)
- Killed the `datetime.utcnow()` deprecation: now timezone-aware `datetime.now(timezone.utc)` in `models.py`, `service.py`, and `tests/test_service.py`
- Full suite: **29 passing, 0 warnings** (was 29 passing / 24 deprecation warnings)
- Notion journal: removed duplicate M3 entry (one canonical entry remains)
- `log-session` tool refactored to push-only (no Anthropic API; runs on Pro via `NOTION_TOKEN`)

---

## Current state

| Layer | Status |
|-------|--------|
| Models + Exceptions | ✅ Done |
| Storage (JSON backend) | ✅ Done |
| Service layer | ✅ Done + merged |
| **CLI ↔ service wiring** | ❌ Stubbed — this is M4 |

CLI commands (`add`, `list`, `complete`, `delete`, `show`) still print placeholders and are NOT connected to `TaskService`.

---

## Next session — M4, Wire CLI to the service layer

**Status:** Planned and scoped (2026-06-04). Not started — picking up next session.

### Goal
Wire the 5 stubbed Click commands in `src/todo_cli/cli.py` to `TaskService` so they
actually persist and read tasks. Right now they print placeholders.

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
- **Wave 1** — factory + `add` + `list` (functional output + `--status` filter, plain text). Full add→list loop end-to-end.
- **Wave 2** — `show`, `complete`, `delete` + `TaskNotFoundError` → exit 2.
- **Wave 3** — Rich table polish: formatting, overdue highlight, summary footer.

### Housekeeping before starting M4
- This branch `chore/post-m3-cleanup` has the committed post-M3 cleanup (`e75f4f9`),
  not yet pushed/PR'd. Decide: PR it on its own, or branch M4 off it and bundle.
- Move the M4 board item to **In Progress** before coding.

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
| M4 — CLI commands wired up | 🔄 Next |
| M5 — Polish + coverage gate (≥80%) | — |
| M6 — Share it (install from GitHub) | — |
