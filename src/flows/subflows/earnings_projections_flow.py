from typing import Optional, Dict, Any
from src.tasks.earnings_projections.earnings_projections_fetch_task import earnings_projections_fetch_task
from src.tasks.earnings_projections.earnings_projections_analysis_task import earnings_projections_analysis_task
from src.tasks.earnings_projections.earnings_projections_reporting_task import earnings_projections_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionData, EarningsProjectionAnalysis
import logging
import time

logger = logging.getLogger(__name__)


async def earnings_projections_flow(
    symbol: str,
    historical_earnings_analysis: Optional[Dict[str, Any]] = None,
    financial_statements_analysis: Optional[Dict[str, Any]] = None
) -> EarningsProjectionAnalysis:
    """
    Main flow for creating independent earnings projections for next quarter validation.
    
    This flow creates your own baseline estimate that's foundational for independently 
    challenging consensus, enabling true validation by providing an independent analytical baseline.
    
    Args:
        symbol: Stock symbol to research
        historical_earnings_analysis: Optional historical earnings analysis results
        financial_statements_analysis: Optional financial statements analysis results
    Returns:
        EarningsProjectionAnalysis containing independent projections and consensus validation
    """
    start_time = time.time()
    logger.info(f"Independent Earnings Projections flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "earnings_projections_flow", "symbol": symbol})
    
    # Fetch comprehensive data for earnings projections
    projection_data: EarningsProjectionData = await earnings_projections_fetch_task(
        symbol, historical_earnings_analysis, financial_statements_analysis
    )

    # Perform independent earnings projections analysis
    projections_analysis: EarningsProjectionAnalysis = await earnings_projections_analysis_task(
        symbol, projection_data
    )

    # Generate reporting output
    await earnings_projections_reporting_task(symbol, projections_analysis)

    logger.info(f"Independent Earnings Projections flow completed for {symbol}")
    logger.info(f"Independent Earnings Projections flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "earnings_projections_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return projections_analysis