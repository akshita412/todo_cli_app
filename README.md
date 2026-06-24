# todo-cli

A terminal-native task manager for developers. Add, list, complete, and edit tasks without leaving the shell.

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

## Cheat sheet

```bash
todo add "Write the Q3 report"               # add a task
todo add "Email client" --due 2026-06-30     # add a task with a due date
todo list                                    # see everything in a table
todo list --status pending                   # only unfinished tasks
todo list --status completed                 # only finished tasks
todo show 2                                   # full detail for task 2
todo complete 2                              # mark task 2 done
todo edit 2 "Email client about invoice"     # change task 2's description
todo delete 2                                # delete task 2 (asks to confirm)
todo delete 2 --force                        # delete without the prompt
```

### Commands at a glance

| Command | What it does |
|---------|--------------|
| `todo add "<text>" [--due YYYY-MM-DD]` | Create a task; prints its id. |
| `todo list [--status pending\|completed\|all]` | Show tasks as a table (default: all). |
| `todo show <id>` | Show every field for one task. |
| `todo complete <id>` | Mark a task done (stamps the completion time). |
| `todo edit <id> "<text>"` | Rewrite a task's description. |
| `todo delete <id> [--force]` | Delete a task; `--force` skips the confirmation. |

Run `todo <command> --help` for the details of any command.

## Tips for getting the most out of it

**Due dates and overdue flagging.** Dates are `YYYY-MM-DD` (e.g. `--due 2026-07-01`). Any task
that's past its due date and still pending is highlighted in `todo list` so it's hard to miss —
this is the main reason to bother adding due dates.

**Your data is just a file.** Everything lives in `~/.todo/tasks.json`. That means you can:
- back it up or sync it (Dropbox, a private git repo, `rsync`) like any other file;
- read it directly (`cat ~/.todo/tasks.json`) or grep it in a pinch;
- start fresh by deleting it — a new empty list is created on the next command.

**Separate lists per project or context.** Point `TODO_DATA_PATH` at a different directory to
keep independent task lists. Handy shell aliases (add to `~/.bashrc`):

```bash
alias work='TODO_DATA_PATH=~/.todo/work todo'
alias home='TODO_DATA_PATH=~/.todo/home todo'
# then:  work add "Ship release"   ·   home list
```

Until a built-in project field exists, a lightweight alternative is to tag the description and
let your eyes (or `grep`) do the filtering:

```bash
todo add "[website] fix the nav bar"
todo list | grep website
```

**Quick daily review.** `todo list --status pending` first thing in the morning shows what's
open, with anything overdue lit up. `todo list --status completed` is a satisfying end-of-day
recap.

**It plays nice with scripts.** Data goes to stdout, errors go to stderr, and the exit code is
non-zero on failure (e.g. an unknown task id) — so `todo` composes with pipes and `&&` chains
in your own shell scripts.

**Staying up to date.** When new versions ship, re-run the install command with `--force` to
upgrade in place — your tasks are untouched:

```bash
uv tool install git+https://github.com/akshita412/todo_cli_app --force
```

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
