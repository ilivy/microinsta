from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from managers.auth import AuthManager
from models.user import db_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(db_user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        return {**user_data, "id": id_}

    @staticmethod
    async def login(user_data):
        user_db_obj = await database.fetch_one(
            db_user.select().where(db_user.c.email == user_data["email"])
        )
        if not user_db_obj:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_db_obj.password):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_db_obj), user_db_obj
