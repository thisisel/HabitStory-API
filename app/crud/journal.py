from app.crud.page import RetrivePage
from app.api.errors.error_categories import JOURNAL_404
from app.schemas.common_models import Dto, JournalPageBundle
from app.schemas.journal import JournalBase_Pydantic, UpdateJournalAfterNewPage, UpdateJournal_Pydantic
from app.core.log.current_logger import CurrentLogger
from app.api.errors import NotFound, REWARD_404, internal_error, NotAllowed, JRNL_OVER_405, InternalError
from typing import Set, Union
from tortoise.query_utils import Prefetch, Q
from app.crud.reward import RetriveReward
from tortoise.queryset import QuerySet, QuerySetSingle
from app.db.models import (
    ChallengeModel,
    JournalModel,
    PageModel,
    StoryReward,
    RewardModel,
    UserModel,
)

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

    #TODO rename fetch_user_single_journal
    @classmethod
    async def fetch_single_journal(
        cls, user_id: int, journal_id: int
    ) -> QuerySetSingle[JournalModel]:
        return JournalModel.get_or_none(id=journal_id, author_id=user_id).prefetch_related("pages")

    @classmethod
    async def check_journal_is_over(cls, journal_id: int)-> Dto:

        journal = (
            await JournalModel.filter(id=journal_id)
            .first()
            .prefetch_related(
                Prefetch(
                    relation="pages", queryset=PageModel.all().only("id", "journal_id", "page_num", "submitted")
                ),
                Prefetch(
                    relation="challenge",
                    queryset=ChallengeModel.all().only("id", "duration"),
                ),
                Prefetch(
                    relation="author",
                    queryset=UserModel.all().only("id", "username")
                )
            )
        )

        if journal is None:
            raise NotFound(category=JOURNAL_404)

        page_count = journal.count_pages()
        
        if(page_count == 0):
            return Dto(status=True, data=JournalPageBundle(journal=journal, page=None))
        
        last_page = await RetrivePage.get_latest_page(journal_id=journal_id, author_id=journal.author.id)
        
        challenge_duration = journal.challenge.duration
        remains = challenge_duration - page_count
        # remains = challenge_duration - last_page.page_num

        bundle = JournalPageBundle(journal=journal, page=last_page)

        if remains > 1:
            return Dto(status=False, data=bundle)
        elif remains == 1:
            return Dto(status=True, data=bundle)
        elif remains == 0:
            raise NotAllowed(allowed_methods=dict(get="GET", patch="PATCH"), category=JRNL_OVER_405)
        else:
            CurrentLogger.get_logger().error(f"remains = {remains} while checking journal stats")
            raise InternalError()

    @classmethod
    async def user_owns_journal(cls, user_id: int, journal_id: int)->bool:
        return await JournalModel.filter(id=journal_id, author_id=user_id).exists()

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

        return await JournalModel.create(
            author_id=user_id,
            challenge_id=challenge_id,
            is_public=is_public,
            reward_id=reward_obj.id,
        )

class UpdateJournal:
    @classmethod
    async def update_journal(cls, journal_obj: JournalModel, data: Union[UpdateJournal_Pydantic, UpdateJournalAfterNewPage]) -> JournalModel:
        
        journal_pydantic = await JournalBase_Pydantic.from_tortoise_orm(journal_obj)
        journal_dict = journal_pydantic.dict()
        
        journal_dict.update(data.dict(exclude_unset=True))
        await journal_obj.update_from_dict(journal_dict).save()

        await journal_obj.refresh_from_db()

        return  journal_obj

class DeleteJournal:
    @classmethod
    async def delete_journal(cls, journal_id: int, user_id: int):
        deleted_journal = await JournalModel.filter(Q(id=journal_id) & Q(author_id=user_id)).delete()
        if not deleted_journal:
            raise NotFound(category=JOURNAL_404)
        return

