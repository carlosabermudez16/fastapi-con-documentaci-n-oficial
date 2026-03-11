from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.core.exceptions import PersistenceError


def get_heroes(
    model_type: SQLModel,
    session: Session,
    offset: int | None = 0,
    limit: int | None = 100,
) -> list:
    try:
        statement = select(model_type).offset(offset).limit(limit)
        heroes = session.exec(statement).all()
        return heroes
    except SQLAlchemyError as e:
        # Nunca exponemos errores del ORM hacia arriba
        raise PersistenceError("Database query failed") from e


def get_heroes_by_team(
    model_type: SQLModel,
    team_model: SQLModel,
    session: Session,
    team_id: int,
) -> list:
    try:
        # statement = select(model_type).where(model_type.team_id==team_id)
        statement = select(model_type).join(team_model).where(team_model.id == team_id)
        # statement = (
        #    select(model_type, team_model)
        #    .join(team_model, model_type.team_id == team_model.id)
        #    .where(team_model.id == team_id)
        # )
        # statement = (
        #    select(model_type,team_model)
        #    .where(
        #        model_type.team_id==team_model.id,
        #        team_model.id==team_id
        #    )
        # )

        heroes = session.exec(statement).all()
        return heroes
    except SQLAlchemyError as e:
        # Nunca exponemos errores del ORM hacia arriba
        raise PersistenceError("Database query failed") from e


def create_hero(model_type: SQLModel, session: Session, hero_data: SQLModel):
    try:
        db_hero = model_type.model_validate(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)

        return db_hero
    except SQLAlchemyError as e:
        raise PersistenceError("Error to create new hero") from e


def get_hero_by_id(model_type: SQLModel, session: Session, hero_id: int):
    try:
        return session.get(model_type, hero_id)
    except SQLAlchemyError as e:
        raise PersistenceError("Database query failed") from e


def update_hero(model_type: SQLModel, session: Session, hero_data: dict):
    try:
        model_type.sqlmodel_update(hero_data)
        session.add(model_type)
        session.commit()
        session.refresh(model_type)

        return model_type
    except SQLAlchemyError as e:
        raise PersistenceError("Failed to update hero") from e


def delete_hero(model_type: SQLModel, session: Session):
    try:
        session.delete(model_type)
        session.commit()
    except SQLAlchemyError as e:
        raise PersistenceError("Error delete hero") from e
