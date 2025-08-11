from prefect import flow, get_run_logger
from src.prefect.tasks.trade_ideas.trade_ideas_task import trade_ideas_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary

@flow(name="trade-ideas-flow", log_prints=True)
async def trade_ideas_flow(
    symbol: str,
    forward_pe_valuation: ForwardPeValuation,
    news_sentiment_summary: NewsSentimentSummary,
) -> TradeIdea:
    logger = get_run_logger()
    logger.info(f"Starting trade ideas flow for {symbol}")
    
    trade_idea = await trade_ideas_task(symbol, forward_pe_valuation, news_sentiment_summary)
    
    return trade_idea
