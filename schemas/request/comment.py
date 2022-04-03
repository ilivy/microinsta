from schemas.base import BaseComment


class CommentIn(BaseComment):
    post_id: int
