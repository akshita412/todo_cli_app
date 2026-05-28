# agent-notes: ctx="JSON file storage backend" deps=["storage/base.py","models.py"] state=active last="sato@2026-05-28"

import json
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from todo_cli.models import Status, Task
from todo_cli.storage.base import StorageBackend


class JsonStorageBackend(StorageBackend):

    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path.home() / ".todo"
        self._path = Path(data_dir) / "tasks.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)

    # ── internal helpers ──────────────────────────────────────────────────────

    def _load(self) -> dict:
        if not self._path.exists():
            return {"next_id": 1, "tasks": {}}
        with self._path.open() as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        with self._path.open("w") as f:
            json.dump(data, f, indent=2, default=str)

    def _deserialize(self, raw: dict) -> Task:
        return Task(
            id=raw["id"],
            description=raw["description"],
            status=Status(raw["status"]),
            due_date=date.fromisoformat(raw["due_date"]) if raw.get("due_date") else None,
            created_at=datetime.fromisoformat(raw["created_at"]),
            completed_at=datetime.fromisoformat(raw["completed_at"]) if raw.get("completed_at") else None,
        )

    # ── StorageBackend interface ──────────────────────────────────────────────

    def add(self, task: Task) -> Task:
        data = self._load()
        task.id = data["next_id"]
        data["next_id"] += 1
        data["tasks"][str(task.id)] = asdict(task)
        self._save(data)
        return task

    def get(self, task_id: int) -> Optional[Task]:
        data = self._load()
        raw = data["tasks"].get(str(task_id))
        return self._deserialize(raw) if raw else None

    def list(self) -> List[Task]:
        data = self._load()
        tasks = [self._deserialize(t) for t in data["tasks"].values()]
        return sorted(tasks, key=lambda t: t.created_at)

    def update(self, task: Task) -> Task:
        data = self._load()
        data["tasks"][str(task.id)] = asdict(task)
        self._save(data)
        return task

    def delete(self, task_id: int) -> None:
        data = self._load()
        data["tasks"].pop(str(task_id), None)
        self._save(data)
