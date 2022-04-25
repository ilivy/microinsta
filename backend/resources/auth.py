from fastapi import APIRouter

from managers.user import UserManager
from schemas.request.user import UserLoginIn, UserRegisterIn
from schemas.response.user import UserOut


router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201, response_model=UserOut)
async def register(user_data: UserRegisterIn):
    return await UserManager.register(user_data.dict())


@router.post("/login/")
async def login(user_data: UserLoginIn):
    access_token, user = await UserManager.login(user_data.dict())
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }
