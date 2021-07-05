def test_root(test_sync_app):
    
    response = test_sync_app.get("/api/")
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Habit-Story API",
        "status": True,
    }