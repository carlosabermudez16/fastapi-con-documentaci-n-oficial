import time

from celery import chord
from fastapi import APIRouter

from app.tasks.task_status_code import collect_results, io_bound_task

router = APIRouter(prefix="/api/v11/celery_tasks", tags=["Celery_Redis V11"])


@router.get("/sequential")
async def sequential_task():
    start_time = time.time()
    urls = ["https://httpbin.org/delay/3" for n in range(10)]
    results = [io_bound_task(url) for url in urls]
    end_time = time.time()

    return {"status": results, "time_taken": end_time - start_time}


@router.get("/sequential_celery")
async def sequential_celery():
    start_time = time.time()
    urls = ["https://httpbin.org/delay/3" for n in range(10)]
    tasks = [io_bound_task.s(url) for url in urls]
    callback = chord(tasks)(collect_results.s(start_time))
    return {"task_id": callback.id}


@router.get("/result/{task_id}")
async def get_result(task_id: str):
    task = collect_results.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "Task is still in progress", "state": task.state}
    elif task.state != "FAILURE":
        return task.result
    else:
        return {"status": "Task Failed", "state": task.state, "error": str(task.info)}
