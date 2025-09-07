from src.lib.redis_cache import get_redis_cache
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.common.models.peer_group import PeerGroup
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def news_sentiment_cache_retrieval_task(
    symbol: str, 
    peer_group: PeerGroup,
    earnings_projections_analysis: EarningsProjectionAnalysis,
    management_guidance_analysis: ManagementGuidanceAnalysis
) -> Optional[NewsSentimentSummary]:
    """
    Cache retrieval task for news sentiment analysis.
    
    Checks Redis cache for existing news sentiment report. If found, returns cached data.
    If not found, launches the news_sentiment_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        peer_group: Peer group analysis context
        earnings_projections_analysis: Earnings projections analysis context
        management_guidance_analysis: Management guidance analysis context
        
    Returns:
        NewsSentimentSummary from cache or fresh analysis
    """
    logger.info(f"Checking cache for news sentiment analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("news_sentiment", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for news sentiment analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return NewsSentimentSummary(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for news sentiment analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None