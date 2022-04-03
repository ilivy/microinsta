from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db_session
from managers.auth import oauth2_scheme
from managers.comment import CommentManager
from schemas.request.comment import CommentIn
from schemas.response.comment import CommentOut

router = APIRouter(prefix="/comments", tags=["comment"])


@router.post("", dependencies=[Depends(oauth2_scheme)], response_model=CommentOut)
def create(comment_data: CommentIn, db_session: Session = Depends(get_db_session)):
    return CommentManager.create_comment(comment_data, db_session)


@router.get("/all/{post_id}")
def get_all(post_id: int, db_session: Session = Depends(get_db_session)):
    return CommentManager.get_all(post_id, db_session)
