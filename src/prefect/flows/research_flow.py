from prefect import flow, get_run_logger
from dotenv import load_dotenv
from src.prefect.flows.subflows.forward_pe_flow import forward_pe_flow
from src.prefect.flows.subflows.trade_ideas_flow import trade_ideas_flow
from src.prefect.flows.subflows.news_sentiment_flow import news_sentiment_flow
from src.prefect.flows.subflows.forward_pe_flow import forward_pe_sanity_check_flow
from src.prefect.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.prefect.flows.subflows.financial_statements_flow import financial_statements_flow
from src.prefect.flows.subflows.earnings_projections_flow import earnings_projections_flow
from src.prefect.flows.subflows.management_guidance_flow import management_guidance_flow
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
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

    # Step 2: Financial statements analysis (CRITICAL - recent changes for projection accuracy)
    financial_statements_analysis: FinancialStatementsAnalysis = await financial_statements_flow(symbol)

    # Step 3: Independent earnings projections (CRITICAL - foundational baseline for consensus validation)
    earnings_projections_analysis: EarningsProjectionAnalysis = await earnings_projections_flow(
        symbol, 
        historical_earnings_analysis.model_dump(), 
        financial_statements_analysis.model_dump()
    )

    # Step 4: Management guidance analysis (CRITICAL - cross-check against management guidance from earnings calls)
    management_guidance_analysis: ManagementGuidanceAnalysis = await management_guidance_flow(symbol)

    # Step 5: Peer group identification
    peer_group: PeerGroup = await peer_group_agent(symbol)

    # Step 6: Forward PE sanity check
    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_flow(symbol)

    # Step 7: Forward PE analysis
    forward_pe_flow_result: ForwardPeValuation = await forward_pe_flow(symbol, peer_group)

    # Step 8: News sentiment analysis
    news_sentiment_flow_result: NewsSentimentSummary = await news_sentiment_flow(symbol, peer_group)

    # Step 9: Generate trade ideas
    trade_ideas_flow_result: TradeIdea = await trade_ideas_flow(symbol, forward_pe_flow_result, news_sentiment_flow_result)

    logger.info(f"Main research for {symbol} completed successfully!")
    logger.info(f"Historical earnings pattern: {historical_earnings_analysis.earnings_pattern}")
    logger.info(f"Revenue growth trend: {historical_earnings_analysis.revenue_growth_trend}")
    logger.info(f"Margin trend: {historical_earnings_analysis.margin_trend}")
    logger.info(f"Revenue driver trend: {financial_statements_analysis.revenue_driver_trend}")
    logger.info(f"Cost structure trend: {financial_statements_analysis.cost_structure_trend}")
    logger.info(f"Working capital trend: {financial_statements_analysis.working_capital_trend}")
    logger.info(f"Independent EPS projection: ${earnings_projections_analysis.next_quarter_projection.projected_eps:.2f}")
    logger.info(f"Projection confidence: {earnings_projections_analysis.overall_confidence}")
    logger.info(f"Management guidance tone: {management_guidance_analysis.overall_guidance_tone}")
    logger.info(f"Consensus validation signal: {management_guidance_analysis.consensus_validation_signal}")
    
    return trade_ideas_flow_result
