import httpx
from fastapi import status

from app.constants.constants import TIME_OUT, WAITING_TIME
from app.core.config import settings
from app.core.logger import logger

SLACK_WEBHOOK_URL = settings.SLACK_WEBHOOK_URL
ENVIRONMENT = settings.ENVIRONMENT


async def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        logger.warning("Slack webhook not configured")
        return

    payload = {"text": message}

    try:
        async with httpx.AsyncClient(timeout=TIME_OUT) as client:
            await client.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")


def should_alert(duration: float, status_code: int) -> bool:
    if ENVIRONMENT == "development":
        return False

    return (
        duration > WAITING_TIME or status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR
    )
