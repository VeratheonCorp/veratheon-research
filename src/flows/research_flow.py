from dotenv import load_dotenv
from src.flows.subflows.forward_pe_flow import forward_pe_flow, forward_pe_sanity_check_flow
from src.flows.subflows.trade_ideas_flow import trade_ideas_flow
from src.flows.subflows.news_sentiment_flow import news_sentiment_flow
from src.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.flows.subflows.financial_statements_flow import financial_statements_flow
from src.flows.subflows.earnings_projections_flow import earnings_projections_flow
from src.flows.subflows.management_guidance_flow import management_guidance_flow
from src.flows.subflows.cross_reference_flow import cross_reference_flow
from src.flows.subflows.comprehensive_report_flow import comprehensive_report_flow
from src.flows.subflows.key_insights_flow import key_insights_flow
from src.flows.subflows.company_overview_flow import company_overview_flow
from src.flows.subflows.global_quote_flow import global_quote_flow
from src.tasks.common.job_status_task import update_job_status_task
from src.lib.supabase_job_tracker import JobStatus, get_job_tracker
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
from src.research.comprehensive_report.comprehensive_report_models import ComprehensiveReport, KeyInsights
from src.research.company_overview.company_overview_models import CompanyOverviewAnalysis
from src.research.global_quote.global_quote_models import GlobalQuoteData

import logging
import time
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)

load_dotenv()

def get_current_date() -> str:
    """
    Get today's current date in YYYY-MM-DD format.
    
    Returns:
        str: Current date in ISO format (YYYY-MM-DD)
    """
    return datetime.now().strftime("%Y-%m-%d")

async def main_research_flow(
    symbol: str,
    force_recompute: bool = False,
    job_id: str = None,
) -> dict:

    start_time = time.time()
    logger.info(f"Main research flow started for {symbol}")
    
    await ensure_reporting_directory_exists()
    
    await update_job_status_task(job_id, JobStatus.RUNNING, "Starting main research flow", "main_research_flow", symbol)

    # Company overview provides foundational business context
    job_tracker = get_job_tracker()
    co_subjob = job_tracker.create_job(
        job_type="research_subflow",
        symbol=symbol,
        main_job_id=job_id,
        is_sub_job=True,
        job_name="company_overview_flow"
    )
    job_tracker.update_job_status(co_subjob["sub_job_id"], JobStatus.RUNNING, step="Analyzing company overview", use_sub_job_id=True)
    company_overview_analysis: CompanyOverviewAnalysis = await company_overview_flow(symbol, force_recompute=force_recompute)
    job_tracker.update_job_status(co_subjob["sub_job_id"], JobStatus.COMPLETED, step="Company overview complete", use_sub_job_id=True)

    # Global quote provides current price data
    await update_job_status_task(job_id, JobStatus.RUNNING, "Fetching current market data", "global_quote_flow", symbol)
    global_quote_data: GlobalQuoteData = await global_quote_flow(symbol, force_recompute=force_recompute)

    await update_job_status_task(job_id, JobStatus.RUNNING, "Analyzing historical earnings", "historical_earnings_flow", symbol)
    historical_earnings_analysis: HistoricalEarningsAnalysis = await historical_earnings_flow(symbol, force_recompute=force_recompute)

    await update_job_status_task(job_id, JobStatus.RUNNING, "Analyzing financial statements", "financial_statements_flow", symbol)
    financial_statements_analysis: FinancialStatementsAnalysis = await financial_statements_flow(symbol, force_recompute=force_recompute)

    await update_job_status_task(job_id, JobStatus.RUNNING, "Generating earnings projections", "earnings_projections_flow", symbol)
    earnings_projections_analysis: EarningsProjectionAnalysis = await earnings_projections_flow(
        symbol,
        historical_earnings_analysis.model_dump(),
        financial_statements_analysis.model_dump(),
        force_recompute=force_recompute
    )

    await update_job_status_task(job_id, JobStatus.RUNNING, "Analyzing management guidance", "management_guidance_flow", symbol)
    management_guidance_analysis: ManagementGuidanceAnalysis = await management_guidance_flow(
        symbol,
        historical_earnings_analysis,
        financial_statements_analysis,
        force_recompute=force_recompute
    )

    await update_job_status_task(job_id, JobStatus.RUNNING, "Identifying peer group", "peer_group_analysis", symbol)
    peer_group: PeerGroup = await peer_group_agent(symbol, financial_statements_analysis)

    await peer_group_reporting_task(symbol, peer_group)

    await update_job_status_task(job_id, JobStatus.RUNNING, "Performing forward PE sanity check", "forward_pe_sanity_check_flow", symbol)
    forward_pe_sanity_check: ForwardPeSanityCheck = await forward_pe_sanity_check_flow(symbol, force_recompute=force_recompute)

    await update_job_status_task(job_id, JobStatus.RUNNING, "Calculating forward PE analysis", "forward_pe_flow", symbol)
    forward_pe_flow_result: ForwardPeValuation = await forward_pe_flow(
        symbol,
        peer_group,
        earnings_projections_analysis,
        management_guidance_analysis,
        forward_pe_sanity_check,
        force_recompute=force_recompute
    )

    await update_job_status_task(job_id, JobStatus.RUNNING, "Analyzing news sentiment", "news_sentiment_flow", symbol)
    news_sentiment_flow_result: NewsSentimentSummary = await news_sentiment_flow(
        symbol,
        peer_group,
        earnings_projections_analysis,
        management_guidance_analysis,
        force_recompute=force_recompute
    )

    await update_job_status_task(job_id, JobStatus.RUNNING, "Cross-referencing analysis", "cross_reference_flow", symbol)
    cross_reference_flow_result: List[CrossReferencedAnalysisCompletion] = await cross_reference_flow(
        symbol,
        forward_pe_flow_result,
        news_sentiment_flow_result,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis,
        force_recompute=force_recompute
    )

    await update_job_status_task(job_id, JobStatus.RUNNING, "Generating trade ideas", "trade_ideas_flow", symbol)
    trade_ideas_flow_result: TradeIdea = await trade_ideas_flow(
        symbol,
        forward_pe_flow_result,
        news_sentiment_flow_result,
        historical_earnings_analysis,
        financial_statements_analysis,
        earnings_projections_analysis,
        management_guidance_analysis,
        force_recompute=force_recompute
    )

    # Collect all analyses for comprehensive report
    all_analyses = {
        "symbol": symbol,
        "analysis_date": get_current_date(),
        "company_overview_analysis": company_overview_analysis.model_dump(),
        "global_quote_data": global_quote_data.model_dump(),
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

    # Generate comprehensive report
    await update_job_status_task(job_id, JobStatus.RUNNING, "Generating comprehensive report", "comprehensive_report_flow", symbol)
    comprehensive_report: ComprehensiveReport = await comprehensive_report_flow(
        symbol,
        all_analyses,
        force_recompute=force_recompute
    )
    logger.info(f"Comprehensive report generated for {symbol}")

    # Generate key insights from comprehensive report
    await update_job_status_task(job_id, JobStatus.RUNNING, "Extracting key insights", "key_insights_flow", symbol)
    key_insights: KeyInsights = await key_insights_flow(
        symbol,
        comprehensive_report,
        force_recompute=force_recompute
    )
    logger.info(f"Key insights generated for {symbol}")

    duration_seconds = int(time.time() - start_time)
    logger.info(f"Main research for {symbol} completed successfully! in {duration_seconds} seconds")
    
    return {
        "symbol": symbol,
        "comprehensive_report": comprehensive_report.model_dump(),
        "key_insights": key_insights.model_dump()
    }
