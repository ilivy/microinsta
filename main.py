from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

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
  allow_methods=['*'],
  allow_headers=['*']
)


