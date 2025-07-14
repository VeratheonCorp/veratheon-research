from typing import List, Dict, Any
from pydantic import BaseModel

class NewsSentimentFeed(BaseModel):
    title: str
    url: str
    time_published: str
    authors: List[str]
    summary: str
    banner_image: str
    source: str
    category_within_source: str
    source_domain: str
    topics: List[Dict[str, Any]]
    overall_sentiment_score: float
    overall_sentiment_label: str
    ticker_sentiment: List[Dict[str, Any]]

class NewsSentimentSummary(BaseModel):
    symbol: str
    items: str
    sentiment_score_definition: str
    relevance_score_definition: str
    feed: List[NewsSentimentFeed]
    




    