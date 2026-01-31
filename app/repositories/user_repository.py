# app/repositories/user_repository.py
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    async def get_by_id(self, db: AsyncSession, user_id: UUID) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all_paginated(self, db: AsyncSession, limit: int, offset: int) -> list[User]:
        stmt = select(User).order_by(User.name.asc()).limit(limit).offset(offset)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, data: UserCreate) -> User:
        user = User(name=data.name, email=str(data.email), age=data.age)
        db.add(user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(user)
        return user

    async def update(self, db: AsyncSession, user: User, data: UserUpdate) -> User:
        payload = data.model_dump(exclude_unset=True)
        # EmailStr -> garantir string no banco
        if "email" in payload and payload["email"] is not None:
            payload["email"] = str(payload["email"])

        for field, value in payload.items():
            setattr(user, field, value)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(user)
        return user

    async def delete(self, db: AsyncSession, user: User) -> None:
        await db.delete(user)
        await db.commit()
