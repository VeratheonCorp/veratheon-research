import logging as log
from typing import Dict, Any
from agents import function_tool
from src.clients.alpha_vantage_client import AlphaVantageClient

# singleton client for all tools
client = AlphaVantageClient()

@function_tool
def call_alpha_vantage(alpha_vantage_uri: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage time series endpoint.

    Example: 
    call_alpha_vantage("TIME_SERIES_DAILY_ADJUSTED&symbol=AAPL&outputsize=full&datatype=json")
    call_alpha_vantage("GET_DAILY_ADJUSTED&symbol=AAPL&outputsize=full&datatype=json")
    call_alpha_vantage("GLOBAL_QUOTE&symbol=AAPL&datatype=json")
    call_alpha_vantage("TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&outputsize=full&datatype=json")
    call_alpha_vantage("NEWS_SENTIMENT&tickers=AAPL&datatype=json")
    """
    log.info(f"Calling Alpha Vantage API with URI: {alpha_vantage_uri}")
    return client.run_query(alpha_vantage_uri)


