from app.schemas.challenge import (
    ChallengeDetail,
    ChallengeInList,
    SingleChallengeResponse,
)
from app.crud.challenge import RetrieveChallenge
from app.api.errors import NotFound, CHALLENGE_404
from fastapi import APIRouter, Path, Depends
from fastapi_pagination import paginate, Page, Params

router = APIRouter()


@router.get("", response_model=Page[ChallengeInList])
async def get_trending_challenges(params: Params = Depends()):

    challenges_qset = await RetrieveChallenge.fetch_trending_challenges()

    return paginate(await ChallengeInList.from_queryset(challenges_qset), params=params)


@router.get("/{id}")
async def get_single_challenge(id: int = Path(...)):

    challenge_qset = await RetrieveChallenge.fetch_single_challenge(id=id)

    if (challenge_obj := await challenge_qset) is None:
        raise NotFound(category=CHALLENGE_404)

    return SingleChallengeResponse(
        status=True,
        message="Challenge was sent successfully",
        challenge=await ChallengeDetail.from_tortoise_orm(challenge_obj),
    )
