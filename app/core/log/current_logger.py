from loguru import logger


def get_logger() -> logger:
    from app.main import app
    return app.logger


class CurrentLogger:

    _cached_app_logger: logger

    @classmethod
    def set_logger(cls, logger: logger) -> None:
        cls._cached_app_logger = logger

    @classmethod
    def get_logger(cls) -> logger:
        if cls._cached_app_logger is None:
            raise AttributeError()
        return cls._cached_app_logger

