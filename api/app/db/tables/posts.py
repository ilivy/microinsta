from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.tables.comments import Comment
from app.db.tables.enums import ImageUrlType


class Post(Base):
    __tablename__ = "insta_post"

    image_url = Column(String(510), nullable=False)
    image_url_type = Column(Enum(ImageUrlType), nullable=False, server_default=ImageUrlType.relative.name)
    caption = Column(String(255), nullable=False)
    prediction = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(Integer, ForeignKey("insta_user.id"), nullable=False)
    user = relationship("User", lazy="joined")
    comments = relationship("Comment", order_by="desc(Comment.created_at)", back_populates="post")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
