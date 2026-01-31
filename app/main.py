from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.core.database import init_db, close_db
from app.core.cache import init_cache, close_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_cache()
    yield
    # Shutdown
    await close_cache()
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="CRUD de Usuários",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(users_router, prefix="/api/v1", tags=["Usuários"])
    return app


app = create_app()

