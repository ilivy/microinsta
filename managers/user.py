from fastapi import HTTPException
from passlib.context import CryptContext
# from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from managers.auth import AuthManager
from models import DbUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    def register(db_session, user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            new_user = DbUser(**user_data)
            db_session.add(new_user)
            db_session.commit()
            db_session.refresh(new_user)
        # except UniqueViolationError:
        except IntegrityError:
            raise HTTPException(400, "User with this email already exists")
        return new_user

    @staticmethod
    def login(db_session, user_data):
        user_db_obj = (
            db_session.query(DbUser).filter(DbUser.email == user_data["email"]).first()
        )
        if not user_db_obj:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_db_obj.password):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_db_obj), user_db_obj
