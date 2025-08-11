from prefect import task, get_run_logger
from typing import List
from src.research.forward_pe.forward_pe_models import ForwardPEEarningsSummary
from src.research.forward_pe.forward_pe_fetch_earnings_util import get_quarterly_eps_data_for_symbol, get_quarterly_eps_data_for_symbols


@task(name="forward_pe_fetch_earnings_for_symbols_task", log_prints=False)
async def forward_pe_fetch_earnings_for_symbols_task(symbol: str, peer_group: List[str]) -> ForwardPEEarningsSummary:
    """
    Task to fetch the earnings data for the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
        peer_group: List of peer symbols
    Returns:
        EarningsSummary containing the earnings data
    """
    logger = get_run_logger()
    logger.info(f"Fetching earnings data for {symbol} with peer group {peer_group}")

    return get_quarterly_eps_data_for_symbols([symbol] + peer_group)


@task(name="forward_pe_fetch_single_earnings_task", log_prints=False)
async def forward_pe_fetch_single_earnings_task(symbol: str) -> ForwardPEEarningsSummary:
    """
    Task to fetch the earnings data for the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        EarningsSummary containing the earnings data
    """
    logger = get_run_logger()
    logger.info(f"Fetching earnings data for {symbol}")

    return get_quarterly_eps_data_for_symbol(symbol)
