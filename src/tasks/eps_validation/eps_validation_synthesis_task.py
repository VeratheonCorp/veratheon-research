from typing import Optional
from src.research.eps_validation.eps_validation_models import (
    EpsValidationSynthesis, BottomUpEpsValidation, PeerRelativeEpsValidation,
    MarketSentimentEpsCheck, EpsValidationVerdict
)
from src.research.eps_validation.eps_validation_synthesis_agent import eps_validation_synthesis_agent
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from agents import Runner, RunResult
import json
import logging

logger = logging.getLogger(__name__)

async def eps_validation_synthesis_task(
    symbol: str,
    historical_earnings_analysis: Optional[HistoricalEarningsAnalysis] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    management_guidance_analysis: Optional[ManagementGuidanceAnalysis] = None,
    bottom_up_eps_validation: Optional[BottomUpEpsValidation] = None,
    peer_relative_eps_validation: Optional[PeerRelativeEpsValidation] = None,
    market_sentiment_eps_check: Optional[MarketSentimentEpsCheck] = None,
    consensus_eps: Optional[float] = None
) -> EpsValidationSynthesis:
    """
    Task to orchestrate EPS validation synthesis across all validation methods.

    Args:
        symbol: Stock symbol to research
        historical_earnings_analysis: Historical earnings patterns analysis
        earnings_projections_analysis: Independent earnings projections analysis
        management_guidance_analysis: Management guidance analysis
        bottom_up_eps_validation: Bottom-up EPS validation results
        peer_relative_eps_validation: Peer-relative EPS validation results
        market_sentiment_eps_check: Market sentiment EPS check results
        consensus_eps: Wall Street consensus EPS estimate for reference
    Returns:
        EpsValidationSynthesis containing comprehensive multi-method validation verdict
    """

    logger.info(f"EPS validation synthesis started for {symbol}")

    # Count available validation methods
    available_methods = []
    if historical_earnings_analysis:
        available_methods.append("historical_earnings")
    if earnings_projections_analysis:
        available_methods.append("earnings_projections")
    if management_guidance_analysis:
        available_methods.append("management_guidance")
    if bottom_up_eps_validation:
        available_methods.append("bottom_up")
    if peer_relative_eps_validation:
        available_methods.append("peer_relative")
    if market_sentiment_eps_check:
        available_methods.append("market_sentiment")

    logger.info(f"Available validation methods for {symbol}: {len(available_methods)} ({', '.join(available_methods)})")

    # Handle insufficient validation data
    if len(available_methods) < 2:
        logger.warning(f"Insufficient validation methods for {symbol} (only {len(available_methods)} available)")

        # If we have at least one method, try to extract its verdict for basic synthesis
        single_verdict = EpsValidationVerdict.INSUFFICIENT_DATA
        if bottom_up_eps_validation:
            single_verdict = bottom_up_eps_validation.validation_verdict
        elif peer_relative_eps_validation:
            single_verdict = peer_relative_eps_validation.peer_comparison_verdict
        elif market_sentiment_eps_check:
            single_verdict = market_sentiment_eps_check.sentiment_validation_verdict

        return EpsValidationSynthesis(
            symbol=symbol,
            overall_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            confidence_score=0.2,  # Low confidence due to insufficient methods
            method_agreement={method: single_verdict for method in available_methods},
            key_risks=["Insufficient validation methods", "Limited data for comprehensive analysis"],
            supporting_evidence=["Limited validation data available"],
            consensus_adjustment_recommendation=None,
            synthesis_analysis=f"Only {len(available_methods)} validation method(s) available, insufficient for reliable synthesis",
            investment_implications="High uncertainty due to limited EPS validation data - require additional analysis"
        )

    # Extract consensus EPS from available sources if not provided
    if consensus_eps is None:
        if earnings_projections_analysis and earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate:
            consensus_eps = earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate
            logger.info(f"Using consensus EPS from earnings projections: ${consensus_eps:.2f}")
        elif bottom_up_eps_validation:
            consensus_eps = bottom_up_eps_validation.consensus_eps
            logger.info(f"Using consensus EPS from bottom-up validation: ${consensus_eps:.2f}")
        elif peer_relative_eps_validation:
            consensus_eps = peer_relative_eps_validation.consensus_eps
            logger.info(f"Using consensus EPS from peer-relative validation: ${consensus_eps:.2f}")
        else:
            logger.warning(f"No consensus EPS available for {symbol}")
            consensus_eps = 0.0

    # Prepare comprehensive input data for the synthesis agent
    input_data = f"""
    symbol: {symbol}
    consensus_eps_estimate: {consensus_eps}
    available_validation_methods: {available_methods}
    """

    # Add historical earnings analysis if available
    if historical_earnings_analysis:
        input_data += f"""
    historical_earnings_analysis: {historical_earnings_analysis.model_dump_json()}
    """

    # Add earnings projections analysis if available
    if earnings_projections_analysis:
        input_data += f"""
    earnings_projections_analysis: {earnings_projections_analysis.model_dump_json()}
    """

    # Add management guidance analysis if available
    if management_guidance_analysis:
        input_data += f"""
    management_guidance_analysis: {management_guidance_analysis.model_dump_json()}
    """

    # Add bottom-up EPS validation if available
    if bottom_up_eps_validation:
        input_data += f"""
    bottom_up_eps_validation: {bottom_up_eps_validation.model_dump_json()}
    """

    # Add peer-relative EPS validation if available
    if peer_relative_eps_validation:
        input_data += f"""
    peer_relative_eps_validation: {peer_relative_eps_validation.model_dump_json()}
    """

    # Add market sentiment EPS check if available
    if market_sentiment_eps_check:
        input_data += f"""
    market_sentiment_eps_check: {market_sentiment_eps_check.model_dump_json()}
    """

    try:
        # Run the EPS validation synthesis agent
        result: RunResult = await Runner.run(
            eps_validation_synthesis_agent,
            input=input_data
        )

        synthesis_result: EpsValidationSynthesis = result.final_output

        # Log key synthesis metrics
        logger.info(f"EPS validation synthesis completed for {symbol}: "
                   f"Overall verdict: {synthesis_result.overall_verdict}, "
                   f"Confidence: {synthesis_result.confidence_score:.2f}, "
                   f"Methods analyzed: {len(synthesis_result.method_agreement)}")

        # Log individual method agreements
        for method, verdict in synthesis_result.method_agreement.items():
            logger.info(f"  {method}: {verdict}")

        # Log key insights
        logger.info(f"Key risks identified: {len(synthesis_result.key_risks)} factors")
        logger.info(f"Supporting evidence: {len(synthesis_result.supporting_evidence)} points")

        # Log the full synthesis result as JSON for development visibility
        logger.debug(f"EPS validation synthesis result for {symbol}: {json.dumps(synthesis_result.model_dump(), indent=2)}")

        return synthesis_result

    except Exception as e:
        logger.error(f"Error during EPS validation synthesis for {symbol}: {str(e)}")

        # Create method agreement dict from available methods with error verdict
        method_agreement = {method: EpsValidationVerdict.INSUFFICIENT_DATA for method in available_methods}

        # Return error result with insufficient data verdict
        return EpsValidationSynthesis(
            symbol=symbol,
            overall_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            confidence_score=0.1,  # Very low confidence due to error
            method_agreement=method_agreement,
            key_risks=[f"Synthesis process error: {str(e)}", "Unable to complete multi-method validation"],
            supporting_evidence=["Synthesis process failed"],
            consensus_adjustment_recommendation=None,
            synthesis_analysis=f"EPS validation synthesis failed due to error: {str(e)}",
            investment_implications="Unable to provide reliable EPS validation - recommend manual analysis"
        )