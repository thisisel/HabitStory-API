from tortoise.query_utils import Prefetch
from app.db.models import JournalModel, ChallengeModel

#TODO assign reward based on challenge duration and story word count
async def assign_reward():
    pass


async def get_story_piece(journal_id: int, page_num: int):
    
    # fetch_journal_with_relations
    journal = (
        await JournalModel.filter(id=journal_id)
        .prefetch_related(
            Prefetch(
                relation="challenge",
                queryset=ChallengeModel.all().only("id", "duration"),
            ),
            Prefetch(
                relation="reward"
            )
        )
        .only("id", "challenge_id", "reward_id").first()
    )

    duration = journal.challenge.duration
    story_length = journal.reward.word_count
    piece_size = story_length / duration
    start_idx = (page_num-1)*piece_size
    
