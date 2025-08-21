"""Prefect subflow for management guidance analysis."""

from prefect import flow, get_run_logger
from src.prefect.tasks.management_guidance.management_guidance_fetch_task import management_guidance_fetch_task
from src.prefect.tasks.management_guidance.management_guidance_analysis_task import management_guidance_analysis_task
from src.prefect.tasks.events.event_emission_task import emit_event_task
from src.research.management_guidance.management_guidance_models import ManagementGuidanceData, ManagementGuidanceAnalysis
from typing import Optional, Any


@flow(name="management-guidance-flow", log_prints=True)
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
    logger = get_run_logger()
    
    # Emit stage start event
    emit_event_task(symbol, "stage_start", stage="management_guidance",
                   message="Analyzing management guidance from earnings calls...")
    
    logger.info(f"Starting management guidance flow for {symbol}")
    
    # Fetch management guidance data (earnings estimates + transcripts)
    guidance_data: ManagementGuidanceData = await management_guidance_fetch_task(symbol)

    # Analyze management guidance for risks, opportunities, and signals
    guidance_analysis: ManagementGuidanceAnalysis = await management_guidance_analysis_task(
        symbol, guidance_data, historical_earnings_analysis, financial_statements_analysis
    )

    # Log key guidance results
    if guidance_analysis.transcript_available:
        logger.info(f"Management guidance flow completed for {symbol}: "
                   f"Consensus validation signal: {guidance_analysis.consensus_validation_signal}")
        
        if guidance_analysis.guidance_confidence == "high":
            logger.info(f"High-confidence guidance signals detected for {symbol}")
        elif guidance_analysis.guidance_confidence == "low":
            logger.warning(f"Low-confidence guidance signals for {symbol}")
            
        if guidance_analysis.consensus_validation_signal == "bullish":
            logger.info(f"BULLISH guidance signal: Management outlook supports upside to consensus")
        elif guidance_analysis.consensus_validation_signal == "bearish":
            logger.warning(f"BEARISH guidance signal: Management outlook suggests downside to consensus")
    else:
        logger.warning(f"Management guidance flow completed for {symbol}: No transcript available for analysis")

    # Emit stage complete event
    emit_event_task(symbol, "stage_complete", stage="management_guidance",
                   message="Management guidance analysis completed",
                   data={
                       "guidance_tone": guidance_analysis.overall_guidance_tone,
                       "consensus_validation": guidance_analysis.consensus_validation_signal,
                       "guidance_confidence": guidance_analysis.guidance_confidence,
                       "transcript_available": guidance_analysis.transcript_available
                   })

    return guidance_analysis