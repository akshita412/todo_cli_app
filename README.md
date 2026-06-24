# todo-cli

A terminal-native task manager for developers. Add, list, complete, and delete tasks without leaving the shell.

Tasks are stored locally in `~/.todo/tasks.json` — no accounts, no cloud, no browser.

## Install

Install straight from GitHub with [uv](https://docs.astral.sh/uv/) or [pipx](https://pipx.pypa.io/).
Either command puts a `todo` executable on your `PATH`. Requires Python 3.10+.

```bash
uv tool install git+https://github.com/akshita412/todo_cli_app
# or
pipx install git+https://github.com/akshita412/todo_cli_app
```

Verify it worked:

```bash
todo --help
```

## Usage

```bash
todo add "Buy milk"                       # add a task
todo add "Ship release" --due 2026-07-01  # add a task with a due date
todo list                                 # list all tasks in a table
todo list --status pending                # filter by pending | completed | all
todo show 1                               # show every field for task 1
todo complete 1                           # mark task 1 complete
todo edit 1 "Buy oat milk"                # change task 1's description
todo delete 1                             # delete task 1 (asks to confirm)
todo delete 1 --force                     # delete without the confirmation prompt
```

Overdue tasks (past their due date and still pending) are highlighted in the `list` table.

## Development

```bash
git clone https://github.com/akshita412/todo_cli_app
cd todo_cli_app
uv sync --dev       # install dependencies into .venv
uv run todo --help  # run the CLI from source
uv run pytest       # run the test suite (coverage gate ≥95%)
uv build            # build a wheel + sdist
```

## Stack

Python 3.10+ · [Click](https://click.palletsprojects.com/) · [Rich](https://rich.readthedocs.io/) · JSON storage · pytest · uv

## License

[MIT](LICENSE)
