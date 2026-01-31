# app/services/user_service.py
from __future__ import annotations

import json
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import get_cache, set_cache, invalidate_prefix, delete_key
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, repo: UserRepository | None = None, cache_ttl_seconds: int = 60):
        self.repo = repo or UserRepository()
        self.cache_ttl_seconds = cache_ttl_seconds

    # ---------- Cache keys ----------
    @staticmethod
    def _key_user(user_id: UUID) -> str:
        return f"users:{user_id}"

    @staticmethod
    def _key_list(limit: int, offset: int) -> str:
        return f"users:list:{limit}:{offset}"

    # ---------- Helpers ----------
    @staticmethod
    def _not_found(user_id: UUID) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )

    @staticmethod
    def _email_conflict() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    async def _invalidate_users_cache(self, user_id: UUID | None = None) -> None:
        # invalida todas as listas
        await invalidate_prefix("users:list:")
        # invalida item específico (se fornecido)
        if user_id is not None:
            await delete_key(self._key_user(user_id))

    # ---------- Public API ----------
    async def get_user(self, db: AsyncSession, user_id: UUID) -> UserResponse:
        key = self._key_user(user_id)
        cached = await get_cache(key)
        if cached:
            return UserResponse.model_validate_json(cached)

        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise self._not_found(user_id)

        out = UserResponse.model_validate(user)
        await set_cache(key, out.model_dump_json(), ttl_seconds=self.cache_ttl_seconds)
        return out

    async def list_users(self, db: AsyncSession, limit: int, offset: int) -> list[UserResponse]:
        key = self._key_list(limit, offset)
        cached = await get_cache(key)
        if cached:
            raw = json.loads(cached)
            return [UserResponse.model_validate(item) for item in raw]

        users = await self.repo.get_all_paginated(db, limit=limit, offset=offset)
        out = [UserResponse.model_validate(u) for u in users]

        await set_cache(
            key,
            json.dumps([u.model_dump(mode="json") for u in out]),
            ttl_seconds=self.cache_ttl_seconds,
        )
        return out

    async def create_user(self, db: AsyncSession, data: UserCreate) -> UserResponse:
        try:
            user = await self.repo.create(db, data)
        except IntegrityError:
            # geralmente email unique violation
            raise self._email_conflict()

        await self._invalidate_users_cache(user_id=user.id)
        return UserResponse.model_validate(user)

    async def update_user(self, db: AsyncSession, user_id: UUID, data: UserUpdate) -> UserResponse:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise self._not_found(user_id)

        try:
            user = await self.repo.update(db, user, data)
        except IntegrityError:
            raise self._email_conflict()

        await self._invalidate_users_cache(user_id=user_id)
        return UserResponse.model_validate(user)

    async def delete_user(self, db: AsyncSession, user_id: UUID) -> None:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise self._not_found(user_id)

        await self.repo.delete(db, user)
        await self._invalidate_users_cache(user_id=user_id)
