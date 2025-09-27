from typing import Optional, Any
from src.research.eps_validation.eps_validation_models import MarketSentimentEpsCheck, RevisionMomentum, SentimentAlignment, EpsValidationVerdict
from src.research.eps_validation.market_sentiment_eps_check_agent import market_sentiment_eps_check_agent
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from agents import Runner, RunResult
import json
import logging

logger = logging.getLogger(__name__)

async def market_sentiment_eps_check_task(
    symbol: str,
    news_sentiment_analysis: Optional[NewsSentimentSummary] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    management_guidance_analysis: Optional[ManagementGuidanceAnalysis] = None,
    consensus_eps: Optional[float] = None
) -> MarketSentimentEpsCheck:
    """
    Task to orchestrate sentiment EPS validation using market sentiment and revision analysis.

    Args:
        symbol: Stock symbol to research
        news_sentiment_analysis: Analyzed news sentiment data for market sentiment context
        earnings_projections_analysis: Independent earnings projections for revision context
        management_guidance_analysis: Management guidance analysis for whisper number context
        consensus_eps: Wall Street consensus EPS estimate for validation
    Returns:
        MarketSentimentEpsCheck containing sentiment-based EPS validation results
    """

    logger.info(f"Market sentiment EPS check started for {symbol}")

    # Handle missing sentiment data gracefully
    if not news_sentiment_analysis:
        logger.warning(f"No news sentiment analysis available for {symbol}")
        return MarketSentimentEpsCheck(
            symbol=symbol,
            revision_momentum=RevisionMomentum.INSUFFICIENT_DATA,
            sentiment_eps_alignment=SentimentAlignment.NEUTRAL,
            whisper_vs_consensus=None,
            sentiment_validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            revision_analysis="Cannot perform sentiment EPS validation due to missing news sentiment data",
            sentiment_insights=["Missing news sentiment data", "Unable to assess market sentiment alignment"],
            market_expectation_summary="Insufficient sentiment data to assess market expectations vs consensus"
        )

    # Handle missing consensus EPS
    if consensus_eps is None:
        if earnings_projections_analysis and earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate:
            consensus_eps = earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate
            logger.info(f"Using consensus EPS from earnings projections: ${consensus_eps:.2f}")
        else:
            logger.warning(f"No consensus EPS available for {symbol}")
            consensus_eps = 0.0

    # Prepare comprehensive input data for the agent
    input_data = f"""
    symbol: {symbol}
    consensus_eps: {consensus_eps}
    """

    # Add news sentiment analysis
    if news_sentiment_analysis:
        input_data += f"""
    news_sentiment_analysis: {news_sentiment_analysis.model_dump_json()}
    """

    # Add earnings projections analysis if available for revision context
    if earnings_projections_analysis:
        input_data += f"""
    earnings_projections_analysis: {earnings_projections_analysis.model_dump_json()}
    """

    # Add management guidance analysis if available for whisper number context
    if management_guidance_analysis:
        input_data += f"""
    management_guidance_analysis: {management_guidance_analysis.model_dump_json()}
    """

    try:
        # Run the market sentiment EPS check agent
        result: RunResult = await Runner.run(
            market_sentiment_eps_check_agent,
            input=input_data
        )

        validation_result: MarketSentimentEpsCheck = result.final_output

        # Log key sentiment validation metrics
        logger.info(f"Market sentiment EPS check completed for {symbol}: "
                   f"Revision momentum: {validation_result.revision_momentum}, "
                   f"Sentiment alignment: {validation_result.sentiment_eps_alignment}, "
                   f"Validation verdict: {validation_result.sentiment_validation_verdict}")

        # Log whisper vs consensus if available
        if validation_result.whisper_vs_consensus is not None:
            logger.info(f"Whisper vs consensus variance: {validation_result.whisper_vs_consensus:.1f}%")

        # Log sentiment insights count
        logger.info(f"Sentiment insights identified: {len(validation_result.sentiment_insights)} factors")

        # Log news sentiment context if available
        if news_sentiment_analysis:
            logger.info(f"News sentiment trend: {news_sentiment_analysis.sentiment_trend}, "
                       f"Volume: {news_sentiment_analysis.news_volume}, "
                       f"Confidence: {news_sentiment_analysis.sentiment_confidence}")

        # Log the full validation result as JSON for development visibility
        logger.debug(f"Market sentiment EPS check result for {symbol}: {json.dumps(validation_result.model_dump(), indent=2)}")

        return validation_result

    except Exception as e:
        logger.error(f"Error during market sentiment EPS check for {symbol}: {str(e)}")

        # Return error result with insufficient data verdict
        return MarketSentimentEpsCheck(
            symbol=symbol,
            revision_momentum=RevisionMomentum.INSUFFICIENT_DATA,
            sentiment_eps_alignment=SentimentAlignment.NEUTRAL,
            whisper_vs_consensus=None,
            sentiment_validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            revision_analysis=f"Market sentiment EPS check failed due to error: {str(e)}",
            sentiment_insights=[f"Validation process error: {str(e)}", "Unable to complete sentiment analysis"],
            market_expectation_summary="Sentiment validation error prevented market expectation analysis"
        )