"""Supabase client initialization and singleton management."""
import os
import logging
from typing import Optional
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client wrapper with singleton pattern."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize Supabase client.

        Args:
            url: Supabase URL (defaults to SUPABASE_URL env var)
            key: Supabase service key (defaults to SUPABASE_SERVICE_KEY env var)
        """
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_SERVICE_KEY")

        if not self.url:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not self.key:
            raise ValueError("SUPABASE_SERVICE_KEY environment variable is required")

        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        """Get or create Supabase client connection."""
        if self._client is None:
            self._client = create_client(self.url, self.key)
            logger.info(f"Supabase client initialized: {self.url}")
        return self._client

    def close(self):
        """Close Supabase connection (if needed)."""
        # Supabase Python client doesn't require explicit closing
        # but we provide this for consistency with Redis interface
        self._client = None
        logger.debug("Supabase client connection closed")

# Global client instance
_client_instance: Optional[SupabaseClient] = None

def get_supabase_client() -> Client:
    """Get or create global Supabase client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = SupabaseClient()
    return _client_instance.client

def close_supabase_client():
    """Close global Supabase client connection."""
    global _client_instance
    if _client_instance:
        _client_instance.close()
        _client_instance = None
