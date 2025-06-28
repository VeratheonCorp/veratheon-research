from prefect import flow, task, get_run_logger
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import your existing Researcher class
from src.researcher import Researcher

@task(name="run_research")
async def run_research(symbol: str, price_target: int, timeframe: str) -> Dict[str, Any]:
    """
    Task to run the market research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        price_target: Target price for the stock
        timeframe: Timeframe for the research
        
    Returns:
        Dict containing the research results
    """
    logger = get_run_logger()
    logger.info(f"Starting research for {symbol} with target ${price_target}")
    
    try:
        researcher = Researcher()
        result = await researcher.run(symbol, price_target, timeframe)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        return {"status": "error", "message": str(e)}

@flow(name="market-research-flow")
async def market_research_flow(
    symbol: str,
    price_target: int,
    timeframe: str = "1y",
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main flow for running market research.
    
    Args:
        symbol: Stock symbol to research (e.g., "AAPL")
        price_target: Target price for the stock
        timeframe: Timeframe for the research (default: "1y")
        run_id: Optional run ID for tracking (auto-generated if not provided)
        
    Returns:
        Dict containing the research results and metadata
    """
    logger = get_run_logger()
    
    if not run_id:
        run_id = f"{symbol.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"Starting market research flow (Run ID: {run_id})")
    
    # Run the research task
    research_result = await run_research(symbol, price_target, timeframe)
    
    if research_result["status"] == "error":
        logger.error(f"Research failed: {research_result.get('message')}")
    else:
        logger.info("Research completed successfully")
    
    return {
        "run_id": run_id,
        "symbol": symbol,
        "price_target": price_target,
        "timeframe": timeframe,
        "status": research_result["status"],
        "result": research_result.get("data"),
        "timestamp": datetime.utcnow().isoformat()
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