from typing import Optional, Set

from app.core.log.current_logger import CurrentLogger
from fastapi import Query, Request
from tortoise.query_utils import Q


class PersonalJournalFilters:
    def __init__(
        self,
        request: Request,
        duration_gte: Optional[int] = Query(None),
        duration_lte: Optional[int] = Query(None),
        title: Optional[str] = Query(None),
        active: Optional[bool] = Query(None),
        is_public: Optional[bool] = Query(None),
    ):
        self._q_filters = dict(
            title=Q(challenge__title__icontains=title),
            duration_gte=Q(borrow_interval__gte=duration_gte),
            duration_lte=Q(borrow_interval__lte=duration_lte),
            active=Q(active=active),
            is_public=Q(is_public=is_public)
        )

        self.q_filters_pruned: Set[Q] = {
            q_object
            for param, q_object in self._q_filters.items()
            if request.query_params.get(param) is not None
        }

        CurrentLogger.get_logger().debug(self.q_filters_pruned)


class PublicJournalFilters(PersonalJournalFilters):
    def __init__(
        self,
        request: Request,
        duration_gte: Optional[int] = Query(None),
        duration_lte: Optional[int] = Query(None),
        title: Optional[str] = Query(None),
    ):
        super().__init__(
            request,
            duration_gte=duration_gte,
            duration_lte=duration_lte,
            title=title,
            active=True,
            is_public=True
        )

class PageFilters:
    def __init__(
        self,
        request: Request,
        page_num: Optional[int] = Query(None),
        submitted_year: Optional[int] = Query(None),
        submitted_month: Optional[int] = Query(None),
        submitted_day: Optional[int] = Query(None),
    ):
        self._q_filters = dict(
        page_num=Q(page_num=page_num),
        submitted_year=Q(submitted__year=submitted_year),
        submitted_month=Q(submitted__month=submitted_month),
        submitted_day=Q(submitted__day=submitted_day),
        )
        self.q_filters_pruned: Set[Q] = {
            q_object
            for param, q_object in self._q_filters.items()
            if request.query_params.get(param) is not None
        }

