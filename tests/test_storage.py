# agent-notes: ctx="storage backend tests — M2 JSON and SQLite" deps=["todo_cli.storage.json_store","todo_cli.models"] state=active last="tara@2026-05-28"

import pytest
from todo_cli.models import Task, Status
from todo_cli.storage.json_store import JsonStorageBackend


@pytest.fixture
def store(tmp_path):
    return JsonStorageBackend(data_dir=tmp_path)


def test_add_returns_task_with_assigned_id(store):
    task = Task(description="Buy milk", status=Status.PENDING)
    result = store.add(task)
    assert result.id == 1


def test_get_returns_task_by_id(store):
    task = Task(description="Buy milk", status=Status.PENDING)
    store.add(task)
    result = store.get(1)
    assert result is not None
    assert result.description == "Buy milk"


def test_get_returns_none_for_missing_id(store):
    assert store.get(999) is None


def test_list_returns_all_tasks_sorted_by_created_at(store):
    store.add(Task(description="First", status=Status.PENDING))
    store.add(Task(description="Second", status=Status.PENDING))
    tasks = store.list()
    assert len(tasks) == 2
    assert tasks[0].description == "First"
    assert tasks[1].description == "Second"


def test_update_persists_changes(store):
    task = store.add(Task(description="Buy milk", status=Status.PENDING))
    task.status = Status.COMPLETED
    store.update(task)
    result = store.get(task.id)
    assert result.status == Status.COMPLETED


def test_delete_removes_task(store):
    task = store.add(Task(description="Buy milk", status=Status.PENDING))
    store.delete(task.id)
    assert store.get(task.id) is None


def test_id_not_reused_after_deletion(store):
    task1 = store.add(Task(description="First", status=Status.PENDING))
    store.add(Task(description="Second", status=Status.PENDING))
    store.delete(task1.id)
    task3 = store.add(Task(description="Third", status=Status.PENDING))
    assert task3.id == 3


def test_tasks_persist_across_reinitialisation(tmp_path):
    store1 = JsonStorageBackend(data_dir=tmp_path)
    store1.add(Task(description="Persisted task", status=Status.PENDING))

    store2 = JsonStorageBackend(data_dir=tmp_path)
    result = store2.get(1)
    assert result is not None
    assert result.description == "Persisted task"
