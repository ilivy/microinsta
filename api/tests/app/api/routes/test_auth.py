from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.repositories.users import UsersRepository
from app.managers.user import UsersManager
from app.models.schema.users import InUserRegisterSchema

pytestmark = pytest.mark.asyncio


async def test_register(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    payload = {
        "username": "test",
        "email": "test@test.com",
        "password": "test",
    }
    users_repository = UsersRepository(db_session)

    response = await async_client.post("/v1/register", json=payload)
    user = await users_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": user.id,
        "username": payload["username"],
        "email": payload["email"],
    }


async def test_login(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    payload = {
        "username": "test",
        "email": "test@test.com",
        "password": "test",
    }
    user_data = InUserRegisterSchema(**payload)
    user_out = await UsersManager.register(db_session, user_data)

    payload = {
        "email": "test@test.com",
        "password": "test",
    }
    response = await async_client.post("/v1/login", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "user_id": user_out.id,
        "username": user_out.username,
        "email": user_out.email,
        "token_type": "bearer",
        "access_token": mock.ANY,
    }
