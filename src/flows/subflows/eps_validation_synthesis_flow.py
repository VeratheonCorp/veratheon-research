from src.tasks.eps_validation.eps_validation_synthesis_task import eps_validation_synthesis_task
from src.tasks.cache_retrieval.eps_validation_synthesis_cache_retrieval_task import eps_validation_synthesis_cache_retrieval_task
from src.tasks.common.job_status_task import update_job_status_task
from src.research.eps_validation.eps_validation_models import EpsValidationSynthesis
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation, PeerRelativeEpsValidation, MarketSentimentEpsCheck
from src.lib.job_tracker import JobStatus
from src.lib.redis_cache import get_redis_cache
from src.lib.eps_validation_cache_utils import get_eps_validation_ttl
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

async def eps_validation_synthesis_flow(
    symbol: str,
    force_recompute: bool = False,
    historical_earnings_analysis: Optional[HistoricalEarningsAnalysis] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    management_guidance_analysis: Optional[ManagementGuidanceAnalysis] = None,
    bottom_up_eps_validation: Optional[BottomUpEpsValidation] = None,
    peer_relative_eps_validation: Optional[PeerRelativeEpsValidation] = None,
    market_sentiment_eps_check: Optional[MarketSentimentEpsCheck] = None,
    consensus_eps: Optional[float] = None,
    job_id: Optional[str] = None
) -> EpsValidationSynthesis:
    """
    Flow orchestrating EPS validation synthesis across all validation methods.

    Synthesizes results from multiple EPS validation approaches to provide a comprehensive,
    multi-method consensus validation verdict with confidence scoring.

    Args:
        symbol: Stock symbol to research
        force_recompute: Whether to force recomputation (bypasses cache when implemented)
        historical_earnings_analysis: Historical earnings patterns analysis
        earnings_projections_analysis: Independent earnings projections analysis
        management_guidance_analysis: Management guidance analysis
        bottom_up_eps_validation: Bottom-up EPS validation results
        peer_relative_eps_validation: Peer-relative EPS validation results
        market_sentiment_eps_check: Market sentiment EPS check results
        consensus_eps: Wall Street consensus EPS estimate for reference
        job_id: Optional job ID for status tracking
    Returns:
        EpsValidationSynthesis containing comprehensive multi-method validation verdict
    """

    start_time = time.time()
    logger.info(f"EPS validation synthesis flow started for {symbol}")

    # Update job status
    await update_job_status_task(job_id, JobStatus.RUNNING, "Running EPS validation synthesis analysis", "eps_validation_synthesis_flow")

    # Try to get cached result first
    cached_result = await eps_validation_synthesis_cache_retrieval_task(symbol, force_recompute)
    if cached_result is not None:
        logger.info(f"Returning cached EPS validation synthesis for {symbol}")
        await update_job_status_task(job_id, JobStatus.RUNNING, "EPS validation synthesis completed (cached)", "eps_validation_synthesis_flow")
        return cached_result

    logger.info(f"Running fresh EPS validation synthesis analysis for {symbol}")

    # Perform EPS validation synthesis
    synthesis_result: EpsValidationSynthesis = await eps_validation_synthesis_task(
        symbol=symbol,
        historical_earnings_analysis=historical_earnings_analysis,
        earnings_projections_analysis=earnings_projections_analysis,
        management_guidance_analysis=management_guidance_analysis,
        bottom_up_eps_validation=bottom_up_eps_validation,
        peer_relative_eps_validation=peer_relative_eps_validation,
        market_sentiment_eps_check=market_sentiment_eps_check,
        consensus_eps=consensus_eps
    )

    # Cache the result for future use
    cache = get_redis_cache()
    ttl = get_eps_validation_ttl("eps_validation_synthesis")
    cache.cache_report("eps_validation_synthesis", symbol, synthesis_result, ttl=ttl)

    # Update job status with completion
    verdict_message = f"EPS validation synthesis completed - {synthesis_result.overall_verdict.value} (confidence: {synthesis_result.confidence_score:.2f})"
    await update_job_status_task(job_id, JobStatus.RUNNING, verdict_message, "eps_validation_synthesis_flow")

    logger.info(f"EPS validation synthesis flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    logger.info(f"Overall verdict: {synthesis_result.overall_verdict.value}, Confidence: {synthesis_result.confidence_score:.2f}")

    return synthesis_result