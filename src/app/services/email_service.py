from fastapi import BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi_mail import MessageSchema, MessageType

from app.core.config import settings
from app.core.config_email import mail
from app.tasks.send_email_task import send_email

templates = Jinja2Templates(directory="src/app/template")


def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )
    return message


def prepare_message_data(recipients: list[str]):
    html = templates.get_template("test.html").render()
    subject = "Welcome to our app"
    message = create_message(recipients=recipients, subject=subject, body=html)
    return message


async def process_send_message(message, mail=mail):
    await send_email(message=message, mail=mail)


def prepare_message_verify_account(recipients: list[str], token: str):
    link = f"http://{settings.DOMAIN}/api/v12/email/verify/{token}"
    html = templates.get_template("verify_account.html").render(link=link)
    subject = "Verify Email Address"
    message = create_message(recipients=recipients, subject=subject, body=html)
    return message


def process_send_message_bg_task(message, background_tasks: BackgroundTasks, mail=mail):
    background_tasks.add_task(send_email, message, mail)
