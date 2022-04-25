from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import database
from resources.routers import api_router

app = FastAPI()
app.include_router(api_router)


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


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def hello():
    return {"message": "Hello world!"}
