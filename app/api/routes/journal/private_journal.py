from app.api.errors import NotFound, JOURNAL_404
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from app.crud.journal import CreateJournal, DeleteJournal, RetriveJournal, UpdateJournal
from app.crud.challenge import CreateChallenge

from app.api.routes import page
from app.schemas import challenge
from app.schemas.common_models import ApiErrorResponse
from app.schemas.journal import (
    NewJournalCreatedResponse,
    NewJournalModel_Pydantic,
    PrivateJournal_Pydantic,
    PrivateJournalResponse,
    UpdateJournal_Pydantic,
)
from app.schemas.challenge import CreateNewChallenge
from app.schemas.user import UserDB
from fastapi import Body, Depends, Path, Response
from fastapi.routing import APIRouter
from fastapi_pagination.default import Page, Params
from fastapi_pagination.paginator import paginate

from app.core.log.current_logger import CurrentLogger
from ..dependencies import current_active_user, PersonalJournalFilters

router = APIRouter()
router.include_router(page.router, tags=["page"])


# TODO show chears and remaining days
# TODO replace q func dep with q class dep
@router.get(
    "",
    responses={
        200: {"model": Page[PrivateJournal_Pydantic]},
    },
    tags=["journal"],
)
async def retrive_personal_journals(
    # q_filters=Depends(journals_filters),
    q_filters: PersonalJournalFilters = Depends(),
    user: UserDB = Depends(current_active_user),
    params: Params = Depends(),
):
    journals_qset = await RetriveJournal.fetch_user_journals(
        user_id=user.id, q_filters=q_filters.q_filters_pruned
    )

    return paginate(await PrivateJournal_Pydantic.from_queryset(journals_qset), params)


# TODO transaction
@router.post(
    "",
    status_code=201,
    response_description="New Challenge started, Journal instanciated",
    responses={201: {"model": NewJournalCreatedResponse}},
    tags=["journal"],
)
async def create_journal(
    body: CreateNewChallenge = Body(...), user: UserDB = Depends(current_active_user)
):
    # TODO prevent more than 3 ongoing challenges

    new_challenge_obj = await CreateChallenge.create_challenge(
        user_id=user.id, data=body
    )
    CurrentLogger.get_logger().debug(f"Challenge {new_challenge_obj} created")
    new_journal_obj = await CreateJournal.create_journal(
        user_id=new_challenge_obj.created_by_id,
        challenge_id=new_challenge_obj.id,
        challenge_duration=new_challenge_obj.duration,
        is_public=body.dict().get("is_public", False),
    )

    content = PrivateJournalResponse(
        status=True,
        message="New Challenge started, Journal instanciated",
        data=await NewJournalModel_Pydantic.from_tortoise_orm(new_journal_obj),
    )
    return JSONResponse(status_code=201, content=jsonable_encoder(content))


# TODO show chears and remaining days
@router.get(
    "/{id}",
    responses={
        200: {"model": PrivateJournalResponse},
        404: {"model": ApiErrorResponse},
    },
    tags=["journal"],
)
async def retrive_single_journal(
    id: int = Path(..., description="journal id"),
    user: UserDB = Depends(current_active_user),
):

    journal_qset = await RetriveJournal.fetch_single_journal(
        user_id=user.id, journal_id=id
    )
    if not (journal := await journal_qset):
        raise NotFound(category=JOURNAL_404)


    content = PrivateJournalResponse(
        status=True,
        message="Journal successfully retrived",
        data=await PrivateJournal_Pydantic.from_tortoise_orm(journal),
    )
    
    return JSONResponse(status_code=200, content=jsonable_encoder(content))



@router.delete(
    "/{id}",
    status_code=204,
    response_description="Journal deleted",
    tags=["journal"],
)
async def remove_journal(
    id: int = Path(..., description="journal id"),
    user: UserDB = Depends(current_active_user),
):
    await DeleteJournal.delete_journal(journal_id=id, user_id=user.id)
    return Response(status_code=204)


@router.patch("/{id}", 
responses={
    200: {"model" : PrivateJournalResponse}, 
    404: {"model" : ApiErrorResponse}
},
tags=["journal"])
async def update_journal(
    id: int = Path(...),
    user: UserDB = Depends(current_active_user),
    data: UpdateJournal_Pydantic = Body(...),
):
    journal_qset = await RetriveJournal.fetch_single_journal(
        user_id=user.id, journal_id=id
    )

    if (journal_obj := await journal_qset) is None:
        raise NotFound(JOURNAL_404)

    return PrivateJournalResponse(
        status=True,
        message="Journal updated successfully",
        data=await PrivateJournal_Pydantic.from_tortoise_orm(
            await UpdateJournal.update_journal(journal_obj=journal_obj, data=data)
        )
    )
