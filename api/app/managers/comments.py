from typing import List

from fastapi import HTTPException
from starlette import status

from app.db.errors import DoesNotExist
from app.db.repositories.comments import CommentsRepository
from app.db.repositories.posts import PostsRepository
from app.models.schema.comments import OutCommentSchema


class CommentsManager:
    @staticmethod
    async def create_comment(db, comment_data, username):
        posts_repo = PostsRepository(db)
        try:
            post = await posts_repo.get_by_id(comment_data.post_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {comment_data['post_id']} not found",
            )
        comment_data.username = username
        comments_repo = CommentsRepository(db)
        comment = await comments_repo.create(comment_data)
        return OutCommentSchema(**comment.dict())

    @staticmethod
    async def get_by_post(db, post_id) -> List:
        posts_repo = PostsRepository(db)
        try:
            post = await posts_repo.get_by_id(post_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        comments_repo = CommentsRepository(db)
        comments = await comments_repo.get_by_post(post_id)
        return comments
