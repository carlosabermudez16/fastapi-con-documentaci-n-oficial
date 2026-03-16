import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.database.session import get_session
from app.main import app

# 📌 Crear base de datos de test (como TestingConfig en Flask)

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# 🔁 esta dependencia es utilizada por todas las operaciones de ruta para obtener el objeto de sesión
def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


# 👇 Equivalente a test_client fixture en Flask
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# 👇 Equivalente a init_database fixture en Flask
@pytest.fixture(scope="function", autouse=True)
def init_database():
    SQLModel.metadata.create_all(engine)

    yield

    # SQLModel.metadata.drop_all(engine)
