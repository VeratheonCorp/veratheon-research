from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RawNewsSentimentFeed(BaseModel):
    # title: str
    # url: str
    # time_published: str
    # authors: List[str]
    # summary: str
    # banner_image: Optional[str]
    # source: str
    # category_within_source: str
    # source_domain: str
    # topics: List[Dict[str, Any]]
    overall_sentiment_score: float
    overall_sentiment_label: str
    ticker_sentiment: List[Dict[str, Any]]

class RawNewsSentimentSummary(BaseModel):
    # items: int
    # sentiment_score_definition: str
    # relevance_score_definition: str
    feed: List[RawNewsSentimentFeed]
    

class NewsSentimentSummary(BaseModel):
    symbol: Optional[str]
    news_sentiment_analysis: str
    confidence_score: int
    overall_sentiment_label: str