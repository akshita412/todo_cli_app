# agent-notes: { ctx: "env-driven factory: builds a TaskService from TODO_BACKEND/TODO_DATA_PATH", deps: [service.py, storage/json_store.py], state: active, last: "sato@2026-06-13" }
import os
from pathlib import Path

from todo_cli.service import TaskService
from todo_cli.storage.json_store import JsonStorageBackend


def build_service() -> TaskService:
    """Construct a TaskService from environment configuration.

    TODO_BACKEND   selects the storage backend (default: "json").
    TODO_DATA_PATH directory holding the data file (default: ~/.todo).
    """
    backend = os.environ.get("TODO_BACKEND", "json").strip().lower()
    data_path = os.environ.get("TODO_DATA_PATH")
    data_dir = Path(data_path) if data_path else None

    if backend == "json":
        return TaskService(JsonStorageBackend(data_dir))

    raise ValueError(
        f"Unknown TODO_BACKEND {backend!r}. Supported backends: json."
    )
