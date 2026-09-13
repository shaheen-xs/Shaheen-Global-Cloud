"""Dagger service — invokes Dagger module for infrastructure provisioning.

In Phase 1, this is a thin wrapper that logs the intent and delegates
to the mock provider. When a real Dagger CLI is available, this module
will shell out to `dagger call` with the appropriate arguments.
"""

import logging
from app.services import provider_service

logger = logging.getLogger(__name__)


async def run_provision(name: str, region: str, image: str) -> dict:
    logger.info(f"[Dagger] Provision pipeline: {name} / {region} / {image}")
    result = await provider_service.provision(name, region, image)
    logger.info(f"[Dagger] Provision complete: {result.get('provider_id')}")
    return result


async def run_destroy(provider_id: str) -> bool:
    logger.info(f"[Dagger] Destroy pipeline: {provider_id}")
    return await provider_service.destroy(provider_id)


async def run_start(provider_id: str) -> bool:
    logger.info(f"[Dagger] Start pipeline: {provider_id}")
    return await provider_service.start(provider_id)


async def run_stop(provider_id: str) -> bool:
    logger.info(f"[Dagger] Stop pipeline: {provider_id}")
    return await provider_service.stop(provider_id)


async def run_restart(provider_id: str) -> bool:
    logger.info(f"[Dagger] Restart pipeline: {provider_id}")
    return await provider_service.restart(provider_id)
