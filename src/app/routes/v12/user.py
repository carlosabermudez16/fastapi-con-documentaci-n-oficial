from datetime import timedelta
from typing import Annotated

from celery.result import AsyncResult
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import DuplicateRegisterError
from app.core.security import create_access_token, decode_access_token
from app.dependencies.role_dep import get_current_user_factory, role_checker_factory
from app.models.event import Event
from app.models.user import UserModel
from app.repositories.user_repository import get_user_by_email
from app.routes.deps import SessionDep
from app.schemas.v6.event import EventWithEmojiScheme
from app.schemas.v6.token import TokenData
from app.schemas.v7.user import UserCreateScheme, UserPublicScheme
from app.services.email_service import (
    prepare_message_verify_account,
    process_send_message,
    process_send_message_bg_task,
)
from app.services.event_service import read_event_service
from app.services.user_service import create_user_service, update_user_service
from app.tasks.task_status_code import process_send_message_celery

router = APIRouter(prefix="/api/v12/email", tags=["Emails V12"])

role_checker = ["admin", "user"]


@router.get("/user/", response_model=UserPublicScheme, status_code=status.HTTP_200_OK)
async def read_user(
    current_user: Annotated[UserModel, Depends(get_current_user_factory(UserModel))],
):
    return current_user


@router.get(
    "/event/{event_id}",
    response_model=EventWithEmojiScheme,
    status_code=status.HTTP_200_OK,
)
async def read_team(
    event_id: int,
    session: SessionDep,
    _: Annotated[bool, Depends(role_checker_factory(role_checker, UserModel))],
):
    return read_event_service(model_type=Event, session=session, event_id=event_id)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_Account(user_data: UserCreateScheme, session: SessionDep):
    email = user_data.email
    user_exists = get_user_by_email(model_type=UserModel, session=session, email=email)
    if user_exists:
        raise DuplicateRegisterError()

    new_user = create_user_service(
        model_type=UserModel, session=session, user_data=user_data
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"email": email}, expires_delta=access_token_expires
    )
    message = prepare_message_verify_account(recipients=[email], token=token)

    await process_send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": UserPublicScheme.model_validate(new_user),
    }


@router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user_account(
    token_data: Annotated[TokenData, Depends(decode_access_token)], session: SessionDep
):
    user_email = token_data.email

    if user_email:
        update_user_service(model_type=UserModel, session=session, email=user_email)
        return JSONResponse(
            content={"message": "Account verified successfully"},
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# BackgroundTask


@router.post("/signup_background_task", status_code=status.HTTP_201_CREATED)
async def create_user_Account_backgroundTask(
    user_data: UserCreateScheme, bg_task: BackgroundTasks, session: SessionDep
):
    email = user_data.email
    user_exists = get_user_by_email(model_type=UserModel, session=session, email=email)
    if user_exists:
        raise DuplicateRegisterError()

    new_user = create_user_service(
        model_type=UserModel, session=session, user_data=user_data
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"email": email}, expires_delta=access_token_expires
    )
    message = prepare_message_verify_account(recipients=[email], token=token)

    process_send_message_bg_task(message=message, background_tasks=bg_task)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": UserPublicScheme.model_validate(new_user),
    }


# Celery


@router.post("/signup_celery", status_code=status.HTTP_201_CREATED)
async def create_user_Account_celery(user_data: UserCreateScheme, session: SessionDep):
    email = user_data.email
    user_exists = get_user_by_email(model_type=UserModel, session=session, email=email)
    if user_exists:
        raise DuplicateRegisterError()

    new_user = create_user_service(
        model_type=UserModel, session=session, user_data=user_data
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"email": email}, expires_delta=access_token_expires
    )

    task_celery = process_send_message_celery.delay(recipients=[email], token=token)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": UserPublicScheme.model_validate(new_user),
        "task_id": task_celery.id,
    }


@router.get("/result_celery/{task_id}")
async def get_result(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "Task is still in progress", "state": task.state}
    elif task.state != "FAILURE":  # task.ready()
        return {"state": task.state, "result": task.result}
    else:  # task.failed()
        return {"status": "Task Failed", "state": task.state, "error": str(task.info)}
