from dotenv import load_dotenv
from src.flows.subflows.forward_pe_flow import forward_pe_flow
from src.flows.subflows.trade_ideas_flow import trade_ideas_flow
from src.flows.subflows.news_sentiment_flow import news_sentiment_flow
from src.flows.subflows.forward_pe_flow import forward_pe_sanity_check_flow
from src.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.flows.subflows.financial_statements_flow import financial_statements_flow
from src.flows.subflows.earnings_projections_flow import earnings_projections_flow
from src.flows.subflows.management_guidance_flow import management_guidance_flow
from src.flows.subflows.cross_reference_flow import cross_reference_flow
from src.tasks.common.status_update_task import publish_status_update_task
from src.tasks.common.peer_group_reporting_task import peer_group_reporting_task
from src.tasks.common.reporting_directory_setup_task import ensure_reporting_directory_exists
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.common.peer_group_agent import peer_group_agent
from src.research.common.models.peer_group import PeerGroup
from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysisCompletion

import logging
import time

logger = logging.getLogger(__name__)

load_dotenv()

async def main_research_flow(
    symbol: str,
) -> dict:

    start_time = time.time()
    logger.info(f"Main research flow started for {symbol}")
    
    await ensure_reporting_directory_exists()
    
    await publish_status_update_task("starting", {"flow": "main_research_flow", "symbol": symbol})

    historical_earnings_analysis: HistoricalEarningsAnalysis = await historical_earnings_flow(symbol)

    financial_statements_analysis: FinancialStatementsAnalysis = await financial_statements_flow(symbol)

    earnings_projections_analysis: EarningsProjectionAnalysis = await earnings_projections_flow(
        symbol, 
        historical_earnings_analysis.model_dump(), 
        financial_statements_analysis.model_dump()
    )

    management_guidance_analysis: ManagementGuidanceAnalysis = await management_guidance_flow(
        symbol, 
        historical_earnings_analysis, 
        financial_statements_analysis
    )

    peer_group: PeerGroup = await peer_group_agent(symbol, financial_statements_analysis)
    
    await peer_group_reporting_task(symbol, peer_group)

    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_flow(symbol)

    forward_pe_flow_result: ForwardPeValuation = await forward_pe_flow(
        symbol, 
        peer_group, 
        earnings_projections_analysis,
        management_guidance_analysis, 
        forward_pe_sanity_check
    )

    news_sentiment_flow_result: NewsSentimentSummary = await news_sentiment_flow(
        symbol, 
        peer_group, 
        earnings_projections_analysis, 
        management_guidance_analysis
    )

    cross_reference_flow_result: List[CrossReferencedAnalysisCompletion] = await cross_reference_flow(
        symbol, 
        forward_pe_flow_result, 
        news_sentiment_flow_result,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis
    )

    trade_ideas_flow_result: TradeIdea = await trade_ideas_flow(
        symbol, 
        forward_pe_flow_result, 
        news_sentiment_flow_result,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis
    )
    
    logger.info(f"Main research for {symbol} completed successfully! in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "main_research_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})
    
    return {
        "symbol": symbol,
        "historical_earnings_analysis": historical_earnings_analysis.model_dump(),
        "financial_statements_analysis": financial_statements_analysis.model_dump(),
        "earnings_projections_analysis": earnings_projections_analysis.model_dump(),
        "management_guidance_analysis": management_guidance_analysis.model_dump(),
        "peer_group": peer_group.model_dump(),
        "forward_pe_sanity_check": forward_pe_sanity_check.model_dump(),
        "forward_pe_valuation": forward_pe_flow_result.model_dump(),
        "news_sentiment_summary": news_sentiment_flow_result.model_dump(),
        "cross_reference": [item.model_dump() for item in cross_reference_flow_result],
        "trade_idea": trade_ideas_flow_result.model_dump()
    }
