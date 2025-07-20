from prefect import task
from typing import Tuple
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from agents import Runner, RunResult
from prefect import get_run_logger
from src.research.trade_ideas.no_position_trade_idea_agent import no_position_trade_idea_agent
from src.research.trade_ideas.has_position_trade_idea_agent import has_position_trade_idea_agent
from src.research.trade_ideas.trade_idea_models import NoPositionTradeIdea, HasPositionTradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary

@task(name="trade_ideas_task", persist_result=True)
async def trade_ideas_task(symbol: str, earnings_analysis: ForwardPeValuation, news_sentiment_summary: NewsSentimentSummary) -> Tuple[NoPositionTradeIdea, HasPositionTradeIdea]:
    """
    Task to perform trade ideas for the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        earnings_analysis: ForwardPeValuation containing the forward PE analysis
        news_sentiment_summary: NewsSentimentSummary containing the news sentiment summary
    Returns:
        Tuple containing the trade ideas for users with no position and users with position
    """
    logger = get_run_logger()
    logger.info(f"Performing trade ideas for users with no position in {symbol}")

    result: RunResult = await Runner.run(
        no_position_trade_idea_agent,
        input=f"original_symbol: {symbol}, earnings_analysis: {earnings_analysis}, news_sentiment_summary: {news_sentiment_summary}")
    no_position_trade_idea: NoPositionTradeIdea = result.final_output

    logger.info(f"Performing trade ideas for users with position in {symbol}")

    result: RunResult = await Runner.run(
        has_position_trade_idea_agent,
        input=f"original_symbol: {symbol}, earnings_analysis: {earnings_analysis}, news_sentiment_summary: {news_sentiment_summary}")
    has_position_trade_idea: HasPositionTradeIdea = result.final_output

    logger.info(f"No position trade idea for {symbol}: {no_position_trade_idea}")
    logger.info(f"Has position trade idea for {symbol}: {has_position_trade_idea}")

    return no_position_trade_idea, has_position_trade_idea
