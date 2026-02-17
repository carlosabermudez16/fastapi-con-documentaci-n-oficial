from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.services.get_query import get_query
from app.services.notifications_service import (
    notifications_deps,
    send_notification_classic,
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
