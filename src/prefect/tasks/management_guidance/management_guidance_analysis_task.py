"""Prefect task for analyzing management guidance."""

from prefect import task, get_run_logger
from src.research.management_guidance.management_guidance_models import ManagementGuidanceData, ManagementGuidanceAnalysis
from src.research.management_guidance.management_guidance_agent import management_guidance_agent


@task(name="management_guidance_analysis_task", persist_result=True)
async def management_guidance_analysis_task(
    symbol: str,
    guidance_data: ManagementGuidanceData
) -> ManagementGuidanceAnalysis:
    """
    Task to analyze management guidance for qualitative risks and opportunities.
    
    Args:
        symbol: Stock symbol being analyzed
        guidance_data: Management guidance data including transcripts and estimates
        
    Returns:
        ManagementGuidanceAnalysis with extracted guidance indicators
    """
    logger = get_run_logger()
    logger.info(f"Analyzing management guidance for {symbol}")

    guidance_analysis = await management_guidance_agent(symbol, guidance_data)
    
    if guidance_analysis.transcript_available:
        logger.info(f"Management guidance analysis completed for {symbol}: "
                   f"Overall tone: {guidance_analysis.overall_guidance_tone}, "
                   f"Signal: {guidance_analysis.consensus_validation_signal}")
        
        if guidance_analysis.guidance_indicators:
            logger.info(f"Found {len(guidance_analysis.guidance_indicators)} guidance indicators")
            
        if guidance_analysis.risk_factors_mentioned:
            logger.warning(f"Risk factors identified: {', '.join(guidance_analysis.risk_factors_mentioned[:3])}")
            
        if guidance_analysis.opportunities_mentioned:
            logger.info(f"Opportunities identified: {', '.join(guidance_analysis.opportunities_mentioned[:3])}")
    else:
        logger.warning(f"Management guidance analysis for {symbol}: No transcript available")

    return guidance_analysis