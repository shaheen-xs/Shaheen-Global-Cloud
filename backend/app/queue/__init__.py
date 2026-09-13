"""Redis-backed job queue for Shaheen Global Cloud."""

import json
import logging
import redis.asyncio as aioredis
from app.config import get_settings

logger = logging.getLogger(__name__)
QUEUE_NAME = "shaheen:jobs"


async def get_redis() -> aioredis.Redis:
    settings = get_settings()
    return aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def enqueue_job(job_type: str, server_id: str, job_id: str) -> None:
    payload = json.dumps({"job_type": job_type, "server_id": server_id, "job_id": job_id})
    r = await get_redis()
    try:
        await r.lpush(QUEUE_NAME, payload)
        logger.info(f"Enqueued job {job_id}: {job_type} for server {server_id}")
    finally:
        await r.close()


async def dequeue_job(timeout: int = 5) -> dict | None:
    r = await get_redis()
    try:
        result = await r.brpop(QUEUE_NAME, timeout=timeout)
        if result:
            _, data = result
            return json.loads(data)
        return None
    finally:
        await r.close()
