# tests/test_users_api.py
import pytest
from uuid import uuid4
from app.main import app

def unique_email(prefix: str = "api") -> str:
    return f"{prefix}-{uuid4()}@example.com"


@pytest.mark.asyncio
async def test_create_and_get_user(client):
    payload = {
        "name": f"Teste API {uuid4()}",
        "email": unique_email("create-get"),
        "age": 25,
    }

    # cria usuário
    response = await client.post("/api/v1/usuarios", json=payload)
    assert response.status_code == 201

    created = response.json()
    assert created["name"] == payload["name"]
    assert created["email"] == payload["email"]
    assert "id" in created

    user_id = created["id"]

    # busca usuário
    response = await client.get(f"/api/v1/usuarios/{user_id}")
    assert response.status_code == 200

    fetched = response.json()
    assert fetched["id"] == user_id
    assert fetched["email"] == payload["email"]


@pytest.mark.asyncio
async def test_list_users_pagination(client):
    # cria alguns usuários para garantir que exista conteúdo
    for _ in range(3):
        payload = {
            "name": f"Paginação {uuid4()}",
            "email": unique_email("list"),
            "age": 30,
        }
        resp = await client.post("/api/v1/usuarios", json=payload)
        assert resp.status_code == 201

    response = await client.get("/api/v1/usuarios?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2


@pytest.mark.asyncio
async def test_email_conflict_returns_409(client):
    email = unique_email("dup")

    payload_a = {"name": f"User A {uuid4()}", "email": email, "age": 22}
    payload_b = {"name": f"User B {uuid4()}", "email": email, "age": 33}

    resp = await client.post("/api/v1/usuarios", json=payload_a)
    assert resp.status_code == 201

    resp = await client.post("/api/v1/usuarios", json=payload_b)
    assert resp.status_code == 409
