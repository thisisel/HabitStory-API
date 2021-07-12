from typing import Set, Union
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned
from tortoise.query_utils import Prefetch, Q
from tortoise.queryset import QuerySet, QuerySetSingle
from app.db.models import JournalModel, PageModel
from app.schemas.page import AddPage
from app.api.errors import NotFound, InternalError, PAGE_404


class RetrivePage:
    @classmethod
    async def fetch_pages_in_user_journal(
        cls, journal_id: int, author_id: int
    ) -> QuerySet[PageModel]:
        return PageModel.filter(
            Q(journal_id=journal_id),
            Q(journal__author_id=author_id),
            join_type="AND",
        ).all()

    @classmethod
    async def get_page_count(cls, journal_id: int, author_id: int) -> int:
        pages_qset = await cls.fetch_pages_in_user_journal(
            journal_id=journal_id, author_id=author_id
        )
        return await pages_qset.count()

    @classmethod
    async def get_latest_page(
        cls, journal_id: int, author_id: int
    ) -> Union[PageModel, None]:

        pages_qset = await cls.fetch_pages_in_user_journal(
            journal_id=journal_id, author_id=author_id
        )
        
        latest_page= await pages_qset.order_by("-page_num").first()
        await latest_page.refresh_from_db()
        
        return latest_page

    @classmethod
    async def fetch_all_journal_pages(cls, journal_id: int) -> QuerySet[PageModel]:
        return PageModel.filter(journal_id=journal_id).prefetch_related(
            Prefetch(relation="journal", queryset=JournalModel.all().only("id"))
        )

    @classmethod
    async def fetch_filtered_journal_pages(
        cls, journal_id: int, filters: Set[Q]
    ) -> QuerySet[PageModel]:
        all_pages_qset = await cls.fetch_all_journal_pages(journal_id=journal_id)
        return all_pages_qset.filter(*filters, join_type="AND")

    @classmethod
    async def fetch_single_page(
        cls, journal_id: int, page_id: int
    ) -> QuerySetSingle[PageModel]:
        return (
            PageModel.filter(Q(id=page_id), Q(journal_id=journal_id), join_type="AND")
            .prefetch_related(
                Prefetch(relation="journal", queryset=JournalModel.all().only("id"))
            )
            .first()
        )


class CreatePage:
    @classmethod
    async def add_new_page(
        cls, data: AddPage, journal_id: int, author_id: int
    ) -> PageModel:

        try:

            data_dict = data.dict(exclude_unset=True)

            # TODO exploit saved value for page_num in the record
            latest_page_num = await RetrivePage.get_page_count(
                journal_id=journal_id, author_id=author_id
            )
            new_page = await PageModel.create(
                page_num=latest_page_num + 1,
                journal_id=data_dict.get("journal_id"),
                note=data_dict.get("note"),
            )

        except DoesNotExist:
            raise NotFound(category=PAGE_404)

        except MultipleObjectsReturned:
            raise InternalError()

        return new_page
