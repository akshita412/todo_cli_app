# agent-notes: ctx="service layer tests — M3 business logic" deps=["todo_cli.service","todo_cli.models"] state=active last="tara@2026-06-04"

from datetime import date, datetime, timedelta

import pytest
from todo_cli.exceptions import (
    InvalidDateError,
    TaskNotFoundError,
    ValidationError,
)
from todo_cli.models import Status
from todo_cli.service import TaskService
from todo_cli.storage.json_store import JsonStorageBackend


@pytest.fixture
def service(tmp_path):
    """A TaskService wired to a throwaway storage backend in a temp folder."""
    return TaskService(JsonStorageBackend(data_dir=tmp_path))


def test_add_task_returns_task_with_id(service):
    task = service.add_task("Buy milk")
    assert task.id == 1
    assert task.description == "Buy milk"
    assert task.status == Status.PENDING


@pytest.mark.parametrize("bad", ["", "   "])
def test_add_task_raises_on_empty_description(service, bad):
    with pytest.raises(ValidationError):
        service.add_task(bad)


def test_add_task_raises_on_past_due_date(service):
    yesterday = date.today() - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        service.add_task("Buy milk", due_date=yesterday)


def test_add_task_accepts_future_due_date(service):
    tomorrow = date.today() + timedelta(days=1)
    task = service.add_task("Buy milk", due_date=tomorrow)
    assert task.due_date == tomorrow


def test_add_task_accepts_due_date_today(service):
    today = date.today()
    task = service.add_task("Buy milk", due_date=today)
    assert task.due_date == today


def test_complete_task_sets_status_and_timestamp(service):
    task = service.add_task("Buy milk")
    completed = service.complete_task(task.id)
    assert completed.status == Status.COMPLETED
    assert completed.completed_at is not None


def test_complete_task_raises_for_missing_id(service):
    with pytest.raises(TaskNotFoundError):
        service.complete_task(999)


def test_complete_task_stamps_current_time(service):
    task = service.add_task("Buy milk")
    before = datetime.utcnow()
    completed = service.complete_task(task.id)
    after = datetime.utcnow()
    assert before <= completed.completed_at <= after


def test_complete_task_persists_to_storage(service):
    task = service.add_task("Buy milk")
    service.complete_task(task.id)
    reloaded = service.list_tasks()[0]
    assert reloaded.status == Status.COMPLETED
    assert reloaded.completed_at is not None


def test_delete_task_removes_it(service):
    task = service.add_task("Buy milk")
    service.delete_task(task.id)
    assert service.list_tasks() == []


def test_delete_task_raises_for_missing_id(service):
    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)


def test_list_tasks_returns_all(service):
    service.add_task("First")
    service.add_task("Second")
    tasks = service.list_tasks()
    assert [t.description for t in tasks] == ["First", "Second"]
