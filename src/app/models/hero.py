from sqlmodel import Field, Relationship, SQLModel

from app.models.team import Team


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, BaseModel, table=True):
    secret_name: str
    active: bool | None = True
    is_deleted: bool | None = False
    team_id: int | None = Field(
        default=None, foreign_key="team.id", ondelete="SET NULL"
    )

    # Relations
    team: Team | None = Relationship(back_populates="heroes")
