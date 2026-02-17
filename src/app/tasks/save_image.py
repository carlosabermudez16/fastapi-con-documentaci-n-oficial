import os
from datetime import datetime

from fastapi import UploadFile


async def save_image(photo: UploadFile):
    tmp_folder = "./tmp"
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)

    content = await photo.read()

    route = f"{tmp_folder}/{datetime.now().date()}-{photo.filename}"
    print(route)
    with open(route, "wb") as f:
        f.write(content)
