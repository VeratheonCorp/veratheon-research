from prefect import flow, get_run_logger
from src.prefect.tasks.trade_ideas.trade_ideas_task import trade_ideas_task
from src.prefect.tasks.events.event_emission_task import emit_event_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from typing import Optional, Any

@flow(name="trade-ideas-flow", log_prints=True)
async def trade_ideas_flow(
    symbol: str,
    forward_pe_valuation: ForwardPeValuation,
    news_sentiment_summary: NewsSentimentSummary,
    historical_earnings_analysis: Optional[Any] = None,
    financial_statements_analysis: Optional[Any] = None,
    earnings_projections_analysis: Optional[Any] = None,
    management_guidance_analysis: Optional[Any] = None,
) -> TradeIdea:
    logger = get_run_logger()
    
    # Emit stage start event
    emit_event_task(symbol, "stage_start", stage="trade_ideas",
                   message="Generating trade ideas and recommendations...")
    
    logger.info(f"Starting trade ideas flow for {symbol}")
    
    trade_idea = await trade_ideas_task(
        symbol, 
        forward_pe_valuation, 
        news_sentiment_summary,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis
    )
    
    # Emit stage complete event
    emit_event_task(symbol, "stage_complete", stage="trade_ideas",
                   message="Trade ideas generation completed",
                   data={
                       "recommendation": trade_idea.recommendation,
                       "target_price": trade_idea.target_price,
                       "confidence_level": trade_idea.confidence_level
                   })
    
    # Emit final research complete event
    emit_event_task(symbol, "research_complete",
                   message=f"Complete research analysis for {symbol} finished successfully!",
                   data=trade_idea.model_dump())
    
    return trade_idea
