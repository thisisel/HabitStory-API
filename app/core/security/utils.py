from fastapi import Request

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
