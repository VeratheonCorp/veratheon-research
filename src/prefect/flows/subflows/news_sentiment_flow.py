from prefect import flow, get_run_logger
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary, RawNewsSentimentSummary
from src.prefect.tasks.news_sentiment.news_sentiment_analysis_task import news_sentiment_analysis_task
from src.prefect.tasks.news_sentiment.news_sentiment_fetch_summaries_task import news_sentiment_fetch_summaries_task
from src.research.common.models.peer_group import PeerGroup
from typing import List, Optional, Any

@flow(name="news-sentiment-flow", log_prints=True)
async def news_sentiment_flow(
    symbol: str,
    peer_group: PeerGroup,
    earnings_projections_analysis: Optional[Any] = None,
    management_guidance_analysis: Optional[Any] = None,
) -> NewsSentimentSummary:
    logger = get_run_logger()
    logger.info(f"Performing news sentiment analysis for {symbol}")

    peer_group_summaries: List[RawNewsSentimentSummary] = await news_sentiment_fetch_summaries_task(symbol, peer_group.peer_group)

    news_sentiment_analysis_task_result: NewsSentimentSummary = await news_sentiment_analysis_task(
        symbol, peer_group_summaries, earnings_projections_analysis, management_guidance_analysis
    )

    return news_sentiment_analysis_task_result

