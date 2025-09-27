"""
TEMPLATE: Technical EPS Validation Task

This file serves as a template for creating new EPS validation tasks.
Replace 'technical' with your validation method name throughout.
"""

import json
import logging
from typing import Optional

from agents import Runner, RunResult

from src.research.eps_validation.eps_validation_models import (
    ConfidenceLevel,
    EpsValidationVerdict,
    TechnicalEpsValidation,
)
from src.research.eps_validation.technical_eps_validation_agent import (
    technical_eps_validation_agent,
)

# TEMPLATE: Add imports for your specific data dependencies
# from src.research.market_data.models import TechnicalIndicators
# from src.research.price_data.models import PriceData

logger = logging.getLogger(__name__)


async def technical_eps_validation_task(
    symbol: str,
    # TEMPLATE: Add your specific input parameters here
    # technical_indicators: Optional[TechnicalIndicators] = None,
    # price_data: Optional[PriceData] = None,
    consensus_eps: Optional[float] = None,
) -> TechnicalEpsValidation:
    """
    TEMPLATE: Task to orchestrate technical EPS validation.

    Replace this docstring and parameters with your specific validation method.

    Args:
        symbol: Stock symbol to research
        consensus_eps: Wall Street consensus EPS estimate for comparison
        # TEMPLATE: Add documentation for your specific parameters

    Returns:
        TechnicalEpsValidation containing technical analysis validation results
    """

    logger.info(f"Technical EPS validation started for {symbol}")

    # TEMPLATE: Handle missing data gracefully - customize for your method
    if consensus_eps is None:
        logger.warning(f"No consensus EPS available for {symbol}")
        return TechnicalEpsValidation(
            symbol=symbol,
            price_momentum_score=0.0,
            volume_trend_indicator="INSUFFICIENT_DATA",
            technical_consensus_eps=0.0,
            implied_eps_from_technicals=0.0,
            technical_variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            technical_indicators=["Insufficient data for technical analysis"],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            support_resistance_analysis="Cannot perform technical analysis due to missing consensus EPS data",
            risk_factors=["Missing consensus data", "Unable to validate estimates"],
        )

    # TEMPLATE: Add your specific data validation logic here
    # Example: Check for required technical indicators, price data, etc.

    # TEMPLATE: Prepare comprehensive input data for the agent
    input_data = f"""
    symbol: {symbol}
    consensus_eps_estimate: {consensus_eps}
    """

    # TEMPLATE: Add your specific data inputs
    # if technical_indicators:
    #     input_data += f"""
    #     technical_indicators: {technical_indicators.model_dump_json()}
    #     """

    try:
        # Run the technical EPS validation agent
        result: RunResult = await Runner.run(
            technical_eps_validation_agent, input=input_data
        )

        validation_result: TechnicalEpsValidation = result.final_output

        # Log key validation metrics
        logger.info(
            f"Technical EPS validation completed for {symbol}: "
            f"Technical EPS: ${validation_result.implied_eps_from_technicals:.2f}, "
            f"Consensus EPS: ${validation_result.technical_consensus_eps:.2f}, "
            f"Variance: {validation_result.technical_variance_percentage:.1f}%, "
            f"Verdict: {validation_result.validation_verdict}"
        )

        # Log confidence level and technical indicators
        logger.info(
            f"Validation confidence: {validation_result.confidence_level}, "
            f"Technical indicators: {len(validation_result.technical_indicators)} analyzed"
        )

        # Log the full validation result as JSON for development visibility
        logger.debug(
            f"Technical EPS validation result for {symbol}: {json.dumps(validation_result.model_dump(), indent=2)}"
        )

        return validation_result

    except Exception as e:
        logger.error(f"Error during technical EPS validation for {symbol}: {str(e)}")

        # Return error result with insufficient data verdict
        return TechnicalEpsValidation(
            symbol=symbol,
            price_momentum_score=0.0,
            volume_trend_indicator="ERROR",
            technical_consensus_eps=consensus_eps or 0.0,
            implied_eps_from_technicals=0.0,
            technical_variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            technical_indicators=[f"Error during validation: {str(e)}"],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            support_resistance_analysis=f"Technical EPS validation failed due to error: {str(e)}",
            risk_factors=[
                "Validation process error",
                "Unable to complete technical analysis",
            ],
        )