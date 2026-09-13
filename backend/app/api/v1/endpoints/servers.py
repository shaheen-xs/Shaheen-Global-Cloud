"""Server CRUD and lifecycle endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.base import get_db
from app.database.models import Server, ServerStatus, Job, JobType, JobStatus
from app.api.v1.schemas import (
    ServerCreate, ServerResponse, ServerUpdate,
    JobResponse, ServerPlanResponse, RegionResponse, ImageResponse,
)
from app.queue.job_queue import enqueue_job
from app.services.provider_service import get_plan_specs

router = APIRouter()


PLAN_SPECS = {
    "micro": {"cpu_cores": 1, "memory_mb": 1024, "disk_gb": 20, "price_per_hour": 0.005},
    "small": {"cpu_cores": 2, "memory_mb": 2048, "disk_gb": 40, "price_per_hour": 0.012},
    "medium": {"cpu_cores": 4, "memory_mb": 4096, "disk_gb": 80, "price_per_hour": 0.024},
    "large": {"cpu_cores": 8, "memory_mb": 8192, "disk_gb": 160, "price_per_hour": 0.048},
    "xlarge": {"cpu_cores": 16, "memory_mb": 16384, "disk_gb": 320, "price_per_hour": 0.096},
}

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


@router.get("", response_model=list[ServerResponse])
@router.get("/", response_model=list[ServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Server).order_by(Server.created_at.desc()))
    servers = result.scalars().all()
    return [ServerResponse.model_validate(s) for s in servers]


@router.post("", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
async def create_server(req: ServerCreate, db: AsyncSession = Depends(get_db)):
    specs = get_plan_specs(req.plan)
    server = Server(
        name=req.name,
        hostname=req.hostname,
        plan=req.plan,
        region=req.region,
        image=req.image,
        status=ServerStatus.provisioning,
        cpu_cores=specs["cpu_cores"],
        memory_mb=specs["memory_mb"],
        disk_gb=specs["disk_gb"],
    )
    db.add(server)
    await db.flush()

    job = Job(
        server_id=server.id,
        job_type=JobType.provision,
        status=JobStatus.queued,
        message=f"Provisioning {server.name} in {server.region}",
    )
    db.add(job)
    await db.commit()
    await db.refresh(server)

    await enqueue_job("provision", server.id, job.id)

    return ServerResponse.model_validate(server)


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return ServerResponse.model_validate(server)


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    server.status = ServerStatus.deleting
    job = Job(
        server_id=server.id,
        job_type=JobType.destroy,
        status=JobStatus.queued,
        message=f"Destroying {server.name}",
    )
    db.add(job)
    await db.commit()

    await enqueue_job("destroy", server.id, job.id)


@router.post("/{server_id}/start", response_model=JobResponse)
async def start_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    if server.status == ServerStatus.running:
        raise HTTPException(status_code=409, detail="Server is already running")

    job = Job(
        server_id=server.id,
        job_type=JobType.start,
        status=JobStatus.queued,
        message=f"Starting {server.name}",
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    await enqueue_job("start", server.id, job.id)
    return JobResponse.model_validate(job)


@router.post("/{server_id}/stop", response_model=JobResponse)
async def stop_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    if server.status == ServerStatus.stopped:
        raise HTTPException(status_code=409, detail="Server is already stopped")

    job = Job(
        server_id=server.id,
        job_type=JobType.stop,
        status=JobStatus.queued,
        message=f"Stopping {server.name}",
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    await enqueue_job("stop", server.id, job.id)
    return JobResponse.model_validate(job)


@router.post("/{server_id}/restart", response_model=JobResponse)
async def restart_server(server_id: str, db: AsyncSession = Depends(get_db)):
    server = await db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    job = Job(
        server_id=server.id,
        job_type=JobType.restart,
        status=JobStatus.queued,
        message=f"Restarting {server.name}",
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    await enqueue_job("restart", server.id, job.id)
    return JobResponse.model_validate(job)
