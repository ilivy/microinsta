from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.managers.user import UsersManager
from app.models.schema.users import InUserLoginSchema, InUserRegisterSchema, OutUserSchema

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=OutUserSchema)
async def register(
    payload: InUserRegisterSchema, db: AsyncSession = Depends(get_db)
) -> OutUserSchema:
    return await UsersManager.register(db, payload)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    payload: InUserLoginSchema, db: AsyncSession = Depends(get_db)
):
    access_token, user = await UsersManager.login(db, payload)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }
