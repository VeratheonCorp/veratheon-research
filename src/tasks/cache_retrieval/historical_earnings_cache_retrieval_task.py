from src.lib.supabase_cache import get_supabase_cache
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def historical_earnings_cache_retrieval_task(symbol: str, force_recompute: bool = False) -> Optional[HistoricalEarningsAnalysis]:
    """
    Cache retrieval task for historical earnings analysis.
    
    Checks Redis cache for existing historical earnings report. If found, returns cached data.
    If not found, returns None. If force_recompute is True, skips cache lookup.
    
    Args:
        symbol: Stock symbol to analyze
        force_recompute: If True, skip cache lookup and return None
        
    Returns:
        HistoricalEarningsAnalysis from cache or None if cache miss/force_recompute
    """
    if force_recompute:
        logger.info(f"Skipping cache lookup for historical earnings analysis: {symbol} (force_recompute=True)")
        return None
        
    logger.info(f"Checking cache for historical earnings analysis: {symbol}")
    
    cache = get_supabase_cache()
    cached_report = cache.get_cached_report("historical_earnings", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for historical earnings analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return HistoricalEarningsAnalysis(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for historical earnings analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None