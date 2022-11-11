import aiohttp

from app.core.config import settings


async def request_prediction(base64img):
    # url = "http://localhost:8081/celebrity/"
    # url = "http://localhost:8081/"
    # url = settings.FACE_APP_URL + "celebrity/"
    url = settings.FACE_APP_URL
    client = aiohttp.ClientSession()
    async with client.post(url, json={'img': base64img}) as resp:
        # assert resp.status == 200
        return await resp.read()
