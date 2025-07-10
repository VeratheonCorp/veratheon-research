from prefect import flow, get_run_logger
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

from src.prefect.tasks.forward_pe.forward_pe_peer_group_task import forward_pe_peer_group_task
from src.prefect.tasks.forward_pe.forward_pe_fetch_earnings_task import forward_pe_fetch_earnings_task
from src.prefect.tasks.forward_pe.forward_pe_analysis_task import forward_pe_analysis_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, PeerGroup, EarningsSummary
from src.prefect.tasks.trade_ideas.trade_ideas_task import trade_ideas_task

@flow(name="market-research-flow", log_prints=True)
async def market_research_flow(
    symbol: str,
    #price_target: int,
) -> Dict[str, Any]:
    """
    Main flow for running forward PE analysis.
    
    Args:
        symbol: Stock symbol to research
        #price_target: Target price for the stock
    Returns:
        Dict containing the research results and metadata
    """
    logger = get_run_logger()
    
    logger.info(f"Starting forward PE flow for {symbol}")
    
    # Get the peer group of the user's symbol
    peer_group: PeerGroup = await forward_pe_peer_group_task(symbol)        

    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: EarningsSummary = await forward_pe_fetch_earnings_task(peer_group.original_symbol, peer_group.peer_group)

    #return earnings_summary
    # Perform forward PE analysis
    forward_pe_valuation: ForwardPeValuation = await forward_pe_analysis_task(peer_group.original_symbol, earnings_summary)

    # Perform trade ideas
    no_position_trade_idea, has_position_trade_idea = await trade_ideas_task(peer_group.original_symbol, forward_pe_valuation)

    return {
        "forward_pe_valuation": forward_pe_valuation,
        "no_position_trade_idea": no_position_trade_idea,
        "has_position_trade_idea": has_position_trade_idea
    }