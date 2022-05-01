from fastapi import APIRouter

from app.api.routes import auth, comments
from app.api.routes import posts


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(posts.router)
api_router.include_router(comments.router)
