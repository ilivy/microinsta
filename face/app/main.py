import os
import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from model import vggface


class Item(BaseModel):
    img: str


os.environ["TZ"] = "UTC"
time.tzset()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
def main(item: Item):
    base64img = item.img
    res = vggface.predict_person_base64img(base64img)
    return res


@app.post("/celebrity")
def main(item: Item):
    base64img = item.img
    res = vggface.predict_celebrity_base64img(base64img)
    return res


