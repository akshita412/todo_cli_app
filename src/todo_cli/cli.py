# agent-notes: { ctx: "CLI entry point; add/list wired to service, show/complete/delete stubbed", deps: [factory.py, service.py, exceptions.py, models.py], state: active, last: "sato@2026-06-13" }
import functools
import sys
from datetime import date

import click

from todo_cli.exceptions import InvalidDateError, TodoError
from todo_cli.factory import build_service
from todo_cli.models import Status, Task


def handle_errors(func):
    """Map domain errors to friendly stderr messages + exit codes.

    TodoError -> message on stderr, exit 1 (no stack trace).
    Wave 2 will extend this for TaskNotFoundError -> exit 2.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TodoError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)

    return wrapper


def _parse_due(due: str) -> date:
    """Parse a YYYY-MM-DD string, raising InvalidDateError on bad input."""
    try:
        return date.fromisoformat(due)
    except ValueError:
        raise InvalidDateError(
            f"Invalid date {due!r}. Expected format YYYY-MM-DD."
        )


def _format_task(task: Task) -> str:
    """One plain-text line for a task (Rich table comes in Wave 3)."""
    mark = "x" if task.status == Status.COMPLETED else " "
    line = f"{task.id}  [{mark}] {task.description}"
    if task.due_date is not None:
        line += f"  (due {task.due_date.isoformat()})"
    return line


@click.group()
def cli() -> None:
    """todo — terminal-native task scheduler."""


@cli.command()
@click.argument("description")
@click.option("--due", metavar="YYYY-MM-DD", default=None, help="Due date.")
@handle_errors
def add(description: str, due: str) -> None:
    """Add a new task."""
    due_date = _parse_due(due) if due else None
    task = build_service().add_task(description, due_date)
    click.echo(f"Added task {task.id}: {task.description}")


@cli.command("list")
@click.option(
    "--status",
    type=click.Choice(["pending", "completed", "all"]),
    default="all",
    help="Filter by status.",
)
@handle_errors
def list_tasks(status: str) -> None:
    """List tasks in a formatted table."""
    tasks = build_service().list_tasks()
    if status != "all":
        wanted = Status(status)
        tasks = [t for t in tasks if t.status == wanted]

    if not tasks:
        click.echo("No tasks yet.")
        return

    for task in tasks:
        click.echo(_format_task(task))


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task complete."""
    click.echo(f"Toggled task {task_id}.")


@cli.command()
@click.argument("task_id", type=int)
@click.option("--force", is_flag=True, help="Skip confirmation prompt.")
def delete(task_id: int, force: bool) -> None:
    """Permanently delete a task."""
    if not force:
        click.confirm(f"Delete task {task_id}?", abort=True)
    click.echo(f"Deleted task {task_id}.")


@cli.command()
@click.argument("task_id", type=int)
def show(task_id: int) -> None:
    """Show all fields for a single task."""
    click.echo(f"Task {task_id}: (not yet implemented)")
