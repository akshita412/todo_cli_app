# agent-notes: ctx="JSON file storage backend" deps=["storage/base.py","models.py"] state=active last="sato@2026-06-24"

import json
import os
import tempfile
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from todo_cli.exceptions import StorageAccessError, StorageCorruptError
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
        try:
            with self._path.open() as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise StorageCorruptError(
                f"Task file is corrupted: {self._path}"
            ) from exc
        except OSError as exc:
            raise StorageAccessError(
                f"Cannot access task file: {self._path}"
            ) from exc

        if (
            not isinstance(data, dict)
            or not isinstance(data.get("next_id"), int)
            or isinstance(data.get("next_id"), bool)
            or not isinstance(data.get("tasks"), dict)
        ):
            raise StorageCorruptError(f"Task file is corrupted: {self._path}")
        return data

    def _save(self, data: dict) -> None:
        # Atomic write: serialize into a temp file in the same directory, flush it
        # to disk, then os.replace() it over the destination. A torn or failed
        # write touches only the temp file — the prior good tasks.json survives.
        # Note: mkstemp creates the temp at 0600 and os.replace preserves that
        # mode, so tasks.json ends up owner-only (was 0644 under the old in-place
        # open). This is intentional — task descriptions shouldn't be world-readable.
        tmp_name = None
        try:
            tmp_fd, tmp_name = tempfile.mkstemp(
                dir=self._path.parent, prefix=".tasks-", suffix=".tmp"
            )
            with os.fdopen(tmp_fd, "w") as f:
                json.dump(data, f, indent=2, default=str)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_name, self._path)
        except OSError as exc:
            if tmp_name is not None:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
            raise StorageAccessError(
                f"Cannot access task file: {self._path}"
            ) from exc

    def _deserialize(self, raw: dict) -> Task:
        try:
            return Task(
                id=raw["id"],
                description=raw["description"],
                status=Status(raw["status"]),
                due_date=date.fromisoformat(raw["due_date"]) if raw.get("due_date") else None,
                created_at=datetime.fromisoformat(raw["created_at"]),
                completed_at=datetime.fromisoformat(raw["completed_at"]) if raw.get("completed_at") else None,
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise StorageCorruptError(
                f"Task file is corrupted: {self._path}"
            ) from exc

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
