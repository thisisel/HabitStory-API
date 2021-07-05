from app.schemas.common_models import ApiBaseResponse
from app.core.log.current_logger import CurrentLogger
from app.api.errors import NotFound, REWARD_404, internal_error
from typing import Set
from tortoise.query_utils import Prefetch, Q
from app.crud.reward import RetriveReward
from tortoise.queryset import QuerySet, QuerySetSingle
from app.db.models import (
    ChallengeModel,
    JournalModel,
    PageModel,
    StoryReward,
    RewardModel,
)
from fastapi.encoders import jsonable_encoder


class RetriveJournal:
    @classmethod
    async def fetch_user_journals(
        cls, user_id: int, q_filters: Set[Q] = None
    ) -> QuerySet[JournalModel]:
        try:
            # TODO separate fetch user journal from extra filters
            return (
                JournalModel.filter(Q(author_id=user_id), *q_filters, join_type="AND")
                .prefetch_related(
                    Prefetch(
                        relation="pages",
                        queryset=PageModel.all().only("id", "journal_id"),
                    )
                )
                .all()
            )

        except KeyError as ke:

            CurrentLogger.get_logger().error(ke)
            raise internal_error()

    @classmethod
    async def fetch_single_journal(
        cls, user_id: int, journal_id: int
    ) -> QuerySetSingle[JournalModel]:
        return JournalModel.get_or_none(id=journal_id, author_id=user_id)

    @classmethod
    async def journal_is_over(cls, journal_id: int) -> bool:

        journal = (
            await JournalModel.filter(id=journal_id)
            .first()
            .prefetch_related(
                Prefetch(
                    relation="pages", queryset=PageModel.all().only("id", "journal_id")
                ),
                Prefetch(
                    relation="challenge",
                    queryset=ChallengeModel.all().only("id", "duration"),
                ),
            )
        )
        page_count = journal.count_pages()
        challenge_duration = journal.challenge.duration

        if page_count < challenge_duration:
            return False

        return True


class CreateJournal:
    @classmethod
    async def create_journal(
        cls,
        user_id: int,
        challenge_id: int,
        is_public: bool = False,
        reward_model: RewardModel = StoryReward,
    ) -> JournalModel:

        # TODO random reward
        reward_qset = await RetriveReward.fetch_random_reward(reward_model=StoryReward)
        if (reward_obj := await reward_qset) is None:

            raise NotFound(category=REWARD_404)

        return JournalModel.create(
            author_id=user_id,
            challenge_id=challenge_id,
            is_public=is_public,
            reward_id=reward_obj.id,
        )
