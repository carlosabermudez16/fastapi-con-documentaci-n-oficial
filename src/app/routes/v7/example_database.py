from typing import Annotated

from fastapi import APIRouter, Query, status

from app.models.hero import Hero
from app.repositories.hero_repository import create_hero
from app.routes.deps import SessionDep
from app.schemas.v6.hero import HeroCreate, HeroPublic, HeroUpdate
from app.services.hero_services import (
    delete_hero_service,
    read_heroes_service,
    read_single_hero_service,
    update_hero_service,
)

router = APIRouter(prefix="/api/v7/database", tags=["database V7"])


@router.post("/heroes/", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
async def create_new_hero(hero: HeroCreate, session: SessionDep):
    db_hero = create_hero(model_type=Hero, hero_data=hero, session=session)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
async def read_heroes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = read_heroes_service(
        model_type=Hero, session=session, offset=offset, limit=limit
    )
    return heroes


@router.get(
    "/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK
)
async def read_single_hero(
    hero_id: int,
    session: SessionDep,
):
    hero = read_single_hero_service(model_type=Hero, session=session, hero_id=hero_id)
    return hero


@router.put(
    "/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK
)
async def update_single_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    return update_hero_service(
        hero_id=hero_id, hero_update=hero, model_type=Hero, session=session
    )


@router.delete("/heroes/{hero_id}", status_code=status.HTTP_200_OK)
async def delete_single_hero(hero_id: int, session: SessionDep) -> dict:
    delete_hero_service(model_type=Hero, session=session, hero_id=hero_id)
    return {"deleted hero": True}
