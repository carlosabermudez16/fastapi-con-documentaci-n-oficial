from typing import Any

from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from pydantic import BaseModel

from app.constants.constants import CODE_200
from app.schemas.v3.items3 import UserBase, UserIn, UserOut
from app.services.save_user import fake_save_user

router = APIRouter(prefix="/api/v3/auth", tags=["AUTH V3"])


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class ItemDescription(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@cbv(router)
class ItemsView:
    @router.post("/items/")
    async def create_item(self, item: Item) -> Item:
        return item

    @router.get("/items/")
    async def read_items(self) -> list[Item]:
        return [
            Item(name="Portal Gun", price=42.0),
            Item(name="Plumbus", price=32.0),
        ]

    @router.get("/items3/", response_model=list[ItemDescription])
    async def read_items3(self):
        return items


@router.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


@router.post("/user2/")
async def create_user2(user: UserIn) -> UserBase:
    return user


@router.post("/user3/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user3(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@router.get("/keyword-weights/", response_model=dict[str, float], status_code=CODE_200)
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
