from tortoise.queryset import QuerySetSingle
from app.db.models import StoryReward


class RetrieveStory:
    @classmethod
    async def fetch_random_story(cls, filters)->QuerySetSingle[StoryReward]:
        return StoryReward.filter(*filters, join_type="AND").first()