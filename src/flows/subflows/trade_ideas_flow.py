from src.tasks.trade_ideas.trade_ideas_task import trade_ideas_task
from src.tasks.trade_ideas.trade_ideas_reporting_task import trade_ideas_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.tasks.cache_retrieval.trade_ideas_cache_retrieval_task import trade_ideas_cache_retrieval_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from typing import Optional, Any
import logging
import time

logger = logging.getLogger(__name__)

async def trade_ideas_flow(
    symbol: str,
    forward_pe_valuation: ForwardPeValuation,
    news_sentiment_summary: NewsSentimentSummary,
    historical_earnings_analysis: Optional[Any] = None,
    financial_statements_analysis: Optional[Any] = None,
    earnings_projections_analysis: Optional[Any] = None,
    management_guidance_analysis: Optional[Any] = None,
) -> TradeIdea:
    
    start_time = time.time()
    logger.info(f"Trade Ideas flow started for {symbol}")
    
    # Try to get cached report first
    cached_result = await trade_ideas_cache_retrieval_task(symbol, forward_pe_valuation, news_sentiment_summary, historical_earnings_analysis, financial_statements_analysis, earnings_projections_analysis, management_guidance_analysis)
    if cached_result is not None:
        logger.info(f"Returning cached trade ideas analysis for {symbol}")
        return cached_result
    
    logger.info(f"No cached data found, running fresh trade ideas analysis for {symbol}")
    await publish_status_update_task("starting", {"flow": "trade_ideas_flow", "symbol": symbol})
    
    trade_idea = await trade_ideas_task(
        symbol, 
        forward_pe_valuation, 
        news_sentiment_summary,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis
    )
    
    # Generate reporting output
    await trade_ideas_reporting_task(symbol, trade_idea)
    
    logger.info(f"Trade Ideas flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "trade_ideas_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})
    
    return trade_idea
