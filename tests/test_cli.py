# agent-notes: { ctx: "CLI tests — all five commands wired to service", deps: [cli.py, factory.py], state: active, last: "tara@2026-06-23" }
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


def test_version_flag_reports_package_version(runner):
    # `todo --version` should print the installed package version and exit 0,
    # sourced from package metadata (pyproject) so it stays in sync with releases.
    from importlib.metadata import version

    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert version("todo-cli") in result.output


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


# ── list: Rich table + summary footer (Wave 3) ───────────────────────────────


def _add_overdue_task(tmp_path, description="Overdue task", days=1):
    """Insert a past-due pending task straight to storage (add rejects past dates)."""
    from datetime import date, timedelta

    from todo_cli.models import Task
    from todo_cli.storage.json_store import JsonStorageBackend

    backend = JsonStorageBackend(tmp_path)
    backend.add(Task(description=description, due_date=date.today() - timedelta(days=days)))


def test_list_shows_status_labels(runner):
    runner.invoke(cli, ["add", "Pending one"])
    runner.invoke(cli, ["add", "Done one"])
    runner.invoke(cli, ["complete", "2"])

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "PENDING" in result.output
    assert "DONE" in result.output


def test_list_marks_overdue(runner, tmp_path):
    _add_overdue_task(tmp_path)

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "OVERDUE" in result.output


def test_list_summary_footer(runner):
    runner.invoke(cli, ["add", "A"])
    runner.invoke(cli, ["add", "B"])
    runner.invoke(cli, ["add", "C"])
    runner.invoke(cli, ["complete", "1"])

    out = runner.invoke(cli, ["list"]).output
    assert "3 tasks" in out
    assert "1 completed" in out
    assert "2 pending" in out
    assert "0 overdue" in out


def test_list_footer_counts_overdue(runner, tmp_path):
    _add_overdue_task(tmp_path)

    out = runner.invoke(cli, ["list"]).output
    assert "1 overdue" in out
    assert "1 pending" in out  # an overdue task is still pending


def test_list_shows_table_headers(runner):
    runner.invoke(cli, ["add", "Buy milk"])

    out = runner.invoke(cli, ["list"]).output
    for header in ("ID", "Description", "Due Date", "Status"):
        assert header in out


def test_list_preserves_brackets_in_description(runner):
    # Rich treats [..] as markup; user descriptions must render literally.
    runner.invoke(cli, ["add", "[urgent] pay rent"])

    out = runner.invoke(cli, ["list"]).output
    assert "[urgent] pay rent" in out


# ── storage corruption: friendly failure (M5 Wave 2) ──────────────────────────

def test_list_on_corrupt_file_is_friendly(runner, tmp_path):
    # The data file is garbage; `list` must fail cleanly, not crash with a stack
    # trace. A friendly one-liner goes to stderr.
    (tmp_path / "tasks.json").write_text("{ not valid json")

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 1
    assert result.stderr.strip()  # friendly message present
    assert "Traceback" not in result.stderr  # no stack trace leaks to the user


def test_add_on_corrupt_file_is_friendly(runner, tmp_path):
    # Same guarantee on the write path: `add` reads first, hits the corrupt file,
    # and must report a friendly error rather than raising.
    (tmp_path / "tasks.json").write_text("{ not valid json")

    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 1
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr


# ── show ──────────────────────────────────────────────────────────────────────

def test_show_existing_task(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    result = runner.invoke(cli, ["show", "1"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "pending" in result.output.lower()


def test_show_unknown_task_exits_2(runner):
    result = runner.invoke(cli, ["show", "999"])
    assert result.exit_code == 2
    assert result.stderr.strip()


# ── complete ──────────────────────────────────────────────────────────────────

def test_complete_existing_task(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    result = runner.invoke(cli, ["complete", "1"])
    assert result.exit_code == 0

    # actually marked completed
    completed = runner.invoke(cli, ["list", "--status", "completed"])
    assert "Buy milk" in completed.output


def test_complete_unknown_task_exits_2(runner):
    result = runner.invoke(cli, ["complete", "999"])
    assert result.exit_code == 2
    assert result.stderr.strip()


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_with_force(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    result = runner.invoke(cli, ["delete", "1", "--force"])
    assert result.exit_code == 0

    listing = runner.invoke(cli, ["list"])
    assert "Buy milk" not in listing.output


def test_delete_unknown_task_exits_2(runner):
    result = runner.invoke(cli, ["delete", "999", "--force"])
    assert result.exit_code == 2
    assert result.stderr.strip()


def test_delete_confirm_yes(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    result = runner.invoke(cli, ["delete", "1"], input="y\n")
    assert result.exit_code == 0

    listing = runner.invoke(cli, ["list"])
    assert "Buy milk" not in listing.output


def test_delete_confirm_no_aborts(runner):
    runner.invoke(cli, ["add", "Buy milk"])
    result = runner.invoke(cli, ["delete", "1"], input="n\n")
    assert result.exit_code == 1

    # task survives
    listing = runner.invoke(cli, ["list"])
    assert "Buy milk" in listing.output


# ── edit ──────────────────────────────────────────────────────────────────────

def test_edit_updates_description(runner):
    runner.invoke(cli, ["add", "Old text"])
    result = runner.invoke(cli, ["edit", "1", "New text"])
    assert result.exit_code == 0

    listing = runner.invoke(cli, ["list"])
    assert "New text" in listing.output
    assert "Old text" not in listing.output


def test_edit_unknown_task_exits_2(runner):
    result = runner.invoke(cli, ["edit", "999", "Whatever"])
    assert result.exit_code == 2
    assert result.stderr.strip()


def test_edit_empty_description_exits_1(runner):
    runner.invoke(cli, ["add", "Old text"])
    result = runner.invoke(cli, ["edit", "1", ""])
    assert result.exit_code == 1
    assert result.stderr.strip()

    listing = runner.invoke(cli, ["list"])
    assert "Old text" in listing.output  # unchanged
