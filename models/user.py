from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    # posts = relationship('DbPost', back_populates='user')

