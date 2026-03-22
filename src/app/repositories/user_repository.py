from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.core.exceptions import (
    CreateModelError,
    DuplicateRegisterError,
    PersistenceError,
    UpdateModelError,
)


def get_user_by_email(model_type: SQLModel, session: Session, email: str):
    try:
        statement = select(model_type).where(model_type.email == email)
        return session.exec(statement).one_or_none()
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e


def create_user(session: Session, db_data: SQLModel):
    try:
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except IntegrityError as e:
        session.rollback()
        raise DuplicateRegisterError("Database error") from e
    except SQLAlchemyError as e:
        session.rollback()
        raise PersistenceError("Database error") from e
    except Exception as e:
        raise CreateModelError("Error creating user") from e


def update_user(model_type: SQLModel, session: Session, user_data: dict):
    try:
        model_type.sqlmodel_update(user_data)
        session.add(model_type)
        session.commit()
        session.refresh(model_type)

        return model_type
    except SQLAlchemyError as e:
        raise UpdateModelError("Error update item") from e
