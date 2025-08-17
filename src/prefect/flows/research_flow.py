from prefect import flow, get_run_logger
from dotenv import load_dotenv
from src.prefect.flows.subflows.forward_pe_flow import forward_pe_flow
from src.prefect.flows.subflows.trade_ideas_flow import trade_ideas_flow
from src.prefect.flows.subflows.news_sentiment_flow import news_sentiment_flow
from src.prefect.flows.subflows.forward_pe_flow import forward_pe_sanity_check_flow
from src.prefect.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.common.peer_group_agent import peer_group_agent
from src.research.common.models.peer_group import PeerGroup

load_dotenv()

@flow(name="main-research-flow", log_prints=True)
async def main_research_flow(
    symbol: str,
) -> TradeIdea:
    logger = get_run_logger()
    logger.info(f"Starting main research for {symbol}")

    # Step 1: Historical earnings analysis (CRITICAL - foundational baseline)
    historical_earnings_analysis: HistoricalEarningsAnalysis = await historical_earnings_flow(symbol)

    # Step 2: Peer group identification
    peer_group: PeerGroup = await peer_group_agent(symbol)

    # Step 3: Forward PE sanity check
    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_flow(symbol)

    # Step 4: Forward PE analysis
    forward_pe_flow_result: ForwardPeValuation = await forward_pe_flow(symbol, peer_group)

    # Step 5: News sentiment analysis
    news_sentiment_flow_result: NewsSentimentSummary = await news_sentiment_flow(symbol, peer_group)

    # Step 6: Generate trade ideas
    trade_ideas_flow_result: TradeIdea = await trade_ideas_flow(symbol, forward_pe_flow_result, news_sentiment_flow_result)

    logger.info(f"Main research for {symbol} completed successfully!")
    logger.info(f"Historical earnings pattern: {historical_earnings_analysis.earnings_pattern}")
    logger.info(f"Revenue growth trend: {historical_earnings_analysis.revenue_growth_trend}")
    logger.info(f"Margin trend: {historical_earnings_analysis.margin_trend}")
    
    return trade_ideas_flow_result
