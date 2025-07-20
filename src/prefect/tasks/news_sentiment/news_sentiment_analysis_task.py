from prefect import task
from src.research.news_sentiment.news_sentiment_agent import news_sentiment_agent
from src.research.news_sentiment.news_sentiment_models import RawNewsSentimentSummary, NewsSentimentSummary
from prefect import get_run_logger
from agents import Runner
from typing import List

@task(name="news-sentiment-analysis-task", log_prints=True)
async def news_sentiment_analysis_task(
    symbol: str,
    raw_news_sentiment_summaries: List[RawNewsSentimentSummary],
) -> NewsSentimentSummary:
    logger = get_run_logger()
    logger.info(f"Performing news sentiment analysis for {symbol}")
    result = await Runner.run(news_sentiment_agent, input=f"symbol: {symbol}, raw_news_sentiment_summaries: {raw_news_sentiment_summaries}")
    return result.final_output
    