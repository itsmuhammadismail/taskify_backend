from config.db import db
from fastapi import APIRouter, status
from schemas.task_history import task_history_entity, tasks_history_entity
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models.task_history import TaskHistory
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/tasks_history",
    tags=["Tasks History"],
)


@router.get("/")
async def read_tasks_history(id: str):
    lookup_stage = {
        "$lookup": {
            "from": "tasks",  # the collection to join
            "localField": "task",  # the field from the input documents
            "foreignField": "_id",  # the field from the joined documents
            "as": "task_details"  # the output array field
        }
    }

    match_stage = {
        "$match": {
            "user": ObjectId(id)
        }
    }

    tasks_data = db.task_history.aggregate([match_stage, lookup_stage])

    if not tasks_data or tasks_data == []:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    tasks = tasks_history_entity(tasks_data)
    return tasks


@router.get("/{id}")
async def read_task_history(id: str):
    task_data = db.task_history.find_one({"_id":  ObjectId(id)})

    if not task_data or task_data == {}:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "task not found"}
        )

    task = task_history_entity(task_data)
    return task


@router.post("/")
async def create_task_history(task: TaskHistory):
    db.tasks.find_one_and_update({"_id": ObjectId(task.task)}, {
        "$set": {
            "is_pending": False,
            "running_status": "started",
            "updated_at": datetime.now()
        }
    })

    db.task_history.insert_one({
        "user": ObjectId(task.user),
        "task": ObjectId(task.task),
        "start_time": str(datetime.now()),
        "end_time": None,
        "is_started": True,
        "is_completed": False,
    })

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "task history created successfully"}
    )


@router.put("/complete/{id}")
async def update_task_history(id: str):
    db.task_history.find_one_and_update({"task": ObjectId(id)}, {
        "$set": {
            "end_time": str(datetime.now()),
            "is_completed": True,
        }
    })

    db.tasks.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "running_status": "finished"
        }
    })

    return {"message": "task updated successfully"}


@router.delete("/all/{id}")
async def delete_all_task_history(id: str):
    db.task_history.delete_many({"user": ObjectId(id)})
    return {"message": "task deleted successfully"}


@router.delete("/{id}")
async def delete_task_history(id: str):
    db.task_history.find_one_and_delete({"_id": ObjectId(id)})

    return {"message": "task deleted successfully"}


@router.get("/graph/{id}")
async def get_graph_data(id: str):
    dateTimeList = list(map(lambda n: datetime.now() -
                        timedelta(minutes=n), [0, 15, 30, 45, 60, 75]))
    counts = [0 for date in dateTimeList]

    lookup_stage = {
        "$lookup": {
            "from": "tasks",  # the collection to join
            "localField": "task",  # the field from the input documents
            "foreignField": "_id",  # the field from the joined documents
            "as": "task_details"  # the output array field
        }
    }

    match_stage = {
        "$match": {
            "user": ObjectId(id)
        }
    }

    tasks_data = db.task_history.aggregate([match_stage, lookup_stage])

    tasks = tasks_history_entity(tasks_data)

    for index, time in enumerate(dateTimeList):
        for task in tasks:
            start_time = datetime.strptime(
                task["start_time"], "%Y-%m-%d %H:%M:%S.%f")
            if start_time <= time:
                if task["end_time"] == None:
                    counts[index] += 1
                else:
                    end_time = datetime.strptime(
                        task["end_time"], "%Y-%m-%d %H:%M:%S.%f")

                    if end_time <= time and end_time >= (time - timedelta(minutes=15)):
                        counts[index] += 1

    return {
        "dateTimeList": dateTimeList,
        "counts": counts
    }
