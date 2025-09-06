from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysisCompletion
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

async def cross_reference_reporting_task(
    symbol: str, 
    cross_reference_analysis: List[CrossReferencedAnalysisCompletion]
) -> None:
    """
    Reporting task to write JSON dump of cross reference analysis results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        cross_reference_analysis: List of CrossReferencedAnalysisSummary models to report
    """
    logger.info(f"Cross Reference Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cross_reference_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    analysis_data = [analysis.model_dump() for analysis in cross_reference_analysis]
    with open(filepath, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    logger.info(f"Cross Reference report written to: {filepath.absolute()}")