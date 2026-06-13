# Session Handoff

**Date:** 2026-06-13
**Branch:** docs/m4-done-m5-plan (off main)
**Last merged work:** PR #9 — feat(m4): Rich table for list (Wave 3, MERGED) — **M4 complete**

---

## What was completed this session

### M4 — CLI wired to the service (ALL THREE WAVES DONE + MERGED)
- **Wave 1** (PR #6) — `factory.build_service()` (env-driven); `add` + `list` wired; `handle_errors` → stderr + exit 1
- **Wave 2** (PR #8) — `show` / `complete` / `delete` wired; `TaskService.get_task()`; `TaskNotFoundError` → exit 2
- **Wave 3** (PR #9) — `list` is now a Rich table (ID · Description · Due Date · Status), `✓ DONE` / `! OVERDUE` / `PENDING` labels, red overdue rows, summary footer. Fixed a markup bug (descriptions wrapped in `rich.text.Text` so brackets render literally).
- **50 tests passing.** App verified end-to-end via live demo.

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
| CLI: all 5 commands (`add`/`list`/`show`/`complete`/`delete`) | ✅ Done + merged |

The app is **fully functional end-to-end**. Default storage is `~/.todo/tasks.json` (override with `TODO_DATA_PATH`). Run with `uv run todo …`.

---

## Next: M5 — Polish (LEAN path; SQLite deferred)

**Status:** Scoped 2026-06-13. SQLite backend explicitly deferred (optional/opt-in;
JSON is plenty for sharing with a few people; clean add-on later). Two small waves.

### Wave A — Coverage gate (≥80%)
- `pytest-cov` is already a dev dependency. Add `--cov=todo_cli --cov-report=term-missing
  --cov-fail-under=80` to the pytest config in `pyproject.toml`.
- Wire it into the CI workflow so coverage <80% fails the build.
- **Acceptance:** `uv run pytest` reports coverage; CI red if <80%. (Likely already
  well above with 50 tests — this ratchets it in.)

### Wave B — Error-message audit / storage hardening
- **Known gap found while scoping:** `exceptions.py` defines `StorageCorruptError` and
  `StorageAccessError`, but `json_store.py` never raises them. A hand-corrupted
  `~/.todo/tasks.json` → `json.JSONDecodeError` → **uncaught traceback** (violates the
  PRD "never a stack trace" rule).
- Work: `JsonStorageBackend` raises `StorageCorruptError` on unparseable JSON and
  `StorageAccessError` on read/write failure; both already flow through `handle_errors`
  → exit 1. Audit every command's failure paths for friendly messages.
- **Acceptance:** corrupt/unreadable data file → friendly stderr + exit 1, no traceback;
  tests cover it.
- *(Minor cosmetic nits like footer pluralization can fold in here or be skipped.)*

**Net lean M5 ≈ 1.5 sessions.** Then M6 (README + verify GitHub install) is the finish.

### M4 contract delivered (for reference)
- Exit codes `0`/`1`/`2`; data→stdout, errors→stderr, never a stack trace.
- `todo list`: Rich table (ID · Description · Due Date · Status) + `✓ DONE` /
  `! OVERDUE` / `PENDING` + footer `N tasks · X completed · Y pending · Z overdue`.

### Housekeeping before starting M5
- Move the M5 board item to **In Progress** before coding.

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
| M4 — CLI commands wired up | ✅ Done + merged (Waves 1–3) |
| M5 — Polish (coverage gate + error audit; SQLite deferred) | 🔄 Next |
| M6 — Share it (install from GitHub) | — |
