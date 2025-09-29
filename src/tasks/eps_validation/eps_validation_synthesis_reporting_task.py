from src.research.eps_validation.eps_validation_models import EpsValidationSynthesis
from src.lib.redis_cache import get_redis_cache
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def eps_validation_synthesis_reporting_task(
    symbol: str,
    eps_validation_synthesis: EpsValidationSynthesis
) -> None:
    """
    Reporting task to write JSON dump of EPS validation synthesis analysis results to file and cache to Redis.

    Args:
        symbol: Stock symbol being analyzed
        eps_validation_synthesis: EpsValidationSynthesis model to report
    """
    logger.info(f"EPS Validation Synthesis Reporting for {symbol}")

    # Cache the analysis in Redis (24 hour TTL for reports)
    cache = get_redis_cache()
    cache.cache_report("eps_validation_synthesis", symbol, eps_validation_synthesis, ttl=86400)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"eps_validation_synthesis_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename

    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(eps_validation_synthesis.model_dump(), f, indent=2)

    logger.info(f"EPS Validation Synthesis report written to: {filepath.absolute()}")