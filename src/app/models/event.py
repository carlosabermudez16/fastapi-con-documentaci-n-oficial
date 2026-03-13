from sqlmodel import Field, Relationship, SQLModel, String

from app.models.event_emoji import EventEmoji


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class EventBase(SQLModel):
    event_type: str = Field(String(50), index=True)
    event_type_id: int


class Event(EventBase, BaseModel, table=True):
    is_deleted: bool | None = False

    # Relations
    # emojis: list["Emoji"] = Relationship(back_populates="events", link_model=EventEmoji)  # noqa: F821
    emoji_links: list[EventEmoji] = Relationship(back_populates="event")
