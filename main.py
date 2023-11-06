from fastapi import FastAPI

from routers import users, tasks, tasks_history

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(tasks_history.router)
