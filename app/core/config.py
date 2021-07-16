import os
import logging
logger = logging.getLogger(__name__)

from pydantic import BaseSettings
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# base settings
PROJECT_NAME: str = "Habit Story API"
VERSION: str = "0.0.1"
API_PREFIX = "/api"

config = Config(".env")

FASTAPI_ENV: str = config("FASTAPI_ENV")

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default=os.urandom(24))

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

GOOGLE_CLIENT_ID: str = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: str = config("GOOGLE_CLIENT_SECRET")


class DevelopmentSettings(BaseSettings):

    debug: bool = True
    logging_level: str = "debug"

    from ..db.settings import basedir
    db_uri: str = config(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(basedir, "dev.sqlite"),
    )
    min_connection_count: int = 10
    max_connection_count: int = 10

    class Config:
        env_file = ".env"


class TestingSettings(BaseSettings):

    debug: bool = True

    db_uri: str = config("TEST_DATABASE_URL", default="sqlite://:memory:")
    min_connection_count: int = 10
    max_connection_count: int = 10

    class Config:
        env_file = ".env"


class ProductionSettings(BaseSettings):

    debug: bool = False
    try:

        db_uri: str = "{}://{}:{}@{}:{}/{}".format(
            os.environ["DB_ENGINE"],
            os.environ["DB_USERNAME"],
            os.environ["DB_PASS"],
            os.environ["DB_HOST"],
            os.environ["DB_PORT"],
            os.environ["DB_NAME"],
        )

    except KeyError:

        print(f"could not resolve database uri parameter(s) for postgres")

    min_connection_count: int = 10
    max_connection_count: int = 10

    class Config:
        env_file = ".env"


setting_by_name = dict(
    development=DevelopmentSettings(),
    testing=TestingSettings(),
    production=ProductionSettings(),
    default=DevelopmentSettings(),
)
