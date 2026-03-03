import time

from fastapi import BackgroundTasks

from app.tasks.send_email_task import write_log, write_notification


def notifications_deps(email: str, background_tasks: BackgroundTasks):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)


def send_notification_classic(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")


task_status: dict = {}


def write_log_with_status(task_id: str, message: str):
    task_status[task_id] = "in progress"
    time.sleep(30)
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")
    task_status[task_id] = "done"
