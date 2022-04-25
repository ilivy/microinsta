from fastapi import HTTPException

from db import database
from models.comment import db_comment
from models.post import db_post
from schemas.request.comment import CommentIn


class CommentManager:
    @staticmethod
    async def create_comment(comment_data: CommentIn):
        query = db_post.select().where(db_post.c.id == comment_data["post_id"])
        post = await database.fetch_all(query)
        if not post:
            raise HTTPException(404, f"Post with id {comment_data['post_id']} not found")
        id_ = await database.execute(db_comment.insert().values(**comment_data))
        query = db_comment.select().where(db_comment.c.id == id_)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all(post_id: int):
        query = db_comment.select().where(db_comment.c.post_id == post_id)
        return await database.fetch_all(query)
