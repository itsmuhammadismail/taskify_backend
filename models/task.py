from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class StatusEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Task(BaseModel):
    desc: str
    due_date: datetime
    status: StatusEnum = StatusEnum.medium
    user: str
    is_pending: bool = True
