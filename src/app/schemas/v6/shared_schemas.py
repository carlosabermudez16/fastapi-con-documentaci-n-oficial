from pydantic import BaseModel

from app.models.hero import HeroBase


class HeroPublic(HeroBase):
    id: int


class TeamScheme(BaseModel):
    name: str
    headquarters: str
