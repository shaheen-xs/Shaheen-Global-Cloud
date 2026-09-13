"""Base provider interface for infrastructure operations."""

from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    @abstractmethod
    async def provision(self, name: str, region: str, image: str) -> dict:
        ...

    @abstractmethod
    async def destroy(self, provider_id: str) -> bool:
        ...

    @abstractmethod
    async def start(self, provider_id: str) -> bool:
        ...

    @abstractmethod
    async def stop(self, provider_id: str) -> bool:
        ...

    @abstractmethod
    async def restart(self, provider_id: str) -> bool:
        ...


class MockProvider(BaseProvider):
    """Mock provider implementation for Phase 1 MVP."""

    async def provision(self, name: str, region: str, image: str) -> dict:
        from app.providers import provision_server
        return await provision_server(name, region, image)

    async def destroy(self, provider_id: str) -> bool:
        from app.providers import destroy_server
        return await destroy_server(provider_id)

    async def start(self, provider_id: str) -> bool:
        from app.providers import start_server
        return await start_server(provider_id)

    async def stop(self, provider_id: str) -> bool:
        from app.providers import stop_server
        return await stop_server(provider_id)

    async def restart(self, provider_id: str) -> bool:
        from app.providers import restart_server
        return await restart_server(provider_id)
