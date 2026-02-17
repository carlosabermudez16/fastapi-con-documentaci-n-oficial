from typing import Annotated

from fastapi import Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.exceptions import HeroNotFoundError
from app.core.security import decode_access_token
from app.database.fake_database import fake_users_db
from app.schemas.v6.user import User
from app.services.auth_service import get_user


async def get_current_user(
    token_data: Annotated[str, Depends(decode_access_token)],
):
    user = get_user(db=fake_users_db, username=token_data.username)
    if not user:
        raise HeroNotFoundError

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user
