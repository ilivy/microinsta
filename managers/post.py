import os
import random
import shutil
import string
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from constants import UPLOADED_IMAGES_DIR
from models import DbPost, ImageUrlType
from schemas.request.post import PostIn


class PostManager:
    @staticmethod
    def create_post(post: PostIn, user_id: int, db_session: Session):

        if not isinstance(post.image_url_type, ImageUrlType):
            # if post.image_url_type not in image_url_types:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Parameter image_url_type can only take values 'absolute' or 'relative'.",
            )

        new_post = DbPost(
            image_url=post.image_url,
            image_url_type=post.image_url_type,
            caption=post.caption,
            created_at=datetime.utcnow(),
            user_id=user_id,
        )
        db_session.add(new_post)
        db_session.commit()
        db_session.refresh(new_post)
        return new_post

    @staticmethod
    def get_all(db_session: Session):
        return db_session.query(DbPost).all()

    @staticmethod
    def delete_post(db_session: Session, post_id: int, user_id: int):
        post = db_session.query(DbPost).filter(DbPost.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found",
            )
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only post creator can delete the post",
            )

        db_session.delete(post)
        db_session.commit()

        if post.image_url_type == ImageUrlType.relative:
            os.remove(post.image_url)

        return "ok"

    @staticmethod
    def upload_image(image):
        letters = string.ascii_letters
        rand_str = "".join(random.choice(letters) for i in range(6))
        new = f"_{rand_str}."
        filename = new.join(image.filename.rsplit(".", 1))
        path = os.path.join(UPLOADED_IMAGES_DIR, filename)

        with open(path, "w+b") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return {"filename": path}
