from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
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


def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if isinstance(username, type(None)):
            raise TokenDecodeError
        token_data = TokenData(username=username)
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
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encode_jwt
    except PyJWTError as e:
        raise TokenCreationError("Failed to create access token") from e
