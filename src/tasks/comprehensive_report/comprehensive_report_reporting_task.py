from src.lib.redis_cache import get_redis_cache
from src.research.comprehensive_report.comprehensive_report_models import ComprehensiveReport
import logging

logger = logging.getLogger(__name__)

async def comprehensive_report_reporting_task(symbol: str, comprehensive_report: ComprehensiveReport) -> None:
    """
    Reporting task for comprehensive report analysis.
    
    Caches the comprehensive report results to Redis for future retrieval.
    
    Args:
        symbol: Stock symbol analyzed
        comprehensive_report: ComprehensiveReport model with analysis results
    """
    logger.info(f"Caching comprehensive report results for {symbol}")
    
    cache = get_redis_cache()
    success = cache.cache_report(
        "comprehensive_report", 
        symbol, 
        comprehensive_report,
        ttl=24*60*60  # 24 hours
    )
    
    if success:
        logger.info(f"Successfully cached comprehensive report for {symbol}")
    else:
        logger.warning(f"Failed to cache comprehensive report for {symbol}")
        
    # Note: We don't raise exceptions here because caching failure 
    # shouldn't break the analysis flow