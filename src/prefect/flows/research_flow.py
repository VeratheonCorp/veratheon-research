from prefect import flow, get_run_logger
from dotenv import load_dotenv
from src.prefect.flows.forward_pe_flow import forward_pe_flow
from src.prefect.flows.trade_ideas_flow import trade_ideas_flow
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.trade_ideas.trade_idea_models import TradeIdeas

load_dotenv()

@flow(name="main-research-flow", log_prints=True)
async def main_research_flow(
    symbol: str,
) -> TradeIdeas:
    logger = get_run_logger()
    logger.info(f"Starting main research for {symbol}")
    forward_pe_flow_result: ForwardPeValuation = await forward_pe_flow(symbol)
    trade_ideas_flow_result: TradeIdeas = await trade_ideas_flow(symbol, forward_pe_flow_result)
    logger.info(f"Trade ideas for {symbol}: {trade_ideas_flow_result}")
    logger.info(f"Main research for {symbol} completed successfully!")
    return trade_ideas_flow_result
