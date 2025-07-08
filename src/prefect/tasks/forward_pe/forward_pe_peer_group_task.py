from prefect import task, get_run_logger
from src.research.forward_pe.forward_pe_models import PeerGroup
from src.research.forward_pe.forward_pe_peer_group_agent import peer_group_agent, peer_group_chatcompletion

@task(name="forward_pe_peer_group_task", persist_result=True)
async def forward_pe_peer_group_task(symbol: str) -> PeerGroup:
    """
    Task to fetch the peer group for the forward PE research for a given symbol.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        PeerGroup containing the peer group
    """
    logger = get_run_logger()
    logger.info(f"Fetching peer group for {symbol}")

    peer_group: PeerGroup = await peer_group_chatcompletion(symbol)

    logger.info(f"Peer group for {symbol}: {peer_group}")

    return peer_group