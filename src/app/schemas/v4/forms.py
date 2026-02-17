from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class FormData(BaseModel):
    model_config = {"extra": "forbid"}

    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ):
        return cls(username=username, password=password)


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None
