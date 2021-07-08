import uuid
from typing import List

from app.db.models import (
    ChallengeModel,
    JournalModel,
    PageModel,
    RewardModel,
    StoryReward,
    UserModel,
)
from fastapi_users.password import get_password_hash


def seed_users_db() -> List[UserModel]:

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

    return [user_1, user_2, user_3]


def seed_rewards_db() -> StoryReward:
    story = StoryReward(
        author="test author",
        title="test title",
        tag="story",
        word_count=31,
    )
    return story
