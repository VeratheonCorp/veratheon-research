from src.lib.redis_cache import get_redis_cache
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def bottom_up_eps_validation_cache_retrieval_task(symbol: str, force_recompute: bool = False) -> Optional[BottomUpEpsValidation]:
    """
    Cache retrieval task for bottom-up EPS validation analysis.

    Checks Redis cache for existing bottom-up EPS validation report. If found, returns cached data.
    If not found, returns None. If force_recompute is True, skips cache lookup.

    Args:
        symbol: Stock symbol to analyze
        force_recompute: If True, skip cache lookup and return None

    Returns:
        BottomUpEpsValidation from cache or None if cache miss/force_recompute
    """
    if force_recompute:
        logger.info(f"Skipping cache lookup for bottom-up EPS validation: {symbol} (force_recompute=True)")
        return None

    logger.info(f"Checking cache for bottom-up EPS validation: {symbol}")

    cache = get_redis_cache()
    cached_report = cache.get_cached_report("bottom_up_eps_validation", symbol)

    if cached_report:
        logger.info(f"Cache hit for bottom-up EPS validation: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return BottomUpEpsValidation(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached bottom-up EPS validation data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for bottom-up EPS validation: {symbol}")

    # Cache miss or reconstruction failed
    return None