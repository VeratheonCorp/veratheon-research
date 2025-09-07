from src.lib.redis_cache import get_redis_cache
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
from src.research.common.models.peer_group import PeerGroup
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def forward_pe_sanity_check_cache_retrieval_task(symbol: str) -> Optional[ForwardPeSanityCheck]:
    """
    Cache retrieval task for forward PE sanity check analysis.
    
    Checks Redis cache for existing forward PE sanity check report. If found, returns cached data.
    If not found, launches the forward_pe_sanity_check_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        
    Returns:
        ForwardPeSanityCheck from cache or fresh analysis
    """
    logger.info(f"Checking cache for forward PE sanity check analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("forward_pe_sanity_check", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for forward PE sanity check analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return ForwardPeSanityCheck(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for forward PE sanity check analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None

async def forward_pe_valuation_cache_retrieval_task(
    symbol: str, 
    peer_group: PeerGroup,
    earnings_projections_analysis: EarningsProjectionAnalysis,
    management_guidance_analysis: ManagementGuidanceAnalysis,
    forward_pe_sanity_check: ForwardPeSanityCheck
) -> Optional[ForwardPeValuation]:
    """
    Cache retrieval task for forward PE valuation analysis.
    
    Checks Redis cache for existing forward PE valuation report. If found, returns cached data.
    If not found, launches the forward_pe_flow to generate fresh analysis.
    
    Args:
        symbol: Stock symbol to analyze
        peer_group: Peer group analysis context
        earnings_projections_analysis: Earnings projections analysis context
        management_guidance_analysis: Management guidance analysis context
        forward_pe_sanity_check: Forward PE sanity check analysis context
        
    Returns:
        ForwardPeValuation from cache or fresh analysis
    """
    logger.info(f"Checking cache for forward PE valuation analysis: {symbol}")
    
    cache = get_redis_cache()
    cached_report = cache.get_cached_report("forward_pe_valuation", symbol)
    
    if cached_report:
        logger.info(f"Cache hit for forward PE valuation analysis: {symbol}")
        # Remove cache metadata for clean model reconstruction
        clean_data = {k: v for k, v in cached_report.items() if not k.startswith('_cache_')}
        try:
            return ForwardPeValuation(**clean_data)
        except Exception as e:
            logger.warning(f"Failed to reconstruct cached data for {symbol}, falling back to fresh analysis: {str(e)}")
    else:
        logger.info(f"Cache miss for forward PE valuation analysis: {symbol}")
    
    # Cache miss or reconstruction failed
    return None