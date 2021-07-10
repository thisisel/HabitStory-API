from typing_extensions import Annotated
from app.db.models import ChallengeModel
from app.schemas.challenge import CreateNewChallenge
from tortoise.functions import Count


class CreateChallenge:
    @classmethod
    async def create_challenge(
        cls, user_id: int, data: CreateNewChallenge
    ) -> ChallengeModel:
        return await ChallengeModel.create(
            **data.dict(exclude_unset=True),
            created_by_id=user_id,
        )


class RetrieveChallenge:
    @classmethod
    async def fetch_trending_challenges(cls):
        return (
            ChallengeModel.all()
            .only("id", "title", "duration")
            .annotate(participants_count=Count("participants"))
            .order_by("participants_count")
        )

    @classmethod
    async def fetch_single_challenge(cls, id: int):
        return ChallengeModel.get_or_none(id=id).annotate(
            participants_count=Count("participants")
        )
