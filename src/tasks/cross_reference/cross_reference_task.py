from src.research.cross_reference.cross_reference_agent import cross_reference_agent
from agents import Runner, RunResult
import json
import logging
from typing import List, Any
from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysis

logger = logging.getLogger(__name__)

async def cross_reference_task(
    symbol: str, 
    original_analysis: Any,
    data_points: List[Any]
) -> CrossReferencedAnalysis:
    """
    Task to perform cross reference analysis for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        original_analysis: Original analysis for the symbol
        data_points: List of data points to cross reference against
    Returns:
        CrossReferencedAnalysis containing the cross reference analysis
    """
    logger.info(f"Performing cross reference analysis for {symbol}")

    # Build input with optional context
    input_data = f"original_symbol: {symbol}, original_analysis: {original_analysis}, data_points: {data_points}"

    result: RunResult = await Runner.run(
        cross_reference_agent,
        input=input_data)
    cross_reference: CrossReferencedAnalysis = result.final_output

    logger.debug(f"Cross reference for {symbol}: {json.dumps(cross_reference.model_dump(), indent=2)}")

    return cross_reference
