"""Supabase caching utility for reporting tasks and analysis results."""
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
from src.lib.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseCache:
    """Supabase caching utility for reporting tasks and analysis results."""

    def __init__(self, default_ttl: int = 3600):
        """
        Initialize Supabase cache connection.

        Args:
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.default_ttl = default_ttl
        self._client = None

    @property
    def client(self):
        """Get Supabase client connection."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    def close(self):
        """Close connection (no-op for Supabase compatibility with Redis interface)."""
        self._client = None

    def _generate_cache_key(self, prefix: str, symbol: str, **kwargs) -> str:
        """
        Generate a cache key based on prefix, symbol, daily timestamp and optional parameters.

        Args:
            prefix: Cache key prefix (e.g., 'historical_earnings', 'financial_statements')
            symbol: Stock symbol
            **kwargs: Additional parameters to include in key generation

        Returns:
            String cache key in format: prefix:symbol:YYYYMMDD[:kwargs_hash]
        """
        # Add daily timestamp in YYYYMMDD format
        daily_timestamp = datetime.now().strftime("%Y%m%d")

        # Create a consistent hash of kwargs for cache key stability
        kwargs_str = json.dumps(kwargs, sort_keys=True) if kwargs else ""
        key_components = [prefix, symbol.upper(), daily_timestamp, kwargs_str]
        key_base = ":".join(filter(None, key_components))

        # For very long keys, use hash to keep key length reasonable
        if len(key_base) > 200:
            key_hash = hashlib.md5(key_base.encode()).hexdigest()
            return f"{prefix}:{symbol.upper()}:{daily_timestamp}:{key_hash}"

        return key_base

    def get_cached_report(self, report_type: str, symbol: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get cached report data.

        Args:
            report_type: Type of report (e.g., 'historical_earnings', 'financial_statements')
            symbol: Stock symbol
            **kwargs: Additional parameters for cache key generation

        Returns:
            Cached data as dict or None if not found
        """
        try:
            cache_key = self._generate_cache_key(f"report:{report_type}", symbol, **kwargs)

            # Query Supabase for cache entry
            response = self.client.table("research_cache")\
                .select("data, expires_at")\
                .eq("cache_key", cache_key)\
                .execute()

            if response.data and len(response.data) > 0:
                cache_entry = response.data[0]

                # Check if expired
                if cache_entry.get("expires_at"):
                    expires_at = datetime.fromisoformat(cache_entry["expires_at"])
                    if expires_at < datetime.now():
                        logger.debug(f"Cache expired for {report_type} report: {symbol}")
                        return None

                logger.info(f"Cache hit for {report_type} report: {symbol}")
                return cache_entry["data"]

            logger.debug(f"Cache miss for {report_type} report: {symbol}")
            return None

        except Exception as e:
            logger.error(f"Failed to get cached report for {symbol} ({report_type}): {str(e)}")
            return None

    def cache_report(self, report_type: str, symbol: str, data: Union[Dict[str, Any], Any], ttl: Optional[int] = None, **kwargs) -> bool:
        """
        Cache report data.

        Args:
            report_type: Type of report (e.g., 'historical_earnings', 'financial_statements')
            symbol: Stock symbol
            data: Data to cache (dict or pydantic model with model_dump method)
            ttl: Time-to-live in seconds (uses default_ttl if None)
            **kwargs: Additional parameters for cache key generation

        Returns:
            True if successful, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(f"report:{report_type}", symbol, **kwargs)

            # Handle both dict and pydantic model data
            if hasattr(data, 'model_dump'):
                cache_data = data.model_dump()
            elif isinstance(data, dict):
                cache_data = data
            else:
                cache_data = {"data": data}

            # Add metadata
            cache_data["_cache_metadata"] = {
                "cached_at": datetime.now().isoformat(),
                "cache_key": cache_key,
                "report_type": report_type,
                "symbol": symbol.upper()
            }

            ttl = ttl or self.default_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            cache_date = datetime.now().date()

            # Upsert into Supabase
            cache_entry = {
                "cache_key": cache_key,
                "cache_type": "report",
                "report_type": report_type,
                "symbol": symbol.upper(),
                "cache_date": cache_date.isoformat(),
                "expires_at": expires_at.isoformat(),
                "data": cache_data,
                "metadata": {
                    "ttl": ttl,
                    "cached_at": datetime.now().isoformat()
                }
            }

            # Use upsert to handle conflicts
            self.client.table("research_cache").upsert(
                cache_entry,
                on_conflict="cache_key"
            ).execute()

            logger.info(f"Cached {report_type} report for {symbol} (TTL: {ttl}s)")
            return True

        except Exception as e:
            logger.error(f"Failed to cache report for {symbol} ({report_type}): {str(e)}")
            return False

    def get_cached_analysis(self, analysis_type: str, symbol: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis data (for intermediate analysis results).

        Args:
            analysis_type: Type of analysis (e.g., 'historical_earnings_analysis', 'news_sentiment')
            symbol: Stock symbol
            **kwargs: Additional parameters for cache key generation

        Returns:
            Cached analysis data as dict or None if not found
        """
        try:
            cache_key = self._generate_cache_key(f"analysis:{analysis_type}", symbol, **kwargs)

            # Query Supabase for cache entry
            response = self.client.table("research_cache")\
                .select("data, expires_at")\
                .eq("cache_key", cache_key)\
                .execute()

            if response.data and len(response.data) > 0:
                cache_entry = response.data[0]

                # Check if expired
                if cache_entry.get("expires_at"):
                    expires_at = datetime.fromisoformat(cache_entry["expires_at"])
                    if expires_at < datetime.now():
                        logger.debug(f"Cache expired for {analysis_type} analysis: {symbol}")
                        return None

                logger.info(f"Cache hit for {analysis_type} analysis: {symbol}")
                return cache_entry["data"]

            logger.debug(f"Cache miss for {analysis_type} analysis: {symbol}")
            return None

        except Exception as e:
            logger.error(f"Failed to get cached analysis for {symbol} ({analysis_type}): {str(e)}")
            return None

    def cache_analysis(self, analysis_type: str, symbol: str, data: Union[Dict[str, Any], Any], ttl: Optional[int] = None, **kwargs) -> bool:
        """
        Cache analysis data (for intermediate analysis results).

        Args:
            analysis_type: Type of analysis (e.g., 'historical_earnings_analysis', 'news_sentiment')
            symbol: Stock symbol
            data: Analysis data to cache
            ttl: Time-to-live in seconds (uses default_ttl if None)
            **kwargs: Additional parameters for cache key generation

        Returns:
            True if successful, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(f"analysis:{analysis_type}", symbol, **kwargs)

            # Handle both dict and pydantic model data
            if hasattr(data, 'model_dump'):
                cache_data = data.model_dump()
            elif isinstance(data, dict):
                cache_data = data
            else:
                cache_data = {"data": data}

            # Add metadata
            cache_data["_cache_metadata"] = {
                "cached_at": datetime.now().isoformat(),
                "cache_key": cache_key,
                "analysis_type": analysis_type,
                "symbol": symbol.upper()
            }

            ttl = ttl or self.default_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            cache_date = datetime.now().date()

            # Upsert into Supabase
            cache_entry = {
                "cache_key": cache_key,
                "cache_type": "analysis",
                "report_type": analysis_type,
                "symbol": symbol.upper(),
                "cache_date": cache_date.isoformat(),
                "expires_at": expires_at.isoformat(),
                "data": cache_data,
                "metadata": {
                    "ttl": ttl,
                    "cached_at": datetime.now().isoformat()
                }
            }

            # Use upsert to handle conflicts
            self.client.table("research_cache").upsert(
                cache_entry,
                on_conflict="cache_key"
            ).execute()

            logger.info(f"Cached {analysis_type} analysis for {symbol} (TTL: {ttl}s)")
            return True

        except Exception as e:
            logger.error(f"Failed to cache analysis for {symbol} ({analysis_type}): {str(e)}")
            return False

    def invalidate_cache(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.

        Args:
            pattern: Cache key pattern (supports SQL LIKE wildcards: % and _)

        Returns:
            Number of keys deleted
        """
        try:
            # Convert Redis wildcard pattern to SQL LIKE pattern
            sql_pattern = pattern.replace("*", "%")

            # Delete matching entries
            response = self.client.table("research_cache")\
                .delete()\
                .like("cache_key", sql_pattern)\
                .execute()

            deleted_count = len(response.data) if response.data else 0
            logger.info(f"Invalidated {deleted_count} cache entries matching pattern: {pattern}")
            return deleted_count

        except Exception as e:
            logger.error(f"Failed to invalidate cache with pattern {pattern}: {str(e)}")
            return 0

    def get_cache_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get cache information and statistics.

        Args:
            symbol: Optional symbol to filter results

        Returns:
            Dictionary with cache statistics
        """
        try:
            query = self.client.table("research_cache").select("cache_key, cache_type, symbol, created_at, expires_at")

            if symbol:
                query = query.eq("symbol", symbol.upper())

            response = query.limit(100).execute()

            cache_keys = [item["cache_key"] for item in response.data] if response.data else []

            info = {
                "total_cached_items": len(cache_keys),
                "keys": cache_keys,
                "entries": response.data[:100] if response.data else []
            }

            if response.data and len(response.data) >= 100:
                info["keys_truncated"] = True

            return info

        except Exception as e:
            logger.error(f"Failed to get cache info: {str(e)}")
            return {"error": str(e)}

# Global cache instance
_cache_instance = None

def get_supabase_cache() -> SupabaseCache:
    """Get or create global Supabase cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = SupabaseCache()
    return _cache_instance

# Alias for compatibility with Redis cache interface
def get_redis_cache() -> SupabaseCache:
    """Get or create global cache instance (Supabase-backed)."""
    return get_supabase_cache()

def close_supabase_cache():
    """Close global Supabase cache connection."""
    global _cache_instance
    if _cache_instance:
        _cache_instance.close()
        _cache_instance = None
