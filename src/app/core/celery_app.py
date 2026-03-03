from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.task_status_code"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # task_routes={"tasks.task_status_code.*": {"queue": "celery"}},
)

# celery_app.autodiscover_tasks(["app.tasks"])
