# app/core/database.py
from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# IMPORTANTE:
# DATABASE_URL deve ser algo como:
# postgresql+asyncpg://postgres:postgres@db:5432/users_db
_engine: AsyncEngine | None = None
_SessionLocal: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("Database engine não inicializado. Chame init_db() no startup.")
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if _SessionLocal is None:
        raise RuntimeError("SessionLocal não inicializado. Chame init_db() no startup.")
    return _SessionLocal


async def init_db() -> None:
    """
    Inicializa engine + sessionmaker.
    Para desafio técnico, podemos também criar as tabelas automaticamente.
    Em produção, o ideal é usar Alembic.
    """
    global _engine, _SessionLocal

    if _engine is not None and _SessionLocal is not None:
        return  # já inicializado

    _engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=False,  # troque para True se quiser debug de SQL
    )

    _SessionLocal = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    # (Opcional) cria tabelas automaticamente
    # Para funcionar, seus models devem expor Base.metadata.
    from app.models.user import Base  # noqa: WPS433

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    global _engine, _SessionLocal
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _SessionLocal = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency do FastAPI para injetar sessão:
    async def handler(db: AsyncSession = Depends(get_db)):
        ...
    """
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session
