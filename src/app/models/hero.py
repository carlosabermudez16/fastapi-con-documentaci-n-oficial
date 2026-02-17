from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, BaseModel, table=True):
    secret_name: str
    active: bool = True
