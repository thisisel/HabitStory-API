import asyncio
import os

import pytest
from httpx import AsyncClient
from app.main import create_app
from tortoise.contrib.test import finalizer, initializer
from .utils import seed_rewards_db, seed_users_db
from ..components import login_headers, testing_users


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


test_user_1 = testing_users["user_1"]


@pytest.mark.asyncio
@pytest.fixture(scope="module", params=[test_user_1])
async def register_user(client, request):
    response = await client.post("/auth/register", json=request.param)
    assert response.status_code == 201

    resp_json = response.json()
    assert resp_json["id"]
    assert resp_json["email"] == request.param["email"]
    assert resp_json["username"] == request.param["username"]
    assert "joined_date" in resp_json
    assert resp_json["is_active"] == True
    assert resp_json["is_superuser"] == False

    yield


@pytest.mark.asyncio
@pytest.fixture(
    scope="module",
    params=[{"username": test_user_1["email"], "password": test_user_1["password"]}],
)
async def logged_user_jwt(client, register_user, request):
    response = await client.post(
        "/auth/jwt/login", data=request.param, headers=login_headers
    )

    assert response.status_code == 200

    resp_json = response.json()
    assert "access_token" in resp_json
    access_token = resp_json["access_token"]

    auth_access_headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
    }
    yield auth_access_headers
