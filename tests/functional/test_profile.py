from ..components import testing_users


user_1 = testing_users["user_1"]

def test_valid_user_profile_info(test_sync_app, test_user_logged):
    

    response = test_sync_app.get("/api/profile", headers=test_user_logged)
    
    assert response.status_code == 200
    
    resp_json = response.json()
    assert resp_json["status"] == True
    assert resp_json["message"] == "User private profile retrived"

    resp_json_profile = resp_json["profile"]
    assert resp_json_profile["id"]
    assert resp_json_profile["email"] == user_1["email"]
    assert resp_json_profile["username"] == user_1["username"]