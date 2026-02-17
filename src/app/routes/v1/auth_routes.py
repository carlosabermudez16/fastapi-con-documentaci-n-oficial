import random
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import AfterValidator

from app.schemas.v1.items import FilterParams, Item, User
from app.tasks.muestra import check_valid_id

router = APIRouter(prefix="/api/v1/auth", tags=["AUTH V1"])


@router.get("/login")
async def login():
    return {"message": "Login route"}


@router.post("/register")
async def register():
    return {"message": "Register route"}


@router.post("/logout")
async def logout():
    return {"message": "Logout route"}


@router.get("/profile")
async def profile():
    return {"message": "Profile route"}


@router.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    item_dict = item.model_dump()
    print(type(item_dict))
    print(item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    item_dict.update({"item_id": item_id})
    print(item_dict)
    return item_dict


@router.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@router.get("/items3/")
async def read_items(
    q: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/items4/")
async def read_items4(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


@router.get("/items5/")
async def read_items5(
    item_id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if item_id:
        item = data.get(item_id)
    else:
        item_id, item = random.choice(list(data.items()))
    return {"item_id": item_id, "name": item}


@router.get("/items6/")
async def read_items6(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@router.put("/items7/{item_id}")
async def update_item7(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
