from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import MarketSentimentEpsCheck

market_sentiment_eps_check_agent = Agent(
    name="Market Sentiment EPS Check Analyst",
    model=get_model(),
    output_type=MarketSentimentEpsCheck,
    instructions="""
            Validate consensus EPS via market sentiment, revision trends, and whisper numbers.

            ENUMS:
            - revision_momentum: UPWARD/DOWNWARD/STABLE/VOLATILE/INSUFFICIENT_DATA
            - sentiment_eps_alignment: BULLISH/BEARISH/NEUTRAL/CONFLICTED
            - sentiment_validation_verdict: CONSENSUS_VALIDATED/CONSENSUS_TOO_HIGH/CONSENSUS_TOO_LOW/INSUFFICIENT_DATA

            REVISION MOMENTUM (last 30-90 days):
            - UPWARD: Net positive revisions (>5% revised up)
            - DOWNWARD: Net negative revisions (>5% revised down)
            - STABLE: Minimal activity (<3% change)
            - VOLATILE: Mixed revisions, no clear trend

            SENTIMENT ALIGNMENT:
            - BULLISH: Positive sentiment supports/exceeds EPS
            - BEARISH: Negative sentiment suggests EPS risk
            - NEUTRAL: Balanced sentiment
            - CONFLICTED: Mixed signals

            VALIDATION LOGIC:
            - Positive sentiment + upward revisions: CONSENSUS_TOO_LOW
            - Negative sentiment + downward revisions: CONSENSUS_TOO_HIGH
            - Mixed/neutral signals: CONSENSUS_VALIDATED
            - Insufficient data: INSUFFICIENT_DATA

            Analyze whisper numbers, options flow, analyst dispersion, and news sentiment.
            Provide revision_analysis, sentiment_insights, and market_expectation_summary.
        """,
)
