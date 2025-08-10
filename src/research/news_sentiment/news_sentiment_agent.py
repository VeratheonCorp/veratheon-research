from agents import Agent
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.lib.llm_model import get_model

SYSTEM_INSTRUCTIONS = """
You are a financial analyst performing a news sentiment analysis for a given stock.

INSTRUCTIONS:
- Perform a news sentiment analysis for the given symbol.
- Write a detailed analysis of the news sentiment analysis, framed in such a way that trade ideas can be made based on the analysis.
- Determine if the news is on balance, bullish, bearish, or neutral, and provide that judgement as a label.
"""

news_sentiment_agent = Agent(   
            name="News Sentiment Analyst",      
            model=get_model(),
            output_type=NewsSentimentSummary,
            # TODO: Allow Web Search Tool
            instructions=SYSTEM_INSTRUCTIONS
        )
