from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def news_sentiment_reporting_task(
    symbol: str, 
    news_sentiment_summary: NewsSentimentSummary
) -> None:
    """
    Reporting task to write JSON dump of news sentiment analysis results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        news_sentiment_summary: NewsSentimentSummary model to report
    """
    logger.info(f"News Sentiment Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"news_sentiment_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(news_sentiment_summary.model_dump(), f, indent=2)
    
    logger.info(f"News Sentiment report written to: {filepath.absolute()}")