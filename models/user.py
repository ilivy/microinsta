from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("DbPost", back_populates="user")
