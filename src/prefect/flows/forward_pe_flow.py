
from prefect import flow, get_run_logger
from src.prefect.tasks.forward_pe.forward_pe_fetch_earnings_task import forward_pe_fetch_earnings_task
from src.prefect.tasks.forward_pe.forward_pe_analysis_task import forward_pe_analysis_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPEEarningsSummary
from src.research.common.models.peer_group import PeerGroup

@flow(name="forward-pe-flow", log_prints=True)
async def forward_pe_flow(
    symbol: str,
    peer_group: PeerGroup,
) -> ForwardPeValuation:
    """
    Main flow for running forward PE analysis.
    
    Args:
        symbol: Stock symbol to research
        peer_group: Peer group of the symbol
    Returns:
        ForwardPeValuation containing the research results and metadata
    """
    logger = get_run_logger()
    
    logger.info(f"Starting forward PE flow for {symbol}")
    
    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: ForwardPEEarningsSummary = await forward_pe_fetch_earnings_task(peer_group.original_symbol, peer_group.peer_group)

    # Perform forward PE analysis
    forward_pe_valuation: ForwardPeValuation = await forward_pe_analysis_task(peer_group.original_symbol, earnings_summary)

    return forward_pe_valuation