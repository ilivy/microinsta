from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: id = Column(Integer, primary_key=True)
    __name__: str
