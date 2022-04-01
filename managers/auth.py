from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.requests import Request

from db import get_db_session
from models import DbUser


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user.id,
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
        except Exception as ex:
            # TODO: write exception into logs
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request, db_session: Session = Depends(get_db_session)
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, config("JWT_SECRET"), algorithms=["HS256"]
            )
            user_data = (
                db_session.query(DbUser).filter(DbUser.id == payload["sub"]).first()
            )
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Token is not valid")


oauth2_scheme = CustomHTTPBearer()
