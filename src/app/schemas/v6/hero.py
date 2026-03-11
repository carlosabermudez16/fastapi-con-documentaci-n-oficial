from app.models.hero import HeroBase
from app.schemas.v6.shared_schemas import TeamScheme


class HeroScheme(HeroBase):
    id: int
    team_id: int


class HeroWithTeamScheme(HeroBase):
    id: int
    team: TeamScheme | None


class HeroCreate(HeroBase):
    secret_name: str
    active: bool


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
