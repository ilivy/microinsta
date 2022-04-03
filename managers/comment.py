from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from models import DbComment, DbPost
from schemas.request.comment import CommentIn


class CommentManager:
    @staticmethod
    def create_comment(comment: CommentIn, db_session: Session):
        post = db_session.query(DbPost).filter(DbPost.id == comment.post_id).first()
        if not post:
            raise HTTPException(404, f"Post with id {comment.post_id} not found")
        new_comment = DbComment(
            text=comment.text,
            username=comment.username,
            post_id=comment.post_id,
            created_at=datetime.utcnow(),
        )
        db_session.add(new_comment)
        db_session.commit()
        db_session.refresh(new_comment)
        return new_comment

    @staticmethod
    def get_all(post_id: int, db_session: Session):
        return db_session.query(DbComment).filter(DbComment.post_id == post_id).all()
