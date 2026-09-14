"""Provider service — maps plans to specs and delegates to selected provider."""

import logging
from app.config import get_settings
from app.providers.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)

PLAN_SPECS = {
    "micro": {"cpu_cores": 1, "memory_mb": 1024, "disk_gb": 20, "price_per_hour": 0.005},
    "small": {"cpu_cores": 2, "memory_mb": 2048, "disk_gb": 40, "price_per_hour": 0.012},
    "medium": {"cpu_cores": 4, "memory_mb": 4096, "disk_gb": 80, "price_per_hour": 0.024},
    "large": {"cpu_cores": 8, "memory_mb": 8192, "disk_gb": 160, "price_per_hour": 0.048},
    "xlarge": {"cpu_cores": 16, "memory_mb": 16384, "disk_gb": 320, "price_per_hour": 0.096},
}


def get_plan_specs(plan: str) -> dict:
    """Get hardware specs for a plan.
    
    Args:
        plan: Plan name (micro, small, medium, large, xlarge).
        
    Returns:
        Dict with cpu_cores, memory_mb, disk_gb, price_per_hour.
    """
    return PLAN_SPECS.get(plan, PLAN_SPECS["small"])


async def provision(name: str, region: str, image: str, plan: str) -> dict:
    """Provision a new server using the configured provider.
    
    Args:
        name: Server name.
        region: Region ID.
        image: Image/OS ID.
        plan: Server plan.
        
    Returns:
        Dict with provider_id, ipv4, ipv6, status.
    """
    settings = get_settings()
    logger.info(f"Provisioning server using {settings.PROVIDER_TYPE} provider")
    
    # Validate credentials before provisioning
    cred_error = settings.validate_provider_credentials()
    if cred_error:
        raise RuntimeError(f"Provider credential error: {cred_error}")
    
    provider = ProviderFactory.get_provider()
    return await provider.provision(name, region, image, plan)


async def get_server(provider_id: str) -> dict:
    """Get server status from provider.
    
    Args:
        provider_id: Provider-specific server ID.
        
    Returns:
        Dict with id, status, ipv4, ipv6.
    """
    provider = ProviderFactory.get_provider()
    return await provider.get_server(provider_id)


async def destroy(provider_id: str) -> bool:
    """Destroy a server.
    
    Args:
        provider_id: Provider-specific server ID.
        
    Returns:
        True if successful.
    """
    provider = ProviderFactory.get_provider()
    return await provider.destroy(provider_id)


async def reboot(provider_id: str) -> bool:
    """Reboot a server.
    
    Args:
        provider_id: Provider-specific server ID.
        
    Returns:
        True if successful.
    """
    provider = ProviderFactory.get_provider()
    return await provider.reboot(provider_id)


async def power_on(provider_id: str) -> bool:
    """Power on a server.
    
    Args:
        provider_id: Provider-specific server ID.
        
    Returns:
        True if successful.
    """
    provider = ProviderFactory.get_provider()
    return await provider.power_on(provider_id)


async def power_off(provider_id: str) -> bool:
    """Power off a server.
    
    Args:
        provider_id: Provider-specific server ID.
        
    Returns:
        True if successful.
    """
    provider = ProviderFactory.get_provider()
    return await provider.power_off(provider_id)
