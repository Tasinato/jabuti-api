# app/core/cache.py
from __future__ import annotations

from typing import Any

import redis.asyncio as redis

from app.core.config import settings

_redis: redis.Redis | None = None


def get_redis() -> redis.Redis:
    if _redis is None:
        raise RuntimeError("Redis não inicializado. Chame init_cache() no startup.")
    return _redis


async def init_cache() -> None:
    """
    Inicializa cliente Redis e valida conexão com um ping.
    """
    global _redis
    if _redis is not None:
        return

    _redis = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,  # retorna str ao invés de bytes
    )
    await _redis.ping()


async def close_cache() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
    _redis = None


async def get_cache(key: str) -> str | None:
    r = get_redis()
    return await r.get(key)


async def set_cache(key: str, value: str, ttl_seconds: int = 60) -> None:
    """
    value deve ser string (normalmente JSON).
    """
    r = get_redis()
    await r.set(name=key, value=value, ex=ttl_seconds)


async def delete_key(key: str) -> None:
    r = get_redis()
    await r.delete(key)


async def invalidate_prefix(prefix: str) -> int:
    """
    Remove todas as chaves que começam com 'prefix'.
    Ex.: prefix="users:list:" ou prefix="users:"
    Retorna quantidade de chaves removidas.
    """
    r = get_redis()
    pattern = f"{prefix}*"

    deleted = 0
    # scan_iter é seguro para produção (não bloqueia como KEYS)
    async for key in r.scan_iter(match=pattern, count=200):
        deleted += await r.delete(key)

    return deleted
