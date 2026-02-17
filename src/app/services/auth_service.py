from app.core.security import verify_password
from app.schemas.v6.user import UserInDB


def get_user(db, username: str):
    if username not in db:
        return False
    user_dict = db[username]
    return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(db=fake_db, username=username)
    if not user:
        return False
    if not verify_password(
        plan_password=password, hashed_password=user.hashed_password
    ):
        return False
    return user
