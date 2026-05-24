# agent-notes: { ctx: "domain exceptions for CLI error handling", deps: [], state: active, last: "sato@2026-05-24" }


class TodoError(Exception):
    """Base exception for all todo-cli errors."""


class ValidationError(TodoError):
    """Raised when task input fails validation."""


class InvalidDateError(ValidationError):
    """Raised when a date string cannot be parsed as YYYY-MM-DD."""


class TaskNotFoundError(TodoError):
    """Raised when a task ID does not exist in storage."""


class StorageCorruptError(TodoError):
    """Raised when the storage file cannot be parsed."""


class StorageAccessError(TodoError):
    """Raised when the storage file cannot be read or written."""
