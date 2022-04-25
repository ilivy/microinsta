from pydantic import BaseModel

from models.enums import ImageUrlType


class BasePost(BaseModel):
    image_url: str
    image_url_type: ImageUrlType
    caption: str
    user_id: int


class BaseComment(BaseModel):
    username: str
    text: str
