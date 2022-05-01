from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.db.errors import DoesNotExist
from app.db.repositories.users import UsersRepository
from app.managers.auth import AuthManager
from app.models.schema.users import OutUserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersManager:
    @staticmethod
    async def register(db, user_data):
        users_repo = UsersRepository(db)
        user_data.password = pwd_context.hash(user_data.password)
        try:
            user = await users_repo.create(user_data)
        except IntegrityError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User with this email already exists")
        return OutUserSchema(**user.dict())

    @staticmethod
    async def login(db, user_data):
        try:
            users_repo = UsersRepository(db)
            user_db_obj = await users_repo.get_by_email(user_data.email)
        except DoesNotExist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Wrong email or password")

        if not pwd_context.verify(user_data.password, user_db_obj.password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Wrong email or password")
        return AuthManager.encode_token(user_db_obj), user_db_obj
