from app.api.errors import InternalError
from typing import List

from app.core.log.current_logger import CurrentLogger
from app.crud.story import RetrieveStory
from app.db.models import StoryPieceModel, StoryReward
from tortoise.query_utils import Q


class StoryManager:

    PIECE_SIZE: int = 50

    default_durations = {i * 10 for i in range(1, 10)}
    find_words_per_page = {
        10: 300,
        20: 300,
        30: 250,
        40: 200,
        50: 200,
        60: 150,
        70: 100,
        80: 100,
        90: 100,
    }
    pieces_to_get = lambda words, piece_size: int(words / piece_size)

    piece_boundary_filters = {
        10: {Q(saved_pieces_count__gte=60), Q(saved_pieces_count__lt=150)},
        20: {Q(saved_pieces_count__gte=60), Q(saved_pieces_count__lt=150)},
        30: {Q(saved_pieces_count__gte=150), Q(saved_pieces_count__lt=160)},
        40: {Q(saved_pieces_count__gte=160), Q(saved_pieces_count__lt=200)},
        50: {Q(saved_pieces_count__gte=200)},
        60: {Q(saved_pieces_count__gte=180), Q(saved_pieces_count__lt=200)},
        70: {Q(saved_pieces_count__gte=140), Q(saved_pieces_count__lt=160)},
        80: {Q(saved_pieces_count__gte=160), Q(saved_pieces_count__lt=180)},
        90: {Q(saved_pieces_count__gte=180), Q(saved_pieces_count__lt=200)},
    }

    @classmethod
    def get_story_filter(cls, duration: int):
        filters = cls.piece_boundary_filters.get(duration, None)

        if duration not in cls.default_durations:
            raise Exception(
                f"Invalid Duration {duration}\nValid duration Must be in : {cls.default_durations}"
            )

        if filters is None:
            CurrentLogger.get_logger().error("no filter found for story pieces")
            raise InternalError()

        return filters

    @classmethod
    async def assign_story(cls, duration: int) -> StoryReward:
        filters = cls.get_story_filter(duration=duration)
        story_qset = await RetrieveStory.fetch_random_story(filters=filters)

        return await story_qset


    # assumption : story never runs out of page words
    @classmethod
    def arrange_filter_pieces(cls, page_num: int, duration: int) -> List[Q]:

        if (words := cls.find_words_per_page.get(duration, None)) is None:
            raise Exception(
                f"Invalid duration. Duration must be in {cls.default_durations}"
            )

        challenge_over = False

        if page_num > duration:
            raise Exception(f"Over insert")

        if page_num == duration:
            challenge_over = True

        window = cls.pieces_to_get(words=words, piece_size=50)

        finish_piece_num = page_num * window
        start_piece_num = finish_piece_num - window + 1
        idx_filters = [
            Q(piece_num__gte=start_piece_num),
            Q(piece_num__lte=finish_piece_num),
        ]

        if challenge_over:
            del idx_filters[-1]

        return idx_filters

    @classmethod
    async def merge_pieces(cls, pieces: List[StoryPieceModel]) -> str:

        content_list = [str(p.content) for p in pieces]
        return " ".join(content_list)