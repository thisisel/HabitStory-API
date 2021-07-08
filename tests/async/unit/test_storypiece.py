import pytest
from app.db.models import StoryPieceModel, StoryReward


@pytest.mark.asyncio
async def test_insert_story_piece():

    story_obj = await StoryReward.first()
    await StoryPieceModel.create(
        content="piece 1", word_count=len("piece 1"), story_id=story_obj.pk, piece_num=1
    )
    await StoryPieceModel.create(
        content="piece 2", word_count=len("piece 2"), story_id=story_obj.pk, piece_num=2
    )

    await story_obj.refresh_from_db()
    pieces = await story_obj.pieces.all()
    assert len(pieces) == 2
    order = 1
    for p in pieces:
        assert p.story_id == story_obj.pk
        assert p.content
        assert p.piece_num == order
        order +=1
