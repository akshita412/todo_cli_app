# todo-cli

A terminal-native task manager for developers. Add, list, complete, and delete tasks without leaving the shell.

## Install

```bash
pip install todo-cli   # coming at M6 — PyPI release
```

For local development:

```bash
git clone <repo>
cd todo_cli_app
uv sync --dev
uv run todo --help
```

## Usage

```bash
todo add "Buy milk" --due 2026-06-01   # add a task
todo list                               # list all tasks
todo list --status pending             # filter by status
todo complete 1                        # toggle task 1 done/pending
todo show 1                            # show full detail for task 1
todo delete 1 --force                  # delete task 1
```

## Development

```bash
uv sync --dev      # install dependencies
uv run pytest      # run tests
uv build           # build a wheel
```

## Stack

Python 3.10+ · Click · Rich · SQLite / JSON · pytest · uv
