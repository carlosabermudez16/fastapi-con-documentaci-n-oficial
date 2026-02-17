from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.schemas.v5.form_data import CommonQueryParams, FormData
from app.tasks.use_depends import (
    common_parameters,
    query_or_cookie_extractor,
    verify_key,
    verify_token,
)

router = APIRouter(prefix="/api/v5/depends", tags=["Depends V5"])


commonsDep = Annotated[dict, Depends(common_parameters)]


@router.get("/items/")
async def read_items(commons: commonsDep):
    return commons


@router.get("/users/")
async def read_users(commons: commonsDep):
    return commons


@router.post("/files_multipart/", status_code=status.HTTP_201_CREATED)
async def upload_data_form(
    data: Annotated[FormData, Depends()],
    file: Annotated[bytes | None, File()] = None,
    file_uploadfile: UploadFile | None = None,
):
    data = {
        "data": data,
        "file_size": len(file) if file else None,
        "file_content_type": file_uploadfile.content_type if file_uploadfile else None,
    }
    return data


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/items2/")
async def read_items2(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


@router.get("/items3/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"query_or_cookie": query_or_default}


@router.get("/items4/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items3():
    return [{"item": "Foo"}, {"item": "Bar"}]
