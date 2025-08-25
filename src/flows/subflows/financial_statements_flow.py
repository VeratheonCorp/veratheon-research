from src.tasks.financial_statements.financial_statements_fetch_task import financial_statements_fetch_task
from src.tasks.financial_statements.financial_statements_analysis_task import financial_statements_analysis_task
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis
import logging
import time

logger = logging.getLogger(__name__)

async def financial_statements_flow(symbol: str) -> FinancialStatementsAnalysis:
    """
    Main flow for analyzing recent financial statements for changes in revenue drivers, cost structures, and working capital.
    
    This analysis directly informs the accuracy of near-term projections by examining recent operational changes
    that affect business fundamentals driving earnings.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        FinancialStatementsAnalysis containing the research results and trends
    """
    start_time = time.time()
    logger.info(f"Financial statements flow started for {symbol}")
    
    # Fetch financial statements data from Alpha Vantage
    financial_data: FinancialStatementsData = await financial_statements_fetch_task(symbol)

    # Perform financial statements analysis
    financial_analysis: FinancialStatementsAnalysis = await financial_statements_analysis_task(
        symbol, financial_data
    )

    logger.info(f"Financial statements flow completed for {symbol}")
    logger.info(f"Financial statements flow completed for {symbol} in {int(time.time() - start_time)} seconds")

    return financial_analysis