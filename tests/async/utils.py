import uuid
from typing import Dict, List

from app.db.models import (
    ChallengeModel,
    JournalModel,
    PageModel,
    RewardModel,
    StoryReward,
    UserModel,
)
from fastapi_users.password import get_password_hash


def seed_users_db() -> Dict[str, UserModel]:

    user_1 = UserModel(
        id=uuid.uuid4(),
        email="harry.potter@hogwarts.wiz",
        hashed_password=get_password_hash("expectopatronum"),
        username="boy_who_lived",
    )
    user_2 = UserModel(
        id=uuid.uuid4(),
        email="ron.weasley@hogwarts.wiz",
        hashed_password=get_password_hash("vickycram"),
        username="the_king",
    )
    user_3 = UserModel(
        id=uuid.uuid4(),
        email="albus_dumbeldore@hogwarts.wiz",
        hashed_password=get_password_hash("mambojambo"),
        username="golden_phoenix",
    )

    return dict(
        user_1=user_1,
        user_2=user_2,
        user_3=user_3
    )


def seed_rewards_db() -> Dict[str, StoryReward]:
    story_1 = StoryReward(
        author="test author",
        title="test title",
        tag="story",
        word_count=31,
    )
    return dict(story_1=story_1)

def seed_challenges_db():

    users = seed_users_db()
    challenge_1 = ChallengeModel(
        title="Challenge 1",
        description="description for challenge 1",
        duration=20,
    )
    return dict(challenge_1=challenge_1)