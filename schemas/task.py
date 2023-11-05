def task_entity(task) -> dict:
    return {
        "id": str(task["_id"]),
        "desc": task["desc"],
        "due_date": task["due_date"],
        "status": task["status"],
        "user": str(task["user"])
    }


def tasks_entity(tasks) -> list:
    return [task_entity(task) for task in tasks]
