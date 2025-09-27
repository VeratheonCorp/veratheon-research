import logging
import time
from typing import Optional

from src.lib.eps_validation_cache_utils import get_eps_validation_ttl
from src.lib.job_tracker import JobStatus
from src.lib.redis_cache import get_redis_cache
from src.research.earnings_projections.earnings_projections_models import (
    EarningsProjectionAnalysis,
    EarningsProjectionData,
)
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation
from src.research.financial_statements.financial_statements_models import (
    FinancialStatementsAnalysis,
    FinancialStatementsData,
)
from src.tasks.cache_retrieval.bottom_up_eps_validation_cache_retrieval_task import (
    bottom_up_eps_validation_cache_retrieval_task,
)
from src.tasks.common.job_status_task import update_job_status_task
from src.tasks.eps_validation.bottom_up_eps_validation_task import (
    bottom_up_eps_validation_task,
)

logger = logging.getLogger(__name__)


async def bottom_up_eps_validation_flow(
    symbol: str,
    force_recompute: bool = False,
    financial_statements_data: Optional[FinancialStatementsData] = None,
    financial_statements_analysis: Optional[FinancialStatementsAnalysis] = None,
    earnings_projections_data: Optional[EarningsProjectionData] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    consensus_eps: Optional[float] = None,
    job_id: Optional[str] = None,
) -> BottomUpEpsValidation:
    """
    Flow orchestrating bottom-up EPS validation using financial fundamentals.

    Performs independent EPS reconstruction from revenue, margins, share count, and CapEx data
    to validate consensus estimates through fundamental analysis.

    Args:
        symbol: Stock symbol to research
        force_recompute: Whether to force recomputation (bypasses cache when implemented)
        financial_statements_data: Raw financial statements data for fundamental analysis
        financial_statements_analysis: Analysis of financial statements trends
        earnings_projections_data: Raw earnings projection data
        earnings_projections_analysis: Independent earnings projections analysis
        consensus_eps: Wall Street consensus EPS estimate for comparison
        job_id: Optional job ID for status tracking
    Returns:
        BottomUpEpsValidation containing independent EPS validation results
    """

    start_time = time.time()
    logger.info(f"Bottom-up EPS validation flow started for {symbol}")

    # Update job status
    await update_job_status_task(
        job_id,
        JobStatus.RUNNING,
        "Running bottom-up EPS validation analysis",
        "bottom_up_eps_validation_flow",
    )

    # Try to get cached result first
    cached_result = await bottom_up_eps_validation_cache_retrieval_task(
        symbol, force_recompute
    )
    if cached_result is not None:
        logger.info(f"Returning cached bottom-up EPS validation for {symbol}")
        await update_job_status_task(
            job_id,
            JobStatus.RUNNING,
            "Bottom-up EPS validation completed (cached)",
            "bottom_up_eps_validation_flow",
        )
        return cached_result

    logger.info(f"Running fresh bottom-up EPS validation analysis for {symbol}")

    # Perform bottom-up EPS validation
    validation_result: BottomUpEpsValidation = await bottom_up_eps_validation_task(
        symbol=symbol,
        financial_statements_data=financial_statements_data,
        financial_statements_analysis=financial_statements_analysis,
        earnings_projections_data=earnings_projections_data,
        earnings_projections_analysis=earnings_projections_analysis,
        consensus_eps=consensus_eps,
    )

    # Cache the result for future use
    cache = get_redis_cache()
    ttl = get_eps_validation_ttl("bottom_up_eps_validation")
    cache.cache_report("bottom_up_eps_validation", symbol, validation_result, ttl=ttl)

    # Update job status with completion
    verdict_message = f"Bottom-up EPS validation completed - {validation_result.validation_verdict.value}"
    await update_job_status_task(
        job_id, JobStatus.RUNNING, verdict_message, "bottom_up_eps_validation_flow"
    )

    logger.info(
        f"Bottom-up EPS validation flow completed for {symbol} in {int(time.time() - start_time)} seconds"
    )
    logger.info(f"Validation verdict: {validation_result.validation_verdict.value}")

    return validation_result
