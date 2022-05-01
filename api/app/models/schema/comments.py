from datetime import datetime

from app.models.schema.base import BaseSchema


class CommentSchemaBase(BaseSchema):
    username: str
    text: str


class InCommentSchema(CommentSchemaBase):
    post_id: int


class CommentSchema(CommentSchemaBase):
    created_at: datetime


class OutCommentSchema(CommentSchema):
    pass
