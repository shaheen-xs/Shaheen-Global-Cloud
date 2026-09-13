"""Job processing service — consumes jobs from the queue and updates the database."""

import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Server, Job, ServerStatus, JobType, JobStatus
from app.services import dagger_service

logger = logging.getLogger(__name__)


async def process_job(db: AsyncSession, job: Job) -> None:
    job.status = JobStatus.running
    job.updated_at = datetime.now(timezone.utc)
    await db.commit()

    server = await db.get(Server, job.server_id) if job.server_id else None

    try:
        if job.job_type == JobType.provision and server:
            result = await dagger_service.run_provision(
                server.name, server.region, server.image,
            )
            server.ipv4 = result.get("ipv4")
            server.ipv6 = result.get("ipv6")
            server.status = ServerStatus.running
            job.message = f"Provisioned successfully — IP: {server.ipv4}"

        elif job.job_type == JobType.destroy and server:
            await dagger_service.run_destroy(server.id)
            server.status = ServerStatus.stopped
            job.message = "Destroyed successfully"
            await db.delete(server)

        elif job.job_type == JobType.start and server:
            await dagger_service.run_start(server.id)
            server.status = ServerStatus.running
            job.message = "Started successfully"

        elif job.job_type == JobType.stop and server:
            await dagger_service.run_stop(server.id)
            server.status = ServerStatus.stopped
            job.message = "Stopped successfully"

        elif job.job_type == JobType.restart and server:
            await dagger_service.run_restart(server.id)
            server.status = ServerStatus.running
            job.message = "Restarted successfully"

        job.status = JobStatus.completed
    except Exception as e:
        logger.error(f"Job {job.id} failed: {e}")
        job.status = JobStatus.failed
        job.message = f"Error: {str(e)}"
        if server and job.job_type == JobType.provision:
            server.status = ServerStatus.error

    job.updated_at = datetime.now(timezone.utc)
    await db.commit()
