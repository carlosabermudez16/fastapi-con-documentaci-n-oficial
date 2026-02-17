from fastapi import APIRouter

from app.schemas.v2.items2 import Item, Item2

router = APIRouter(prefix="/api/v2/auth", tags=["AUTH V2"])


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@router.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results
