from src.lib.supabase_cache import get_supabase_cache
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def management_guidance_cache_retrieval_task(
    symbol: str, 
    historical_earnings_analysis: HistoricalEarningsAnalysis,
    financial_statements_analysis: FinancialStatementsAnalysis,
    force_recompute: bool = False
) -> Optional[ManagementGuidanceAnalysis]:
    """
    Cache retrieval task for management guidance analysis.
    
    Checks Redis cache for existing management guidance report. If found, returns cached data.
    If not found, returns None. If force_recompute is True, skips cache lookup.
    
    Args:
        symbol: Stock symbol to analyze
        historical_earnings_analysis: Historical earnings analysis context
        financial_statements_analysis: Financial statements analysis context
        force_recompute: If True, skip cache lookup and return None
        
    Returns:
        ManagementGuidanceAnalysis from cache or None if cache miss/force_recompute
    """
    if force_recompute:
        logger.info(f"Skipping cache lookup for management guidance analysis: {symbol} (force_recompute=True)")
        return None
        
    logger.info(f"Checking cache for management guidance analysis: {symbol}")
    
    cache = get_supabase_cache()
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