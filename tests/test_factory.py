# agent-notes: { ctx: "tests for service/backend factory (env-driven)", deps: [factory.py], state: active, last: "sato@2026-06-13" }
import pytest

from todo_cli.factory import build_service
from todo_cli.service import TaskService
from todo_cli.storage.json_store import JsonStorageBackend


def test_build_service_defaults_to_json(monkeypatch, tmp_path):
    """With no TODO_BACKEND set, the factory returns a JSON-backed TaskService."""
    monkeypatch.delenv("TODO_BACKEND", raising=False)
    monkeypatch.setenv("TODO_DATA_PATH", str(tmp_path))  # keep out of real ~/.todo

    svc = build_service()

    assert isinstance(svc, TaskService)
    assert isinstance(svc._storage, JsonStorageBackend)


def test_build_service_honors_data_path(monkeypatch, tmp_path):
    """TODO_DATA_PATH points storage at that directory, not the user's home."""
    monkeypatch.delenv("TODO_BACKEND", raising=False)
    monkeypatch.setenv("TODO_DATA_PATH", str(tmp_path))

    svc = build_service()
    svc.add_task("Buy milk")

    assert (tmp_path / "tasks.json").exists()


def test_build_service_unknown_backend_errors(monkeypatch, tmp_path):
    """An unknown TODO_BACKEND raises a clear error rather than crashing."""
    monkeypatch.setenv("TODO_BACKEND", "mongo")
    monkeypatch.setenv("TODO_DATA_PATH", str(tmp_path))

    with pytest.raises(ValueError, match="mongo"):
        build_service()
