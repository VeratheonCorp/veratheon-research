from src.tasks.forward_pe.forward_pe_fetch_earnings_task import forward_pe_fetch_single_earnings_task, forward_pe_fetch_earnings_for_symbols_task
from src.tasks.forward_pe.forward_pe_analysis_task import forward_pe_analysis_task
from src.tasks.forward_pe.forward_pe_sanity_check_task import forward_pe_sanity_check_task
from src.tasks.forward_pe.forward_pe_reporting_task import forward_pe_valuation_reporting_task, forward_pe_sanity_check_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPEEarningsSummary, ForwardPeSanityCheck
from src.research.common.models.peer_group import PeerGroup
from typing import Optional, Any
import logging
import time

logger = logging.getLogger(__name__)

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
    
    start_time = time.time()
    logger.info(f"Forward PE flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "forward_pe_flow", "symbol": symbol})
    
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

    # Generate reporting output
    await forward_pe_valuation_reporting_task(symbol, forward_pe_valuation)

    logger.info(f"Forward PE flow completed for {symbol}")
    logger.info(f"Forward PE flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "forward_pe_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return forward_pe_valuation


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
    
    start_time = time.time()
    logger.info(f"Forward PE sanity check flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "forward_pe_sanity_check_flow", "symbol": symbol})
    
    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: ForwardPEEarningsSummary = await forward_pe_fetch_single_earnings_task(symbol)

    # Perform forward PE sanity check
    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_task(earnings_summary)

    # Generate reporting output
    await forward_pe_sanity_check_reporting_task(symbol, forward_pe_sanity_check)

    logger.info(f"Forward PE sanity check flow completed for {symbol}")
    logger.info(f"Forward PE sanity check flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "forward_pe_sanity_check_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return forward_pe_sanity_check
