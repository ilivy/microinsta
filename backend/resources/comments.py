from fastapi import APIRouter, Depends

from managers.auth import oauth2_scheme
from managers.comment import CommentManager
from schemas.request.comment import CommentIn
from schemas.response.comment import CommentOut

router = APIRouter(prefix="/comments", tags=["comment"])


@router.post("/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=CommentOut)
async def create(comment_data: CommentIn):
    return await CommentManager.create_comment(comment_data.dict())


@router.get("/all/{post_id}")
async def get_all(post_id: int):
    return await CommentManager.get_all(post_id)
