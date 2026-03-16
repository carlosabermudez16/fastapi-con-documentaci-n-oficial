from app.models.event import EventBase
from app.schemas.v6.event_emoji import EventEmojiScheme


class EventScheme(EventBase):
    id: int

    class ConfigDict:
        from_attributes = True


class EventCreate(EventBase):
    slugs: list[dict[str, str | bool]] = []


class EventWithEmojiScheme(EventScheme):
    emoji_links: list[EventEmojiScheme] = []
