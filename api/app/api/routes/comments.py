from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.managers.auth import AuthManager, oauth2_scheme
from app.managers.comments import CommentsManager
from app.models.schema.comments import InCommentSchema, OutCommentSchema
from app.models.schema.users import OutUserSchema

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=OutCommentSchema
)
async def create(
    payload: InCommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: OutUserSchema = Depends(AuthManager.get_current_user)
) -> OutCommentSchema:
    return await CommentsManager.create_comment(db, payload, current_user.username)


@router.get(
    "/all/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=List
)
async def get_by_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
) -> List:
    return await CommentsManager.get_by_post(db, post_id)
