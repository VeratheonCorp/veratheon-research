
from prefect import flow, get_run_logger
from src.prefect.tasks.forward_pe.forward_pe_fetch_earnings_task import forward_pe_fetch_single_earnings_task, forward_pe_fetch_earnings_for_symbols_task
from src.prefect.tasks.forward_pe.forward_pe_analysis_task import forward_pe_analysis_task
from src.prefect.tasks.forward_pe.forward_pe_sanity_check_task import forward_pe_sanity_check_task
from src.prefect.tasks.events.event_emission_task import emit_event_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPEEarningsSummary, ForwardPeSanityCheck
from src.research.common.models.peer_group import PeerGroup
from typing import Optional, Any

@flow(name="forward-pe-flow", log_prints=True)
async def forward_pe_flow(
    symbol: str,
    peer_group: PeerGroup,
    earnings_projections_analysis: Optional[Any] = None,
    management_guidance_analysis: Optional[Any] = None,
    forward_pe_sanity_check: Optional[ForwardPeSanityCheck] = None,
) -> ForwardPeValuation:
    """
    Main flow for running forward PE analysis.
    
    Args:
        symbol: Stock symbol to research
        peer_group: Peer group of the symbol
        earnings_projections_analysis: Optional independent earnings projections for validation
        management_guidance_analysis: Optional management guidance analysis for context
        forward_pe_sanity_check: Optional sanity check results for validation
    Returns:
        ForwardPeValuation containing the research results and metadata
    """
    logger = get_run_logger()
    
    # Emit stage start event
    emit_event_task(symbol, "stage_start", stage="forward_pe",
                   message="Calculating forward PE valuation...")
    
    logger.info(f"Starting forward PE flow for {symbol}")
    
    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: ForwardPEEarningsSummary = await forward_pe_fetch_earnings_for_symbols_task(peer_group.original_symbol, peer_group.peer_group)

    # Perform forward PE analysis
    forward_pe_valuation: ForwardPeValuation = await forward_pe_analysis_task(
        peer_group.original_symbol, 
        earnings_summary, 
        earnings_projections_analysis,
        management_guidance_analysis, 
        forward_pe_sanity_check
    )

    # Emit stage complete event
    emit_event_task(symbol, "stage_complete", stage="forward_pe",
                   message="Forward PE analysis completed",
                   data={
                       "current_forward_pe": forward_pe_valuation.current_forward_pe,
                       "peer_average_pe": forward_pe_valuation.peer_average_forward_pe,
                       "relative_valuation": forward_pe_valuation.relative_valuation_signal
                   })

    return forward_pe_valuation



@flow(name="forward-pe-sanity-check-flow", log_prints=True)
async def forward_pe_sanity_check_flow(
    symbol: str,
) -> ForwardPeSanityCheck:
    """
    Main flow for running forward PE sanity check.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        ForwardPeSanityCheck containing the research results and metadata
    """
    logger = get_run_logger()
    
    # Emit stage start event
    emit_event_task(symbol, "stage_start", stage="forward_pe_sanity",
                   message="Running forward PE sanity check...")
    
    logger.info(f"Starting forward PE sanity check flow for {symbol}")
    
    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: ForwardPEEarningsSummary = await forward_pe_fetch_single_earnings_task(symbol)

    # Perform forward PE sanity check
    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_task(earnings_summary)

    # Emit stage complete event
    emit_event_task(symbol, "stage_complete", stage="forward_pe_sanity",
                   message="Forward PE sanity check completed",
                   data={
                       "data_quality": forward_pe_sanity_check.data_quality_assessment,
                       "sanity_check_passed": forward_pe_sanity_check.sanity_check_passed
                   })

    return forward_pe_sanity_check
