import pytest
from ..utils import JournalModel
from ...components import new_journal_data
@pytest.mark.asyncio
async def test_create_journal(client, logged_user_jwt):

    response = await client.post("/api/profile/journals", json=new_journal_data, headers=logged_user_jwt)

    assert response.status_code == 201, response.text

    resp_json = response.json()
    data = resp_json["data"]
    id = data["id"]
    new_journal_obj = await JournalModel.get(id=id).prefetch_related("challenge")
    new_challenge_obj = new_journal_obj.challenge

    assert id == new_journal_obj.id
    assert new_journal_data["is_public"] == new_journal_obj.is_public
    assert new_challenge_obj.title == new_journal_data["title"]
    assert new_challenge_obj.description == new_journal_data["description"]
    assert new_challenge_obj.duration == new_journal_data["duration"]


