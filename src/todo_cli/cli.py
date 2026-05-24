# agent-notes: { ctx: "CLI entry point, all top-level commands", deps: [models.py, exceptions.py, service.py], state: stub, last: "sato@2026-05-24" }
import sys
import click


@click.group()
def cli() -> None:
    """todo — terminal-native task scheduler."""


@cli.command()
@click.argument("description")
@click.option("--due", metavar="YYYY-MM-DD", default=None, help="Due date.")
def add(description: str, due: str) -> None:
    """Add a new task."""
    click.echo(f"Added: {description}")


@cli.command("list")
@click.option(
    "--status",
    type=click.Choice(["pending", "completed", "all"]),
    default="all",
    help="Filter by status.",
)
def list_tasks(status: str) -> None:
    """List tasks in a formatted table."""
    click.echo("No tasks yet.")


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Toggle a task between pending and completed."""
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
