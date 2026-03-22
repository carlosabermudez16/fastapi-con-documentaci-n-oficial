from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.constants.constants import MULTIPLIER_VALUE
from app.core.config import settings
from app.core.exceptions import TokenCreationError, TokenDecodeError
from app.schemas.v6.token import TokenData

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="...", auto_error=False)


async def get_token(
    request: Request,
    token_from_header: str | None = Depends(oauth2_scheme),
) -> str:
    # 1. Intentar desde header
    if token_from_header:
        return token_from_header

    # 2. Intentar desde path
    token_from_path = request.path_params.get("token")
    if token_from_path:
        return token_from_path

    # 3. No hay token
    raise TokenDecodeError("Token not provided")


def decode_access_token(token: Annotated[str, Depends(get_token)]) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        data = {"sub": payload.get("sub"), "email": payload.get("email")}
        if not data.get("sub") and not data.get("email"):
            raise TokenDecodeError
        token_data = (
            TokenData(username=data.get("sub"))
            if data.get("sub")
            else TokenData(email=data.get("email"))
        )
    except InvalidTokenError as e:
        raise TokenDecodeError("Failed to decode access token") from e

    return token_data


def development_environment(environment):
    separator = f"\n\n{MULTIPLIER_VALUE*'*'}\n"
    message = f"Execution environment: {environment}"
    return f"{separator}{message}{separator}"


def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"


def verify_password(plan_password, hashed_password):
    return password_hash.verify(plan_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    try:
        encode_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encode_jwt
    except PyJWTError as e:
        raise TokenCreationError("Failed to create access token") from e


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")
