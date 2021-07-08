from ...components import login_headers, testing_users


user_1 = testing_users["user_1"]

def test_valid_register(test_sync_app):

    data = {
        "email": "merlyn_beard@camelot.bt",
        "username": "mr_wizard",
        "password": "abracadabra",
    }

    response = test_sync_app.post("/auth/register", json=data)
    resp_json = response.json()

    assert response.status_code == 201
    assert resp_json["id"]
    assert resp_json["email"] == "merlyn_beard@camelot.bt"
    assert resp_json["username"] == "mr_wizard"
    assert resp_json["joined_date"]
    assert resp_json["is_active"] == True
    assert resp_json["is_superuser"] == False


def test_valid_login(test_sync_app, test_user_registered):
    

    data = {
        "username": user_1["email"],
        "password": user_1["password"],
    }

    response = test_sync_app.post("/auth/jwt/login", data=data, headers=login_headers)
    resp_json = response.json()

    assert response.status_code == 200
    assert resp_json["access_token"]
    assert resp_json["token_type"] == "bearer"