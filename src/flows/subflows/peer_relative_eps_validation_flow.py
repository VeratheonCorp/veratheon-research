from src.tasks.eps_validation.peer_relative_eps_validation_task import peer_relative_eps_validation_task
from src.tasks.cache_retrieval.peer_relative_eps_validation_cache_retrieval_task import peer_relative_eps_validation_cache_retrieval_task
from src.tasks.common.job_status_task import update_job_status_task
from src.research.eps_validation.eps_validation_models import PeerRelativeEpsValidation
from src.research.common.models.peer_group import PeerGroup
from src.research.forward_pe.forward_pe_models import ForwardPEEarningsSummary
from src.lib.job_tracker import JobStatus
from src.lib.redis_cache import get_redis_cache
from src.lib.eps_validation_cache_utils import get_eps_validation_ttl
from typing import Optional, List
import logging
import time

logger = logging.getLogger(__name__)

async def peer_relative_eps_validation_flow(
    symbol: str,
    force_recompute: bool = False,
    current_stock_price: Optional[float] = None,
    peer_group: Optional[PeerGroup] = None,
    peer_earnings_data: Optional[List[ForwardPEEarningsSummary]] = None,
    consensus_eps: Optional[float] = None,
    job_id: Optional[str] = None
) -> PeerRelativeEpsValidation:
    """
    Flow orchestrating peer-relative EPS validation using peer group forward P/E ratios.

    Calculates implied EPS from current stock price and peer average forward P/E
    to validate consensus estimates through peer comparison analysis.

    Args:
        symbol: Stock symbol to research
        force_recompute: Whether to force recomputation (bypasses cache when implemented)
        current_stock_price: Current stock price for implied EPS calculation
        peer_group: Peer group data with list of comparable companies
        peer_earnings_data: Forward P/E earnings data for peer companies
        consensus_eps: Wall Street consensus EPS estimate for comparison
        job_id: Optional job ID for status tracking
    Returns:
        PeerRelativeEpsValidation containing peer-relative EPS validation results
    """

    start_time = time.time()
    logger.info(f"Peer-relative EPS validation flow started for {symbol}")

    # Update job status
    await update_job_status_task(job_id, JobStatus.RUNNING, "Running peer-relative EPS validation analysis", "peer_relative_eps_validation_flow")

    # Try to get cached result first
    cached_result = await peer_relative_eps_validation_cache_retrieval_task(symbol, force_recompute)
    if cached_result is not None:
        logger.info(f"Returning cached peer-relative EPS validation for {symbol}")
        await update_job_status_task(job_id, JobStatus.RUNNING, "Peer-relative EPS validation completed (cached)", "peer_relative_eps_validation_flow")
        return cached_result

    logger.info(f"Running fresh peer-relative EPS validation analysis for {symbol}")

    # Perform peer-relative EPS validation
    validation_result: PeerRelativeEpsValidation = await peer_relative_eps_validation_task(
        symbol=symbol,
        current_stock_price=current_stock_price,
        peer_group=peer_group,
        peer_earnings_data=peer_earnings_data,
        consensus_eps=consensus_eps
    )

    # Cache the result for future use
    cache = get_redis_cache()
    ttl = get_eps_validation_ttl("peer_relative_eps_validation")
    cache.cache_report("peer_relative_eps_validation", symbol, validation_result, ttl=ttl)

    # Update job status with completion
    verdict_message = f"Peer-relative EPS validation completed - {validation_result.peer_comparison_verdict.value}"
    await update_job_status_task(job_id, JobStatus.RUNNING, verdict_message, "peer_relative_eps_validation_flow")

    logger.info(f"Peer-relative EPS validation flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    logger.info(f"Validation verdict: {validation_result.peer_comparison_verdict.value}")

    return validation_result