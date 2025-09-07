from src.lib.redis_cache import get_redis_cache
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def management_guidance_cache_retrieval_task(
    symbol: str, 
    historical_earnings_analysis: HistoricalEarningsAnalysis,
    financial_statements_analysis: FinancialStatementsAnalysis
) -> Optional[ManagementGuidanceAnalysis]:
    """
    Cache retrieval task for management guidance analysis.
    
    Checks Redis cache for existing management guidance report. If found, returns cached data.
    If not found, launches the management_guidance_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        historical_earnings_analysis: Historical earnings analysis context
        financial_statements_analysis: Financial statements analysis context
        
    Returns:
        ManagementGuidanceAnalysis from cache or fresh analysis
    """
    logger.info(f"Checking cache for management guidance analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("management_guidance", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for management guidance analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return ManagementGuidanceAnalysis(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for management guidance analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None