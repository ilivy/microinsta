from pydantic.schema import datetime

from schemas.base import BaseComment


class CommentOut(BaseComment):
    created_at: datetime

    class Config:
        orm_mode = True
