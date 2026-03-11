from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel

from app.core.exceptions import PersistenceError


def get_team_by_id(model_type: SQLModel, session: Session, team_id: int):
    try:
        return session.get(model_type, team_id)
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e
