# agent-notes: { ctx: "smoke tests for CLI entry point and task subcommands", deps: [cli.py, commands/tasks.py], state: active, last: "sato@2026-05-24" }
from click.testing import CliRunner

from todo_cli.cli import cli


def test_help_exits_cleanly():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "todo" in result.output


def test_tasks_help():
    result = CliRunner().invoke(cli, ["tasks", "--help"])
    assert result.exit_code == 0


def test_tasks_add():
    result = CliRunner().invoke(cli, ["tasks", "add", "Buy milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output


def test_tasks_list():
    result = CliRunner().invoke(cli, ["tasks", "list"])
    assert result.exit_code == 0


def test_tasks_done():
    result = CliRunner().invoke(cli, ["tasks", "done", "1"])
    assert result.exit_code == 0


def test_tasks_delete():
    result = CliRunner().invoke(cli, ["tasks", "delete", "1"])
    assert result.exit_code == 0
