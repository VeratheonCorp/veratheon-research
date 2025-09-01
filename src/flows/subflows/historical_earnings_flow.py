from src.tasks.historical_earnings.historical_earnings_fetch_task import historical_earnings_fetch_task
from src.tasks.historical_earnings.historical_earnings_analysis_task import historical_earnings_analysis_task
from src.tasks.historical_earnings.historical_earnings_reporting_task import historical_earnings_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsData, HistoricalEarningsAnalysis
import logging
import time

logger = logging.getLogger(__name__)

async def historical_earnings_flow(symbol: str) -> HistoricalEarningsAnalysis:
    """
    Main flow for running historical earnings analysis.
    
    Analyzes historical earnings data for patterns in beats/misses, revenue growth rates, 
    and margin trends to establish baseline performance and predictability context.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        HistoricalEarningsAnalysis containing the research results and patterns
    """
    
    start_time = time.time()
    logger.info(f"Historical Earnings flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "historical_earnings_flow", "symbol": symbol})
    
    # Fetch historical earnings data from Alpha Vantage
    historical_data: HistoricalEarningsData = await historical_earnings_fetch_task(symbol)

    # Perform historical earnings analysis
    historical_analysis: HistoricalEarningsAnalysis = await historical_earnings_analysis_task(
        symbol, historical_data
    )

    # Generate reporting output
    await historical_earnings_reporting_task(symbol, historical_analysis)

    logger.info(f"Historical Earnings flow completed for {symbol}")
    logger.info(f"Historical Earnings flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "historical_earnings_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return historical_analysis  