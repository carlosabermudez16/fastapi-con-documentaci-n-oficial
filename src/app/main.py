import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status  # ,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import (
    HeroNotFoundError,
    PersistenceError,
    TokenCreationError,
    TokenDecodeError,
)
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

# from app.tasks.use_depends import verify_token, verify_key
from app.routes.v6 import example_security, login_jwt
from app.routes.v7 import example_database
from app.routes.v8 import send_email
from app.routes.v9 import example_response_status_code


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


@app.exception_handler(HeroNotFoundError)
async def hero_not_found_handler(request: Request, exc: HeroNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "register not found"}
    )


@app.exception_handler(PersistenceError)
async def persistence_exception_handler(request: Request, exc: PersistenceError):
    logger.error(f"Error on {request.method} {request.url} -> {exc}")
    # logging.Logger.exception(f"DB Error on {request.method} {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "operation failed"},
    )


@app.exception_handler(TokenCreationError)
async def token_error_handler(request: Request, exc: TokenCreationError):
    logger.error(msg=f"Error on {request.method} {request.url} -> {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Authentication system error"},
    )


@app.exception_handler(TokenDecodeError)
async def decode_token_error_handler(request: Request, exc: TokenDecodeError):
    logger.error(msg=f"Error on {request.method} {request.url} -> {exc}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Could not validate credentials"},
        headers={"WWW.Authenticate": "Bearer"},
    )


app.include_router(auth_routes.router)
app.include_router(items.router)
app.include_router(items3.router)
app.include_router(forms.router)
app.include_router(images.router)
app.include_router(examples_depends.router)
app.include_router(example_security.router)
app.include_router(login_jwt.router)
app.include_router(example_database.router)
app.include_router(send_email.router)
app.include_router(example_response_status_code.router)

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
