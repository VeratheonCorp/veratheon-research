import logging as log
from typing import Dict, Any
from agents import function_tool
from src.tools.clients.alpha_vantage_client import AlphaVantageClient

# singleton client for all tools
client = AlphaVantageClient()

@function_tool
def call_alpha_vantage(alpha_vantage_uri: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage endpoint.

    Example: 
    call_alpha_vantage("OVERVIEW&symbol=AAPL")
    call_alpha_vantage("INCOME_STATEMENT&symbol=AAPL")
    call_alpha_vantage("BALANCE_SHEET&symbol=AAPL")
    call_alpha_vantage("CASH_FLOW&symbol=AAPL")
    call_alpha_vantage("GLOBAL_QUOTE&symbol=AAPL&datatype=json")
    call_alpha_vantage("EARNINGS&symbol=AAPL")
    call_alpha_vantage("TIME_SERIES_DAILY_ADJUSTED&symbol=AAPL&outputsize=full&datatype=json")
    call_alpha_vantage("RSI&symbol=AAPL&interval=daily&time_period=50&series_type=close")
    call_alpha_vantage("MACD&symbol=AAPL&interval=daily&time_period=50&series_type=close")
    call_alpha_vantage("BBANDS&symbol=AAPL&interval=daily&time_period=50&series_type=close")
    call_alpha_vantage("NEWS_SENTIMENT&tickers=AAPL&datatype=json")
    call_alpha_vantage("EARNINGS_CALENDAR&symbol=AAPL&horizon=12month")
    call_alpha_vantage("EARNINGS_CALL_TRANSCRIPTS&symbol=AAPL&quarter=2024Q1")
    """
    log.info(f"Calling Alpha Vantage API with URI: {alpha_vantage_uri}")
    return client.run_query(alpha_vantage_uri)


@function_tool
def call_alpha_vantage_overview(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage overview endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: OVERVIEW&symbol={symbol}")
    return client.run_query(f"OVERVIEW&symbol={symbol}")

@function_tool
def call_alpha_vantage_income_statement(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage income statement endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: INCOME_STATEMENT&symbol={symbol}")
    return client.run_query(f"INCOME_STATEMENT&symbol={symbol}")

@function_tool
def call_alpha_vantage_balance_sheet(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage balance sheet endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: BALANCE_SHEET&symbol={symbol}")
    return client.run_query(f"BALANCE_SHEET&symbol={symbol}")

@function_tool
def call_alpha_vantage_cash_flow(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage cash flow endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: CASH_FLOW&symbol={symbol}")
    return client.run_query(f"CASH_FLOW&symbol={symbol}")

@function_tool
def call_alpha_vantage_global_quote(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage global quote endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: GLOBAL_QUOTE&symbol={symbol}")
    return client.run_query(f"GLOBAL_QUOTE&symbol={symbol}")

@function_tool
def call_alpha_vantage_earnings(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage earnings endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: EARNINGS&symbol={symbol}")
    return client.run_query(f"EARNINGS&symbol={symbol}")

@function_tool
def call_alpha_vantage_time_series_daily_adjusted(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage time series daily adjusted endpoint.
    Outputsize is always compact.
    Datatype is always json.
    """
    log.info(f"Calling Alpha Vantage API with URI: TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}")
    return client.run_query(f"TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}")

@function_tool
def call_alpha_vantage_news_sentiment(tickers: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage news sentiment endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: NEWS_SENTIMENT&tickers={tickers}")
    return client.run_query(f"NEWS_SENTIMENT&tickers={tickers}")

@function_tool
def call_alpha_vantage_rsi(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage RSI endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: RSI&symbol={symbol}")
    return client.run_query(f"RSI&symbol={symbol}")

@function_tool
def call_alpha_vantage_macd(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage MACD endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: MACD&symbol={symbol}")
    return client.run_query(f"MACD&symbol={symbol}")

@function_tool
def call_alpha_vantage_bbands(symbol: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage Bollinger Bands endpoint.
    """
    log.info(f"Calling Alpha Vantage API with URI: BBANDS&symbol={symbol}")
    return client.run_query(f"BBANDS&symbol={symbol}")

@function_tool
def call_alpha_vantage_earnings_calendar(symbol: str, horizon: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage earnings calendar endpoint.
    Important: Contains the estimated earnings for the next interval.
    Optional parameters:
    - symbol: Stock symbol to research
    - horizon: Time horizon for the earnings calendar (default: "3month", or "6month" and "12month")
    """
    log.info(f"Calling Alpha Vantage API with URI: EARNINGS_CALENDAR&symbol={symbol}&horizon={horizon}")
    return client.run_query(f"EARNINGS_CALENDAR&symbol={symbol}&horizon={horizon}")

@function_tool
def call_alpha_vantage_earnings_call_transcripts(symbol: str, quarter: str) -> Dict[str, Any]:
    """
    Calls an Alpha Vantage earnings call transcripts endpoint.
    Quarter format: YYYYQM
    Example: 2024Q1
    """
    log.info(f"Calling Alpha Vantage API with URI: EARNINGS_CALL_TRANSCRIPTS&symbol={symbol}&quarter={quarter}")
    return client.run_query(f"EARNINGS_CALL_TRANSCRIPTS&symbol={symbol}&quarter={quarter}")
