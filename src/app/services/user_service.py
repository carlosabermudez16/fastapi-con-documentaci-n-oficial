from pydantic import ValidationError
from sqlmodel import Session, SQLModel

from app.core.exceptions import ModelSerializationError, RegisterNotFoundError
from app.core.security import hash_password
from app.repositories.user_repository import create_user, get_user_by_email, update_user
from app.schemas.v7.user import UserCreateScheme


def create_user_service(
    model_type: SQLModel, session: Session, user_data: UserCreateScheme
):
    try:
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = hash_password(user_data.password)
        db_user = model_type(**user_dict)
    except (ValidationError, TypeError, ValueError, AttributeError) as e:
        raise ModelSerializationError("Error converting schema to model") from e

    return create_user(session=session, db_data=db_user)


def update_user_service(model_type: SQLModel, session: Session, email: str):
    user_db = get_user_by_email(model_type=model_type, session=session, email=email)

    if not user_db:
        raise RegisterNotFoundError()

    update_fields = {"is_verified": True}
    try:
        update_user(model_type=user_db, session=session, user_data=update_fields)
    except (ValidationError, TypeError, ValueError, AttributeError) as e:
        raise ModelSerializationError("Error converting schema to model") from e
