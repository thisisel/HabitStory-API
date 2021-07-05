from tortoise.queryset import QuerySetSingle
from app.db.models import UserModel
from app.api.errors import not_found_error, USER_404


class RetriveUser:

    @classmethod
    async def fetch_user_by_id(cls, user_id: int)  -> QuerySetSingle[UserModel]:
       
        if(user := UserModel.get_or_none(id=user_id)) is None:
            raise not_found_error(category=USER_404)
       
        return user