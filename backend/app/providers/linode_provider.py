"""Linode provider implementation for real cloud provisioning."""

import logging
import os
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

# Linode API configuration
LINODE_API_URL = "https://api.linode.com/v4"

# Region mapping: Linode region ID -> Shaheen region label
REGION_MAP = {
    "us-east": "us-east-1",
    "us-west": "us-west-1",
    "eu-west": "eu-central-1",
    "ap-south": "ap-south-1",
    "ap-southeast": "ap-south-1",
    "ca-central": "us-east-1",
}

# Instance type mapping: Linode type ID -> plan
TYPE_MAP = {
    "g6-nanode-1": "micro",
    "g6-standard-1": "small",
    "g6-standard-2": "medium",
    "g6-standard-4": "large",
    "g6-standard-6": "xlarge",
}

REVERSE_TYPE_MAP = {
    "micro": "g6-nanode-1",
    "small": "g6-standard-1",
    "medium": "g6-standard-2",
    "large": "g6-standard-4",
    "xlarge": "g6-standard-6",
}

# Ubuntu image mapping
UBUNTU_IMAGES = {
    "ubuntu-24.04": "linode/ubuntu24.04",
    "ubuntu-22.04": "linode/ubuntu22.04",
}


class LinodeProviderError(Exception):
    """Linode provider error."""
    pass


class LinodeProvider:
    """Linode cloud provider implementation."""

    def __init__(self, api_token: Optional[str] = None):
        """Initialize Linode provider.
        
        Args:
            api_token: Linode API token. If None, reads from LINODE_API_TOKEN env var.
            
        Raises:
            LinodeProviderError: If API token is missing.
        """
        self.api_token = api_token or os.getenv("LINODE_API_TOKEN")
        if not self.api_token:
            raise LinodeProviderError(
                "LINODE_API_TOKEN environment variable is required for Linode provider"
            )
        
        self.client = httpx.Client(
            base_url=LINODE_API_URL,
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=30.0,
        )

    def __del__(self):
        """Cleanup HTTP client."""
        if hasattr(self, "client"):
            self.client.close()

    async def list_regions(self) -> list[dict]:
        """List available Linode regions.
        
        Returns:
            List of region dicts with id, label, country.
        """
        try:
            response = self.client.get("/regions")
            response.raise_for_status()
            regions = response.json().get("data", [])
            
            result = []
            for region in regions:
                shaheen_id = REGION_MAP.get(region["id"], region["id"])
                result.append({
                    "id": shaheen_id,
                    "label": region["label"],
                    "country": region.get("country", "Unknown"),
                })
            return result
        except Exception as e:
            logger.error(f"Failed to list Linode regions: {e}")
            raise LinodeProviderError(f"Failed to list regions: {e}")

    async def list_server_types(self) -> list[dict]:
        """List available Linode server types.
        
        Returns:
            List of type dicts with id, label, vcpus, memory, disk.
        """
        try:
            response = self.client.get("/linode/types")
            response.raise_for_status()
            types = response.json().get("data", [])
            
            result = []
            for t in types:
                if t["id"] in REVERSE_TYPE_MAP.values():
                    result.append({
                        "id": t["id"],
                        "label": t["label"],
                        "vcpus": t["vcpus"],
                        "memory": t["memory"],
                        "disk": t["disk"],
                    })
            return result
        except Exception as e:
            logger.error(f"Failed to list Linode types: {e}")
            raise LinodeProviderError(f"Failed to list server types: {e}")

    async def list_images(self) -> list[dict]:
        """List available Ubuntu images.
        
        Returns:
            List of image dicts with id, label.
        """
        try:
            response = self.client.get("/images?type=public")
            response.raise_for_status()
            images = response.json().get("data", [])
            
            result = []
            for img in images:
                if "ubuntu" in img["id"].lower():
                    result.append({
                        "id": img["id"],
                        "label": img["label"],
                        "version": img.get("version", "unknown"),
                    })
            return result
        except Exception as e:
            logger.error(f"Failed to list Linode images: {e}")
            raise LinodeProviderError(f"Failed to list images: {e}")

    async def create_server(
        self,
        name: str,
        region: str,
        image: str,
        plan: str,
    ) -> dict:
        """Create a new Linode instance.
        
        Args:
            name: Server name/label.
            region: Shaheen region ID (e.g., 'us-east-1').
            image: Ubuntu image ID (e.g., 'ubuntu-24.04').
            plan: Server plan (e.g., 'small').
            
        Returns:
            Dict with provider_id, ipv4, ipv6, status.
            
        Raises:
            LinodeProviderError: If provisioning fails.
        """
        # Map Shaheen IDs to Linode IDs
        linode_region = None
        for linode_id, shaheen_id in REGION_MAP.items():
            if shaheen_id == region:
                linode_region = linode_id
                break
        if not linode_region:
            raise LinodeProviderError(f"Unknown region: {region}")
        
        linode_image = UBUNTU_IMAGES.get(image)
        if not linode_image:
            raise LinodeProviderError(f"Unknown image: {image}")
        
        linode_type = REVERSE_TYPE_MAP.get(plan)
        if not linode_type:
            raise LinodeProviderError(f"Unknown plan: {plan}")
        
        logger.info(f"[Linode] Creating instance: {name} in {linode_region} with {linode_type}")
        
        payload = {
            "label": name,
            "region": linode_region,
            "type": linode_type,
            "image": linode_image,
            "root_pass": os.urandom(16).hex(),  # Generate random root password
            "authorized_keys": [],
        }
        
        try:
            response = self.client.post("/linode/instances", json=payload)
            response.raise_for_status()
            instance = response.json()
            
            provider_id = str(instance["id"])
            ipv4 = None
            ipv6 = None
            
            # Extract IPs if available
            if "ipv4" in instance and instance["ipv4"]:
                ipv4 = instance["ipv4"][0]
            if "ipv6" in instance and instance["ipv6"]:
                ipv6 = instance["ipv6"]
            
            logger.info(f"[Linode] Instance created: {provider_id}")
            
            return {
                "provider_id": provider_id,
                "ipv4": ipv4,
                "ipv6": ipv6,
                "status": instance.get("status", "provisioning"),
            }
        except httpx.HTTPError as e:
            logger.error(f"[Linode] HTTP error creating instance: {e}")
            error_msg = str(e)
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_msg = e.response.json().get("errors", [{}])[0].get("field", error_msg)
                except Exception:
                    pass
            raise LinodeProviderError(f"Failed to create instance: {error_msg}")

    async def get_server(self, provider_id: str) -> dict:
        """Get server details.
        
        Args:
            provider_id: Linode instance ID.
            
        Returns:
            Dict with id, status, ipv4, ipv6.
            
        Raises:
            LinodeProviderError: If server not found or API error.
        """
        try:
            response = self.client.get(f"/linode/instances/{provider_id}")
            response.raise_for_status()
            instance = response.json()
            
            ipv4 = None
            ipv6 = None
            if "ipv4" in instance and instance["ipv4"]:
                ipv4 = instance["ipv4"][0]
            if "ipv6" in instance and instance["ipv6"]:
                ipv6 = instance["ipv6"]
            
            return {
                "id": str(instance["id"]),
                "status": instance.get("status", "unknown"),
                "ipv4": ipv4,
                "ipv6": ipv6,
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise LinodeProviderError(f"Instance not found: {provider_id}")
            logger.error(f"[Linode] Error getting instance {provider_id}: {e}")
            raise LinodeProviderError(f"Failed to get instance: {e}")

    async def delete_server(self, provider_id: str) -> bool:
        """Delete a Linode instance.
        
        Args:
            provider_id: Linode instance ID.
            
        Returns:
            True if deletion succeeded.
            
        Raises:
            LinodeProviderError: If deletion fails.
        """
        try:
            logger.info(f"[Linode] Deleting instance: {provider_id}")
            response = self.client.delete(f"/linode/instances/{provider_id}")
            response.raise_for_status()
            logger.info(f"[Linode] Instance deleted: {provider_id}")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"[Linode] Instance not found (already deleted?): {provider_id}")
                return True
            logger.error(f"[Linode] Error deleting instance {provider_id}: {e}")
            raise LinodeProviderError(f"Failed to delete instance: {e}")

    async def reboot_server(self, provider_id: str) -> bool:
        """Reboot a Linode instance.
        
        Args:
            provider_id: Linode instance ID.
            
        Returns:
            True if reboot initiated.
            
        Raises:
            LinodeProviderError: If reboot fails.
        """
        try:
            logger.info(f"[Linode] Rebooting instance: {provider_id}")
            response = self.client.post(f"/linode/instances/{provider_id}/reboot")
            response.raise_for_status()
            logger.info(f"[Linode] Reboot initiated: {provider_id}")
            return True
        except Exception as e:
            logger.error(f"[Linode] Error rebooting instance {provider_id}: {e}")
            raise LinodeProviderError(f"Failed to reboot instance: {e}")

    async def power_on_server(self, provider_id: str) -> bool:
        """Power on a Linode instance.
        
        Args:
            provider_id: Linode instance ID.
            
        Returns:
            True if power-on initiated.
        """
        try:
            logger.info(f"[Linode] Powering on instance: {provider_id}")
            response = self.client.post(f"/linode/instances/{provider_id}/boot")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"[Linode] Error powering on instance {provider_id}: {e}")
            raise LinodeProviderError(f"Failed to power on instance: {e}")

    async def power_off_server(self, provider_id: str) -> bool:
        """Power off a Linode instance.
        
        Args:
            provider_id: Linode instance ID.
            
        Returns:
            True if power-off initiated.
        """
        try:
            logger.info(f"[Linode] Powering off instance: {provider_id}")
            response = self.client.post(f"/linode/instances/{provider_id}/shutdown")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"[Linode] Error powering off instance {provider_id}: {e}")
            raise LinodeProviderError(f"Failed to power off instance: {e}")
