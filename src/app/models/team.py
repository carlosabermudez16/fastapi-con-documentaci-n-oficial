from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    is_deleted: bool | None = False

    # Relations
    heroes: list["Hero"] = Relationship(back_populates="team")  # noqa: F821
