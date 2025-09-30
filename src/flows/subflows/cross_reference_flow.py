from src.research.cross_reference.cross_reference_models import (
    CrossReferencedAnalysisCompletion,
)
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import (
    HistoricalEarningsAnalysis,
)
from src.research.financial_statements.financial_statements_models import (
    FinancialStatementsAnalysis,
)
from src.research.earnings_projections.earnings_projections_models import (
    EarningsProjectionAnalysis,
)
from src.research.management_guidance.management_guidance_models import (
    ManagementGuidanceAnalysis,
)
from src.research.eps_validation.eps_validation_models import (
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    TechnicalEpsValidation,
)
import logging
import time
from typing import List
from src.tasks.cache_retrieval.cross_reference_cache_retrieval_task import cross_reference_cache_retrieval_task
from src.tasks.cross_reference.cross_reference_task import cross_reference_task
from src.tasks.cross_reference.cross_reference_reporting_task import (
    cross_reference_reporting_task,
)
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CrossReferenceContext:
    symbol: str
    forward_pe_flow_result: ForwardPeValuation
    news_sentiment_flow_result: NewsSentimentSummary
    historical_earnings_analysis: HistoricalEarningsAnalysis
    financial_statements_analysis: FinancialStatementsAnalysis
    earnings_projections_analysis: EarningsProjectionAnalysis
    management_guidance_analysis: ManagementGuidanceAnalysis
    peer_relative_eps_validation: PeerRelativeEpsValidation = None
    market_sentiment_eps_check: MarketSentimentEpsCheck = None
    technical_eps_validation: TechnicalEpsValidation = None
    eps_validation_synthesis: EpsValidationSynthesis = None


async def cross_reference_flow(
    symbol: str,
    forward_pe_flow_result: ForwardPeValuation,
    news_sentiment_flow_result: NewsSentimentSummary,
    historical_earnings_analysis: HistoricalEarningsAnalysis,
    financial_statements_analysis: FinancialStatementsAnalysis,
    earnings_projections_analysis: EarningsProjectionAnalysis,
    management_guidance_analysis: ManagementGuidanceAnalysis,
    peer_relative_eps_validation: PeerRelativeEpsValidation = None,
    market_sentiment_eps_check: MarketSentimentEpsCheck = None,
    technical_eps_validation: TechnicalEpsValidation = None,
    eps_validation_synthesis: EpsValidationSynthesis = None,
    force_recompute: bool = False,
) -> List[CrossReferencedAnalysisCompletion]:

    context = CrossReferenceContext(
        symbol=symbol,
        forward_pe_flow_result=forward_pe_flow_result,
        news_sentiment_flow_result=news_sentiment_flow_result,
        historical_earnings_analysis=historical_earnings_analysis,
        financial_statements_analysis=financial_statements_analysis,
        earnings_projections_analysis=earnings_projections_analysis,
        management_guidance_analysis=management_guidance_analysis,
        peer_relative_eps_validation=peer_relative_eps_validation,
        market_sentiment_eps_check=market_sentiment_eps_check,
        technical_eps_validation=technical_eps_validation,
        eps_validation_synthesis=eps_validation_synthesis,
    )

    start_time = time.time()
    logger.info(f"Cross Reference flow started for {context.symbol}")

    # Try to get cached report first
    cached_result = await cross_reference_cache_retrieval_task(context.symbol, forward_pe_flow_result, news_sentiment_flow_result, historical_earnings_analysis, financial_statements_analysis, earnings_projections_analysis, management_guidance_analysis, force_recompute)
    if cached_result is not None:
        logger.info(f"Returning cached cross reference analysis for {context.symbol}")
        return cached_result
    
    logger.info(f"No cached data found, running fresh cross reference analysis for {context.symbol}")

    cross_reference_forward_pe_completion = await forward_pe_cross_reference(context)

    cross_reference_news_sentiment_completion = await news_sentiment_cross_reference(
        context
    )

    cross_reference_historical_earnings_completion = (
        await historical_earnings_cross_reference(context)
    )

    cross_reference_financial_statements_completion = (
        await financial_statements_cross_reference(context)
    )

    cross_reference_earnings_projections_completion = (
        await earnings_projections_cross_reference(context)
    )

    cross_reference_management_guidance_completion = (
        await management_guidance_cross_reference(context)
    )

    cross_referenced_analysis = [
        cross_reference_forward_pe_completion,
        cross_reference_news_sentiment_completion,
        cross_reference_historical_earnings_completion,
        cross_reference_financial_statements_completion,
        cross_reference_earnings_projections_completion,
        cross_reference_management_guidance_completion,
    ]

    # Add EPS validation cross references if data is available
    if context.eps_validation_synthesis:
        eps_validation_synthesis_cross_reference_completion = (
            await eps_validation_synthesis_cross_reference(context)
        )
        cross_referenced_analysis.append(eps_validation_synthesis_cross_reference_completion)

    # Generate reporting output
    await cross_reference_reporting_task(symbol, cross_referenced_analysis)

    logger.info(
        f"Cross Reference flow completed for {context.symbol} in {int(time.time() - start_time)} seconds"
    )

    return cross_referenced_analysis


async def forward_pe_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.news_sentiment_flow_result,
        context.historical_earnings_analysis,
        context.financial_statements_analysis,
        context.earnings_projections_analysis,
        context.management_guidance_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_forward_pe_completion: CrossReferencedAnalysisCompletion = (
        await cross_reference_task(
            symbol=context.symbol,
            original_analysis_type="forward_pe",
            original_analysis=context.forward_pe_flow_result,
            data_points=data_points,
        )
    )
    return cross_reference_forward_pe_completion


async def news_sentiment_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.forward_pe_flow_result,
        context.historical_earnings_analysis,
        context.financial_statements_analysis,
        context.earnings_projections_analysis,
        context.management_guidance_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_news_sentiment_completion: CrossReferencedAnalysisCompletion = (
        await cross_reference_task(
            symbol=context.symbol,
            original_analysis_type="news_sentiment",
            original_analysis=context.news_sentiment_flow_result,
            data_points=data_points,
        )
    )
    return cross_reference_news_sentiment_completion


async def historical_earnings_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.forward_pe_flow_result,
        context.news_sentiment_flow_result,
        context.financial_statements_analysis,
        context.earnings_projections_analysis,
        context.management_guidance_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_historical_earnings_completion: (
        CrossReferencedAnalysisCompletion
    ) = await cross_reference_task(
        symbol=context.symbol,
        original_analysis_type="historical_earnings",
        original_analysis=context.historical_earnings_analysis,
        data_points=data_points,
    )
    return cross_reference_historical_earnings_completion


async def financial_statements_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.forward_pe_flow_result,
        context.historical_earnings_analysis,
        context.news_sentiment_flow_result,
        context.earnings_projections_analysis,
        context.management_guidance_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_financial_statements_completion: (
        CrossReferencedAnalysisCompletion
    ) = await cross_reference_task(
        symbol=context.symbol,
        original_analysis_type="financial_statements",
        original_analysis=context.financial_statements_analysis,
        data_points=data_points,
    )
    return cross_reference_financial_statements_completion


async def earnings_projections_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.forward_pe_flow_result,
        context.historical_earnings_analysis,
        context.news_sentiment_flow_result,
        context.financial_statements_analysis,
        context.management_guidance_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_earnings_projections_completion: (
        CrossReferencedAnalysisCompletion
    ) = await cross_reference_task(
        symbol=context.symbol,
        original_analysis_type="earnings_projections",
        original_analysis=context.earnings_projections_analysis,
        data_points=data_points,
    )
    return cross_reference_earnings_projections_completion


async def management_guidance_cross_reference(context: CrossReferenceContext):
    data_points = [
        context.forward_pe_flow_result,
        context.historical_earnings_analysis,
        context.news_sentiment_flow_result,
        context.financial_statements_analysis,
        context.earnings_projections_analysis,
    ]

    # Add EPS validation data if available
    if context.eps_validation_synthesis:
        data_points.append(context.eps_validation_synthesis)

    cross_reference_management_guidance_completion: (
        CrossReferencedAnalysisCompletion
    ) = await cross_reference_task(
        symbol=context.symbol,
        original_analysis_type="management_guidance",
        original_analysis=context.management_guidance_analysis,
        data_points=data_points,
    )
    return cross_reference_management_guidance_completion


async def eps_validation_synthesis_cross_reference(context: CrossReferenceContext):
    """Cross-reference EPS validation synthesis against all other analyses"""
    data_points = [
        context.forward_pe_flow_result,
        context.news_sentiment_flow_result,
        context.historical_earnings_analysis,
        context.financial_statements_analysis,
        context.earnings_projections_analysis,
        context.management_guidance_analysis,
    ]

    # Add individual EPS validation results if available
    if context.peer_relative_eps_validation:
        data_points.append(context.peer_relative_eps_validation)
    if context.market_sentiment_eps_check:
        data_points.append(context.market_sentiment_eps_check)
    if context.technical_eps_validation:
        data_points.append(context.technical_eps_validation)

    cross_reference_eps_validation_synthesis_completion: (
        CrossReferencedAnalysisCompletion
    ) = await cross_reference_task(
        symbol=context.symbol,
        original_analysis_type="eps_validation_synthesis",
        original_analysis=context.eps_validation_synthesis,
        data_points=data_points,
    )
    return cross_reference_eps_validation_synthesis_completion
