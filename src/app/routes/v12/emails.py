from fastapi import APIRouter, status

from app.schemas.v7.email import EmailScheme
from app.services.email_service import prepare_message_data, process_send_message

router = APIRouter(prefix="/api/v12/email", tags=["Emails V12"])


@router.post("/send_mail", status_code=status.HTTP_200_OK)
async def send_mail(emails: EmailScheme):
    emails = emails.addresses
    message = prepare_message_data(recipients=emails)

    await process_send_message(message)

    return {"message": "Email sent successfully"}
