# app/api/v1/users.py
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter()
service = UserService(cache_ttl_seconds=60)


@router.get(
    "/usuarios",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_users(db=db, limit=limit, offset=offset)


@router.get(
    "/usuarios/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_user(db=db, user_id=user_id)


@router.post(
    "/usuarios",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await service.create_user(db=db, data=payload)


@router.put(
    "/usuarios/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await service.update_user(db=db, user_id=user_id, data=payload)


@router.delete(
    "/usuarios/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await service.delete_user(db=db, user_id=user_id)
    return None
