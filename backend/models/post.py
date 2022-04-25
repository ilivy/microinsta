import sqlalchemy
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db import metadata
from models.comment import db_comment
from models.user import db_user
from models.enums import ImageUrlType


db_post = Table(
    "insta_post",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("image_url", String(510), nullable=False),
    Column(
        "image_url_type",
        Enum(ImageUrlType),
        nullable=False,
        server_default=ImageUrlType.relative.name,
    ),
    Column("caption", String(255), nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    Column(
        "user_id", ForeignKey("insta_user.id"), nullable=False
    ),
)
