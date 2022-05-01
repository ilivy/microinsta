import abc
from typing import Generic, TypeVar, Type, List

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.errors import DoesNotExist
from app.models.schema.base import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE")


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=abc.ABCMeta):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        pass

    async def create(self, in_schema: IN_SCHEMA) -> SCHEMA:
        entry = self._table(**in_schema.dict())
        self._db_session.add(entry)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def get_by_id(self, entry_id: Integer) -> SCHEMA:
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{entry_id}> does not exist")
        return self._schema.from_orm(entry)

    async def get_all(self) -> List:
        stmt = select(self._table).order_by(self._table.id.asc())
        result = await self._db_session.execute(stmt)
        entries = result.scalars()
        return entries
