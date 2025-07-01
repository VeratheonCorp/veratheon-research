from prefect import flow, get_run_logger
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from src.prefect.tasks.forward_pe_task import forward_pe_task
from src.research_agents.forward_pe_agent import EarningsSummary

@flow(name="market-research-flow")
async def market_research_flow(
    symbol: str,
    price_target: int,
    timeframe: str,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main flow for running market research.
    
    Args:
        symbol: Stock symbol to research
        price_target: Target price for the stock
        timeframe: Timeframe for the research
        run_id: Optional run ID for tracking (auto-generated if not provided)
        
    Returns:
        Dict containing the research results and metadata
    """
    logger = get_run_logger()
    
    if not run_id:
        run_id = f"{symbol.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"Starting market research flow for {symbol} with target ${price_target} in {timeframe} (Run ID: {run_id})")
    
    # Run the research task
    research_result: EarningsSummary = await forward_pe_task(symbol)
    
    return {
        "run_id": run_id,
        "symbol": symbol,
        "price_target": price_target,
        "timeframe": timeframe,
        "result": research_result,
        "timestamp": datetime.now().isoformat()
    }

# This allows the flow to be run directly with `python -m src.flows.research_flow`
if __name__ == "__main__":
    import asyncio

    async def main():
        result = await market_research_flow(
            symbol="AAPL",
            price_target=250,
            timeframe="1y"
        )
        print(f"Research completed: {result}")
    
    asyncio.run(main())