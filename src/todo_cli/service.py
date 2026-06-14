# agent-notes: ctx="service layer — business rules between CLI and storage" deps=["storage/base.py","models.py"] state=active last="sato@2026-06-13"

from datetime import date, datetime, timezone
from typing import List, Optional

from todo_cli.exceptions import (
    InvalidDateError,
    TaskNotFoundError,
    ValidationError,
)
from todo_cli.models import Status, Task
from todo_cli.storage.base import StorageBackend


class TaskService:
    """Business logic layer: validates input and orchestrates storage."""

    def __init__(self, storage: StorageBackend):
        self._storage = storage

    def add_task(self, description: str, due_date: Optional[date] = None) -> Task:
        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty.")
        if due_date is not None and due_date < date.today():
            raise InvalidDateError("Due date cannot be in the past.")
        return self._storage.add(Task(description=description, due_date=due_date))

    def complete_task(self, task_id: int) -> Task:
        task = self._storage.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"No task with id {task_id}.")
        task.status = Status.COMPLETED
        task.completed_at = datetime.now(timezone.utc)
        return self._storage.update(task)

    def delete_task(self, task_id: int) -> None:
        if self._storage.get(task_id) is None:
            raise TaskNotFoundError(f"No task with id {task_id}.")
        self._storage.delete(task_id)

    def get_task(self, task_id: int) -> Task:
        task = self._storage.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"No task with id {task_id}.")
        return task

    def update_description(self, task_id: int, description: str) -> Task:
        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty.")
        task = self.get_task(task_id)
        task.description = description
        return self._storage.update(task)

    def list_tasks(self) -> List[Task]:
        return self._storage.list()
