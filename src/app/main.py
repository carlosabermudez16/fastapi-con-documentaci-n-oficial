import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logger import logger
from app.core.security import development_environment
from app.database.engine import engine
from app.database.init_db import create_database_if_not_exists, create_tables
from app.middleware.logging_middleware import logging_middleware
from app.routes.v1 import auth_routes
from app.routes.v2 import items
from app.routes.v3 import items3
from app.routes.v4 import forms, images
from app.routes.v5 import examples_depends
from app.routes.v6 import example_security, login_jwt
from app.routes.v7 import example_database, example_relationship_nxn, team
from app.routes.v8 import send_email
from app.routes.v9 import example_response_status_code
from app.routes.v10 import websocket
from app.routes.v11 import example_celery


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup logic
    create_database_if_not_exists()
    create_tables(engine)
    print("✅ DB initialized")

    yield

    # 🛑 Shutdown logic (opcional)
    print("🛑 App shutting down")


app = FastAPI(
    title="Prueba api 1",
    summary="Esto es algo nuevo.",
    lifespan=lifespan,
    # dependencies=[Depends(verify_token),Depends(verify_key)]
    # servers=[
    #    {"url": "https://stag.example.com", "description": "Staging environment"},
    #    {"url": "https://prod.example.com", "description": "Production environment"},
    # ]
)

print(development_environment(f"{settings.ENVIRONMENT}"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ["*"],
    allow_headers=["Authorization", "Content-Type"],  # ["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # logger.exception(
    #    f"Unhandled error on {request.method} {request.url}"
    # )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "internal server error"},
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    if exc.status_code != status.HTTP_404_NOT_FOUND:
        logger.exception(
            f"Application error on {request.method} {request.url} -> {exc}"
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


routers: list = [
    auth_routes.router,
    items.router,
    items3.router,
    forms.router,
    images.router,
    examples_depends.router,
    example_security.router,
    login_jwt.router,
    example_database.router,
    send_email.router,
    example_response_status_code.router,
    websocket.router,
    example_celery.router,
    team.router,
    example_relationship_nxn.router,
]

for router in routers:
    app.include_router(router)


app.middleware("http")(logging_middleware)


@app.middleware("http")
async def log_response(request: Request, call_next):
    response = await call_next(request)
    start_time = time.perf_counter()
    process_time = time.perf_counter() - start_time
    response.headers["X-Custom-Header"] = "Hello, World!"
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
