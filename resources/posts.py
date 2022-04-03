from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from db import get_db_session
from managers.auth import oauth2_scheme
from managers.post import PostManager
from schemas.request.post import PostIn
from schemas.response.post import PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", dependencies=[Depends(oauth2_scheme)], response_model=PostOut)
def create(
    post_data: PostIn, request: Request, db_session: Session = Depends(get_db_session)
):
    user = request.state.user
    return PostManager.create_post(post_data, user.id, db_session)


@router.post("/image", dependencies=[Depends(oauth2_scheme)])
def upload_image(image: UploadFile = File(...)):
    return PostManager.upload_image(image)


@router.get("/all", response_model=List[PostOut])
def posts(db_session: Session = Depends(get_db_session)):
    return PostManager.get_all(db_session)


@router.delete("/delete/{post_id}", dependencies=[Depends(oauth2_scheme)])
def delete(
    post_id: int, request: Request, db_session: Session = Depends(get_db_session)
):
    user = request.state.user
    return PostManager.delete_post(db_session, post_id, user.id)
