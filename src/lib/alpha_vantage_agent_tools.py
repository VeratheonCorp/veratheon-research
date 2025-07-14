from typing import Dict, Any
from src.lib.clients.alpha_vantage_client import AlphaVantageClient
from agents import function_tool

client = AlphaVantageClient()

@function_tool
def call_alpha_vantage_news_sentiment_tool(tickers: str, topics: str = "", time_from: str = "", time_to: str = "") -> Dict[str, Any]:
    """Retrieve news sentiment data for specified ticker(s).
    
    This endpoint provides news sentiment and content analysis for stocks,
    including sentiment scores, relevance scores, and article metadata.

    Args:
        tickers: Comma-separated list of stock symbols (e.g., 'AAPL,MSFT,GOOGL')
        topics: The stock/crypto/forex symbols of your choice. 
            The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. Below is the full list of supported topics:
                Blockchain: blockchain
                Earnings: earnings
                IPO: ipo
                Mergers & Acquisitions: mergers_and_acquisitions
                Financial Markets: financial_markets
                Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
                Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
                Economy - Macro/Overall: economy_macro
                Energy & Transportation: energy_transportation
                Finance: finance
                Life Sciences: life_sciences
                Manufacturing: manufacturing
                Real Estate & Construction: real_estate
                Retail & Wholesale: retail_wholesale
                Technology: technology
        time_from: The time from which to retrieve news. 
            The time from which to retrieve news. 
            Format: YYYYMMDDTHHMM. 
            Example: time_from=20220101T0000
        time_to: The time to which to retrieve news. 
            Format: YYYYMMDDTHHMM. 
            Example: time_to=20220101T0000

    Returns:
        Dict containing:
            - items: Number of news items returned
            - sentiment_score_definition: Description of sentiment score range
            - relevance_score_definition: Description of relevance score range
            - feed: List of news articles with:
                - title: Article headline
                - url: Source URL
                - time_published: Publication timestamp (YYYYMMDDTHHMM)
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
        >>> call_alpha_vantage_news_sentiment_tool("AAPL,MSFT,GOOGL", topics="technology", time_from="20220101T0000", time_to="20220101T0000")
        
    Note:
        - Each request returns up to 50 news items
    """
    query = f"NEWS_SENTIMENT&tickers={tickers}"
    if topics:
        query = f"{query}&topics={topics}"
    if time_from:
        query = f"{query}&time_from={time_from}"
    if time_to:
        query = f"{query}&time_to={time_to}"
    return client.run_query(query)