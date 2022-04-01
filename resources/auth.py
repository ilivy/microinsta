from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from db import get_db_session
from managers.auth import oauth2_scheme
from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserLoginIn
from schemas.response.user import UserOut

router = APIRouter(tags=["auth"])


@router.post("/register/", status_code=201, response_model=UserOut)
def register(user_data: UserRegisterIn, db_session: Session = Depends(get_db_session)):
    return UserManager.register(db_session, user_data.dict())


@router.post("/login/")
def login(user_data: UserLoginIn, db_session: Session = Depends(get_db_session)):
    access_token, user = UserManager.login(db_session, user_data.dict())
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }


@router.get("/", dependencies=[Depends(oauth2_scheme)])
def hello():
    return "Hello world!"
