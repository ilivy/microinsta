from schemas.base import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    email: str

