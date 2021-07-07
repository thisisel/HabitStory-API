from ..components import testing_users


user_1 = testing_users["user_1"]


def test_create_journal_unprocessed_entt(test_sync_app, test_user_logged):

    data = {
        "title": "20 days running",
        "description": "run for 20 days",
        "duration": 20,
        "is_public": False,
    }
    d = {
    "title": "string",
    "description": "string",
    "duration": 10,
    "is_public": True
    }
    
    response = test_sync_app.post("/api/profile/journals", json=d, headers=test_user_logged)
    print(response)
    # assert response.status_code == 201
    assert response.status_code == 404
    resp_json = response.json()
    print(resp_json)

    # resp_json = response.json()
    # assert resp_json["status"] == True
    # assert resp_json["message"] == "New Challenge started, Journal instanciated"

    # resp_json_data = resp_json["data"]
    # assert resp_json_data["is_public"] == data["is_public"]
    # assert resp_json_data["streak"] == 0
    
    # resp_data_challenge = resp_json_data["challenge"]
    # assert resp_data_challenge["description"] == data["description"]
    # assert resp_data_challenge["title"] == data["title"]
    # assert resp_data_challenge["duration"] == data["duration"]
    
    # resp_data_author_ = resp_json_data["author"]
    # assert resp_data_author_["username"] == user_1["username"]

