from src.tasks.eps_validation.market_sentiment_eps_check_task import market_sentiment_eps_check_task
from src.tasks.cache_retrieval.market_sentiment_eps_check_cache_retrieval_task import market_sentiment_eps_check_cache_retrieval_task
from src.tasks.common.job_status_task import update_job_status_task
from src.research.eps_validation.eps_validation_models import MarketSentimentEpsCheck
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.lib.job_tracker import JobStatus
from src.lib.redis_cache import get_redis_cache
from src.lib.eps_validation_cache_utils import get_eps_validation_ttl
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

async def market_sentiment_eps_check_flow(
    symbol: str,
    force_recompute: bool = False,
    news_sentiment_analysis: Optional[NewsSentimentSummary] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    management_guidance_analysis: Optional[ManagementGuidanceAnalysis] = None,
    consensus_eps: Optional[float] = None,
    job_id: Optional[str] = None
) -> MarketSentimentEpsCheck:
    """
    Flow orchestrating sentiment EPS validation using market sentiment and revision analysis.

    Analyzes sentiment alignment with EPS expectations, revision momentum trends,
    and whisper numbers to validate consensus estimates through market sentiment.

    Args:
        symbol: Stock symbol to research
        force_recompute: Whether to force recomputation (bypasses cache when implemented)
        news_sentiment_analysis: Analyzed news sentiment data for market sentiment context
        earnings_projections_analysis: Independent earnings projections for revision context
        management_guidance_analysis: Management guidance analysis for whisper number context
        consensus_eps: Wall Street consensus EPS estimate for validation
        job_id: Optional job ID for status tracking
    Returns:
        MarketSentimentEpsCheck containing sentiment-based EPS validation results
    """

    start_time = time.time()
    logger.info(f"Market sentiment EPS check flow started for {symbol}")

    # Update job status
    await update_job_status_task(job_id, JobStatus.RUNNING, "Running market sentiment EPS validation analysis", "market_sentiment_eps_check_flow")

    # Try to get cached result first
    cached_result = await market_sentiment_eps_check_cache_retrieval_task(symbol, force_recompute)
    if cached_result is not None:
        logger.info(f"Returning cached market sentiment EPS check for {symbol}")
        await update_job_status_task(job_id, JobStatus.RUNNING, "Market sentiment EPS check completed (cached)", "market_sentiment_eps_check_flow")
        return cached_result

    logger.info(f"Running fresh market sentiment EPS check analysis for {symbol}")

    # Perform market sentiment EPS check
    validation_result: MarketSentimentEpsCheck = await market_sentiment_eps_check_task(
        symbol=symbol,
        news_sentiment_analysis=news_sentiment_analysis,
        earnings_projections_analysis=earnings_projections_analysis,
        management_guidance_analysis=management_guidance_analysis,
        consensus_eps=consensus_eps
    )

    # Cache the result for future use
    cache = get_redis_cache()
    ttl = get_eps_validation_ttl("market_sentiment_eps_check")
    cache.cache_report("market_sentiment_eps_check", symbol, validation_result, ttl=ttl)

    # Update job status with completion
    verdict_message = f"Market sentiment EPS check completed - {validation_result.sentiment_validation_verdict.value}"
    await update_job_status_task(job_id, JobStatus.RUNNING, verdict_message, "market_sentiment_eps_check_flow")

    logger.info(f"Market sentiment EPS check flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    logger.info(f"Validation verdict: {validation_result.sentiment_validation_verdict.value}")

    return validation_result