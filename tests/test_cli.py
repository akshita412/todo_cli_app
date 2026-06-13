# agent-notes: { ctx: "CLI tests — add/list wired to service; show/complete/delete stubbed", deps: [cli.py, factory.py], state: active, last: "sato@2026-06-13" }
import pytest
from click.testing import CliRunner

from todo_cli.cli import cli


@pytest.fixture
def runner(monkeypatch, tmp_path):
    """A CliRunner whose commands read/write an isolated tmp data dir."""
    monkeypatch.setenv("TODO_DATA_PATH", str(tmp_path))
    monkeypatch.delenv("TODO_BACKEND", raising=False)
    return CliRunner()


def test_help_exits_cleanly(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "todo" in result.output


# ── add ───────────────────────────────────────────────────────────────────────

def test_add_persists_and_reports_id(runner):
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "1" in result.output  # new task id

    # actually persisted — a follow-up list shows it
    listing = runner.invoke(cli, ["list"])
    assert "Buy milk" in listing.output


def test_add_with_future_due_date(runner):
    result = runner.invoke(cli, ["add", "Buy milk", "--due", "2027-01-01"])
    assert result.exit_code == 0

    listing = runner.invoke(cli, ["list"])
    assert "2027-01-01" in listing.output


def test_add_empty_description_errors(runner):
    result = runner.invoke(cli, ["add", ""])
    assert result.exit_code == 1
    assert result.stderr.strip()  # error message on stderr

    # nothing was saved
    listing = runner.invoke(cli, ["list"])
    assert "No tasks yet." in listing.output


def test_add_past_due_date_errors(runner):
    result = runner.invoke(cli, ["add", "x", "--due", "2020-01-01"])
    assert result.exit_code == 1
    assert result.stderr.strip()


def test_add_bad_date_format_errors(runner):
    result = runner.invoke(cli, ["add", "x", "--due", "not-a-date"])
    assert result.exit_code == 1
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr  # friendly message, no stack trace


# ── list ──────────────────────────────────────────────────────────────────────

def test_list_empty(runner):
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No tasks yet." in result.output


def test_list_shows_added_tasks(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    runner.invoke(cli, ["add", "Write tests"])

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "Write tests" in result.output


def test_list_status_filter(runner):
    from todo_cli.factory import build_service

    runner.invoke(cli, ["add", "Pending task"])
    runner.invoke(cli, ["add", "Done task"])
    build_service().complete_task(2)  # complete cmd is Wave 2; use service directly

    pending = runner.invoke(cli, ["list", "--status", "pending"])
    assert "Pending task" in pending.output
    assert "Done task" not in pending.output

    completed = runner.invoke(cli, ["list", "--status", "completed"])
    assert "Done task" in completed.output
    assert "Pending task" not in completed.output

    everything = runner.invoke(cli, ["list", "--status", "all"])
    assert "Pending task" in everything.output
    assert "Done task" in everything.output


def test_add_then_list_end_to_end(runner):
    runner.invoke(cli, ["add", "End to end task"])
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "End to end task" in result.output


# ── still stubbed until Wave 2 (smoke only) ───────────────────────────────────

def test_complete_command_stub(runner):
    result = runner.invoke(cli, ["complete", "1"])
    assert result.exit_code == 0


def test_delete_command_with_force(runner):
    result = runner.invoke(cli, ["delete", "1", "--force"])
    assert result.exit_code == 0


def test_show_command(runner):
    result = runner.invoke(cli, ["show", "1"])
    assert result.exit_code == 0
