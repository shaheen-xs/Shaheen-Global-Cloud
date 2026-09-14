"""Provider factory for selecting and instantiating cloud providers."""

import logging
from typing import Optional
from app.config import get_settings
from app.providers.base import BaseProvider, MockProvider
from app.providers.linode_provider import LinodeProvider, LinodeProviderError

logger = logging.getLogger(__name__)

_provider_instance: Optional[BaseProvider] = None


class ProviderFactory:
    """Factory for creating provider instances."""
    
    @staticmethod
    def create_provider(provider_type: Optional[str] = None) -> BaseProvider:
        """Create and return a provider instance.
        
        Args:
            provider_type: Provider type (mock, linode). If None, reads from config.
            
        Returns:
            Provider instance.
            
        Raises:
            ValueError: If provider type is invalid or credentials are missing.
        """
        settings = get_settings()
        prov_type = provider_type or settings.PROVIDER_TYPE
        
        logger.info(f"Creating provider: {prov_type}")
        
        if prov_type == "mock":
            return MockProvider()
        
        elif prov_type == "linode":
            try:
                return LinodeProvider(settings.LINODE_API_TOKEN)
            except LinodeProviderError as e:
                logger.error(f"Failed to initialize Linode provider: {e}")
                raise ValueError(f"Linode provider initialization failed: {e}")
        
        else:
            raise ValueError(f"Unknown provider type: {prov_type}")
    
    @staticmethod
    def get_provider(provider_type: Optional[str] = None) -> BaseProvider:
        """Get or create a singleton provider instance.
        
        Args:
            provider_type: Provider type. If None, reads from config.
            
        Returns:
            Provider instance.
        """
        global _provider_instance
        
        settings = get_settings()
        prov_type = provider_type or settings.PROVIDER_TYPE
        
        # Reset provider if type changed
        if _provider_instance is not None:
            current_type = type(_provider_instance).__name__
            expected_type = "MockProvider" if prov_type == "mock" else "LinodeProvider"
            if current_type != expected_type:
                _provider_instance = None
        
        if _provider_instance is None:
            _provider_instance = ProviderFactory.create_provider(prov_type)
        
        return _provider_instance
    
    @staticmethod
    def reset_provider() -> None:
        """Reset the singleton provider instance."""
        global _provider_instance
        _provider_instance = None
