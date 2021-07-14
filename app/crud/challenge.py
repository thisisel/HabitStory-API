from typing import Set

from tortoise.query_utils import Q
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
    async def fetch_trending_challenges(cls, q_filters: Set[Q] = None):
        return (
            ChallengeModel.all().filter(*q_filters, join_type="AND")
            .only("id", "title", "duration", "created_at")
            .annotate(participants_count=Count("participants"))
            .order_by("-participants_count", "-created_at")
        )

    @classmethod
    async def fetch_single_challenge(cls, id: int):
        return ChallengeModel.get_or_none(id=id).annotate(
            participants_count=Count("participants")
        )

    @classmethod
    async def challenge_exists(cls, challenge_id: int)-> bool:
        return await ChallengeModel.filter(id=challenge_id).exists()