from src.lib.redis_cache import get_redis_cache
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def financial_statements_cache_retrieval_task(symbol: str) -> Optional[FinancialStatementsAnalysis]:
    """
    Cache retrieval task for financial statements analysis.
    
    Checks Redis cache for existing financial statements report. If found, returns cached data.
    If not found, launches the financial_statements_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        
    Returns:
        FinancialStatementsAnalysis from cache or fresh analysis
    """
    logger.info(f"Checking cache for financial statements analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("financial_statements", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for financial statements analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return FinancialStatementsAnalysis(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for financial statements analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None