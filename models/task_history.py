from datetime import datetime

class TaskHistory(BaseModel):
    user: str
    task: str
    start_time: datetime
    end_time: datetime