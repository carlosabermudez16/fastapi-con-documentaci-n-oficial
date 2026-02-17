from sqlalchemy import create_engine, text
from sqlmodel import SQLModel

from app.core.config import settings


def create_database_if_not_exists():
    database_url = settings.DATABASE_URL

    if not database_url.startswith("mysql"):
        return  # SQLite crea archivo automáticamente

    db_name = database_url.rsplit("/", 1)[-1]
    server_url = database_url.rsplit("/", 1)[0]

    temp_engine = create_engine(server_url)

    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()

    temp_engine.dispose()


def create_tables(engine):
    SQLModel.metadata.create_all(engine)
