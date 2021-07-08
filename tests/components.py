"""
    common parts needed for tests
"""


from app.main import create_app

from fastapi import APIRouter


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
