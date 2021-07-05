from typing import Optional
from pydantic.main import BaseModel
from . import pydantic_model_creator, PydanticModel
from app.db.models import ChallengeModel

class CreateNewChallenge(BaseModel):
    title: str
    description: str
    duration: int
    is_public: bool = False