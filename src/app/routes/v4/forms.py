from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse

from app.schemas.v4.forms import FormData, Item

router = APIRouter(prefix="/api/v4/forms", tags=["AUTH V4"])


@router.post("/login/", status_code=status.HTTP_201_CREATED)
async def login(data: Annotated[FormData, Form()]):
    return data


@router.post("/file/", status_code=status.HTTP_200_OK)
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No upload file sent"}
    return {"file_size": len(file)}


@router.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/files_multipart/", status_code=status.HTTP_201_CREATED)
async def upload_data_form(
    data: FormData = Depends(FormData.as_form),  # noqa: B008
    file: Annotated[bytes | None, File()] = None,
    file_uploadfile: UploadFile | None = None,
):
    print(type(data))
    print(data.model_dump())
    data = {
        "data": data,
        "file_size": len(file) if file else None,
        "file_content_type": file_uploadfile.content_type if file_uploadfile else None,
    }
    return data


@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename}


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@router.get("/")
async def display_html():
    content = """
        <body>
            <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)


items = {"foo": "The Foo Wrestlers"}


@router.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return {"item": items[item_id]}


fake_db = {}


@router.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return fake_db
