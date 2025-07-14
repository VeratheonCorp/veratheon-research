from prefect import flow, get_run_logger
from src.prefect.tasks.trade_ideas.trade_ideas_task import trade_ideas_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.trade_ideas.trade_idea_models import TradeIdeas

@flow(name="trade-ideas-flow", log_prints=True)
async def trade_ideas_flow(
    symbol: str,
    forward_pe_valuation: ForwardPeValuation,
) -> TradeIdeas:
    logger = get_run_logger()
    logger.info(f"Starting trade ideas flow for {symbol}")
    
    no_position_trade_idea, has_position_trade_idea = await trade_ideas_task(symbol, forward_pe_valuation)
    
    return TradeIdeas(
        no_position_trade_idea=no_position_trade_idea,
        has_position_trade_idea=has_position_trade_idea
    )
