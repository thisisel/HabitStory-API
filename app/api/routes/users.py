from fastapi import APIRouter
from .journal import public_journal

router = APIRouter()
router.include_router(public_journal.router, prefix="/journals", tags=["journals"])

