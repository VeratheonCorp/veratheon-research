"""
Utility functions for EPS validation cache management.

Provides cache invalidation and TTL configuration specifically for EPS validation components.
"""

from src.lib.redis_cache import get_redis_cache
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# EPS validation specific TTL configurations (in seconds)
EPS_VALIDATION_TTL_CONFIG = {
    "bottom_up_eps_validation": 7200,      # 2 hours - depends on financial data freshness
    "peer_relative_eps_validation": 7200,   # 2 hours - depends on peer group PE ratios
    "market_sentiment_eps_check": 3600,     # 1 hour - sentiment data changes more frequently
    "eps_validation_synthesis": 7200,       # 2 hours - synthesis of above components
    # TEMPLATE: Add new validation methods here
    "technical_eps_validation": 1800,       # 30 minutes - technical data changes frequently
}

def get_eps_validation_ttl(validation_type: str) -> int:
    """
    Get TTL configuration for specific EPS validation type.

    Args:
        validation_type: Type of EPS validation (e.g., 'bottom_up_eps_validation')

    Returns:
        TTL in seconds, defaults to 2 hours if type not found
    """
    return EPS_VALIDATION_TTL_CONFIG.get(validation_type, 7200)

def invalidate_eps_validation_cache(symbol: str, validation_types: Optional[List[str]] = None) -> int:
    """
    Invalidate EPS validation cache entries for a symbol.

    Args:
        symbol: Stock symbol to invalidate cache for
        validation_types: List of specific validation types to invalidate,
                         or None to invalidate all EPS validation types

    Returns:
        Number of cache entries invalidated
    """
    cache = get_redis_cache()
    total_invalidated = 0

    # Default to all EPS validation types if none specified
    if validation_types is None:
        validation_types = list(EPS_VALIDATION_TTL_CONFIG.keys())

    for validation_type in validation_types:
        pattern = f"report:{validation_type}:{symbol.upper()}:*"
        invalidated = cache.invalidate_cache(pattern)
        total_invalidated += invalidated

        if invalidated > 0:
            logger.info(f"Invalidated {invalidated} cache entries for {validation_type}:{symbol}")

    logger.info(f"Total EPS validation cache entries invalidated for {symbol}: {total_invalidated}")
    return total_invalidated

def invalidate_all_eps_validation_cache() -> int:
    """
    Invalidate all EPS validation cache entries across all symbols.

    Returns:
        Number of cache entries invalidated
    """
    cache = get_redis_cache()
    total_invalidated = 0

    for validation_type in EPS_VALIDATION_TTL_CONFIG.keys():
        pattern = f"report:{validation_type}:*"
        invalidated = cache.invalidate_cache(pattern)
        total_invalidated += invalidated

        if invalidated > 0:
            logger.info(f"Invalidated {invalidated} cache entries for {validation_type}")

    logger.info(f"Total EPS validation cache entries invalidated: {total_invalidated}")
    return total_invalidated

def get_eps_validation_cache_info(symbol: Optional[str] = None) -> dict:
    """
    Get cache information for EPS validation components.

    Args:
        symbol: Optional symbol to filter results

    Returns:
        Dictionary with EPS validation cache statistics
    """
    cache = get_redis_cache()

    if symbol:
        pattern = f"report:*eps*:{symbol.upper()}:*"
    else:
        pattern = "report:*eps*:*"

    # Get basic cache info
    info = cache.get_cache_info(symbol)

    # Add EPS validation specific information
    info["eps_validation_ttl_config"] = EPS_VALIDATION_TTL_CONFIG
    info["eps_validation_types"] = list(EPS_VALIDATION_TTL_CONFIG.keys())

    return info