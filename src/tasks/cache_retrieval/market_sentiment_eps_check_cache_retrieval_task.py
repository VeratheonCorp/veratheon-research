import logging
from typing import Optional

from src.lib.redis_cache import get_redis_cache
from src.research.eps_validation.eps_validation_models import MarketSentimentEpsCheck

logger = logging.getLogger(__name__)


async def market_sentiment_eps_check_cache_retrieval_task(
    symbol: str, force_recompute: bool = False
) -> Optional[MarketSentimentEpsCheck]:
    """
    Cache retrieval task for market sentiment EPS check analysis.

    Checks Redis cache for existing market sentiment EPS check report. If found, returns cached data.
    If not found, returns None. If force_recompute is True, skips cache lookup.

    Args:
        symbol: Stock symbol to analyze
        force_recompute: If True, skip cache lookup and return None

    Returns:
        MarketSentimentEpsCheck from cache or None if cache miss/force_recompute
    """
    if force_recompute:
        logger.info(
            f"Skipping cache lookup for market sentiment EPS check: {symbol} (force_recompute=True)"
        )
        return None

    logger.info(f"Checking cache for market sentiment EPS check: {symbol}")

    cache = get_redis_cache()
    cached_report = cache.get_cached_report("market_sentiment_eps_check", symbol)

    if cached_report:
        logger.info(f"Cache hit for market sentiment EPS check: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {
            k: v for k, v in cached_report.items() if not k.startswith("_cache_")
        }
        try:
            return MarketSentimentEpsCheck(**clean_data)
        except Exception as e:
            logger.warning(
                f"Failed to reconstruct cached market sentiment EPS check data for {symbol}, falling back to fresh analysis: {str(e)}"
            )
    else:
        logger.info(f"Cache miss for market sentiment EPS check: {symbol}")

    # Cache miss or reconstruction failed
    return None
