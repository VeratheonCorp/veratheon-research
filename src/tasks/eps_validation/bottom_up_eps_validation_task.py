from typing import Optional
from src.research.eps_validation.eps_validation_models import BottomUpEpsValidation, ConfidenceLevel, EpsValidationVerdict
from src.research.eps_validation.bottom_up_eps_validation_agent import bottom_up_eps_validation_agent
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionData, EarningsProjectionAnalysis
from agents import Runner, RunResult
import json
import logging

logger = logging.getLogger(__name__)

async def bottom_up_eps_validation_task(
    symbol: str,
    financial_statements_data: Optional[FinancialStatementsData] = None,
    financial_statements_analysis: Optional[FinancialStatementsAnalysis] = None,
    earnings_projections_data: Optional[EarningsProjectionData] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    consensus_eps: Optional[float] = None
) -> BottomUpEpsValidation:
    """
    Task to orchestrate bottom-up EPS validation using financial fundamentals.

    Args:
        symbol: Stock symbol to research
        financial_statements_data: Raw financial statements data for fundamental analysis
        financial_statements_analysis: Analysis of financial statements trends
        earnings_projections_data: Raw earnings projection data
        earnings_projections_analysis: Independent earnings projections analysis
        consensus_eps: Wall Street consensus EPS estimate for comparison
    Returns:
        BottomUpEpsValidation containing independent EPS validation results
    """

    logger.info(f"Bottom-up EPS validation started for {symbol}")

    # Handle missing financial data gracefully
    if not financial_statements_data and not financial_statements_analysis:
        logger.warning(f"No financial statements data available for {symbol}")
        return BottomUpEpsValidation(
            symbol=symbol,
            independent_eps_estimate=0.0,
            consensus_eps=consensus_eps or 0.0,
            variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            key_assumptions=["Insufficient financial data for bottom-up reconstruction"],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            supporting_analysis="Cannot perform bottom-up EPS validation due to missing financial statements data",
            risk_factors=["Missing fundamental data", "Unable to validate consensus estimates"]
        )

    # Handle missing earnings projection data
    if not earnings_projections_analysis:
        logger.warning(f"No earnings projections analysis available for {symbol}")

    # Handle missing consensus EPS
    if consensus_eps is None:
        if earnings_projections_analysis and earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate:
            consensus_eps = earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate
            logger.info(f"Using consensus EPS from earnings projections: ${consensus_eps:.2f}")
        else:
            logger.warning(f"No consensus EPS available for {symbol}")
            consensus_eps = 0.0

    # Prepare comprehensive input data for the agent
    input_data = f"""
    symbol: {symbol}
    consensus_eps_estimate: {consensus_eps}
    """

    # Add financial statements data if available
    if financial_statements_data:
        input_data += f"""
    financial_statements_data: {financial_statements_data.model_dump_json()}
    """

    # Add financial statements analysis if available
    if financial_statements_analysis:
        input_data += f"""
    financial_statements_analysis: {financial_statements_analysis.model_dump_json()}
    """

    # Add earnings projections data if available
    if earnings_projections_data:
        input_data += f"""
    earnings_projections_data: {earnings_projections_data.model_dump_json()}
    """

    # Add earnings projections analysis if available
    if earnings_projections_analysis:
        input_data += f"""
    earnings_projections_analysis: {earnings_projections_analysis.model_dump_json()}
    """

    try:
        # Run the bottom-up EPS validation agent
        result: RunResult = await Runner.run(
            bottom_up_eps_validation_agent,
            input=input_data
        )

        validation_result: BottomUpEpsValidation = result.final_output

        # Log key validation metrics
        logger.info(f"Bottom-up EPS validation completed for {symbol}: "
                   f"Independent EPS: ${validation_result.independent_eps_estimate:.2f}, "
                   f"Consensus EPS: ${validation_result.consensus_eps:.2f}, "
                   f"Variance: {validation_result.variance_percentage:.1f}%, "
                   f"Verdict: {validation_result.validation_verdict}")

        # Log confidence level and key assumptions
        logger.info(f"Validation confidence: {validation_result.confidence_level}, "
                   f"Key assumptions: {len(validation_result.key_assumptions)} factors")

        # Log the full validation result as JSON for development visibility
        logger.debug(f"Bottom-up EPS validation result for {symbol}: {json.dumps(validation_result.model_dump(), indent=2)}")

        return validation_result

    except Exception as e:
        logger.error(f"Error during bottom-up EPS validation for {symbol}: {str(e)}")

        # Return error result with insufficient data verdict
        return BottomUpEpsValidation(
            symbol=symbol,
            independent_eps_estimate=0.0,
            consensus_eps=consensus_eps,
            variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            key_assumptions=[f"Error during validation: {str(e)}"],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            supporting_analysis=f"Bottom-up EPS validation failed due to error: {str(e)}",
            risk_factors=["Validation process error", "Unable to complete fundamental analysis"]
        )