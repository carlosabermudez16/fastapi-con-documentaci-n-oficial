import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel, String

from app.models.shared import TimestampModel


class UserBasic(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserPublic(SQLModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool | None = False
    email: str
    password_hash: str
    role: str = Field(
        sa_column=Column(String(10), nullable=False, server_default="user")
    )


class UserModel(TimestampModel, UserPublic, UserBasic, table=True):
    __tablename__ = "user"

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    update_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )
