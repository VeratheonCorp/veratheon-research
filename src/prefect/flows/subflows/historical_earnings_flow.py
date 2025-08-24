from prefect import flow, get_run_logger
from src.prefect.tasks.historical_earnings.historical_earnings_fetch_task import historical_earnings_fetch_task
from src.prefect.tasks.historical_earnings.historical_earnings_analysis_task import historical_earnings_analysis_task
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsData, HistoricalEarningsAnalysis


@flow(name="historical-earnings-flow", log_prints=True)
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
    logger = get_run_logger()
    
    logger.info(f"Starting historical earnings flow for {symbol}")
    
    # Fetch historical earnings data from Alpha Vantage
    historical_data: HistoricalEarningsData = await historical_earnings_fetch_task(symbol)

    # Perform historical earnings analysis
    historical_analysis: HistoricalEarningsAnalysis = await historical_earnings_analysis_task(
        symbol, historical_data
    )

    logger.info(f"Historical earnings flow completed for {symbol}: "
               f"Pattern: {historical_analysis.earnings_pattern}, "
               f"Predictability: {historical_analysis.predictability_score}/10")

    return historical_analysis