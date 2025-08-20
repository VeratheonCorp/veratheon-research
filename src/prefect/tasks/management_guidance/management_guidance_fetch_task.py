"""Prefect task for fetching management guidance data."""

from prefect import task, get_run_logger
from src.research.management_guidance.management_guidance_models import ManagementGuidanceData
from src.research.management_guidance.management_guidance_util import get_management_guidance_data_for_symbol


@task(name="management_guidance_fetch_task", persist_result=True)
async def management_guidance_fetch_task(symbol: str) -> ManagementGuidanceData:
    """
    Task to fetch management guidance data including earnings estimates and transcripts.
    
    Args:
        symbol: Stock symbol to research
        
    Returns:
        ManagementGuidanceData containing earnings estimates and latest transcript
    """
    logger = get_run_logger()
    logger.info(f"Fetching management guidance data for {symbol}")

    guidance_data = get_management_guidance_data_for_symbol(symbol)
    
    if guidance_data.earnings_transcript:
        logger.info(f"Management guidance data fetched for {symbol}: transcript available for Q{guidance_data.quarter}")
    else:
        logger.warning(f"Management guidance data fetched for {symbol}: no transcript available")

    return guidance_data