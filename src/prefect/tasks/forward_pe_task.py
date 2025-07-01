
from prefect import task, get_run_logger
from src.research_agents.forward_pe_agent import ForwardPeAgent
from src.research_agents.forward_pe_agent import EarningsSummary

@task(name="forward_pe_task")
async def forward_pe_task(symbol: str) -> EarningsSummary:
    """
    Task to run the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        
    Returns:
        EarningsSummary containing the research results
    """
    logger = get_run_logger()
    logger.info(f"Starting forward PE research for {symbol}")
    
    try:
        result = await ForwardPeAgent().analyze(symbol)
        return result
    except Exception as e:
        logger.error(f"Error during forward PE research: {str(e)}")
        return EarningsSummary(
            symbol_earnings={},
            peer_earnings=[],
            summary=f"Analysis could not be completed due to an error: {str(e)}",
        )