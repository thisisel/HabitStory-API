from tortoise.queryset import QuerySetSingle
from app.db.models import RewardModel, StoryReward


class RetriveReward:
    @classmethod
    async def fetch_random_reward(
        cls, reward_model: RewardModel = StoryReward
    ) -> QuerySetSingle[RewardModel]:
        return reward_model.first()
