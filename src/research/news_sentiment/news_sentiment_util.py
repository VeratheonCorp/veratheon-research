from typing import List
from src.lib.alpha_vantage_api import call_alpha_vantage_news_sentiment
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary

def get_news_sentiment_summary_for_peer_group(peer_group: List[str]) -> List[NewsSentimentSummary]:
    news_sentiment_summaries = []
    for peer in peer_group:
        news_sentiment_json = call_alpha_vantage_news_sentiment(tickers=peer)
        news_sentiment_summaries.append(NewsSentimentSummary(**news_sentiment_json))
    return news_sentiment_summaries