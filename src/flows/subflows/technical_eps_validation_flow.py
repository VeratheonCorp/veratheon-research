"""
TEMPLATE: Technical EPS Validation Flow

This file serves as a template for creating flows for new EPS validation methods.
Replace 'technical' with your validation method name throughout.
"""

import logging
import time
from typing import Optional

from src.lib.eps_validation_cache_utils import get_eps_validation_ttl
from src.lib.job_tracker import JobStatus
from src.lib.redis_cache import get_redis_cache
from src.research.eps_validation.eps_validation_models import TechnicalEpsValidation

# TEMPLATE: Add imports for your specific data dependencies
# from src.research.market_data.models import TechnicalIndicators
# from src.research.price_data.models import PriceData

from src.tasks.cache_retrieval.technical_eps_validation_cache_retrieval_task import (
    technical_eps_validation_cache_retrieval_task,
)
from src.tasks.common.job_status_task import update_job_status_task
from src.tasks.eps_validation.technical_eps_validation_task import (
    technical_eps_validation_task,
)

logger = logging.getLogger(__name__)


async def technical_eps_validation_flow(
    symbol: str,
    force_recompute: bool = False,
    # TEMPLATE: Add your specific dependency data parameters
    # technical_indicators: Optional[TechnicalIndicators] = None,
    # price_data: Optional[PriceData] = None,
    consensus_eps: Optional[float] = None,
    job_id: Optional[str] = None,
) -> TechnicalEpsValidation:
    """
    TEMPLATE: Flow orchestrating technical EPS validation using technical analysis.

    Replace this description with your specific validation methodology.

    Args:
        symbol: Stock symbol to research
        force_recompute: Whether to force recomputation (bypasses cache)
        consensus_eps: Wall Street consensus EPS estimate for comparison
        job_id: Optional job ID for status tracking
        # TEMPLATE: Add documentation for your specific parameters

    Returns:
        TechnicalEpsValidation containing technical analysis validation results
    """

    start_time = time.time()
    logger.info(f"Technical EPS validation flow started for {symbol}")

    # Update job status
    await update_job_status_task(
        job_id,
        JobStatus.RUNNING,
        "Running technical EPS validation analysis",
        "technical_eps_validation_flow",
    )

    # Try to get cached result first
    cached_result = await technical_eps_validation_cache_retrieval_task(
        symbol, force_recompute
    )
    if cached_result is not None:
        logger.info(f"Returning cached technical EPS validation for {symbol}")
        await update_job_status_task(
            job_id,
            JobStatus.RUNNING,
            "Technical EPS validation completed (cached)",
            "technical_eps_validation_flow",
        )
        return cached_result

    logger.info(f"Running fresh technical EPS validation analysis for {symbol}")

    # Perform technical EPS validation
    validation_result: TechnicalEpsValidation = await technical_eps_validation_task(
        symbol=symbol,
        # TEMPLATE: Pass your specific parameters
        # technical_indicators=technical_indicators,
        # price_data=price_data,
        consensus_eps=consensus_eps,
    )

    # Cache the result for future use
    cache = get_redis_cache()
    ttl = get_eps_validation_ttl("technical_eps_validation")
    cache.cache_report("technical_eps_validation", symbol, validation_result, ttl=ttl)

    # Update job status with completion
    verdict_message = f"Technical EPS validation completed - {validation_result.validation_verdict.value}"
    await update_job_status_task(
        job_id, JobStatus.RUNNING, verdict_message, "technical_eps_validation_flow"
    )

    logger.info(
        f"Technical EPS validation flow completed for {symbol} in {int(time.time() - start_time)} seconds"
    )
    logger.info(f"Validation verdict: {validation_result.validation_verdict.value}")

    return validation_result