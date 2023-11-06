from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TaskHistory(BaseModel):
    user: str
    task: str