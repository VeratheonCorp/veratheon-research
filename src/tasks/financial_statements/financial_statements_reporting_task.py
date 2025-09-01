from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

async def financial_statements_reporting_task(
    symbol: str, 
    financial_analysis: FinancialStatementsAnalysis
) -> None:
    """
    Reporting task to write JSON dump of financial statements analysis results to file.
    
    Args:
        symbol: Stock symbol being analyzed
        financial_analysis: FinancialStatementsAnalysis model to report
    """
    logger.info(f"Financial Statements Reporting for {symbol}")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"financial_statements_{symbol}_{timestamp}.json"
    filepath = Path("reports") / filename
    
    # Write JSON to file
    with open(filepath, 'w') as f:
        json.dump(financial_analysis.model_dump(), f, indent=2)
    
    logger.info(f"Financial Statements report written to: {filepath.absolute()}")