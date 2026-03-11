from sqlalchemy import text
from sqlmodel import SQLModel, create_engine

from app.core.config import settings
from app.models import *  # noqa: F403


def create_tables():
    print("✅ DB initialized")
    database_url = settings.DATABASE_URL

    connect_args = {
        "check_same_thread": False
    }  # argumento para db sqlite ya que no maneja hilos
    is_sqlite = database_url.startswith("sqlite")
    if database_url.startswith("sqlite"):
        engine = create_engine(database_url, echo=False)
        SQLModel.metadata.create_all(engine)
        return

    # nombre de la base de datos
    db_name = database_url.rsplit("/", 1)[-1]
    # conexión SIN la base de datos
    server_url = database_url.rsplit("/", 1)[0]
    server_engine = create_engine(
        server_url,
        echo=False,  # settings.DEBUG,
        pool_pre_ping=True,
        connect_args=connect_args if is_sqlite else {},
    )

    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()

    server_engine.dispose()
    print("✅ Database ensured")

    engine = create_engine(database_url, echo=True)  # conectamos a la db
    print(SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(engine)  # agregamos los cambios existentes en memoria
    print("✅ Tables created")


if __name__ == "__main__":
    create_tables()
    print("✅ DB Actualized")
