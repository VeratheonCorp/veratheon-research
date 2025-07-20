from prefect import task, get_run_logger
from src.research.news_sentiment.news_sentiment_util import get_news_sentiment_summary_for_peer_group
from src.research.news_sentiment.news_sentiment_models import RawNewsSentimentSummary
from typing import List

@task(name="news-sentiment-fetch-summaries-task", log_prints=True)
async def news_sentiment_fetch_summaries_task(
    symbol:str,
    peer_group: List[str],
) -> List[RawNewsSentimentSummary]:
    logger = get_run_logger()
    peer_group.append(symbol)
    logger.info(f"Fetching news sentiment summaries for peer group: {peer_group}")
    summaries = get_news_sentiment_summary_for_peer_group(peer_group)
    return summaries
