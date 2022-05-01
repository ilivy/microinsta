from typing import Type, List

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.repositories.base import BaseRepository
from app.db.tables.comments import Comment
from app.models.schema.comments import CommentSchema, InCommentSchema


class CommentsRepository(BaseRepository[InCommentSchema, CommentSchema, Comment]):
    @property
    def _in_schema(self) -> Type[InCommentSchema]:
        return InCommentSchema

    @property
    def _schema(self) -> Type[CommentSchema]:
        return CommentSchema

    @property
    def _table(self) -> Type[Comment]:
        return Comment

    async def get_by_post(self, post_id) -> List:
        stmt = select(self._table).where(self._table.post_id == post_id)\
            .order_by(self._table.created_at.desc())
        result = await self._db_session.execute(stmt)
        entries = result.all()
        return [r[0] for r in entries]
