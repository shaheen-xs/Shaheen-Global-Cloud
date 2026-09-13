"""Mock infrastructure provider for Phase 1."""

import random
import string
import logging

logger = logging.getLogger(__name__)


def generate_mock_ip() -> str:
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_mock_ipv6() -> str:
    parts = [f"{random.randint(0, 65535):x}" for _ in range(8)]
    return ":".join(parts)


def generate_mock_server_id() -> str:
    return "srv-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))


async def provision_server(name: str, region: str, image: str) -> dict:
    logger.info(f"[MOCK] Provisioning server '{name}' in {region} with {image}")
    return {
        "provider_id": generate_mock_server_id(),
        "ipv4": generate_mock_ip(),
        "ipv6": generate_mock_ipv6(),
    }


async def destroy_server(provider_id: str) -> bool:
    logger.info(f"[MOCK] Destroying server {provider_id}")
    return True


async def start_server(provider_id: str) -> bool:
    logger.info(f"[MOCK] Starting server {provider_id}")
    return True


async def stop_server(provider_id: str) -> bool:
    logger.info(f"[MOCK] Stopping server {provider_id}")
    return True


async def restart_server(provider_id: str) -> bool:
    logger.info(f"[MOCK] Restarting server {provider_id}")
    return True
