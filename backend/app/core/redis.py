from collections.abc import AsyncGenerator

import redis.asyncio as aioredis
from app.core.config import settings

# Initialize Redis client pool
redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Dependency injector for Redis connection."""
    yield redis_client
