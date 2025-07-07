"""Alpha Vantage API tools for financial market data retrieval.

This module provides a set of tools to interact with various Alpha Vantage API endpoints
for retrieving stock market data, financial statements, technical indicators, and more.
All functions return data in JSON format.

Note:
    An Alpha Vantage API key is required and should be set in the environment
    variables as ALPHA_VANTAGE_API_KEY.
"""

from typing import Dict, Any
from src.lib.clients.alpha_vantage_client import AlphaVantageClient
import logging as log

client = AlphaVantageClient()


def call_alpha_vantage(alpha_vantage_uri: str) -> Dict[str, Any]:
    """Make a direct call to any Alpha Vantage API endpoint.
    
    This is a low-level function that allows direct access to any Alpha Vantage endpoint.
    For most use cases, consider using the specific endpoint functions instead.

    Args:
        alpha_vantage_uri: The complete API endpoint URI including parameters.
                          Example: "OVERVIEW&symbol=AAPL"

    Returns:
        Dict[str, Any]: The JSON response from the Alpha Vantage API.

    Examples:
        >>> call_alpha_vantage("OVERVIEW&symbol=AAPL")
        >>> call_alpha_vantage("INCOME_STATEMENT&symbol=MSFT")
        >>> call_alpha_vantage("TIME_SERIES_DAILY_ADJUSTED&symbol=GOOGL&outputsize=full")

    Note:
        You need to include all required parameters in the URI string.
        The API key is automatically added by the client.
    """
    print(f"Calling Alpha Vantage API with URI: {alpha_vantage_uri}")
    return client.run_query(alpha_vantage_uri)



def call_alpha_vantage_overview(symbol: str) -> Dict[str, Any]:
    """Retrieve company overview and key metrics for a given stock symbol.
    
    This endpoint provides a comprehensive overview of the company, including
    company description, financial ratios, and market metrics.

    Args:
        symbol: The stock symbol (e.g., 'AAPL' for Apple Inc.)

    Returns:
        Dict containing company overview data including:
            - Symbol: Stock ticker symbol
            - AssetType: Type of asset
            - Name: Company name
            - Description: Business description
            - Exchange: Primary exchange
            - Currency: Reporting currency
            - Country: Country of headquarters
            - Sector: Business sector
            - Industry: Industry classification
            - MarketCapitalization: Current market cap
            - PERatio: Price-to-Earnings ratio
            - And many other financial metrics

    Example:
        >>> call_alpha_vantage_overview("MSFT")
    """
    print(f"Calling Alpha Vantage API with URI: OVERVIEW&symbol={symbol}")
    return client.run_query(f"OVERVIEW&symbol={symbol}")


def call_alpha_vantage_income_statement(symbol: str) -> Dict[str, Any]:
    """Retrieve the annual and quarterly income statements for a company.
    
    This endpoint provides detailed income statement data, including revenue,
    cost of revenue, operating expenses, and net income.

    Args:
        symbol: The stock symbol (e.g., 'AAPL' for Apple Inc.)

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - annualReports: List of annual income statements (typically 5 years)
            - quarterlyReports: List of quarterly income statements (typically 5 quarters)
            
        Each report includes:
            - fiscalDateEnding: End date of the reporting period
            - reportedCurrency: Currency of the reported amounts
            - totalRevenue: Total revenue/sales
            - costOfRevenue: Cost of goods sold
            - grossProfit: Revenue minus cost of revenue
            - operatingIncome: Income from operations
            - netIncome: Net income
            - And many other line items

    Example:
        >>> call_alpha_vantage_income_statement("GOOGL")
    """
    print(f"Calling Alpha Vantage API with URI: INCOME_STATEMENT&symbol={symbol}")
    return client.run_query(f"INCOME_STATEMENT&symbol={symbol}")


def call_alpha_vantage_balance_sheet(symbol: str) -> Dict[str, Any]:
    """Retrieve the annual and quarterly balance sheets for a company.
    
    This endpoint provides a snapshot of a company's financial position,
    including assets, liabilities, and shareholders' equity.

    Args:
        symbol: The stock symbol (e.g., 'AMZN' for Amazon.com Inc.)

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - annualReports: List of annual balance sheets (typically 5 years)
            - quarterlyReports: List of quarterly balance sheets (typically 5 quarters)
            
        Each report includes:
            - fiscalDateEnding: End date of the reporting period
            - reportedCurrency: Currency of the reported amounts
            - totalAssets: Sum of all assets
            - totalCurrentAssets: Current assets (convertible within 1 year)
            - cashAndCashEquivalentsAtCarryingValue: Cash and equivalents
            - totalLiabilities: Sum of all liabilities
            - totalCurrentLiabilities: Current liabilities (due within 1 year)
            - totalShareholderEquity: Assets minus liabilities
            - commonStock: Value of common stock
            - And many other line items

    Example:
        >>> call_alpha_vantage_balance_sheet("AMZN")
    """
    print(f"Calling Alpha Vantage API with URI: BALANCE_SHEET&symbol={symbol}")
    return client.run_query(f"BALANCE_SHEET&symbol={symbol}")


def call_alpha_vantage_cash_flow(symbol: str) -> Dict[str, Any]:
    """Retrieve the annual and quarterly cash flow statements for a company.
    
    This endpoint provides detailed information about cash inflows and outflows
    from operating, investing, and financing activities.

    Args:
        symbol: The stock symbol (e.g., 'NFLX' for Netflix Inc.)

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - annualReports: List of annual cash flow statements (typically 5 years)
            - quarterlyReports: List of quarterly cash flow statements (typically 5 quarters)
            
        Each report includes:
            - fiscalDateEnding: End date of the reporting period
            - reportedCurrency: Currency of the reported amounts
            - operatingCashflow: Cash from operating activities
            - cashflowFromInvestment: Cash used in investing activities
            - cashflowFromFinancing: Cash from financing activities
            - capitalExpenditure: Capital expenditures
            - freeCashFlow: Operating cash flow minus capital expenditures
            - And many other line items

    Example:
        >>> call_alpha_vantage_cash_flow("NFLX")
    """
    print(f"Calling Alpha Vantage API with URI: CASH_FLOW&symbol={symbol}")
    return client.run_query(f"CASH_FLOW&symbol={symbol}")


def call_alpha_vantage_global_quote(symbol: str) -> Dict[str, Any]:
    """Retrieve the latest price and volume information for a global equity.
    
    This endpoint provides real-time (delayed) quote data including price,
    volume, and trading information for the most recent trading day.

    Args:
        symbol: The stock symbol (e.g., 'META' for Meta Platforms Inc.)

    Returns:
        Dict containing quote data including:
            - symbol: Stock ticker symbol
            - open: Opening price
            - high: Highest price of the day
            - low: Lowest price of the day
            - price: Current price (delayed)
            - volume: Trading volume
            - latestTradingDay: Date of the latest trading day (YYYY-MM-DD)
            - previousClose: Previous day's closing price
            - change: Price change from previous close
            - changePercent: Percentage price change from previous close

    Example:
        >>> call_alpha_vantage_global_quote("META")
    """
    print(f"Calling Alpha Vantage API with URI: GLOBAL_QUOTE&symbol={symbol}")
    return client.run_query(f"GLOBAL_QUOTE&symbol={symbol}")

def call_alpha_vantage_earnings(symbol: str) -> Dict[str, Any]:
    """Retrieve the annual and quarterly earnings (EPS) for a company.
    
    This endpoint provides historical earnings per share (EPS) data and
    the corresponding reported dates.

    Args:
        symbol: The stock symbol (e.g., 'NVDA' for NVIDIA Corporation)

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - annualEarnings: List of annual EPS data (typically 5+ years)
            - quarterlyEarnings: List of quarterly EPS data (typically 16+ quarters)
            
        Each earnings report includes:
            - fiscalDateEnding: End date of the fiscal period
            - reportedEPS: Actual earnings per share
            - estimatedEPS: Estimated earnings per share (if available)
            - surprise: Difference between actual and estimated EPS
            - surprisePercentage: Surprise as a percentage of estimated EPS

    Example:
        >>> call_alpha_vantage_earnings("NVDA")
    """
    print(f"Calling Alpha Vantage API with URI: EARNINGS&symbol={symbol}")
    return client.run_query(f"EARNINGS&symbol={symbol}")


def call_alpha_vantage_time_series_daily_adjusted(symbol: str) -> Dict[str, Any]:
    """Retrieve daily time series (date, daily open, high, low, close, and volume) of the equity specified.
    
    This endpoint provides 20+ years of historical daily price and volume data.
    Data is adjusted for splits and dividend events.

    Args:
        symbol: The stock symbol (e.g., 'TSLA' for Tesla Inc.)

    Returns:
        Dict containing:
            - Meta Data: Information about the time series
            - Time Series (Daily): Dictionary where keys are dates and values contain:
                - 1. open: Opening price for the day
                - 2. high: Highest price during the day
                - 3. low: Lowest price during the day
                - 4. close: Closing price for the day
                - 5. adjusted close: Adjusted closing price
                - 6. volume: Trading volume
                - 7. dividend amount: Dividend amount (if any)
                - 8. split coefficient: Split coefficient (if any)

    Example:
        >>> call_alpha_vantage_time_series_daily_adjusted("TSLA")
        
    Note:
        - Data is returned in JSON format
        - Default outputsize is 'compact' (last 100 data points)
    """
    print(f"Calling Alpha Vantage API with URI: TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}")
    return client.run_query(f"TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}")


def call_alpha_vantage_news_sentiment(tickers: str) -> Dict[str, Any]:
    """Retrieve news sentiment data for specified ticker(s).
    
    This endpoint provides news sentiment and content analysis for stocks,
    including sentiment scores, relevance scores, and article metadata.

    Args:
        tickers: Comma-separated list of stock symbols (e.g., 'AAPL,MSFT,GOOGL')

    Returns:
        Dict containing:
            - items: Number of news items returned
            - sentiment_score_definition: Description of sentiment score range
            - relevance_score_definition: Description of relevance score range
            - feed: List of news articles with:
                - title: Article headline
                - url: Source URL
                - time_published: Publication timestamp (YYYYMMDDTHHMMSS)
                - authors: List of authors
                - summary: Article summary
                - banner_image: URL of the banner image (if available)
                - source: News source
                - category_within_source: Category classification
                - source_domain: Domain of the source
                - topics: List of related topics
                - overall_sentiment_score: Sentiment score (-1.0 to 1.0)
                - overall_sentiment_label: Sentiment classification
                - ticker_sentiment: Sentiment analysis per ticker

    Example:
        >>> call_alpha_vantage_news_sentiment("AAPL,MSFT,GOOGL")
        
    Note:
        - Free tier is limited to 1 request per minute
        - Each request returns up to 50 news items
    """
    print(f"Calling Alpha Vantage API with URI: NEWS_SENTIMENT&tickers={tickers}")
    return client.run_query(f"NEWS_SENTIMENT&tickers={tickers}")


def call_alpha_vantage_rsi(
    symbol: str,
    interval: str = "daily",
    time_period: int = 14,
    series_type: str = "close"
) -> Dict[str, Any]:
    """Retrieve the Relative Strength Index (RSI) values for a given stock.
    
    RSI is a momentum oscillator that measures the speed and change of price movements.
    It oscillates between 0 and 100 and is typically used to identify overbought or
    oversold conditions in a market.

    Args:
        symbol: The stock symbol (e.g., 'AMD' for Advanced Micro Devices)
        interval: Time interval between two consecutive data points. Options:
                 '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                 Default: 'daily'
        time_period: Number of data points used to calculate each RSI value.
                   Default: 14 periods
        series_type: The price type used to calculate RSI. Options:
                   'open', 'high', 'low', 'close'. Default: 'close'

    Returns:
        Dict containing:
            - Meta Data: Information about the technical indicator
            - Technical Analysis: RSI: Dictionary where keys are timestamps and values contain:
                - RSI: The RSI value for the timestamp

    Example:
        >>> call_alpha_vantage_rsi("AMD", interval="daily", time_period=14, series_type="close")
        
    Note:
        - RSI values above 70 are typically considered overbought
        - RSI values below 30 are typically considered oversold
        - The default 14-period RSI is the most common setting
    """
    print(f"Calling Alpha Vantage API with URI: RSI&symbol={symbol}")
    return client.run_query(f"RSI&symbol={symbol}")


def call_alpha_vantage_macd(
    symbol: str,
    interval: str = "daily",
    series_type: str = "close",
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9
) -> Dict[str, Any]:
    """Retrieve Moving Average Convergence Divergence (MACD) values for a given stock.
    
    MACD is a trend-following momentum indicator that shows the relationship between
    two moving averages of a security's price.

    Args:
        symbol: The stock symbol (e.g., 'INTC' for Intel Corporation)
        interval: Time interval between two consecutive data points. Options:
                 '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                 Default: 'daily'
        series_type: The price type used to calculate MACD. Options:
                   'open', 'high', 'low', 'close'. Default: 'close'
        fastperiod: Number of periods for the fast EMA. Default: 12
        slowperiod: Number of periods for the slow EMA. Default: 26
        signalperiod: Number of periods for the signal line. Default: 9

    Returns:
        Dict containing:
            - Meta Data: Information about the technical indicator
            - Technical Analysis: MACD: Dictionary where keys are timestamps and values contain:
                - MACD: The MACD line value
                - MACD_Hist: The MACD histogram value
                - MACD_Signal: The signal line value

    Example:
        >>> call_alpha_vantage_macd(
        ...     symbol="INTC",
        ...     interval="daily",
        ...     series_type="close",
        ...     fastperiod=12,
        ...     slowperiod=26,
        ...     signalperiod=9
        ... )
        
    Note:
        - A bullish signal occurs when the MACD line crosses above the signal line
        - A bearish signal occurs when the MACD line crosses below the signal line
        - The histogram represents the difference between the MACD and signal line
    """
    print(f"Calling Alpha Vantage API with URI: MACD&symbol={symbol}")
    return client.run_query(f"MACD&symbol={symbol}")


def call_alpha_vantage_bbands(
    symbol: str,
    interval: str = "daily",
    time_period: int = 50,
    series_type: str = "close"
) -> Dict[str, Any]:
    """Retrieve Bollinger Bands® values for a given stock.
    
    Bollinger Bands are volatility bands placed above and below a moving average.
    Volatility is based on the standard deviation, which changes as volatility
    increases or decreases.

    Args:
        symbol: The stock symbol (e.g., 'AMZN' for Amazon.com Inc.)
        interval: Time interval between two consecutive data points. Options:
                 '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                 Default: 'daily'
        time_period: Number of data points used to calculate each BB value.
                   Default: 50 periods
        series_type: The price type used to calculate BB. Options:
                   'open', 'high', 'low', 'close'. Default: 'close'

    Returns:
        Dict containing:
            - Meta Data: Information about the technical indicator
            - Technical Analysis: BBANDS: Dictionary where keys are timestamps and values contain:
                - Real Upper Band: Upper Bollinger Band
                - Real Middle Band: Middle Bollinger Band (SMA)
                - Real Lower Band: Lower Bollinger Band

    Example:
        >>> call_alpha_vantage_bbands(
        ...     symbol="AMZN",
        ...     interval="daily",
        ...     time_period=50,
        ...     series_type="close"
        ... )
        
    Note:
        - The middle band is typically a 20-period simple moving average (SMA)
        - The upper and lower bands are typically 2 standard deviations away from the middle band
        - Prices tend to stay within the bands; breakouts may indicate significant moves
    """
    print(
        f"Calling Alpha Vantage API with URI: BBANDS&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}"
    )
    return client.run_query(
        f"BBANDS&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&datatype=json"
    )


def call_alpha_vantage_earnings_calendar(symbol: str, horizon: str = "3month") -> Dict[str, Any]:
    """Retrieve the earnings calendar for a specific company.
    
    This endpoint provides upcoming earnings announcement dates, fiscal quarter end,
    and EPS estimate for the next earnings announcement.

    Args:
        symbol: The stock symbol (e.g., 'AAPL' for Apple Inc.)
        horizon: Time horizon for the earnings calendar. Options:
                '3month' (default), '6month', '12month'

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - name: Company name
            - reportDate: Expected earnings report date (YYYY-MM-DD)
            - fiscalDateEnding: End date of the fiscal quarter (YYYY-MM-DD)
            - estimate: Estimated EPS for the upcoming earnings
            - currency: Reporting currency

    Example:
        >>> call_alpha_vantage_earnings_calendar("AAPL", horizon="3month")
        
    Note:
        - Data is typically available 1-2 weeks before the earnings date
        - The estimate field represents the consensus EPS estimate from analysts
        - The report date is subject to change
        - The API returns a CSV string, which is then converted to a JSON object
    """
    print(f"Calling Alpha Vantage API with URI: EARNINGS_CALENDAR&symbol={symbol}&horizon={horizon}")
    csv_data = client.run_query(f"EARNINGS_CALENDAR&symbol={symbol}&horizon={horizon}")

    # Convert the CSV to a JSON object
    json_data = []
    for row in csv_data.splitlines()[1:]:
        columns = row.split(",")
        try:
            json_data.append({
                "symbol": columns[0],
                "name": columns[1],
                "reportDate": columns[2],
                "fiscalDateEnding": columns[3],
                "estimate": float(columns[4]),
                "currency": columns[5]
            })
        except ValueError as e:
            log.warning(f"Skipping row due to value error in estimate: {row}")
            log.warning(f"Error: {e}")

    return {"earnings_calendar": json_data}


def call_alpha_vantage_earnings_call_transcripts(symbol: str, quarter: str) -> Dict[str, Any]:
    """Retrieve the earnings call transcript for a specific company and quarter.
    
    This endpoint provides the full text of earnings call conference calls,
    including management discussion and Q&A sessions.

    Args:
        symbol: The stock symbol (e.g., 'MSFT' for Microsoft Corporation)
        quarter: Fiscal quarter in format YYYYQM where:
                - YYYY: 4-digit year
                - Q: Quarter (1-4)
                - M: Month (1-3 for Q1, 4-6 for Q2, etc.)
                Example: '2023Q1' for Q1 2023

    Returns:
        Dict containing:
            - symbol: The stock symbol
            - name: Company name
            - quarter: Fiscal quarter
            - date: Date of the earnings call (YYYY-MM-DD)
            - transcript: Full text of the earnings call
            - participants: List of participants in the call
            - qa: Q&A session transcript (if available)

    Example:
        >>> call_alpha_vantage_earnings_call_transcripts("MSFT", "2023Q1")
        
    Note:
        - Transcripts are typically available 24-48 hours after the earnings call
        - Some companies may not have transcripts available for all quarters
        - The quality and format of transcripts may vary by company
    """
    print(f"Calling Alpha Vantage API with URI: EARNINGS_CALL_TRANSCRIPTS&symbol={symbol}&quarter={quarter}")
    return client.run_query(f"EARNINGS_CALL_TRANSCRIPTS&symbol={symbol}&quarter={quarter}")
