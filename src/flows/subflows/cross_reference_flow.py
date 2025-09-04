from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysis
from src.tasks.common.status_update_task import publish_status_update_task
from src.tasks.cross_reference.cross_reference_reporting_task import cross_reference_reporting_task
from src.tasks.cross_reference.cross_reference_task import cross_reference_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
import logging
import time
from typing import List

logger = logging.getLogger(__name__)


async def cross_reference_flow(
    symbol: str,
    forward_pe_flow_result: ForwardPeValuation,
    news_sentiment_flow_result: NewsSentimentSummary,
    historical_earnings_analysis: HistoricalEarningsAnalysis,
    financial_statements_analysis: FinancialStatementsAnalysis,
    earnings_projections_analysis: EarningsProjectionAnalysis,
    management_guidance_analysis: ManagementGuidanceAnalysis,
) -> List[CrossReferencedAnalysis]:
    
    start_time = time.time()
    logger.info(f"Cross Reference flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "cross_reference_flow", "symbol": symbol})

    cross_reference_forward_pe_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=forward_pe_flow_result,
        data_points=[
            news_sentiment_flow_result,
            historical_earnings_analysis,
            financial_statements_analysis,
            earnings_projections_analysis,
            management_guidance_analysis
        ],
        original_analysis_type="forward_pe"
    )

    cross_reference_news_sentiment_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=news_sentiment_flow_result,
        data_points=[
            forward_pe_flow_result,
            historical_earnings_analysis,
            financial_statements_analysis,
            earnings_projections_analysis,
            management_guidance_analysis
        ],
        original_analysis_type="news_sentiment"
    )

    cross_reference_historical_earnings_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=historical_earnings_analysis,
        data_points=[
            forward_pe_flow_result,
            news_sentiment_flow_result,
            financial_statements_analysis,
            earnings_projections_analysis,
            management_guidance_analysis
        ],
        original_analysis_type="historical_earnings"
    )

    cross_reference_financial_statements_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=financial_statements_analysis,
        data_points=[
            forward_pe_flow_result,
            historical_earnings_analysis,
            news_sentiment_flow_result,
            earnings_projections_analysis,
            management_guidance_analysis
        ],
        original_analysis_type="financial_statements"
    )

    cross_reference_earnings_projections_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=earnings_projections_analysis,
        data_points=[
            forward_pe_flow_result,
            historical_earnings_analysis,
            financial_statements_analysis,
            news_sentiment_flow_result,
            management_guidance_analysis
        ],
        original_analysis_type="earnings_projections"
    )

    cross_reference_management_guidance_analysis: CrossReferencedAnalysis = await cross_reference_task(
        symbol=symbol,
        original_analysis=management_guidance_analysis,
        data_points=[
            forward_pe_flow_result,
            historical_earnings_analysis,
            financial_statements_analysis,
            earnings_projections_analysis,
            news_sentiment_flow_result
        ],
        original_analysis_type="management_guidance"
    )

    cross_referenced_analysis = [
        cross_reference_forward_pe_analysis,
        cross_reference_news_sentiment_analysis,
        cross_reference_historical_earnings_analysis,
        cross_reference_financial_statements_analysis,
        cross_reference_earnings_projections_analysis,
        cross_reference_management_guidance_analysis
    ]

    # Generate reporting output
    # await cross_reference_reporting_task(symbol, cross_reference_analysis)

    logger.info(f"Cross Reference flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "cross_reference_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return cross_referenced_analysis
