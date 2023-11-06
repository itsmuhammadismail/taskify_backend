def task_history_entity(task) -> dict:
    return {
        "id": str(task["_id"]),
        "user": task["user"],
        "task": task["task"],
        "start_time": task["start_time"],
        "end_time": task["end_time"],
    }


def tasks_history_entity(tasks) -> list:
    return [task_history_entity(task) for task in tasks]
