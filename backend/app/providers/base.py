"""Base provider interface for infrastructure operations."""

from abc import ABC, abstractmethod
from typing import Any
import logging
import random
import string

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """Abstract base class for cloud providers."""
    
    @abstractmethod
    async def provision(
        self, name: str, region: str, image: str, plan: str
    ) -> dict:
        """Provision a new server.
        
        Args:
            name: Server name.
            region: Region ID.
            image: Image/OS ID.
            plan: Server plan/size.
            
        Returns:
            Dict with provider_id, ipv4, ipv6, status.
        """
        ...

    @abstractmethod
    async def get_server(self, provider_id: str) -> dict:
        """Get server status.
        
        Args:
            provider_id: Provider-specific server ID.
            
        Returns:
            Dict with id, status, ipv4, ipv6.
        """
        ...

    @abstractmethod
    async def destroy(self, provider_id: str) -> bool:
        """Destroy a server.
        
        Args:
            provider_id: Provider-specific server ID.
            
        Returns:
            True if successful.
        """
        ...

    @abstractmethod
    async def reboot(self, provider_id: str) -> bool:
        """Reboot a server.
        
        Args:
            provider_id: Provider-specific server ID.
            
        Returns:
            True if successful.
        """
        ...

    @abstractmethod
    async def power_on(self, provider_id: str) -> bool:
        """Power on a server.
        
        Args:
            provider_id: Provider-specific server ID.
            
        Returns:
            True if successful.
        """
        ...

    @abstractmethod
    async def power_off(self, provider_id: str) -> bool:
        """Power off a server.
        
        Args:
            provider_id: Provider-specific server ID.
            
        Returns:
            True if successful.
        """
        ...


class MockProvider(BaseProvider):
    """Mock provider implementation for testing."""

    @staticmethod
    def _generate_mock_id() -> str:
        """Generate a mock server ID."""
        return "srv-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))

    @staticmethod
    def _generate_mock_ip() -> str:
        """Generate a mock IPv4 address."""
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    @staticmethod
    def _generate_mock_ipv6() -> str:
        """Generate a mock IPv6 address."""
        parts = [f"{random.randint(0, 65535):x}" for _ in range(8)]
        return ":".join(parts)

    async def provision(
        self, name: str, region: str, image: str, plan: str
    ) -> dict:
        """Simulate provisioning."""
        logger.info(f"[MOCK] Provisioning {name} in {region} with {image} ({plan})")
        return {
            "provider_id": self._generate_mock_id(),
            "ipv4": self._generate_mock_ip(),
            "ipv6": self._generate_mock_ipv6(),
            "status": "running",
        }

    async def get_server(self, provider_id: str) -> dict:
        """Simulate getting server status."""
        logger.info(f"[MOCK] Getting status for {provider_id}")
        return {
            "id": provider_id,
            "status": "running",
            "ipv4": self._generate_mock_ip(),
            "ipv6": self._generate_mock_ipv6(),
        }

    async def destroy(self, provider_id: str) -> bool:
        """Simulate destruction."""
        logger.info(f"[MOCK] Destroying {provider_id}")
        return True

    async def reboot(self, provider_id: str) -> bool:
        """Simulate reboot."""
        logger.info(f"[MOCK] Rebooting {provider_id}")
        return True

    async def power_on(self, provider_id: str) -> bool:
        """Simulate power on."""
        logger.info(f"[MOCK] Powering on {provider_id}")
        return True

    async def power_off(self, provider_id: str) -> bool:
        """Simulate power off."""
        logger.info(f"[MOCK] Powering off {provider_id}")
        return True
