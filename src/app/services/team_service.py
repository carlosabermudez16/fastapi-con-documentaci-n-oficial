from sqlmodel import Session, SQLModel

from app.core.exceptions import HeroNotFoundError
from app.repositories.team_repository import get_team_by_id


def read_team_service(model_type: SQLModel, session: Session, team_id: int):
    hero = get_team_by_id(model_type=model_type, session=session, team_id=team_id)

    if not hero:
        raise HeroNotFoundError()

    return hero
