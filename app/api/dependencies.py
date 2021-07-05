from typing import Optional
from fastapi.param_functions import Query
from starlette.requests import Request

from tortoise.query_utils import Q
from app.core.security.auth import UsersAuth
from app.core.log.current_logger import CurrentLogger
current_active_user = UsersAuth.get_fastapiusers().current_user(active=True)


async def journals_filters(
    request: Request, title: Optional[str] = Query(None) , active: Optional[bool] = Query(None), min_duration: Optional[int] = Query(None), max_duration: Optional[int] = Query(None)
):

    q_filters = dict(title=Q(challenge__title__icontains=title), active=Q(active=active), duration=Q(duration__range=(min_duration, max_duration)))

    q_filters_pruned = {
        v for k, v in q_filters.items() if request.query_params.get(k) is not None
    }

    CurrentLogger.get_logger().debug(f"PRUNED {q_filters_pruned}")
    return q_filters_pruned
