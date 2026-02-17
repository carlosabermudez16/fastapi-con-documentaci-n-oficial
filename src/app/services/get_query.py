from fastapi import BackgroundTasks

from app.tasks.send_email_task import write_log


def get_query(background_tasks: BackgroundTasks, task: str | None = None):
    if task:
        message = f"Found query: {task}\n"
        background_tasks.add_task(write_log, message)

    return task
