import datetime
import os
import shutil
import uuid

from fastapi import HTTPException
from starlette import status

from constants import TEMP_FILE_FOLDER
from db import database
from models.comment import db_comment
from models.post import db_post
from models.user import db_user
from models.enums import ImageUrlType
from schemas.request.post import PostIn
from services.s3 import S3Service

from utils import logger

s3 = S3Service()

class PostManager:
    @staticmethod
    async def create_post(post_data: PostIn, user_id: int):
        if not isinstance(post_data["image_url_type"], ImageUrlType):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Parameter image_url_type can only take values 'absolute' or 'relative'.",
            )
        post_data["user_id"] = user_id
        id_ = await database.execute(db_post.insert().values(**post_data))
        # Get a Post object
        # post_obj = await database.fetch_one(db_post.select().where(db_post.c.id == id_))
        post_data["id"] = id_
        post_data["created_at"] = datetime.datetime.utcnow()
        # Get post's user
        user_obj = await database.fetch_one(db_user.select().where(db_user.c.id == user_id))
        post_data["user"] = user_obj
        # Post's comments is a empty list
        post_data["comments"] = []
        return post_data

    @staticmethod
    async def get_all():
        query = """
            SELECT p.*, u.username, u.email
            FROM insta_post AS p
            INNER JOIN insta_user AS u ON p.user_id = u.id
        """
        rows = await database.fetch_all(query=query)
        res = []
        for rec in rows:
            res_dict = dict(rec.items())
            res_dict["user"] = {
                "id": res_dict["user_id"],
                "username": res_dict["username"],
                "email": res_dict["email"]
            }
            comments = await database.fetch_all(db_comment.select().where(db_comment.c.post_id == res_dict["id"]))
            res_dict["comments"] = comments
            res.append(res_dict)
        return res

    @staticmethod
    async def delete_post(post_id: int, user_id: int):
        query = db_post.select().where(db_post.c.id == post_id)
        post = await database.fetch_one(query)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only post creator can delete the post",
            )

        if post.image_url_type == ImageUrlType.absolute.name:
            image_url = post.image_url
            _, photo_key = image_url.rsplit("/", 1)
            s3.delete_photo(photo_key)

        query = db_post.delete().where(db_post.c.id == post_id)
        await database.execute(query)

        return "ok"

    @staticmethod
    async def upload_image(image):
        filename = image.filename
        _, extension = filename.rsplit(".", 1)
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        with open(path, "w+b") as buffer:
            shutil.copyfileobj(image.file, buffer)
        photo_url = s3.upload_photo(path, name, extension)
        os.remove(path)
        return {"filename": photo_url}
