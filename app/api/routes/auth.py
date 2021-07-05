from fastapi import APIRouter
from app.core.security.auth import (
    UsersAuth,
    SECRET_KEY,
)
from app.core.security.utils import on_after_forgot_password, on_after_reset_password


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
