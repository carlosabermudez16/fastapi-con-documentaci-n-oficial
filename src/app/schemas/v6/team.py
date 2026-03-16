from pydantic import BaseModel

from app.schemas.v6.shared_schemas import HeroPublic


class TeamBasicScheme(BaseModel):
    id: int


class TeamWithHeroesScheme(BaseModel):
    name: str
    headquarters: str
    heroes: list[HeroPublic] = []

    class ConfigDict:
        from_attributes = True
