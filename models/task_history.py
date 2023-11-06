from datetime import datetime
from typing import Optional

class TaskHistory(BaseModel):
    user: str
    task: str