import sqlalchemy
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base
from models.enums import ImageUrlType


class DbPost(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    image_url_type = Column(Enum(ImageUrlType), nullable=False)
    caption = Column(String)
    created_at = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", back_populates="post")
