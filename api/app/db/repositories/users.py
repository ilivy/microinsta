from typing import Type

from sqlalchemy import String
from sqlalchemy.future import select

from app.db.errors import DoesNotExist
from app.db.repositories.base import BaseRepository
from app.db.tables.users import User
from app.models.schema.users import InUserRegisterSchema, UserSchema


class UsersRepository(BaseRepository[InUserRegisterSchema, UserSchema, User]):
    @property
    def _in_schema(self) -> Type[InUserRegisterSchema]:
        return InUserRegisterSchema

    @property
    def _schema(self) -> Type[UserSchema]:
        return UserSchema

    @property
    def _table(self) -> Type[User]:
        return User

    async def get_by_email(self, email: String) -> UserSchema:
        stmt = select(self._table).where(self._table.email == email)
        result = await self._db_session.execute(stmt)
        entry = result.scalars().first()

        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<email:{email}> does not exist")
        return entry
