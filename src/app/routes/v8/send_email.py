import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.services.get_query import get_query
from app.services.notifications_service import (
    notifications_deps,
    send_notification_classic,
    task_status,
    write_log_with_status,
)

router = APIRouter(prefix="/api/v8/tasks", tags=["Threads V8"])


@router.post("/send-notification/{email}", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    send_notification_classic(email, background_tasks)
    return {"message": "Notification sent in the background"}


@router.post("/send-notification-deps/{email}")
async def send_notification_deps(
    email: str,
    background_tasks: BackgroundTasks,
    task: Annotated[str, Depends(get_query)],
):
    notifications_deps(email, background_tasks)
    return {"message": "Message sent"}


@router.post("/notify/")
async def notify_user(email: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        write_log_with_status, task_id, f"Notification sent to {email}"
    )
    return {"task_id": task_id}


@router.get("/task-status/{task_id}")
async def get_status(task_id: str):
    return {"status": task_status.get(task_id, "not found")}
