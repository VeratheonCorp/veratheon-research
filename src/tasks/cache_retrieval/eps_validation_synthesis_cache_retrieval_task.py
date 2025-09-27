from src.lib.redis_cache import get_redis_cache
from src.research.eps_validation.eps_validation_models import EpsValidationSynthesis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def eps_validation_synthesis_cache_retrieval_task(symbol: str, force_recompute: bool = False) -> Optional[EpsValidationSynthesis]:
    """
    Cache retrieval task for EPS validation synthesis analysis.

    Checks Redis cache for existing EPS validation synthesis report. If found, returns cached data.
    If not found, returns None. If force_recompute is True, skips cache lookup.

    Args:
        symbol: Stock symbol to analyze
        force_recompute: If True, skip cache lookup and return None

    Returns:
        EpsValidationSynthesis from cache or None if cache miss/force_recompute
    """
    if force_recompute:
        logger.info(f"Skipping cache lookup for EPS validation synthesis: {symbol} (force_recompute=True)")
        return None

    logger.info(f"Checking cache for EPS validation synthesis: {symbol}")

    cache = get_redis_cache()
    cached_report = cache.get_cached_report("eps_validation_synthesis", symbol)

    if cached_report:
        logger.info(f"Cache hit for EPS validation synthesis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return EpsValidationSynthesis(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached EPS validation synthesis data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for EPS validation synthesis: {symbol}")

    # Cache miss or reconstruction failed
    return None