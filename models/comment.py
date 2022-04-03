import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class DbComment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("DbPost", back_populates="comments")
