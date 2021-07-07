import pytest
from app.db.models import UserModel

@pytest.mark.asyncio
async def test_get_user(): 
    user_obj = await UserModel.get(email="albus_dumbeldore@hogwarts.wiz")
    
    assert user_obj.email =="albus_dumbeldore@hogwarts.wiz"