# agent-notes: { ctx: "Task dataclass and Status enum", deps: [], state: active, last: "sato@2026-05-24" }
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    description: str
    id: int = field(default=0)
    due_date: Optional[date] = field(default=None)
    status: Status = field(default=Status.PENDING)
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = field(default=None)

    @property
    def is_overdue(self) -> bool:
        return (
            self.due_date is not None
            and self.status == Status.PENDING
            and self.due_date < date.today()
        )
