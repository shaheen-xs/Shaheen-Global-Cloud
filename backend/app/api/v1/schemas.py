"""Pydantic schemas for API v1."""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ServerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    hostname: str = Field(..., min_length=1, max_length=255)
    plan: str = Field("small", pattern="^(micro|small|medium|large|xlarge)$")
    region: str = Field("us-east-1")
    image: str = Field("ubuntu-24.04")


class ServerUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


class ServerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    hostname: str
    plan: str
    region: str
    image: str
    status: str
    ipv4: str | None
    ipv6: str | None
    cpu_cores: int
    memory_mb: int
    disk_gb: int
    created_at: datetime
    updated_at: datetime


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    server_id: str | None
    job_type: str
    status: str
    message: str
    created_at: datetime
    updated_at: datetime


class ServerPlanResponse(BaseModel):
    id: str
    label: str
    cpu_cores: int
    memory_mb: int
    disk_gb: int
    price_per_hour: float


class RegionResponse(BaseModel):
    id: str
    label: str
    country: str


class ImageResponse(BaseModel):
    id: str
    label: str
    version: str


class HealthResponse(BaseModel):
    status: str
    version: str
    redis_connected: bool
    worker_active: bool
