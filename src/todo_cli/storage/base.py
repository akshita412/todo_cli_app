# agent-notes: { ctx: "abstract StorageBackend interface", deps: [models.py], state: active, last: "sato@2026-05-24" }
from abc import ABC, abstractmethod
from typing import List, Optional

from todo_cli.models import Task


class StorageBackend(ABC):
    """All storage backends must implement this interface."""

    @abstractmethod
    def add(self, task: Task) -> Task:
        """Persist a new task and return it with its assigned id."""

    @abstractmethod
    def get(self, task_id: int) -> Optional[Task]:
        """Return the task with the given id, or None if not found."""

    @abstractmethod
    def list(self) -> List[Task]:
        """Return all tasks sorted by created_at ascending."""

    @abstractmethod
    def update(self, task: Task) -> Task:
        """Persist changes to an existing task and return it."""

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """Permanently remove a task by id."""
