from schemas.base import BaseModel

from email_validator import validate_email as validate_e, EmailNotValidError


class EmailField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            validate_e(v)
            return v
        except EmailNotValidError:
            raise ValueError("Email is not valid")


class UserRegisterIn(BaseModel):
    username: str
    email: EmailField
    password: str


class UserLoginIn(BaseModel):
    email: str
    password: str
