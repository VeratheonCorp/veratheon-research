import json
import logging
from typing import Optional

from agents import Runner, RunResult

from src.lib.fiscal_year_utils import log_fiscal_decision


def filter_financial_data_for_eps_validation(data, fiscal_info, max_periods=4):
    """
    Filter financial data to only include relevant periods for EPS validation.
    Removes historical estimates and focuses on operational data only.

    Args:
        data: Financial data object
        fiscal_info: Fiscal year timing information
        max_periods: Maximum number of periods to include
    Returns:
        Filtered data object with only relevant periods
    """
    if not data:
        return None

    # Create a copy to avoid modifying original
    filtered_data = data.model_copy() if hasattr(data, 'model_copy') else data

    # Filter quarterly income statements to recent periods only
    if hasattr(filtered_data, 'quarterly_income_statements') and filtered_data.quarterly_income_statements:
        # Keep only recent quarters for trend analysis
        filtered_data.quarterly_income_statements = filtered_data.quarterly_income_statements[:max_periods]

        # Remove any EPS fields that might confuse the agent
        for statement in filtered_data.quarterly_income_statements:
            if isinstance(statement, dict):
                # Remove any EPS-related fields to prevent confusion
                eps_fields = ['eps', 'earningsPerShare', 'reportedEPS', 'estimatedEPS', 'consensusEPS']
                for field in eps_fields:
                    statement.pop(field, None)

    # Filter annual income statements similarly
    if hasattr(filtered_data, 'annual_income_statements') and filtered_data.annual_income_statements:
        filtered_data.annual_income_statements = filtered_data.annual_income_statements[:max_periods]

        # Remove EPS fields from annual statements too
        for statement in filtered_data.annual_income_statements:
            if isinstance(statement, dict):
                eps_fields = ['eps', 'earningsPerShare', 'reportedEPS', 'estimatedEPS', 'consensusEPS']
                for field in eps_fields:
                    statement.pop(field, None)

    return filtered_data


def filter_earnings_projections_data(proj_data, consensus_eps):
    """
    Filter earnings projections data to remove any conflicting EPS estimates.

    Args:
        proj_data: Earnings projection data
        consensus_eps: The current consensus EPS we want to use
    Returns:
        Filtered projection data
    """
    if not proj_data:
        return None

    filtered_data = proj_data.model_copy() if hasattr(proj_data, 'model_copy') else proj_data

    # Remove any consensus EPS estimates that might conflict
    if hasattr(filtered_data, 'next_quarter_projection'):
        proj = filtered_data.next_quarter_projection
        if hasattr(proj, 'consensus_eps_estimate'):
            # Replace with our known good consensus
            proj.consensus_eps_estimate = consensus_eps

        # Remove any EPS vs consensus fields that might be wrong
        if hasattr(proj, 'eps_vs_consensus_diff'):
            proj.eps_vs_consensus_diff = None
        if hasattr(proj, 'eps_vs_consensus_percent'):
            proj.eps_vs_consensus_percent = None

    return filtered_data


def remove_historical_eps_estimates(data):
    """
    Recursively remove any EPS estimate fields from data structures to prevent LLM confusion.

    Args:
        data: Any data structure (dict, list, object)
    Returns:
        Cleaned data structure with EPS estimates removed
    """
    if isinstance(data, dict):
        cleaned_data = {}
        for key, value in data.items():
            # Skip any keys that might contain EPS estimates
            skip_keys = [
                'estimates', 'earnings_estimates', 'earnings_calendar',
                'eps_estimate', 'consensus_eps', 'reported_eps',
                'historical_estimates', 'analyst_estimates'
            ]

            if key.lower() in [k.lower() for k in skip_keys]:
                continue  # Skip this field entirely

            # Recursively clean nested structures
            cleaned_data[key] = remove_historical_eps_estimates(value)

        return cleaned_data

    elif isinstance(data, list):
        return [remove_historical_eps_estimates(item) for item in data]

    elif hasattr(data, 'model_dump'):
        # Handle Pydantic models
        dict_data = data.model_dump()
        cleaned_dict = remove_historical_eps_estimates(dict_data)
        return cleaned_dict

    else:
        # Return primitive types as-is
        return data
from src.research.earnings_projections.earnings_projections_models import (
    EarningsProjectionAnalysis,
    EarningsProjectionData,
)
from src.research.eps_validation.bottom_up_eps_validation_agent import (
    bottom_up_eps_validation_agent,
)
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation,
    ConfidenceLevel,
    EpsValidationVerdict,
)
from src.research.financial_statements.financial_statements_models import (
    FinancialStatementsAnalysis,
    FinancialStatementsData,
)

logger = logging.getLogger(__name__)


async def bottom_up_eps_validation_task(
    symbol: str,
    financial_statements_data: Optional[FinancialStatementsData] = None,
    financial_statements_analysis: Optional[FinancialStatementsAnalysis] = None,
    earnings_projections_data: Optional[EarningsProjectionData] = None,
    earnings_projections_analysis: Optional[EarningsProjectionAnalysis] = None,
    consensus_eps: Optional[float] = None,
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

    # Get fiscal year timing information for data period alignment
    fiscal_info = log_fiscal_decision(symbol)

    # Handle missing financial data gracefully
    if not financial_statements_data and not financial_statements_analysis:
        logger.warning(f"No financial statements data available for {symbol}")
        return BottomUpEpsValidation(
            symbol=symbol,
            bottom_up_eps_estimate=0.0,
            consensus_eps=consensus_eps or 0.0,
            variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            key_assumptions=[
                "Insufficient financial data for bottom-up reconstruction"
            ],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            supporting_analysis="Cannot perform bottom-up EPS validation due to missing financial statements data",
            risk_factors=[
                "Missing fundamental data",
                "Unable to validate consensus estimates",
            ],
        )

    # Handle missing earnings projection data
    if not earnings_projections_analysis:
        logger.warning(f"No earnings projections analysis available for {symbol}")

    # Handle missing consensus EPS
    if consensus_eps is None:
        if (
            earnings_projections_analysis
            and earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate
        ):
            consensus_eps = (
                earnings_projections_analysis.next_quarter_projection.consensus_eps_estimate
            )
            logger.info(
                f"Using consensus EPS from earnings projections: ${consensus_eps:.2f}"
            )
        else:
            logger.warning(f"No consensus EPS available for {symbol}")
            consensus_eps = 0.0

    # Prepare comprehensive input data for the agent
    # CRITICAL: Only provide the specific consensus EPS, not historical estimates
    input_data = f"""
    symbol: {symbol}
    consensus_eps_estimate: {consensus_eps}
    fiscal_info: {fiscal_info.use_annual_data} (use_annual_data)
    fiscal_timing_decision: {fiscal_info.decision_reason}

    IMPORTANT: The consensus_eps_estimate above ({consensus_eps}) is the ONLY consensus figure you should use.
    This is the next fiscal quarter consensus from Alpha Vantage Earnings Estimates API.
    Do NOT use any other EPS figures that might appear in historical financial data.
    """

    # Filter and add financial statements data if available
    if financial_statements_data:
        filtered_financial_data = filter_financial_data_for_eps_validation(
            financial_statements_data, fiscal_info
        )
        if filtered_financial_data:
            # Apply comprehensive historical EPS removal
            cleaned_financial_data = remove_historical_eps_estimates(filtered_financial_data)
            input_data += f"""
    financial_statements_data: {json.dumps(cleaned_financial_data)}
    """

    # Add financial statements analysis if available (clean any EPS estimates)
    if financial_statements_analysis:
        cleaned_financial_analysis = remove_historical_eps_estimates(financial_statements_analysis)
        input_data += f"""
    financial_statements_analysis: {json.dumps(cleaned_financial_analysis)}
    """

    # Filter and add earnings projections data if available
    if earnings_projections_data:
        filtered_projections_data = filter_financial_data_for_eps_validation(
            earnings_projections_data, fiscal_info
        )
        if filtered_projections_data:
            # Apply comprehensive historical EPS removal
            cleaned_projections_data = remove_historical_eps_estimates(filtered_projections_data)
            input_data += f"""
    earnings_projections_data: {json.dumps(cleaned_projections_data)}
    """

    # Filter and add earnings projections analysis if available
    if earnings_projections_analysis:
        filtered_projections_analysis = filter_earnings_projections_data(
            earnings_projections_analysis, consensus_eps
        )
        if filtered_projections_analysis:
            # Apply comprehensive historical EPS removal
            cleaned_projections_analysis = remove_historical_eps_estimates(filtered_projections_analysis)
            input_data += f"""
    earnings_projections_analysis: {json.dumps(cleaned_projections_analysis)}
    """

    try:
        # Run the bottom-up EPS validation agent
        result: RunResult = await Runner.run(
            bottom_up_eps_validation_agent, input=input_data
        )

        validation_result: BottomUpEpsValidation = result.final_output

        # Log key validation metrics
        logger.info(
            f"Bottom-up EPS validation completed for {symbol}: "
            f"Bottom-up EPS: ${validation_result.bottom_up_eps_estimate:.2f}, "
            f"Consensus EPS: ${validation_result.consensus_eps:.2f}, "
            f"Variance: {validation_result.variance_percentage:.1f}%, "
            f"Verdict: {validation_result.validation_verdict}"
        )

        # Log confidence level and key assumptions
        logger.info(
            f"Validation confidence: {validation_result.confidence_level}, "
            f"Key assumptions: {len(validation_result.key_assumptions)} factors"
        )

        # Log the full validation result as JSON for development visibility
        logger.debug(
            f"Bottom-up EPS validation result for {symbol}: {json.dumps(validation_result.model_dump(), indent=2)}"
        )

        return validation_result

    except Exception as e:
        logger.error(f"Error during bottom-up EPS validation for {symbol}: {str(e)}")

        # Return error result with insufficient data verdict
        return BottomUpEpsValidation(
            symbol=symbol,
            bottom_up_eps_estimate=0.0,
            consensus_eps=consensus_eps,
            variance_percentage=0.0,
            confidence_level=ConfidenceLevel.LOW,
            key_assumptions=[f"Error during validation: {str(e)}"],
            validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            supporting_analysis=f"Bottom-up EPS validation failed due to error: {str(e)}",
            risk_factors=[
                "Validation process error",
                "Unable to complete fundamental analysis",
            ],
        )
