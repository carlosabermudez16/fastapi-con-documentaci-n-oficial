# manejo de sesión, creación de metadatos, estructura de persistencia para envíar la información a la base de datos

from sqlmodel import Session

from app.database.engine import engine


def get_session():
    with Session(engine) as session:
        yield session
