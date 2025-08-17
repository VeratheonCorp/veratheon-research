from prefect import flow, get_run_logger
from typing import Optional, Dict, Any
from src.prefect.tasks.earnings_projections.earnings_projections_fetch_task import earnings_projections_fetch_task
from src.prefect.tasks.earnings_projections.earnings_projections_analysis_task import earnings_projections_analysis_task
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionData, EarningsProjectionAnalysis


@flow(name="earnings-projections-flow", log_prints=True)
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
    logger = get_run_logger()
    
    logger.info(f"Starting independent earnings projections flow for {symbol}")
    
    # Fetch comprehensive data for earnings projections
    projection_data: EarningsProjectionData = await earnings_projections_fetch_task(
        symbol, historical_earnings_analysis, financial_statements_analysis
    )

    # Perform independent earnings projections analysis
    projections_analysis: EarningsProjectionAnalysis = await earnings_projections_analysis_task(
        symbol, projection_data
    )

    # Log key projection results
    next_quarter = projections_analysis.next_quarter_projection
    logger.info(f"Earnings projections flow completed for {symbol}: "
               f"Independent EPS estimate: ${next_quarter.projected_eps:.2f}")
    
    if next_quarter.consensus_eps_estimate:
        diff_percent = next_quarter.eps_vs_consensus_percent or 0
        if abs(diff_percent) > 5:  # Flag significant differences
            logger.warning(f"SIGNIFICANT DIVERGENCE: Our estimate differs from consensus by {diff_percent:.1f}%")
        else:
            logger.info(f"Estimate aligns with consensus (difference: {diff_percent:.1f}%)")

    return projections_analysis