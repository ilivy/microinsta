from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from db import database
from models.user import db_user
from utils import logger


class AuthManager:
    @staticmethod
    def encode_token(db_user):
        try:
            payload = {
                "sub": db_user.id,
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
        except Exception as ex:
            logger.write_log("auth", str(ex))
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, config("JWT_SECRET"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                db_user.select().where(db_user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Token is not valid")


oauth2_scheme = CustomHTTPBearer()
