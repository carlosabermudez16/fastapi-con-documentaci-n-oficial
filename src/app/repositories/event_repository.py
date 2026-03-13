from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, select

from app.core.exceptions import (
    CreateModelError,
    DuplicateRegisterError,
    PersistenceError,
)
from app.models.event_emoji import EventEmoji


def create_event(session: Session, db_event: SQLModel):
    try:
        session.add(db_event)
        session.commit()
        session.refresh(db_event)

        return db_event
    except IntegrityError as e:
        session.rollback()
        raise DuplicateRegisterError("Database error") from e
    except SQLAlchemyError as e:
        session.rollback()
        raise PersistenceError("Database error") from e
    except Exception as e:
        raise CreateModelError("Error creating user") from e


def get_emoji_by_slug(
    model_type: SQLModel,
    session: Session,
    slug: str,
):
    try:
        statement = select(model_type).where(model_type.slug == slug)
        emoji = session.exec(statement).one_or_none()
        return emoji
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e


def get_event_by_id(model_type: SQLModel, session: Session, event_id: int):
    try:
        statement = (
            select(model_type)
            .where(model_type.id == event_id, model_type.is_deleted.is_(False))
            .options(
                selectinload(model_type.emoji_links).selectinload(EventEmoji.emoji)
            )
        )
        # return session.get(model_type, event_id)
        return session.exec(statement).one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e
