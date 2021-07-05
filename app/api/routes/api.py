from fastapi import APIRouter

from app.schemas.common_models import ApiBaseResponse

from . import profile, explore

router = APIRouter()
router.include_router(profile.router, prefix="/profile")
router.include_router(explore.router, prefix="/explore")


@router.get("", response_model=ApiBaseResponse, tags=["root"])
async def api_root() -> ApiBaseResponse:

    return ApiBaseResponse(
        status=True, code=200, message="Welcome to Habit-Story API"
    ).dict()
