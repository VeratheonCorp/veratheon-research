from prefect import task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.forward_pe.forward_pe_analysis_agent import forward_pe_analysis_agent
from agents import Runner, RunResult
from src.research.forward_pe.forward_pe_models import ForwardPEEarningsSummary
from prefect import get_run_logger

@task(name="forward_pe_analysis_task", persist_result=True)
async def forward_pe_analysis_task(symbol: str, earnings_summary: ForwardPEEarningsSummary) -> ForwardPeValuation:
    """
    Task to perform forward PE analysis for the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        earnings_summary: Earnings summary for the symbol
    Returns:
        ForwardPeValuation containing the forward PE analysis
    """
    logger = get_run_logger()
    logger.info(f"Performing forward PE analysis for {symbol}")

    result: RunResult = await Runner.run(
        forward_pe_analysis_agent,
        input=f"original_symbol: {symbol}, earnings_summary: {earnings_summary}")
    forward_pe_analysis: ForwardPeValuation = result.final_output

    logger.info(f"Forward PE analysis for {symbol}: {forward_pe_analysis}")

    return forward_pe_analysis
