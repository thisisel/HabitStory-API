from fastapi_users.authentication import (CookieAuthentication,
                                          JWTAuthentication)
from fastapi_users.db.tortoise import TortoiseUserDatabase
from fastapi_users.fastapi_users import FastAPIUsers

from ..config import SECRET_KEY
from . import User, UserCreate, UserDB, UserModel, UserUpdate, OAuthAccountModel


class UsersAuth:
    user_db = TortoiseUserDatabase(UserDB, UserModel, OAuthAccountModel)
    jwt_authentication = JWTAuthentication(
        secret=str(SECRET_KEY), lifetime_seconds=3600, tokenUrl="auth/jwt/login"
    )
    cookie_authentication = CookieAuthentication(
        secret=str(SECRET_KEY), lifetime_seconds=3600, cookie_path="/auth/cookie"
    )

    @classmethod
    def get_fastapiusers(cls):
        return FastAPIUsers(
            db=cls.user_db,
            auth_backends=[cls.jwt_authentication, cls.cookie_authentication],
            user_model=User,
            user_create_model=UserCreate,
            user_update_model=UserUpdate,
            user_db_model=UserDB,
        )