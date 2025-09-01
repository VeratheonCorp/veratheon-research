from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary, RawNewsSentimentSummary
from src.tasks.news_sentiment.news_sentiment_analysis_task import news_sentiment_analysis_task
from src.tasks.news_sentiment.news_sentiment_fetch_summaries_task import news_sentiment_fetch_summaries_task
from src.tasks.news_sentiment.news_sentiment_reporting_task import news_sentiment_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.common.models.peer_group import PeerGroup
from typing import List, Optional, Any
import logging
import time

logger = logging.getLogger(__name__)


async def news_sentiment_flow(
    symbol: str,
    peer_group: PeerGroup,
    earnings_projections_analysis: Optional[Any] = None,
    management_guidance_analysis: Optional[Any] = None,
) -> NewsSentimentSummary:
    
    start_time = time.time()
    logger.info(f"News Sentiment flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "news_sentiment_flow", "symbol": symbol})

    peer_group_summaries: List[RawNewsSentimentSummary] = await news_sentiment_fetch_summaries_task(symbol, peer_group.peer_group)

    news_sentiment_analysis_task_result: NewsSentimentSummary = await news_sentiment_analysis_task(
        symbol, peer_group_summaries, earnings_projections_analysis, management_guidance_analysis
    )

    # Generate reporting output
    await news_sentiment_reporting_task(symbol, news_sentiment_analysis_task_result)

    logger.info(f"News Sentiment flow completed for {symbol}")
    logger.info(f"News Sentiment flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "news_sentiment_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return news_sentiment_analysis_task_result
