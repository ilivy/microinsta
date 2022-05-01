from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import validator
from starlette import status

from app.db.tables.enums import ImageUrlType
from app.models.schema.base import BaseSchema
from app.models.schema.comments import OutCommentSchema
from app.models.schema.users import OutUserSchema


class PostSchemaBase(BaseSchema):
    image_url: str
    image_url_type: ImageUrlType
    caption: str
    user_id: int


class InPostSchema(PostSchemaBase):
    @validator('image_url_type')
    def image_url_type_validate(cls, v):
        if not isinstance(v, ImageUrlType):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Parameter image_url_type can only take values 'absolute' or 'relative'.",
            )
        return v


class PostSchema(PostSchemaBase):
    id: int
    created_at: datetime
    user: OutUserSchema


class OutPostSchema(PostSchema):
    comments: List[OutCommentSchema]
