def task_entity(task) -> dict:
    return {
        "id": str(task["_id"]),
        "desc": task["desc"],
        "due_date": task["due_date"],
        "status": task["status"],
        "user": str(task["user"]),
        "is_pending": task["is_pending"],
        "updated_at": task["updated_at"] or None
    }


def tasks_entity(tasks) -> list:
    return [task_entity(task) for task in tasks]
