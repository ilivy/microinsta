import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_hello():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}
