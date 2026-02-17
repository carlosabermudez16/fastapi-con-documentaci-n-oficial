from fastapi import APIRouter, Form, HTTPException, UploadFile, status

from app.tasks.save_image import save_image

router = APIRouter(prefix="/api/v4/images", tags=["AUTH V4"])


@router.post("/upload_images/", status_code=status.HTTP_202_ACCEPTED)
async def upload_image(
    photo: UploadFile,
    username: str = Form(...),
    password: str = Form(...),
):
    if photo.content_type != "image/jpeg":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format {photo.content_type}, only valid images with format jpg",
        )
    await save_image(photo)

    return {
        "username": username,
        "password": password,
        "photo": {"filename": photo.filename, "content_type": photo.content_type},
    }
