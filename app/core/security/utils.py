from fastapi import Request
from app.services.mail import send_background, compose_message

from . import UserDB


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    """Send url-encoded email

    Args:
        user (UserDB):  pydantic model representing user
        token (str): to be encoded in url
        request (Request):
    """
    # TODO send email
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def on_after_reset_password(user: UserDB, request: Request):
    """Change in password warning
    send an email warning user

    Args:
        user (UserDB): pydantic model representing user
        request (Request): actual request
    """
    # TODO
    print(f"User {user.id} has reset their password.")


async def on_after_register(user: UserDB, request: Request):
    """Send greetings email

    Args:
        user (UserDB): [description]
        request (Request): [description]
    """
    print(f"User {user.id} has registered.")
    message = await compose_message(
        recipients=[user.email],
        subject="Welcome to HabitStory",
        body="Your account is successfully registered",
    )
    await send_background(message=message)
