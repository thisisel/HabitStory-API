from app.db.models import ChallengeModel
from app.schemas.challenge import CreateNewChallenge


class CreateChallenge:
    @classmethod
    async def create_challenge(
        cls, user_id: int, data: CreateNewChallenge
    ) -> ChallengeModel:
        return await ChallengeModel.create(
            **data.dict(exclude_unset=True),
            created_by_id=user_id,
        )
