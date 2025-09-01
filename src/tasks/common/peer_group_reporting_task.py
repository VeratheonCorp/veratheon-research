from src.research.common.models.peer_group import PeerGroup
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def peer_group_reporting_task(
    symbol: str, 
    peer_group: PeerGroup
) -> None:
    """
    Reporting task to write JSON dump of peer group analysis results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        peer_group: PeerGroup model to report
    """
    logger.info(f"Peer Group Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"peer_group_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(peer_group.model_dump(), f, indent=2)
    
    logger.info(f"Peer Group report written to: {filepath.absolute()}")