# app/schemas/user.py
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    age: int = Field(..., ge=0, le=130)  # ajuste limites se quiser

    model_config = ConfigDict(extra="forbid")


class UserUpdate(BaseModel):
    # UPDATE geralmente é parcial (campos opcionais)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=130)

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    age: int

    # permite criar resposta a partir de objeto ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True, extra="forbid")


    """
    EmailStr: valida email

    Field com limites: validações claras (evita lixo no banco)

    extra="forbid": impede campos inesperados no payload (segurança e contrato bem definido)

    rom_attributes=True: facilita retornar ORM direto no response model
    """