from src.research.eps_validation.eps_validation_models import PeerRelativeEpsValidation
from src.lib.redis_cache import get_redis_cache
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def peer_relative_eps_validation_reporting_task(
    symbol: str,
    peer_relative_eps_validation: PeerRelativeEpsValidation
) -> None:
    """
    Reporting task to write JSON dump of peer-relative EPS validation analysis results to file and cache to Redis.

    Args:
        symbol: Stock symbol being analyzed
        peer_relative_eps_validation: PeerRelativeEpsValidation model to report
    """
    logger.info(f"Peer-Relative EPS Validation Reporting for {symbol}")

    # Cache the analysis in Redis (24 hour TTL for reports)
    cache = get_redis_cache()
    cache.cache_report("peer_relative_eps_validation", symbol, peer_relative_eps_validation, ttl=86400)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"peer_relative_eps_validation_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename

    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(peer_relative_eps_validation.model_dump(), f, indent=2)

    logger.info(f"Peer-Relative EPS Validation report written to: {filepath.absolute()}")