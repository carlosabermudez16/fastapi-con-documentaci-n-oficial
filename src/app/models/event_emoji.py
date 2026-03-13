from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class EventEmojiBase(SQLModel):
    is_training: bool | None = True
    is_deleted: bool | None = False


class EventEmoji(EventEmojiBase, BaseModel, table=True):
    # Foreign Keys
    event_id: int | None = Field(default=None, foreign_key="event.id")
    emoji_id: int | None = Field(default=None, foreign_key="emoji.id")

    # Relations
    event: "Event" = Relationship(back_populates="emoji_links")  # noqa: F821
    emoji: "Emoji" = Relationship(back_populates="event_links")  # noqa: F821
