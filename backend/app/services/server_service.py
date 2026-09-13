"""Server service — high-level server operations."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Server, ServerStatus
from app.services.provider_service import get_plan_specs


async def list_servers(db: AsyncSession) -> list[Server]:
    result = await db.execute(select(Server).order_by(Server.created_at.desc()))
    return list(result.scalars().all())


async def get_server(db: AsyncSession, server_id: str) -> Server | None:
    return await db.get(Server, server_id)
