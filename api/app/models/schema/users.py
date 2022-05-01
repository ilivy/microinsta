from email_validator import validate_email as validate_e, EmailNotValidError

from pydantic import validator

from app.models.schema.base import BaseSchema


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


class UserSchemaBase(BaseSchema):
    email: EmailField


class InUserRegisterSchema(UserSchemaBase):
    username: str
    password: str

    @validator('username')
    def username_alphanumeric(cls, v):
        assert len(v) > 0, "Username cannot be empty."
        assert v.isalnum(), "Username must be alphanumeric."
        return v

    @validator('password')
    def password_not_empty(cls, v):
        assert len(v) > 0, "Password cannot be empty."
        return v


class InUserLoginSchema(UserSchemaBase):
    password: str


class UserSchema(UserSchemaBase):
    id: int
    username: str


class OutUserSchema(UserSchema):
    pass
