from src.tasks.management_guidance.management_guidance_fetch_task import management_guidance_fetch_task
from src.tasks.management_guidance.management_guidance_analysis_task import management_guidance_analysis_task
from src.tasks.management_guidance.management_guidance_reporting_task import management_guidance_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.management_guidance.management_guidance_models import ManagementGuidanceData, ManagementGuidanceAnalysis
from typing import Optional, Any
import logging
import time

logger = logging.getLogger(__name__)

async def management_guidance_flow(
    symbol: str,
    historical_earnings_analysis: Optional[Any] = None,
    financial_statements_analysis: Optional[Any] = None
) -> ManagementGuidanceAnalysis:
    """
    Main flow for analyzing management guidance from earnings calls.
    
    This flow extracts qualitative risks and opportunities from earnings call transcripts
    to cross-check against consensus estimates and provide validation signals for 
    independent earnings analysis.
    
    Args:
        symbol: Stock symbol to research
        historical_earnings_analysis: Optional historical earnings patterns for context
        financial_statements_analysis: Optional recent financial trends for context
        
    Returns:
        ManagementGuidanceAnalysis containing guidance indicators and validation signals
    """
    
    start_time = time.time()
    logger.info(f"Management Guidance flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "management_guidance_flow", "symbol": symbol})
    
    # Fetch management guidance data (earnings estimates + transcripts)
    guidance_data: ManagementGuidanceData = await management_guidance_fetch_task(symbol)

    # Analyze management guidance for risks, opportunities, and signals
    guidance_analysis: ManagementGuidanceAnalysis = await management_guidance_analysis_task(
        symbol, guidance_data, historical_earnings_analysis, financial_statements_analysis
    )

    # Generate reporting output
    await management_guidance_reporting_task(symbol, guidance_analysis)

    logger.info(f"Management Guidance flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "management_guidance_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return guidance_analysis