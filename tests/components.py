"""
    common parts needed for tests
"""


import uuid
from typing import List

from tortoise.backends.base.client import BaseDBAsyncClient

from app.db.models import UserModel, JournalModel, ChallengeModel, StoryReward, PageModel
from app.main import create_app

from fastapi import APIRouter
from fastapi_users.password import get_password_hash


def get_testing_app():

    testing_app = create_app("testing")
    testing_router = APIRouter(prefix="/test")
    testing_app.include_router(testing_router)

    return testing_app


app = get_testing_app()


def get_logger():

    import sys

    from loguru import logger

    logger.remove()
    logger.add(
        sink=sys.stdout,
        colorize=True,
        diagnose=True,
        format="<blue>[LOGURU]</blue> <yellow>{level}</yellow> CALL IN {module} @ {function} ---> {message} ",
    )
    return logger.bind(request_id=None, method=None)


logger = get_logger()

DB_TEST_URI = "sqlite://:memory:"

testing_users = {
    "user_1": {
        "email": "hermione.granger@hogwarts.wiz",
        "username": "studios_witch",
        "password": "hogwartslib",
    },
    "user_2": {
        "email": "luna.lovegood@hogwarts.wiz",
        "username": "nargol_princess",
        "password": "secretunicorn",
    },
}

login_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "accept": "application/json",
}


def get_users() -> List[UserModel]:

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
