"""Metadata endpoints: plans, regions, images."""

from fastapi import APIRouter
from app.api.v1.schemas import ServerPlanResponse, RegionResponse, ImageResponse

router = APIRouter()

PLANS = [
    {"id": "micro", "label": "Micro", "cpu_cores": 1, "memory_mb": 1024, "disk_gb": 20, "price_per_hour": 0.005},
    {"id": "small", "label": "Small", "cpu_cores": 2, "memory_mb": 2048, "disk_gb": 40, "price_per_hour": 0.012},
    {"id": "medium", "label": "Medium", "cpu_cores": 4, "memory_mb": 4096, "disk_gb": 80, "price_per_hour": 0.024},
    {"id": "large", "label": "Large", "cpu_cores": 8, "memory_mb": 8192, "disk_gb": 160, "price_per_hour": 0.048},
    {"id": "xlarge", "label": "X-Large", "cpu_cores": 16, "memory_mb": 16384, "disk_gb": 320, "price_per_hour": 0.096},
]

REGIONS = [
    {"id": "us-east-1", "label": "US East 1", "country": "United States"},
    {"id": "us-west-1", "label": "US West 1", "country": "United States"},
    {"id": "eu-central-1", "label": "EU Central 1", "country": "Germany"},
    {"id": "ap-south-1", "label": "AP South 1", "country": "Singapore"},
    {"id": "me-central-1", "label": "ME Central 1", "country": "UAE"},
]

IMAGES = [
    {"id": "ubuntu-22.04", "label": "Ubuntu 22.04 LTS", "version": "22.04"},
    {"id": "ubuntu-24.04", "label": "Ubuntu 24.04 LTS", "version": "24.04"},
    {"id": "debian-12", "label": "Debian 12", "version": "12"},
]


@router.get("/plans", response_model=list[ServerPlanResponse])
async def list_plans():
    return [ServerPlanResponse(**p) for p in PLANS]


@router.get("/regions", response_model=list[RegionResponse])
async def list_regions():
    return [RegionResponse(**r) for r in REGIONS]


@router.get("/images", response_model=list[ImageResponse])
async def list_images():
    return [ImageResponse(**i) for i in IMAGES]
