import time

import requests

from app.core.celery_app import celery_app
from app.core.config_email import mail
from app.services.email_service import prepare_message_verify_account
from app.tasks.send_email_task import send_email_sync


@celery_app.task
def io_bound_task(url: str):
    response = requests.get(url)
    return response.status_code


@celery_app.task
def collect_results(results, start_time):
    end_time = time.time()
    return {"status": results, "time_taken": end_time - start_time}


@celery_app.task
def process_send_message_celery(recipients: list[str], token: str):
    start_time = time.time()
    message = prepare_message_verify_account(recipients, token)
    send_email_sync(message=message, mail=mail)
    end_time = time.time()
    return {"status": "sent", "time_taken": end_time - start_time}
