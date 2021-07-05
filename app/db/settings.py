import os

basedir = os.path.abspath(os.path.dirname(__file__))

tortoise_orm = {
    "connections": {
        "production": "postgres://elahe:397397@localhost:5432/habit_tracker",
        "development": "sqlite:///" + os.path.join(basedir, "dev.sqlite"),
        },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "development",
        },
    },
}