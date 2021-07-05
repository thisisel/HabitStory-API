import pytest

from tests.components import testing_users, login_headers
from app.main import create_app

from fastapi.testclient import TestClient

user_1 = testing_users["user_1"]

@pytest.fixture(scope="module", autouse=True)
def test_sync_app() -> TestClient:

    with TestClient(create_app("testing")) as client:
        yield client  # testing happens here


@pytest.fixture(scope="module")
def test_user_registered(test_sync_app):


    register_response = test_sync_app.post("/auth/register", json=user_1)
    resp_json = register_response.json()

    assert register_response.status_code == 201
    assert resp_json["id"]
    assert resp_json["email"] == user_1["email"] 
    assert resp_json["username"] == user_1["username"]
    assert resp_json["joined_date"]
    assert resp_json["is_active"] == True
    assert resp_json["is_superuser"] == False

    yield 
    


@pytest.fixture(scope="module")
def test_user_logged(test_sync_app, test_user_registered):

    credentials = {
        "username" : user_1["email"],
        "password" : user_1["password"]
    }
    response = test_sync_app.post(
        "/auth/jwt/login", data=credentials, headers=login_headers
    )
    resp_json = response.json()

    assert response.status_code == 200

    access_token = resp_json["access_token"]

    auth_access_headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
    }

    yield auth_access_headers
    #  TODO expire token