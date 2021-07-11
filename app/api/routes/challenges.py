from app.schemas.challenge import (
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
    challenges_obj = await challenges_qset
   
    return await ChallengeInList.from_queryset(challenges_qset)


@router.get("/{id}")
async def get_single_challenge(id: int = Path(...)):
    
    challenge_qset = await RetrieveChallenge.fetch_single_challenge(id=id)

    if (challenge_obj := await challenge_qset) is None:
        raise NotFound(category=CHALLENGE_404)

    return SingleChallengeResponse(
        status=True,
        message="challenge sent succ",
        challenge=await ChallengeDetail.from_tortoise_orm(challenge_obj),
    )
