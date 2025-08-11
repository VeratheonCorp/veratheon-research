from prefect import task
import json
from src.research.forward_pe.forward_pe_models import ForwardPeSanityCheck
from src.research.forward_pe.forward_pe_sanity_check_agent import forward_pe_sanity_check_agent
from agents import Runner, RunResult
from prefect import get_run_logger
from src.research.forward_pe.forward_pe_models import ForwardPEEarningsSummary

@task(name="forward_pe_sanity_check_task", persist_result=True)
async def forward_pe_sanity_check_task(earnings_summary: ForwardPEEarningsSummary) -> ForwardPeSanityCheck:
    """
    Task to perform forward PE sanity check for the forward PE research for a given symbol.
    
    Args:
        earnings_summary: Earnings summary for the symbol
    Returns:
        ForwardPeSanityCheck containing the forward PE sanity check
    """
    logger = get_run_logger()
    logger.info(f"Performing forward PE sanity check for {earnings_summary.symbol}")

    result: RunResult = await Runner.run(
        forward_pe_sanity_check_agent,
        input=f"Forward PE Summary Data: {earnings_summary}")
    forward_pe_sanity_check: ForwardPeSanityCheck = result.final_output

    logger.info(f"Forward PE sanity check for {earnings_summary.symbol}: {json.dumps(forward_pe_sanity_check.model_dump(), indent=2)}")

    return forward_pe_sanity_check
