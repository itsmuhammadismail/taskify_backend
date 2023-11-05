from config.db import db
from fastapi import APIRouter, status
from schemas.task import task_entity, tasks_entity
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models.task import Task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/")
async def read_tasks(id: str):
    tasks_data = db.tasks.find({
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
async def read_task(id: str):
    task_data = db.tasks.find_one({"_id":  ObjectId(id)})

    if not task_data or task_data == {}:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    task = task_entity(task_data)
    return task


@router.post("/")
async def create_task(task: Task):
    db.tasks.insert_one({
        "desc": task.desc,
        "due_date": str(task.due_date),
        "status": task.status,
        "user": ObjectId(task.user)
    })

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "task created successfully"}
    )


@router.put("/{id}")
async def update_task(id: str, task: Task):
    db.tasks.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "desc": task.desc,
            "due_date": str(task.due_date),
            "status": task.status,
        }
    })

    return {"message": "task updated successfully"}


@router.delete("/{id}")
async def delete_task(id: str):
    db.tasks.find_one_and_delete({"_id": ObjectId(id)})

    return {"message": "task deleted successfully"}
