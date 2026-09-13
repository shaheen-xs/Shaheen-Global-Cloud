"""Dagger module for Shaheen Global Cloud infrastructure provisioning.

This module provides Dagger functions for provisioning and managing
virtual machines via OpenTofu. In Phase 1, the functions simulate
infrastructure operations using the mock provider.
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

PYTHON_VERSION = 3.11

PLAN_SPECS = {
    "micro":  {"cpu_cores": 1,  "memory_mb": 1024,  "disk_gb": 20},
    "small":  {"cpu_cores": 2,  "memory_mb": 2048,  "disk_gb": 40},
    "medium": {"cpu_cores": 4,  "memory_mb": 4096,  "disk_gb": 80},
    "large":  {"cpu_cores": 8,  "memory_mb": 8192,  "disk_gb": 160},
    "xlarge": {"cpu_cores": 16, "memory_mb": 16384, "disk_gb": 320},
}


@dataclass
class ProvisionResult:
    """Result of a provisioning operation."""
    provider_id: str
    ipv4: str
    ipv6: str
    plan: str
    region: str
    image: str


def provision(
    name: str,
    region: str = "us-east-1",
    image: str = "ubuntu-24.04",
    plan: str = "small",
) -> ProvisionResult:
    """Provision a new virtual machine (mock).

    Args:
        name: Server name
        region: Deployment region
        image: OS image
        plan: Server plan (micro/small/medium/large/xlarge)

    Returns:
        ProvisionResult with provider ID and IP addresses
    """
    import random
    import string

    specs = PLAN_SPECS.get(plan, PLAN_SPECS["small"])
    provider_id = "srv-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    ipv4 = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    ipv6 = ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))

    logger.info(
        f"[Dagger] Provisioned '{name}' ({plan}) in {region}: "
        f"cpu={specs['cpu_cores']}, mem={specs['memory_mb']}MB, "
        f"disk={specs['disk_gb']}GB -> {provider_id} ({ipv4})"
    )

    return ProvisionResult(
        provider_id=provider_id,
        ipv4=ipv4,
        ipv6=ipv6,
        plan=plan,
        region=region,
        image=image,
    )


def destroy(provider_id: str) -> bool:
    """Destroy a virtual machine by provider ID (mock)."""
    logger.info(f"[Dagger] Destroyed {provider_id}")
    return True


def start(provider_id: str) -> bool:
    """Start a stopped virtual machine (mock)."""
    logger.info(f"[Dagger] Started {provider_id}")
    return True


def stop(provider_id: str) -> bool:
    """Stop a running virtual machine (mock)."""
    logger.info(f"[Dagger] Stopped {provider_id}")
    return True


def restart(provider_id: str) -> bool:
    """Restart a virtual machine (mock)."""
    logger.info(f"[Dagger] Restarted {provider_id}")
    return True


def validate(tofu_dir: str = "../infrastructure/environments/production") -> bool:
    """Validate OpenTofu configuration (mock — logs intent)."""
    logger.info(f"[Dagger] Validating OpenTofu config at {tofu_dir}")
    return True
