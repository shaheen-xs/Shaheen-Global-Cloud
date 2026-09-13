"""API v1 router aggregation."""

from fastapi import APIRouter
from app.api.v1.endpoints import health, servers, jobs, metadata

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(servers.router, prefix="/servers", tags=["servers"])
router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
router.include_router(metadata.router, tags=["metadata"])
