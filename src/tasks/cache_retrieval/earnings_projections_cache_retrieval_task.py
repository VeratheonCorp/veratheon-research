from src.lib.redis_cache import get_redis_cache
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

async def earnings_projections_cache_retrieval_task(
    symbol: str, 
    historical_earnings_context: Dict[str, Any], 
    financial_statements_context: Dict[str, Any]
) -> Optional[EarningsProjectionAnalysis]:
    """
    Cache retrieval task for earnings projections analysis.
    
    Checks Redis cache for existing earnings projections report. If found, returns cached data.
    If not found, launches the earnings_projections_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        historical_earnings_context: Historical earnings analysis context
        financial_statements_context: Financial statements analysis context
        
    Returns:
        EarningsProjectionAnalysis from cache or fresh analysis
    """
    logger.info(f"Checking cache for earnings projections analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("earnings_projections", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for earnings projections analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return EarningsProjectionAnalysis(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for earnings projections analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None