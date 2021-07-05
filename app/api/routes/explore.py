from fastapi import APIRouter
from .import challenges
from . import users
router = APIRouter()
router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
router.include_router(users.router, prefix="/users")