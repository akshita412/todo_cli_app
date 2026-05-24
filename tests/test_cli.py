# agent-notes: { ctx: "CLI smoke tests — one per command, happy path only", deps: [cli.py], state: active, last: "sato@2026-05-24" }
from click.testing import CliRunner

from todo_cli.cli import cli


def test_help_exits_cleanly():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "todo" in result.output


def test_add_command():
    result = CliRunner().invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output


def test_add_with_due_date():
    result = CliRunner().invoke(cli, ["add", "Buy milk", "--due", "2026-06-01"])
    assert result.exit_code == 0


def test_list_command():
    result = CliRunner().invoke(cli, ["list"])
    assert result.exit_code == 0


def test_list_with_status_filter():
    result = CliRunner().invoke(cli, ["list", "--status", "pending"])
    assert result.exit_code == 0


def test_complete_command():
    result = CliRunner().invoke(cli, ["complete", "1"])
    assert result.exit_code == 0


def test_delete_command_with_force():
    result = CliRunner().invoke(cli, ["delete", "1", "--force"])
    assert result.exit_code == 0


def test_show_command():
    result = CliRunner().invoke(cli, ["show", "1"])
    assert result.exit_code == 0
