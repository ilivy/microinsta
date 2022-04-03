from typing import List

from pydantic.schema import datetime

from schemas.base import BasePost
from schemas.response.comment import CommentOut
from schemas.response.user import UserOut


class PostOut(BasePost):
    id: int
    created_at = datetime
    user: UserOut
    comments: List[CommentOut]

    class Config:
        orm_mode = True
