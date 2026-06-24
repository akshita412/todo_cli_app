# agent-notes: { ctx: "CLI entry point; 6 commands wired to service + --version", deps: [factory.py, service.py, exceptions.py, models.py], state: active, last: "sato@2026-06-24" }
import functools
import sys
from datetime import date

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from todo_cli.exceptions import InvalidDateError, TaskNotFoundError, TodoError
from todo_cli.factory import build_service
from todo_cli.models import Status, Task


def handle_errors(func):
    """Map domain errors to friendly stderr messages + exit codes.

    TaskNotFoundError -> exit 2; any other TodoError -> exit 1.
    Messages go to stderr; no stack trace reaches the user.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskNotFoundError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(2)
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


def _status_label(task: Task) -> str:
    """Human-facing status text for the list table."""
    if task.status == Status.COMPLETED:
        return "✓ DONE"
    if task.is_overdue:
        return "! OVERDUE"
    return "PENDING"


def _render_table(tasks: list[Task]) -> None:
    """Print a Rich table of tasks, then a one-line summary footer."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", justify="right")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Status")

    completed = pending = overdue = 0
    for task in tasks:
        if task.status == Status.COMPLETED:
            completed += 1
        else:
            pending += 1
        if task.is_overdue:
            overdue += 1
        row_style = "red" if task.is_overdue else None
        table.add_row(
            str(task.id),
            Text(task.description),  # Text() so brackets aren't parsed as Rich markup
            task.due_date.isoformat() if task.due_date else "—",
            _status_label(task),
            style=row_style,
        )

    Console().print(table)
    click.echo(
        f"{len(tasks)} tasks · {completed} completed · "
        f"{pending} pending · {overdue} overdue"
    )


@click.group()
@click.version_option(package_name="todo-cli", prog_name="todo")
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

    _render_table(tasks)


@cli.command()
@click.argument("task_id", type=int)
@handle_errors
def complete(task_id: int) -> None:
    """Mark a task complete."""
    task = build_service().complete_task(task_id)
    click.echo(f"Completed task {task.id}: {task.description}")


@cli.command()
@click.argument("task_id", type=int)
@click.option("--force", is_flag=True, help="Skip confirmation prompt.")
@handle_errors
def delete(task_id: int, force: bool) -> None:
    """Permanently delete a task."""
    if not force:
        click.confirm(f"Delete task {task_id}?", abort=True)
    build_service().delete_task(task_id)
    click.echo(f"Deleted task {task_id}.")


@cli.command()
@click.argument("task_id", type=int)
@click.argument("description")
@handle_errors
def edit(task_id: int, description: str) -> None:
    """Update a task's description."""
    task = build_service().update_description(task_id, description)
    click.echo(f"Updated task {task.id}: {task.description}")


@cli.command()
@click.argument("task_id", type=int)
@handle_errors
def show(task_id: int) -> None:
    """Show all fields for a single task."""
    task = build_service().get_task(task_id)
    due = task.due_date.isoformat() if task.due_date else "—"
    completed = task.completed_at.isoformat() if task.completed_at else "—"
    click.echo(f"Task {task.id}:")
    click.echo(f"  Description: {task.description}")
    click.echo(f"  Status:      {task.status.value}")
    click.echo(f"  Due:         {due}")
    click.echo(f"  Created:     {task.created_at.isoformat()}")
    click.echo(f"  Completed:   {completed}")
