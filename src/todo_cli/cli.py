# agent-notes: { ctx: "CLI entry point, top-level group + subcommands", deps: [commands/], state: active, last: "sato@2026-05-24" }
import click

from todo_cli.commands import tasks


@click.group()
def cli() -> None:
    """todo — terminal-native task scheduler."""


cli.add_command(tasks.tasks)
