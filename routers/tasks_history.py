from config.db import db
from fastapi import APIRouter, status
from schemas.task_history import task_history_entity, tasks_history_entity
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models.task_history import TaskHistory
from datetime import datetime

router = APIRouter(
    prefix="/tasks_history",
    tags=["Tasks History"],
)


@router.get("/")
async def read_tasks_history(id: str):
    tasks_data = db.task_history.find({
        "user": ObjectId(id)
    })

    if not tasks_data or tasks_data == []:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    tasks = tasks_entity(tasks_data)
    return tasks


@router.get("/{id}")
async def read_task_history(id: str):
    task_data = db.task_history.find_one({"_id":  ObjectId(id)})

    if not task_data or task_data == {}:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    task = task_entity(task_data)
    return task


@router.post("/")
async def create_task_history(task: TaskHistory):
    db.task_history.insert_one({
        "user": ObjectId(task.user),
        "task": ObjectId(task.task),
        "start_time": str(datetime.now()),
        "end_time": Null,
        "is_started": True,
        "is_completed": False,
    })

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "task created successfully"}
    )


@router.put("/complete/{id}")
async def update_task_history(id: str, task: TaskHistory):
    db.task_history.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "end_time": str(datetime.now()),
            "is_completed": True,
        }
    })

    return {"message": "task updated successfully"}


@router.delete("/all/{id}")
async def delete_all_task_history(id: str):
    db.task_history.find_and_delete({"user": ObjectId(id)})

    return {"message": "task deleted successfully"}


@router.delete("/{id}")
async def delete_task_history(id: str):
    db.task_history.find_one_and_delete({"_id": ObjectId(id)})

    return {"message": "task deleted successfully"}
