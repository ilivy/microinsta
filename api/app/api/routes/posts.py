from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.db.repositories.posts import PostsRepository
from app.managers.auth import AuthManager, oauth2_scheme
from app.managers.post import PostsManager
from app.models.schema.posts import InPostSchema, OutPostSchema, PostSchema
from app.models.schema.users import OutUserSchema

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/image",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)]
)
async def upload_image(image: UploadFile = File(...)):
    return await PostsManager.upload_image(image)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=PostSchema
)
async def create(
    payload: InPostSchema,
    db: AsyncSession = Depends(get_db),
    current_user: OutUserSchema = Depends(AuthManager.get_current_user)
) -> PostSchema:
    payload.user_id = current_user.id
    posts_repo = PostsRepository(db)
    post = await posts_repo.create(payload)
    return PostSchema(**post.dict())


@router.delete(
    "/delete/{post_id}", status_code=status.HTTP_200_OK
)
async def delete(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: OutUserSchema = Depends(AuthManager.get_current_user)
):
    return await PostsManager.delete_post(db, post_id, current_user.id)


@router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=List[OutPostSchema]
)
async def get_all(
    db: AsyncSession = Depends(get_db)
) -> List[OutPostSchema]:
    posts_repo = PostsRepository(db)
    return await posts_repo.get_all()
