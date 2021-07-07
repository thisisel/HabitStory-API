import asyncio
import os

import pytest
from httpx import AsyncClient
from app.main import create_app
from tortoise.contrib.test import finalizer, initializer
from .utils import seed_rewards_db, seed_users_db

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def tortoise_initialize_tests(request):
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["app.db.models"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)

@pytest.fixture(scope="module", autouse=True)
async def seed_db():
    users = seed_users_db()
    for u in users:
        await u.save()

    story = seed_rewards_db()
    await story.save()


@pytest.mark.asyncio
@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=create_app("testing"), base_url="http://test") as ac:
        yield ac
