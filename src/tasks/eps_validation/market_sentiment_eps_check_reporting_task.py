from src.research.eps_validation.eps_validation_models import MarketSentimentEpsCheck
from src.lib.redis_cache import get_redis_cache
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def market_sentiment_eps_check_reporting_task(
    symbol: str,
    market_sentiment_eps_check: MarketSentimentEpsCheck
) -> None:
    """
    Reporting task to write JSON dump of market sentiment EPS check analysis results to file and cache to Redis.

    Args:
        symbol: Stock symbol being analyzed
        market_sentiment_eps_check: MarketSentimentEpsCheck model to report
    """
    logger.info(f"Market Sentiment EPS Check Reporting for {symbol}")

    # Cache the analysis in Redis (24 hour TTL for reports)
    cache = get_redis_cache()
    cache.cache_report("market_sentiment_eps_check", symbol, market_sentiment_eps_check, ttl=86400)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"market_sentiment_eps_check_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename

    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(market_sentiment_eps_check.model_dump(), f, indent=2)

    logger.info(f"Market Sentiment EPS Check report written to: {filepath.absolute()}")