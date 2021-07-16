from fastapi import APIRouter
from app.core.security.auth import (
    UsersAuth,
    SECRET_KEY,
)
from app.core.security.oauth2 import google_oauth_client
from app.core.security.utils import on_after_forgot_password, on_after_reset_password, on_after_register


router = APIRouter()
fastapi_users = UsersAuth.get_fastapiusers()

router.include_router(
    fastapi_users.get_auth_router(UsersAuth.jwt_authentication),
    prefix="/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_auth_router(UsersAuth.cookie_authentication),
    prefix="/cookie",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(
        str(SECRET_KEY),
        after_forgot_password=on_after_forgot_password,
        after_reset_password=on_after_reset_password,
    ),
    tags=["auth"],
)

google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client, str(SECRET_KEY), after_register=on_after_register
)
router.include_router(google_oauth_router, prefix="/google", tags=["auth"])
