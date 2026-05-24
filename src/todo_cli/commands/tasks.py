# agent-notes: { ctx: "tasks subcommand group (add/list/done/delete)", deps: [db.py], state: stub, last: "sato@2026-05-24" }
import click


@click.group()
def tasks() -> None:
    """Manage tasks."""


@tasks.command()
@click.argument("title")
def add(title: str) -> None:
    """Add a new task."""
    click.echo(f"Added: {title}")


@tasks.command("list")
def list_tasks() -> None:
    """List all tasks."""
    click.echo("No tasks yet.")


@tasks.command()
@click.argument("task_id", type=int)
def done(task_id: int) -> None:
    """Mark a task as complete."""
    click.echo(f"Marked task {task_id} as done.")


@tasks.command()
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task."""
    click.echo(f"Deleted task {task_id}.")
