from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from constants import UPLOADED_IMAGES_DIR
from resources.routers import api_router

app = FastAPI()
app.include_router(api_router)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    str(Path(f"/{UPLOADED_IMAGES_DIR}")),
    StaticFiles(directory=UPLOADED_IMAGES_DIR), name=UPLOADED_IMAGES_DIR,
)
