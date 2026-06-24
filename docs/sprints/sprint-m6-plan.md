<!-- agent-notes: { ctx: "M6 sprint plan: GitHub-install distribution + README", deps: [docs/project-status.md, docs/todo-cli-MVP-PRD.md, pyproject.toml, README.md], state: active, last: "sato@2026-06-24" } -->

# Sprint Plan — M6: Share via GitHub install + README

**Status:** In progress — Wave 1 ✅, Wave 2 ✅ (done 2026-06-24); Wave 3 pending
**Milestone goal:** Anyone can install `todo-cli` straight from the GitHub repo in one
command and get a working `todo`, guided by an accurate README. PyPI stays deferred but
one step away.

## Decisions locked

- **Distribution = GitHub install, not PyPI.** `uv tool install git+…` / `pipx install git+…`
  are the supported install paths. The PRD (which still says "PyPI release") is being
  **updated** to match — GitHub install becomes the corrected source of truth. PyPI is an
  explicit post-MVP option, kept one-step-ready via complete `pyproject.toml` metadata.
- **License = MIT**, copyright holder `akshita412`. (Repo's current `LICENSE` is a
  placeholder stub and must be replaced with the real MIT text.)

## Definition of Done (milestone)

- `uv tool install git+https://github.com/akshita412/todo_cli_app` yields a working `todo`
  on a clean environment.
- `pipx install git+https://github.com/akshita412/todo_cli_app` likewise.
- README documents install + usage accurately, with every example verified against the
  real CLI surface.
- PRD + `project-status.md` reflect the GitHub-install decision (no doc claims pip/PyPI as
  the M6 deliverable).
- `pyproject.toml` carries complete metadata so a future PyPI publish is one step.

## Current-state findings (2026-06-24)

- ✅ Entry point (`todo = todo_cli.cli:cli`), hatchling build, `requires-python>=3.10` in place.
- ⚠️ `LICENSE` is a placeholder stub — needs real MIT text.
- ⚠️ `pyproject.toml` lacks `license`, `authors`, `readme`, `classifiers`, `keywords`, `[project.urls]`.
- ⚠️ README advertises `pip install todo-cli`, lists "SQLite" in the stack (deferred), and
  describes `complete` as "toggle done/pending" (actual: "Mark a task complete").
- Real CLI surface: `add / list / show / complete / delete --force / edit`.

## Waves

### Wave 1 — Packaging metadata + license  ← in progress
- Replace placeholder `LICENSE` with MIT text (holder: `akshita412`).
- Add to `pyproject.toml [project]`: `license`, `authors`, `readme = "README.md"`,
  `classifiers`, `keywords`, and `[project.urls]` (Homepage / Repository / Issues).
- **AC:** `uv build` produces a wheel with complete metadata; `uv tool install .` from a
  clean checkout yields a working `todo`.

### Wave 2 — Verify + document (both depend on Wave 1)  ← done

Verified install via `uv tool install git+file://…@feat/m6-packaging-metadata` and a
pip-in-venv proxy for the pipx path (pipx not installed locally) — both produce a working
`todo` end-to-end. The public `git+https://…` command becomes complete once this branch
merges to `main` (the metadata isn't on `main` yet). README rewritten; every usage example
run-verified against the real CLI.

- **Verify clean GitHub install:** install via `uv tool install git+…` and `pipx install git+…`
  into a throwaway env; fix any packaging gaps surfaced.
  **AC:** both paths produce a working `todo` end-to-end.
- **Rewrite README:** GitHub-install commands; every usage example verified against the real
  CLI; correct the `complete` wording; drop "SQLite" from the stack line.
  **AC:** copy-paste install works; examples match real output.

### Wave 3 — Reconcile docs
- Update PRD M6 ("PyPI release" → "Share via GitHub install + README") and its acceptance
  criterion (`pip install todo-cli` → `uv tool install git+…`); note PyPI as post-MVP.
- Update `project-status.md` as M6 lands.
- **AC:** no doc names pip/PyPI as the M6 deliverable.

## Sequencing & risk

- **Order:** Wave 1 → Wave 2 (both items) → Wave 3. Roughly one focused session.
- **Risk:** the old PRD acceptance named macOS + Ubuntu clean-env installs. Those can't be
  fully reproduced in this WSL2/Linux environment — verification here covers Linux directly;
  an optional CI install-smoke job could cover the other platforms automatically.
