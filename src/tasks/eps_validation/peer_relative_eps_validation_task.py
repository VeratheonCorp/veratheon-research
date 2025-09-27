import json
import logging
from typing import List, Optional

from agents import Runner, RunResult

from src.research.common.models.peer_group import PeerGroup
from src.research.eps_validation.eps_validation_models import (
    EpsValidationVerdict,
    PeerRelativeEpsValidation,
)
from src.research.eps_validation.peer_relative_eps_validation_agent import (
    peer_relative_eps_validation_agent,
)
from src.research.forward_pe.forward_pe_models import ForwardPEEarningsSummary

logger = logging.getLogger(__name__)


async def peer_relative_eps_validation_task(
    symbol: str,
    current_stock_price: Optional[float] = None,
    peer_group: Optional[PeerGroup] = None,
    peer_earnings_data: Optional[List[ForwardPEEarningsSummary]] = None,
    consensus_eps: Optional[float] = None,
) -> PeerRelativeEpsValidation:
    """
    Task to orchestrate peer-relative EPS validation using peer group forward P/E ratios.

    Args:
        symbol: Stock symbol to research
        current_stock_price: Current stock price for implied EPS calculation
        peer_group: Peer group data with list of comparable companies
        peer_earnings_data: Forward P/E earnings data for peer companies
        consensus_eps: Wall Street consensus EPS estimate for comparison
    Returns:
        PeerRelativeEpsValidation containing peer-relative EPS validation results
    """

    logger.info(f"Peer-relative EPS validation started for {symbol}")

    # Handle missing peer group data gracefully
    if not peer_group or not peer_group.peer_group:
        logger.warning(f"No peer group data available for {symbol}")
        return PeerRelativeEpsValidation(
            symbol=symbol,
            peer_group_avg_forward_pe=0.0,
            current_stock_price=current_stock_price or 0.0,
            implied_eps_from_peers=0.0,
            consensus_eps=consensus_eps or 0.0,
            relative_variance=0.0,
            peer_comparison_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            peer_analysis="Cannot perform peer-relative EPS validation due to missing peer group data",
            industry_context="Insufficient peer data to assess industry context",
        )

    # Handle missing current stock price
    if current_stock_price is None:
        # Try to extract from peer earnings data if available
        if peer_earnings_data:
            target_data = next(
                (data for data in peer_earnings_data if data.symbol == symbol), None
            )
            if target_data and target_data.current_price:
                try:
                    current_stock_price = float(target_data.current_price)
                    logger.info(
                        f"Using stock price from earnings data: ${current_stock_price:.2f}"
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        f"Could not parse stock price from earnings data for {symbol}"
                    )

        if current_stock_price is None:
            logger.warning(f"No current stock price available for {symbol}")
            return PeerRelativeEpsValidation(
                symbol=symbol,
                peer_group_avg_forward_pe=0.0,
                current_stock_price=0.0,
                implied_eps_from_peers=0.0,
                consensus_eps=consensus_eps or 0.0,
                relative_variance=0.0,
                peer_comparison_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
                peer_analysis="Cannot perform peer-relative EPS validation due to missing current stock price",
                industry_context="Stock price required for implied EPS calculation",
            )

    # Handle missing consensus EPS
    if consensus_eps is None:
        if peer_earnings_data:
            target_data = next(
                (data for data in peer_earnings_data if data.symbol == symbol), None
            )
            if target_data and target_data.next_quarter_consensus_eps:
                try:
                    consensus_eps = float(target_data.next_quarter_consensus_eps)
                    logger.info(
                        f"Using consensus EPS from earnings data: ${consensus_eps:.2f}"
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        f"Could not parse consensus EPS from earnings data for {symbol}"
                    )

        if consensus_eps is None:
            logger.warning(f"No consensus EPS available for {symbol}")
            consensus_eps = 0.0

    # Prepare comprehensive input data for the agent
    input_data = f"""
    symbol: {symbol}
    current_stock_price: {current_stock_price}
    consensus_eps: {consensus_eps}
    """

    # Add peer group information
    if peer_group:
        input_data += f"""
    peer_group: {peer_group.model_dump_json()}
    """

    # Add peer earnings data if available
    if peer_earnings_data:
        # Convert to JSON for the agent
        peer_data_json = [data.model_dump() for data in peer_earnings_data]
        input_data += f"""
    peer_earnings_data: {json.dumps(peer_data_json, indent=2)}
    """

    try:
        # Run the peer-relative EPS validation agent
        result: RunResult = await Runner.run(
            peer_relative_eps_validation_agent, input=input_data
        )

        validation_result: PeerRelativeEpsValidation = result.final_output

        # Log key validation metrics
        logger.info(
            f"Peer-relative EPS validation completed for {symbol}: "
            f"Peer avg forward P/E: {validation_result.peer_group_avg_forward_pe:.2f}, "
            f"Implied EPS: ${validation_result.implied_eps_from_peers:.2f}, "
            f"Consensus EPS: ${validation_result.consensus_eps:.2f}, "
            f"Variance: {validation_result.relative_variance:.1f}%, "
            f"Verdict: {validation_result.peer_comparison_verdict}"
        )

        # Log peer group details
        if peer_group and peer_group.peer_group:
            logger.info(f"Peer group for {symbol}: {', '.join(peer_group.peer_group)}")

        # Log the full validation result as JSON for development visibility
        logger.debug(
            f"Peer-relative EPS validation result for {symbol}: {json.dumps(validation_result.model_dump(), indent=2)}"
        )

        return validation_result

    except Exception as e:
        logger.error(
            f"Error during peer-relative EPS validation for {symbol}: {str(e)}"
        )

        # Return error result with insufficient data verdict
        return PeerRelativeEpsValidation(
            symbol=symbol,
            peer_group_avg_forward_pe=0.0,
            current_stock_price=current_stock_price,
            implied_eps_from_peers=0.0,
            consensus_eps=consensus_eps,
            relative_variance=0.0,
            peer_comparison_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
            peer_analysis=f"Peer-relative EPS validation failed due to error: {str(e)}",
            industry_context="Validation process error prevented industry context analysis",
        )
