import os

import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

smtp_user = os.getenv("SMTP_USER")
smtp_host = os.getenv("SMTP_HOST")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_port = os.getenv("SMTP_PORT")

async def send_email_async(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = smtp_user
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=smtp_host,
        port=smtp_port,
        start_tls=True,
        username=smtp_user,
        password=smtp_password,
    )
