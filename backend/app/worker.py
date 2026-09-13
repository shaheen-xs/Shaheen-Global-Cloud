"""Async worker that consumes jobs from the Redis queue and processes them."""

import asyncio
import logging
import signal
from app.core.logging import setup_logging
from app.config import get_settings
from app.database.base import async_session
from app.database.models import Job
from app.queue import dequeue_job
from app.services.job_service import process_job

settings = get_settings()
setup_logging(settings.DEBUG)
logger = logging.getLogger(__name__)

running = True


async def worker_loop():
    logger.info("Worker started — listening for jobs...")
    while running:
        try:
            job_data = await dequeue_job(timeout=5)
            if not job_data:
                continue

            job_id = job_data.get("job_id")
            logger.info(f"Processing job {job_id}: {job_data.get('job_type')}")

            async with async_session() as db:
                job = await db.get(Job, job_id)
                if not job:
                    logger.warning(f"Job {job_id} not found in database")
                    continue
                await process_job(db, job)
                logger.info(f"Job {job_id} processed")

        except Exception as e:
            logger.error(f"Worker error: {e}")
            await asyncio.sleep(1)

    logger.info("Worker stopped.")


def handle_shutdown(signum, frame):
    global running
    logger.info(f"Signal {signum} received, shutting down worker...")
    running = False


def main():
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    asyncio.run(worker_loop())


if __name__ == "__main__":
    main()
