from prefect import task, get_run_logger
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsData
from src.research.historical_earnings.historical_earnings_util import get_historical_earnings_data_for_symbol
import json


@task(name="historical_earnings_fetch_task", persist_result=True)
async def historical_earnings_fetch_task(symbol: str) -> HistoricalEarningsData:
    """
    Task to fetch historical earnings data from Alpha Vantage for analysis.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        HistoricalEarningsData containing quarterly earnings, annual earnings, and income statement data
    """
    logger = get_run_logger()
    logger.info(f"Fetching historical earnings data for {symbol}")

    historical_data = get_historical_earnings_data_for_symbol(symbol)
    
    logger.info(f"Historical earnings data fetched for {symbol}: "
               f"{len(historical_data.quarterly_earnings)} quarters, "
               f"{len(historical_data.annual_earnings)} annual reports, "
               f"{len(historical_data.income_statement)} income statements")

    return historical_data