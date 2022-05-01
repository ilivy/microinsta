from typing import Type, List

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.repositories.base import BaseRepository
from app.db.tables.posts import Post
from app.models.schema.posts import InPostSchema, PostSchema


class PostsRepository(BaseRepository[InPostSchema, PostSchema, Post]):
    @property
    def _in_schema(self) -> Type[InPostSchema]:
        return InPostSchema

    @property
    def _schema(self) -> Type[PostSchema]:
        return PostSchema

    @property
    def _table(self) -> Type[Post]:
        return Post

    async def get_all(self) -> List:
        stmt = select(self._table).order_by(self._table.id.desc())\
            .options(selectinload(self._table.user))\
            .options(selectinload(self._table.comments))
        result = await self._db_session.execute(stmt)
        entries = result.all()
        return [r[0] for r in entries]
