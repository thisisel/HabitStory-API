from typing import Optional
from datetime import datetime
from pydantic.main import BaseModel
from . import pydantic_model_creator, PydanticModel
from . common_models import ApiBaseResponse
from app.db.models import ChallengeModel


ChallengeBase_Pydantic = pydantic_model_creator(
    ChallengeModel,
    name="ChallengeBase",
    exclude=("created_at", "created_by", "description", "participants", "created_by_id"),
)


class CreateNewChallenge(BaseModel):
    title: str
    description: str
    duration: int
    is_public: bool = False

class ChallengeInList(ChallengeBase_Pydantic):
    participants_count: int

class ChallengeDetail(ChallengeInList):
    description: str
    created_at: datetime

class SingleChallengeResponse(ApiBaseResponse):
    challenge: ChallengeDetail