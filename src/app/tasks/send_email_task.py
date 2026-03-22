import asyncio


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


async def send_email(message, mail):
    return await mail.send_message(message)


def send_email_sync(message, mail):
    return asyncio.run(mail.send_message(message))
