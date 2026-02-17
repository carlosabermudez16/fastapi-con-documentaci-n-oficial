import time

from fastapi import Request
from starlette.background import BackgroundTask
from starlette.responses import Response

from app.core.logger import logger
from app.core.monitoring import send_slack_alert, should_alert


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response: Response = await call_next(request)

    duration = round(time.time() - start_time, 3)
    client_ip = request.client.host if request.client else "unknown"
    content_length = response.headers.get("content-length", "unknown")

    log_details = {
        "method": request.method,
        "path": request.url.path,
        "duration": duration,
        "client_ip": client_ip,
        "status": response.status_code,
        "size_bytes": content_length,
    }

    logger.info(f"Handled request: {log_details}")

    # Alerta asincrónica si aplica
    if should_alert(duration, response.status_code):
        message = (
            f"⚠️ Slow/Error request\n"
            f"Duration: {duration}s\n"
            f"Method: {request.method}\n"
            f"Path: {request.url.path}\n"
            f"Status: {response.status_code}\n"
            f"Client IP: {client_ip}\n"
            f"Size: {content_length} bytes"
        )

        response.background = BackgroundTask(send_slack_alert, message)

    return response
