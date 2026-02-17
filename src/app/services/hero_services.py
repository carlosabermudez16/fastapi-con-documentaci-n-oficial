from sqlmodel import Session, SQLModel

from app.core.exceptions import HeroNotFoundError
from app.repositories.hero_repository import (
    delete_hero,
    get_hero_by_id,
    get_heroes,
    update_hero,
)
from app.schemas.v6.hero import HeroUpdate


def read_single_hero_service(model_type: SQLModel, session: Session, hero_id: int):
    hero = get_hero_by_id(model_type=model_type, session=session, hero_id=hero_id)

    if not hero:
        raise HeroNotFoundError()

    return hero


def read_heroes_service(
    model_type: SQLModel,
    session: Session,
    offset: int,
    limit: int,
):
    return get_heroes(
        model_type=model_type, session=session, offset=offset, limit=limit
    )


def update_hero_service(
    model_type: SQLModel, session: Session, hero_id: int, hero_update: HeroUpdate
):
    hero_db = read_single_hero_service(
        model_type=model_type, session=session, hero_id=hero_id
    )

    hero_data = hero_update.model_dump(exclude_unset=True)
    hero__update_db = update_hero(
        model_type=hero_db, hero_data=hero_data, session=session
    )

    return hero__update_db


def delete_hero_service(model_type: SQLModel, session: Session, hero_id: int):
    hero = read_single_hero_service(
        model_type=model_type, session=session, hero_id=hero_id
    )

    delete_hero(model_type=hero, session=session)
