from app.schemas.user import UserDB
from app.api.routes.dependencies import optional_current_active_user
from app.crud.journal import CreateJournal
from app.schemas.journal import NewJournalCreatedResponse, NewJournalModel_Pydantic, PrivateJournalResponse
from app.schemas.common_models import ApiErrorResponse
from app.schemas.challenge import (
    ChallengeDetail,
    ChallengeInList,
    SingleChallengeResponse,
)
from app.crud.challenge import RetrieveChallenge
from app.api.errors import NotFound, CHALLENGE_404, UnAuthorized
from fastapi import APIRouter, Path, Depends, Body
from fastapi_pagination import paginate, Page, Params
from .dependencies import ChallengeFilters

router = APIRouter()


@router.get("", response_model=Page[ChallengeInList])
async def get_trending_challenges(
    params: Params = Depends(), q_filters: ChallengeFilters = Depends()
):

    challenges_qset = await RetrieveChallenge.fetch_trending_challenges(
        q_filters=q_filters.q_filters_pruned
    )

    return paginate(await ChallengeInList.from_queryset(challenges_qset), params=params)


@router.get("/{id}", 
    responses={
        200: {"model": SingleChallengeResponse},
        404: {"model": ApiErrorResponse},
    },     
    
)
async def get_single_challenge(id: int = Path(...)):

    challenge_qset = await RetrieveChallenge.fetch_single_challenge(id=id)

    if (challenge_obj := await challenge_qset) is None:
        raise NotFound(category=CHALLENGE_404)

    return SingleChallengeResponse(
        status=True,
        message="Challenge was sent successfully",
        challenge=await ChallengeDetail.from_tortoise_orm(challenge_obj),
    )

#TODO clone challenge POST 
@router.post(
    "/{id}",
    status_code=201,
    response_description="New Challenge started, Journal instanciated",
    responses={201: {"model": NewJournalCreatedResponse}},
)
async def clone_challenge(id: int =Path(...),is_public: bool = Body(False, title="is_public", description="journal is public/private"),user: UserDB = Depends(optional_current_active_user)):
    
    if user:
       
        if not (await RetrieveChallenge.challenge_exists(challenge_id=id)):
            raise NotFound(category=CHALLENGE_404)

        new_journal_obj = await CreateJournal.create_journal(
            user_id=user.id,
            challenge_id=id,
            is_public=is_public,
        )
        return PrivateJournalResponse(
        status=True,
        message="New Challenge started, Journal instanciated",
        data=await NewJournalModel_Pydantic.from_tortoise_orm(new_journal_obj),
        )
    
    raise UnAuthorized(message="Only registered users are authorized to clone a challenge")