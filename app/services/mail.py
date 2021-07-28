from typing import Dict, List, Optional, Union

from pydantic.networks import EmailStr
from starlette.responses import JSONResponse
from app.core.config import MailCredentials
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from fastapi import BackgroundTasks
from starlette.background import BackgroundTask

mail_cred = MailCredentials()
conf = ConnectionConfig(
    MAIL_USERNAME=mail_cred.mail_username,
    MAIL_PASSWORD=mail_cred.mail_password,
    MAIL_FROM=mail_cred.mail_from,
    MAIL_PORT=mail_cred.mail_port,
    MAIL_SERVER=mail_cred.mail_server,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)
fm = FastMail(conf)


async def compose_message(
    recipients: List[EmailStr],
    subject: str = "",
    body: Optional[Union[str, list]] = None,
    template_body: Optional[Union[list, dict]] = None,
    html: Optional[Union[str, List, Dict]] = None,
    subtype: Optional[str] = None,
):

    return MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html",
    )

async def send_background(message):
    try:

        # background_tasks = BackgroundTask()
        # background_tasks.add_task(fm.send_message,message)
        # task = BackgroundTask(fm.send_message, message)
        # # return True
        # return JSONResponse(background=task)
        await fm.send_message(message)
        return True
    
    except Exception:
        return False