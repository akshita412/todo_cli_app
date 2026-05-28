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
