from pydantic import ValidationError
from sqlmodel import Session, SQLModel

from app.core.exceptions import ModelSerializationError, RegisterNotFoundError
from app.models.emoji import Emoji
from app.models.event_emoji import EventEmoji
from app.repositories.event_repository import (
    create_event,
    get_emoji_by_slug,
    get_event_by_id,
)
from app.schemas.v6.event import EventCreate


def read_event_service(model_type: SQLModel, session: Session, event_id: int):
    event = get_event_by_id(model_type=model_type, session=session, event_id=event_id)

    if not event:
        raise RegisterNotFoundError()

    return event


def create_event_service(
    model_type: SQLModel, session: Session, event_data: EventCreate
):
    emoji_links: list[SQLModel] = []

    try:
        emojis = event_data.slugs
        db_event = model_type.model_validate(event_data.model_dump(exclude={"slugs"}))
    except (ValidationError, TypeError, ValueError, AttributeError) as e:
        raise ModelSerializationError("Error converting schema to model") from e

    if emojis:
        for emoji_data in emojis:
            slug = emoji_data.get("slug")
            code = emoji_data.get("code")
            is_training = emoji_data.get("is_training", True)

            emoji = get_emoji_by_slug(model_type=Emoji, session=session, slug=slug)
            if not emoji:
                emoji = Emoji(code=code, slug=slug)

            link = EventEmoji(emoji=emoji, is_training=is_training)

            emoji_links.append(link)

    db_event.emoji_links = emoji_links

    db_event_refresh = create_event(session=session, db_event=db_event)

    return db_event_refresh
