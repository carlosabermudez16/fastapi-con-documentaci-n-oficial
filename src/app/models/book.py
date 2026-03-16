import uuid
from datetime import date

from sqlmodel import Field, SQLModel

from app.models.shared import TimestampModel


class BookBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class BookPublic(SQLModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookModel(TimestampModel, BookPublic, BookBase, table=True):
    __tablename__ = "book"
