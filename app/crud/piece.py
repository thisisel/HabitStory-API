from app.db.models import StoryPieceModel
from app.services.story import StoryManager
from tortoise.query_utils import Q


class RetrievePieces:
    @classmethod
    async def fetch_pieces(cls, story_id: int, page_num: int, duration: int):

        idx_filters = StoryManager.arrange_filter_pieces(
            page_num=page_num, duration=duration
        )

        return await StoryPieceModel.filter(Q(story_id=story_id), *idx_filters).all()
