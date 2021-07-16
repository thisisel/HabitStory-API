from typing import Optional, Union
from datetime import datetime
from fastapi_users import models

from pydantic import UUID4, EmailStr, validator
from pydantic.main import BaseModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator


from app.db.models import UserModel
from .common_models import ApiBaseResponse


#  inherited  pydantic base
#   defines optional basic fields and validation
# originally inherited a method that turns the instance into dict, excluding
#  everything that is unset
class User(models.BaseUser, models.BaseOAuthAccountMixin):
    username: Optional[str]
    joined_date: Optional[datetime] = None

    @validator("joined_date", always=True)
    def defult_joindate(cls, v):
        return v or datetime.now()


#   inherited pydantic model for creation
#  compulsory user registration email and password compulsory
class UserCreate(models.BaseUserCreate):
    username: Optional[str]


#  inherited pydantic model for updating
#  user profile update, password is optional
class UserUpdate(User, models.BaseUserUpdate):
    # TODO
    pass


# Pydantic model of a DB representation of a user,
# all attributes of Base User are now concrete
# added hashed password
class UserDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel  # for PydanticModel of tortoise


class PrivateProfileResponse(ApiBaseResponse):
    profile: User


class UserBaseNestedScheme(BaseModel):
    id: UUID4
    email: EmailStr
    username: Optional[str]


User_Pydantic = pydantic_model_creator(UserModel)

