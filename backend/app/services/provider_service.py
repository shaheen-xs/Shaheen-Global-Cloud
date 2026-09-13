"""Provider service — maps plans to specs and delegates to the mock provider."""

from app.providers.base import MockProvider

_provider = MockProvider()

PLAN_SPECS = {
    "micro": {"cpu_cores": 1, "memory_mb": 1024, "disk_gb": 20, "price_per_hour": 0.005},
    "small": {"cpu_cores": 2, "memory_mb": 2048, "disk_gb": 40, "price_per_hour": 0.012},
    "medium": {"cpu_cores": 4, "memory_mb": 4096, "disk_gb": 80, "price_per_hour": 0.024},
    "large": {"cpu_cores": 8, "memory_mb": 8192, "disk_gb": 160, "price_per_hour": 0.048},
    "xlarge": {"cpu_cores": 16, "memory_mb": 16384, "disk_gb": 320, "price_per_hour": 0.096},
}


def get_plan_specs(plan: str) -> dict:
    return PLAN_SPECS.get(plan, PLAN_SPECS["small"])


async def provision(name: str, region: str, image: str) -> dict:
    return await _provider.provision(name, region, image)


async def destroy(provider_id: str) -> bool:
    return await _provider.destroy(provider_id)


async def start(provider_id: str) -> bool:
    return await _provider.start(provider_id)


async def stop(provider_id: str) -> bool:
    return await _provider.stop(provider_id)


async def restart(provider_id: str) -> bool:
    return await _provider.restart(provider_id)
