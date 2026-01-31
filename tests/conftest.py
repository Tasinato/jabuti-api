# tests/conftest.py
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.database import get_db, get_sessionmaker


# ---------- Event loop (pytest-asyncio) ----------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------- DB session ----------
@pytest.fixture
async def db_session() -> AsyncSession:
    """
    Fornece uma AsyncSession real para testes de service.
    Usa o mesmo banco configurado no Docker (.env).
    """
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session
        await session.rollback()


# ---------- FastAPI client ----------
@pytest.fixture
async def client(db_session: AsyncSession):
    """
    Client HTTP para testes de API.
    Sobrescreve a dependency get_db para reutilizar a mesma sessão.
    """
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
# ---------- Fim do conftest.py ----------