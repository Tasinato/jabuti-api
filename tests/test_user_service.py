# tests/test_user_service.py
import pytest
from uuid import uuid4

from fastapi import HTTPException

from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService
from app.main import app

def unique_email(prefix: str = "user") -> str:
    return f"{prefix}-{uuid4()}@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(db_session):
    service = UserService()
    fake_id = uuid4()

    with pytest.raises(HTTPException) as exc:
        await service.get_user(db=db_session, user_id=fake_id)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_create_user_and_update(db_session):
    service = UserService()

    email = unique_email("service")
    created = await service.create_user(
        db=db_session,
        data=UserCreate(name=f"Service Test {uuid4()}", email=email, age=20),
    )

    assert created.id is not None
    assert created.email == email

    updated = await service.update_user(
        db=db_session,
        user_id=created.id,
        data=UserUpdate(name=f"Service Updated {uuid4()}"),
    )

    assert updated.id == created.id
    assert updated.name.startswith("Service Updated")


@pytest.mark.asyncio
async def test_email_conflict_returns_409(db_session):
    service = UserService()

    email = unique_email("dup")

    # cria o primeiro usuário
    await service.create_user(
        db=db_session,
        data=UserCreate(name=f"User A {uuid4()}", email=email, age=30),
    )

    # tenta criar outro com o mesmo email -> deve retornar 409
    with pytest.raises(HTTPException) as exc:
        await service.create_user(
            db=db_session,
            data=UserCreate(name=f"User B {uuid4()}", email=email, age=40),
        )

    assert exc.value.status_code == 409
# ---------- Fim do test_user_service.py ----------