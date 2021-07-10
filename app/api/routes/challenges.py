from app.schemas import challenge
from app.schemas.challenge import (
    ChallengeBase_Pydantic,
    ChallengeDetail,
    ChallengeInList,
    SingleChallengeResponse,
)
from app.crud.challenge import RetrieveChallenge
from app.api.errors import NotFound, CHALLENGE_404
from fastapi import APIRouter, Path
from fastapi_pagination.default import Page, Params

router = APIRouter()


@router.get("")
async def get_trending_challenges():
    challenges_qset = await RetrieveChallenge.fetch_trending_challenges()
    # return await challenges_qset
    challenges_obj = await challenges_qset
    # return await ChallengeBase_Pydantic.from_queryset(challenges_qset)
    return await ChallengeInList.from_queryset(challenges_qset)


@router.get("/{id}")
async def get_single_challenge(id: int = Path(...)):
    challenge_qset = await RetrieveChallenge.fetch_single_challenge(id=id)

    if (challenge_obj := await challenge_qset) is None:
        raise NotFound(category=CHALLENGE_404)
    # return await ChallengeDetail.from_tortoise_orm(challenge_obj)
    return SingleChallengeResponse(
        status=True,
        message="challenge sent succ",
        challenge=await ChallengeDetail.from_tortoise_orm(challenge_obj),
    )
