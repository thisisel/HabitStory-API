from app.core.security.auth import UsersAuth

from .journal import private_journal
from app.schemas.common_models import ApiErrorResponse
from app.api.errors import Forbidden, OWNER_AUTH


fastapi_users = UsersAuth.get_fastapiusers()
router = fastapi_users.get_users_router()

router.include_router(private_journal.router, prefix="/journals")


@router.get(
    "/{id:uuid}",
    deprecated=True,
    status_code=403,
    response_description="Forbidden",
    response_model=ApiErrorResponse,
)
async def get_user():
    raise Forbidden(category=OWNER_AUTH)


@router.patch(
    "/{id:uuid}",
    deprecated=True,
    status_code=403,
    response_description="Forbidden",
    response_model=ApiErrorResponse,
)
async def update_user():
    raise Forbidden(category=OWNER_AUTH)


@router.delete(
    "/{id:uuid}",
    deprecated=True,
    status_code=403,
    response_description="Forbidden",
    response_model=ApiErrorResponse,
)
async def delete_user():
    raise Forbidden(category=OWNER_AUTH)


# TODO return max streak and total chears in bio