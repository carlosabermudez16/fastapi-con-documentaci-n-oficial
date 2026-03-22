from pydantic import BaseModel
from sqlmodel import Field


class UserBaseScheme(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    role: str = Field(max_length=10)

    class Config:
        from_attributes = True


class UserCreateScheme(UserBaseScheme):
    password: str = Field(min_length=6)


class UserPublicScheme(UserBaseScheme):
    pass
