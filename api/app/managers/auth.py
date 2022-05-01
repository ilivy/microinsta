from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.core.config import settings
# from utils import logger
from app.db.repositories.users import UsersRepository

oauth2_scheme = HTTPBearer()


class AuthManager:
    @staticmethod
    def encode_token(db_user):
        try:
            payload = {
                "sub": db_user.email,
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        except Exception as ex:
            # logger.write_log("auth", str(ex))
            raise ex

    @staticmethod
    async def get_current_user(
            http_cred: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
            db: AsyncSession = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                http_cred.credentials, settings.JWT_SECRET, algorithms=["HS256"]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            credentials_exception.detail = "Token is expired"
            raise credentials_exception
        except jwt.InvalidTokenError:
            raise credentials_exception

        users_repo = UsersRepository(db)
        user_db_obj = await users_repo.get_by_email(email)
        if user_db_obj is None:
            raise credentials_exception

        return user_db_obj
