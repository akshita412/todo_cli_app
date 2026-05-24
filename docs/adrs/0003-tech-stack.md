<!-- agent-notes: { ctx: "ADR: CLI tech stack selection", deps: [CLAUDE.md], state: active, last: "archie@2026-05-24" } -->

# ADR 0003 — CLI Tech Stack

**Date:** 2026-05-24
**Status:** Accepted

## Context

todo-cli is a terminal-native task scheduling app. We need a language, CLI framework, database layer, test framework, and build tooling that supports rapid local development by a solo/small team.

## Decision

| Concern | Choice |
|---------|--------|
| Language | Python 3.12+ |
| CLI framework | Click |
| Local storage | SQLite (via stdlib `sqlite3`) |
| Test framework | pytest |
| Build / package tooling | uv |

## Rationale

- **Python + Click** — mature, well-documented, minimal boilerplate for subcommand CLIs; large ecosystem for date/time handling needed for scheduling features.
- **SQLite** — zero-config, file-based, ships with Python stdlib; right-sized for a single-user local tool with no network requirement.
- **pytest** — de facto standard; rich plugin ecosystem (e.g. `pytest-cov`); integrates cleanly with Click's test runner.
- **uv** — significantly faster than pip/poetry for installs and venv creation; lockfile support (`uv.lock`) gives reproducible environments without heavy overhead.

## Trade-offs Acknowledged

- Click requires more manual wiring than Typer; accepted because the team has existing Click familiarity and Typer's auto-magic can obscure behaviour.
- SQLite is not suitable if multi-user or remote access is ever needed; a future ADR would address a migration to a client-server DB at that point.
- uv is newer than poetry; tooling support in some editors/CIs may lag, but GitHub Actions support is stable.
