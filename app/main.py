from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.api.errors import (
    InternalError,
    NotFound,
    http422_error_handler,
    http_error_handler,
    internal_error_handler,
    notfound_error_handler,
    forbidden_error_handler,
    Forbidden,
    notallowed_error_handler,
    NotAllowed,
    UnAuthorized,
    unauthorized_error_handler,
)
from app.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    FASTAPI_ENV,
    PROJECT_NAME,
    VERSION,
    setting_by_name,
    logger,
)
from app.core.log.costum_logging import CustomizeLogger


def create_app(setting_mode: str) -> FastAPI:

    app_setting = setting_by_name[setting_mode]

    app = FastAPI(title=PROJECT_NAME, debug=app_setting.debug, version=VERSION)

    _init_logger(app, logger=logger, debug=app_setting.debug)
    _add_middleware(app)
    _init_tortoise(app, db_uri=app_setting.db_uri)
    _add_exception_handler(app)
    _include_routes(app)

    app.add_api_route("/", _get_index(app_setting.debug), tags=["index"])

    return app


def _add_middleware(app: FastAPI) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _init_tortoise(app: FastAPI, db_uri: str) -> None:

    Tortoise.init_models(["app.db.models"], "models")
    register_tortoise(
        app,
        db_url=db_uri,
        modules={"models": ["app.db.models", "aerich.models"]},
        generate_schemas=True,
    )


def _get_index(debug: bool):
    def index():
        return RedirectResponse("/docs")

    return index if debug else 204


def _init_logger(app: FastAPI, logger, debug: bool = False):
    from app.core.log.current_logger import CurrentLogger

    logger = CustomizeLogger.make_logger(debug)
    app.logger = logger
    CurrentLogger.set_logger(logger=app.logger)

    app.logger.info(f"APP LOGGER CONFIGURED AS {debug}")


def _add_exception_handler(app: FastAPI):

    app.add_exception_handler(NotFound, notfound_error_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(InternalError, internal_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(Forbidden, forbidden_error_handler)
    app.add_exception_handler(NotAllowed, notallowed_error_handler)
    app.add_exception_handler(UnAuthorized, unauthorized_error_handler)


def _include_routes(app: FastAPI):
    from app.api.routes import auth, api

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(api.router, prefix=API_PREFIX)


app = create_app(FASTAPI_ENV)
