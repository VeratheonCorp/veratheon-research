from prefect import flow, get_run_logger
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

from src.prefect.tasks.forward_pe.forward_pe_peer_group_task import forward_pe_peer_group_task
from src.prefect.tasks.forward_pe.forward_pe_fetch_earnings_task import forward_pe_fetch_earnings_task
from src.research.forward_pe.forward_pe_models import PeerGroup, EarningsSummary


@flow(name="market-research-flow", log_prints=True)
async def market_research_flow(
    symbol: str,
    price_target: int,
    horizon: str,
) -> Dict[str, Any]:
    """
    Main flow for running forward PE analysis.
    
    Args:
        symbol: Stock symbol to research
        price_target: Target price for the stock
        horizon: Time horizon for the earnings calendar (default: "3month", or "6month" and "12month")
    Returns:
        Dict containing the research results and metadata
    """
    logger = get_run_logger()
    
    logger.info(f"Starting forward PE flow for {symbol} with target ${price_target} in {horizon}")
    
    # Get the peer group of the user's symbol
    peer_group: PeerGroup = await forward_pe_peer_group_task(symbol)        

    # Get the earnings data for the user's symbol and its peer group
    earnings_summary: EarningsSummary = await forward_pe_fetch_earnings_task(peer_group.original_symbol, peer_group.peer_group, horizon)

    return earnings_summary
    
    # Run the forward PE analysis
    #analysis: ForwardPeValuation = await forward_pe_analysis_task(earnings_summary, horizon)

    #return analysis

# This allows the flow to be run directly with `python -m src.flows.research_flow`
if __name__ == "__main__":
    import asyncio
    import logging as log

    log.basicConfig(level=log.INFO)
    log.info("Starting forward PE flow")

    async def main():
        result = await market_research_flow(
            symbol="AAPL",
            price_target=250,
            horizon="12month"
        )
        log.warning(f"Forward PE flow completed.")

    asyncio.run(main())