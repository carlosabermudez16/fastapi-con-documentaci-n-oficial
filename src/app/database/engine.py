# Solo conexión
from sqlmodel import create_engine

from app.core.config import settings

db_url = settings.DATABASE_URL
connect_args = {"check_same_thread": False}
is_sqlite = db_url.startswith("sqlite")

engine = create_engine(
    db_url,
    echo=False,  # settings.DEBUG,
    pool_pre_ping=True,
    connect_args=connect_args if is_sqlite else {},
)
