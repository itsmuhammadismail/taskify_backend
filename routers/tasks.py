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
        "user": ObjectId(id),
        "is_pending": True
    })

    if not tasks_data or tasks_data == []:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    tasks_list = tasks_entity(tasks_data)

    # Sort tasks by due_date and then by status (high > medium > low)
    sorted_tasks = sorted(tasks_list, key=lambda x: (
        x['due_date'].split(' ')[0], {"high": 0, "medium": 1, "low": 2}[x['status']]))

    return sorted_tasks


@router.get("/started/")
async def read_running_tasks(id: str):
    tasks_data = db.tasks.find({
        "user": ObjectId(id),
        "running_status": "started"
    })

    if not tasks_data or tasks_data == []:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    tasks_list = tasks_entity(tasks_data)

    # Sort tasks by due_date and then by status (high > medium > low)
    sorted_tasks = sorted(tasks_list, key=lambda x: (
        x['due_date'].split(' ')[0], {"high": 0, "medium": 1, "low": 2}[x['status']]))

    return sorted_tasks


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
        "user": ObjectId(task.user),
        "is_pending": True,
        "running_status": "pending"
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


@router.delete("/all/")
async def delete_all_task():
    db.tasks.delete_many({})

    return {"message": "task deleted successfully"}
