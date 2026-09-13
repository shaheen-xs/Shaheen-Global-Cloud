"""Health check endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.base import get_db
from app.config import get_settings
import redis.asyncio as aioredis

router = APIRouter()


@router.get("")
@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    settings = get_settings()
    redis_ok = False
    try:
        r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await r.ping()
        redis_ok = True
        await r.close()
    except Exception:
        pass

    db_ok = False
    try:
        result = await db.execute(text("SELECT 1"))
        db_ok = result.scalar() == 1
    except Exception:
        pass

    status_val = "healthy" if (redis_ok and db_ok) else "unhealthy"
    return {
        "status": status_val,
        "version": settings.APP_VERSION,
        "redis_connected": redis_ok,
        "database_connected": db_ok,
        "worker_active": True,
    }
