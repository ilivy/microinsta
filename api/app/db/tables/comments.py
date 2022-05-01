from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Comment(Base):
    __tablename__ = "insta_comment"

    text = Column(Text, nullable=False)
    username = Column(String(120), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    post_id = Column(Integer, ForeignKey("insta_post.id", ondelete="CASCADE"), nullable=False)
    post = relationship("Post", back_populates="comments")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
