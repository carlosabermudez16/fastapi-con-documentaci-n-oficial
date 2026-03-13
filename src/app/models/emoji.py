from sqlmodel import Field, Relationship, SQLModel, String

from app.models.event_emoji import EventEmoji


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class EmojiBase(SQLModel):
    code: str = Field(String(200), index=True)
    slug: str | None = Field(String(100))


class Emoji(EmojiBase, BaseModel, table=True):
    is_deleted: bool | None = False

    # Relations
    # events: list["Event"] = Relationship(back_populates="emojis", link_model=EventEmoji)  # noqa: F821
    event_links: list[EventEmoji] = Relationship(back_populates="emoji")
