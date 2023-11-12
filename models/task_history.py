from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskHistory(BaseModel):
    user: str
    task: str
    # start_time: datetime
    # end_time: Optional[datetime | None]
    # is_started: bool
    # is_completed: bool
