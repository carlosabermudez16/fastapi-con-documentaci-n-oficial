from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED

from app.core.config import Settings, get_settings
from app.core.security import create_access_token
from app.database.fake_database import fake_users_db
from app.deps import get_current_active_user
from app.schemas.v6.token import Token
from app.schemas.v6.user import User
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/api/v6/security_jwt", tags=["SECURITY V6"])


@router.post("/token", status_code=HTTP_201_CREATED)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings_env: Annotated[Settings, Depends(get_settings)],
) -> Token:
    authenticated_user = authenticate_user(
        fake_db=fake_users_db, username=form_data.username, password=form_data.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings_env.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="Bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [
        {
            "item_id": "Foo",
            "owner": current_user.username,
        }
    ]
