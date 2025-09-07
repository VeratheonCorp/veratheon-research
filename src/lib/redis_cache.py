import redis
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
import hashlib

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis caching utility for reporting tasks and analysis results."""
    
    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 3600):
        """
        Initialize Redis cache connection.
        
        Args:
            redis_url: Redis connection URL (defaults to REDIS_URL env var)
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.default_ttl = default_ttl
        self._client = None
    
    @property
    def client(self) -> redis.Redis:
        """Get or create Redis client connection."""
        if self._client is None:
            self._client = redis.from_url(self.redis_url, decode_responses=True)
        return self._client
    
    def close(self):
        """Close Redis connection."""
        if self._client:
            self._client.close()
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
            cached_data = self.client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for {report_type} report: {symbol}")
                return json.loads(cached_data)
            
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
            result = self.client.setex(cache_key, ttl, json.dumps(cache_data))
            
            if result:
                logger.info(f"Cached {report_type} report for {symbol} (TTL: {ttl}s)")
                return True
            else:
                logger.warning(f"Failed to cache {report_type} report for {symbol}")
                return False
                
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
            cached_data = self.client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for {analysis_type} analysis: {symbol}")
                return json.loads(cached_data)
            
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
            result = self.client.setex(cache_key, ttl, json.dumps(cache_data))
            
            if result:
                logger.info(f"Cached {analysis_type} analysis for {symbol} (TTL: {ttl}s)")
                return True
            else:
                logger.warning(f"Failed to cache {analysis_type} analysis for {symbol}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to cache analysis for {symbol} ({analysis_type}): {str(e)}")
            return False
    
    def invalidate_cache(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.
        
        Args:
            pattern: Redis key pattern (supports wildcards)
        
        Returns:
            Number of keys deleted
        """
        try:
            keys = self.client.keys(pattern)
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"Invalidated {deleted} cache entries matching pattern: {pattern}")
                return deleted
            else:
                logger.debug(f"No cache entries found matching pattern: {pattern}")
                return 0
                
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
            pattern = f"*:{symbol.upper()}:*" if symbol else "*"
            keys = self.client.keys(pattern)
            
            info = {
                "total_cached_items": len(keys),
                "redis_info": self.client.info(),
                "keys": keys[:100]  # Limit to first 100 keys to avoid overwhelming output
            }
            
            if len(keys) > 100:
                info["keys_truncated"] = True
                info["total_keys"] = len(keys)
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get cache info: {str(e)}")
            return {"error": str(e)}

# Global cache instance
_cache_instance = None

def get_redis_cache() -> RedisCache:
    """Get or create global Redis cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
    return _cache_instance

def close_redis_cache():
    """Close global Redis cache connection."""
    global _cache_instance
    if _cache_instance:
        _cache_instance.close()
        _cache_instance = None