from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from starlette.requests import Request

from managers.auth import oauth2_scheme
from managers.post import PostManager
from schemas.request.post import PostIn
from schemas.response.post import PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", dependencies=[Depends(oauth2_scheme)], response_model=PostOut)
async def create(post_data: PostIn, request: Request):
    user = request.state.user
    return await PostManager.create_post(post_data.dict(), user.id)


@router.post("/image", dependencies=[Depends(oauth2_scheme)])
async def upload_image(image: UploadFile = File(...)):
    return await PostManager.upload_image(image)


@router.get("/all", response_model=List[PostOut])
async def posts():
    return await PostManager.get_all()


@router.delete("/delete/{post_id}", dependencies=[Depends(oauth2_scheme)])
async def delete(post_id: int, request: Request):
    user = request.state.user
    return await PostManager.delete_post(post_id, user.id)
