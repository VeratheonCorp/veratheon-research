from prefect import task
import json
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from agents import Runner, RunResult
from prefect import get_run_logger
from src.research.trade_ideas.trade_idea_agent import trade_idea_agent
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary


@task(name="trade_ideas_task", persist_result=True)
async def trade_ideas_task(
    symbol: str,
    earnings_analysis: ForwardPeValuation,
    news_sentiment_summary: NewsSentimentSummary,
) -> TradeIdea:
    """
    Task to perform trade ideas for the forward PE research for a given symbol.

    Args:
        symbol: Stock symbol to research
        earnings_analysis: ForwardPeValuation containing the forward PE analysis
        news_sentiment_summary: NewsSentimentSummary containing the news sentiment summary
    Returns:
        TradeIdea containing the trade ideas for users with no position
    """
    logger = get_run_logger()
    logger.info(f"Performing trade ideas for users with no position in {symbol}")

    result: RunResult = await Runner.run(
        trade_idea_agent,
        input=f"original_symbol: {symbol}, earnings_analysis: {earnings_analysis}, news_sentiment_summary: {news_sentiment_summary}",
    )
    trade_idea: TradeIdea = result.final_output

    logger.info(
        f"Trade idea for {symbol}: {json.dumps(trade_idea.model_dump(), indent=2)}"
    )

    return trade_idea
