from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def forward_pe_valuation_reporting_task(
    symbol: str, 
    forward_pe_valuation: ForwardPeValuation
) -> None:
    """
    Reporting task to write JSON dump of forward PE valuation analysis results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        forward_pe_valuation: ForwardPeValuation model to report
    """
    logger.info(f"Forward PE Valuation Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"forward_pe_valuation_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(forward_pe_valuation.model_dump(), f, indent=2)
    
    logger.info(f"Forward PE Valuation report written to: {filepath.absolute()}")

async def forward_pe_sanity_check_reporting_task(
    symbol: str, 
    forward_pe_sanity_check: ForwardPeSanityCheck
) -> None:
    """
    Reporting task to write JSON dump of forward PE sanity check results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        forward_pe_sanity_check: ForwardPeSanityCheck model to report
    """
    logger.info(f"Forward PE Sanity Check Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"forward_pe_sanity_check_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(forward_pe_sanity_check.model_dump(), f, indent=2)
    
    logger.info(f"Forward PE Sanity Check report written to: {filepath.absolute()}")