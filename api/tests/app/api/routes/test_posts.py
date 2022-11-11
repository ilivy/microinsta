from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.managers.user import UsersManager
from app.models.schema.users import InUserRegisterSchema

pytestmark = pytest.mark.asyncio


async def test_create_403(
    async_client: AsyncClient
) -> None:
    payload = {
        "image_url": "img_url",
        "image_url_type": "absolute",
        "caption": "caption",
        "prediction": "prediction",
        "user_id": 1,
    }
    response = await async_client.post("/v1/posts", json=payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_201(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    """
    Creates a User, logs in, sets authorization headers
    Creates a Post
    """
    auth_resp = await _authorize(async_client, db_session)
    auth_data = auth_resp.json()

    payload = {
        "image_url": "img_url",
        "image_url_type": "absolute",
        "caption": "caption",
        "prediction": "prediction",
        "user_id": auth_data["user_id"],
    }
    headers = {
        "Authorization": " ".join(["Bearer", auth_data["access_token"]])
    }
    response = await async_client.post("/v1/posts", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "image_url": payload["image_url"],
        "image_url_type": payload["image_url_type"],
        "caption": payload["caption"],
        "prediction": payload["prediction"],
        "user_id": auth_data["user_id"],
        "id": mock.ANY,
        "created_at": mock.ANY,
        "user": mock.ANY,
    }


async def test_get_all(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:

    response = await async_client.get("/v1/posts/all")

    assert response.status_code == status.HTTP_200_OK


async def _authorize(async_client, db_session):
    """
    Creates a User, logs in
    """
    payload = {
        "username": "test",
        "email": "test@test.com",
        "password": "test",
    }
    user_data = InUserRegisterSchema(**payload)
    user_out = await UsersManager.register(db_session, user_data)

    payload.pop("username")
    response = await async_client.post("/v1/login", json=payload)

    return response

