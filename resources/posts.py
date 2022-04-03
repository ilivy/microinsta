from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from db import get_db_session
from managers.auth import oauth2_scheme
from managers.post import PostManager
from schemas.request.post import PostIn
from schemas.response.post import PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", dependencies=[Depends(oauth2_scheme)], response_model=PostOut)
def create(
    post_data: PostIn, request: Request, db_session: Session = Depends(get_db_session)
):
    user = request.state.user
    return PostManager.create_post(post_data, user.id, db_session)


@router.post("/image", dependencies=[Depends(oauth2_scheme)])
def upload_image(image: UploadFile = File(...)):
    return PostManager.upload_image(image)


@router.get("/all", response_model=List[PostOut])
def posts(db_session: Session = Depends(get_db_session)):
    return PostManager.get_all(db_session)


@router.delete("/delete/{post_id}", dependencies=[Depends(oauth2_scheme)])
def delete(
    post_id: int, request: Request, db_session: Session = Depends(get_db_session)
):
    user = request.state.user
    return PostManager.delete_post(db_session, post_id, user.id)
    # return db_post.delete_post(db, id, current_user.id)


# image_url_types = ['absolute', 'relative']
#
#
# @router.post('', response_model=PostDisplay)
# def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     if not request.image_url_type in image_url_types:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                             detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
#     return db_post.create(db, request)
#
#
# @router.get('/all', response_model=List[PostDisplay])
# def posts(db: Session = Depends(get_db)):
#     return db_post.get_all(db)
#
#
# @router.post('/image')
# def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
#     letters = string.ascii_letters
#     rand_str = ''.join(random.choice(letters) for i in range(6))
#     new = f'_{rand_str}.'
#     filename = new.join(image.filename.rsplit('.', 1))
#     path = f'uploaded_images/{filename}'
#
#     with open(path, "w+b") as buffer:
#         shutil.copyfileobj(image.file, buffer)
#
#     return {'filename': path}
#
#
# @router.get('/delete/{id}')
# def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     return db_post.delete(db, id, current_user.id)
