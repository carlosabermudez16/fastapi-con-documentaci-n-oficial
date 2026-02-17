from fastapi import BackgroundTasks

from app.tasks.send_email_task import write_log, write_notification


def notifications_deps(email: str, background_tasks: BackgroundTasks):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)


def send_notification_classic(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
