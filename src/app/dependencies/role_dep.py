from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import SQLModel

from app.core.exceptions import AccountNotVerified, HeroNotFoundError
from app.core.security import decode_access_token
from app.repositories.user_repository import get_user_by_email
from app.routes.deps import SessionDep
from app.schemas.v6.token import TokenData


def get_current_user_factory(model_type: SQLModel):
    async def get_current_user(
        token_data: Annotated[TokenData, Depends(decode_access_token)],
        session: SessionDep,
    ):
        user_db = get_user_by_email(
            model_type=model_type, session=session, email=token_data.email
        )

        if not user_db:
            raise HeroNotFoundError

        return user_db

    return get_current_user


def get_current_active_user_factory(model_type: SQLModel):
    async def get_current_active_user(
        current_user: Annotated[
            model_type, Depends(get_current_user_factory(model_type))
        ],
    ):
        if current_user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )
        return current_user

    return get_current_active_user


def role_checker_factory(allowed_roles: list[str], model_type: SQLModel):
    async def role_checker(
        current_user: Annotated[
            model_type, Depends(get_current_user_factory(model_type))
        ],
    ):
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    return role_checker
